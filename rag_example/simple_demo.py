"""
RAG 简单演示版本 - 接入通义千问 API
"""

import os
import time
import requests
from typing import List
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.documents import Document

# 加载环境变量
load_dotenv()

# 通义千问 API
import dashscope
from dashscope import Generation


class SimpleRAGDemo:
    """简单 RAG 演示"""

    def __init__(self, data_path: str = "./data"):
        self.data_path = data_path
        self.documents = []
        self.chunks = []

    def load_documents(self) -> List[Document]:
        """加载文档"""
        print("=" * 50)
        print("【步骤 1】加载文档")
        print("=" * 50)

        try:
            loader = DirectoryLoader(
                self.data_path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={"autodetect_encoding": True}
            )
            self.documents = loader.load()
            print(f"[OK] 成功加载 {len(self.documents)} 个文档\n")
            return self.documents
        except Exception as e:
            print(f"[ERROR] 加载失败: {e}\n")
            return []

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """分割文档"""
        print("=" * 50)
        print("【步骤 2】分割文档")
        print("=" * 50)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?"]
        )

        self.chunks = splitter.split_documents(documents)
        print(f"[OK] 文档被分割为 {len(self.chunks)} 个块")
        print(f"  - 每块大小: 300 字符")
        print(f"  - 块之间重叠: 50 字符\n")

        # 显示前几个块
        for i, chunk in enumerate(self.chunks[:3]):
            preview = chunk.page_content[:80].replace('\n', ' ')
            print(f"  块 {i+1}: {preview}...")
        if len(self.chunks) > 3:
            print(f"  ... (还有 {len(self.chunks) - 3} 个块)\n")
        else:
            print()

        return self.chunks

    def simple_search(self, query: str, top_k: int = 2) -> List[Document]:
        """简单的关键词搜索（替代向量搜索）"""
        print("=" * 50)
        print("【步骤 3】检索相关文档")
        print("=" * 50)

        query_lower = query.lower()
        # 提取查询中的关键词（过滤掉常见停用词）
        stop_words = {'的', '是', '了', '在', '和', '有', '我', '你', '他', '她', '它', '什么', '怎么', '如何', '?', '？'}
        keywords = [w for w in query_lower.split() if w not in stop_words and len(w) > 1]

        scored_chunks = []

        for idx, chunk in enumerate(self.chunks):
            content_lower = chunk.page_content.lower()
            score = 0

            # 1. 完整关键词匹配
            for keyword in keywords:
                if keyword in content_lower:
                    score += content_lower.count(keyword) * 10

            # 2. 部分匹配（关键词的一部分在内容中）
            for keyword in keywords:
                for i in range(len(keyword) - 1):
                    part = keyword[i:i+2]
                    if part in content_lower:
                        score += 1

            # 3. 添加位置权重（前面的块权重稍高）
            score += max(0, 5 - idx * 0.1)

            if score > 0:
                scored_chunks.append((score, chunk))

        # 按分数排序
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        # 获取top_k个结果
        if len(scored_chunks) >= top_k:
            top_chunks = [chunk for score, chunk in scored_chunks[:top_k]]
        elif len(scored_chunks) > 0:
            # 如果结果不足top_k，返回所有有分数的
            top_chunks = [chunk for score, chunk in scored_chunks]
        else:
            # 实在没有匹配，返回文档中最长的块（可能包含更多信息）
            print(f"[警告] 没有找到相关文档，返回最长的文档块")
            sorted_by_length = sorted(self.chunks, key=lambda c: len(c.page_content), reverse=True)
            top_chunks = sorted_by_length[:top_k]

        print(f"[OK] 找到 {len(top_chunks)} 个相关文档块:")
        for i, chunk in enumerate(top_chunks, 1):
            preview = chunk.page_content[:100].replace('\n', ' ')
            print(f"  [{i}] {preview}...")
        print()

        return top_chunks

    def generate_answer(self, query: str, context_docs: List[Document]) -> str:
        """生成答案（使用通义千问 API）"""
        print("=" * 50)
        print("【步骤 4】生成答案")
        print("=" * 50)

        if not context_docs:
            return f"抱歉，我没有找到与「{query}」相关的文档。请尝试其他问题或添加更多文档到知识库。"

        context = "\n\n".join([doc.page_content for doc in context_docs])

        # 构造提示词
        prompt = f"""你是一个智能助手。请根据以下上下文内容回答用户的问题。

上下文内容:
{context}

用户问题: {query}

要求:
1. 请基于上下文内容回答问题
2. 如果上下文中没有相关信息，请明确说明
3. 回答要简洁准确，语言自然流畅

回答:"""

        print("[OK] 调用通义千问 API 生成答案...")

        try:
            # 调用通义千问 API
            api_key = os.getenv('DASHSCOPE_API_KEY')
            if not api_key:
                print("[警告] 未配置 DASHSCOPE_API_KEY，使用本地模板回答")
                return self._generate_template_answer(query, context_docs)

            # 先尝试使用 dashscope SDK
            dashscope.api_key = api_key

            # 重试机制
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = Generation.call(
                        model='qwen-turbo',
                        prompt=prompt,
                        max_tokens=1500,
                        temperature=0.7,
                    )

                    if response.status_code == 200:
                        answer = response.output.text
                        print("[OK] 生成成功!")
                        return answer
                    else:
                        print(f"[警告] API 返回错误: {response.message}")
                        return self._generate_template_answer(query, context_docs)

                except Exception as sdk_error:
                    print(f"[尝试 {attempt + 1}/{max_retries}] SDK 调用失败: {sdk_error}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    else:
                        # SDK 失败，尝试使用 HTTP 请求
                        print("[SDK 失败] 尝试使用 HTTP 直接调用...")
                        return self._call_qwen_http(api_key, prompt, query, context_docs)

        except Exception as e:
            print(f"[警告] 调用 API 出错: {e}")
            return self._generate_template_answer(query, context_docs)

    def _call_qwen_http(self, api_key: str, prompt: str, query: str, context_docs: List[Document]) -> str:
        """使用 HTTP 直接调用通义千问 API"""
        try:
            url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "qwen-turbo",
                "input": {
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                "parameters": {
                    "max_tokens": 1500,
                    "temperature": 0.7
                }
            }

            response = requests.post(url, json=data, headers=headers, timeout=30)

            if response.status_code == 200:
                result = response.json()
                answer = result["output"]["text"]
                print("[OK] HTTP 调用成功!")
                return answer
            else:
                print(f"[警告] HTTP 调用失败: {response.status_code} - {response.text}")
                return self._generate_template_answer(query, context_docs)

        except Exception as e:
            print(f"[警告] HTTP 调用出错: {e}")
            return self._generate_template_answer(query, context_docs)

    def _generate_template_answer(self, query: str, context_docs: List[Document]) -> str:
        """生成模板答案（API 失败时备用）"""
        answer = f"根据检索到的文档，关于「{query}」的相关内容：\n\n"
        for i, doc in enumerate(context_docs, 1):
            content = doc.page_content[:300]
            answer += f"[文档片段 {i}]\n{content}...\n\n"
        return answer

    def run(self, query: str):
        """运行完整的 RAG 流程"""
        print("\n" + "=" * 50)
        print("RAG 系统演示")
        print("=" * 50)
        print(f"用户问题: {query}\n")

        # 1. 加载文档
        if not self.documents:
            self.load_documents()

        # 2. 分割文档
        if not self.chunks:
            self.split_documents(self.documents)

        # 3. 检索
        relevant_docs = self.simple_search(query)

        # 4. 生成答案
        answer = self.generate_answer(query, relevant_docs)

        print("\n" + "=" * 50)
        print("【最终答案】")
        print("=" * 50)
        print(answer)
        print("=" * 50)


def main():
    """主程序"""
    demo = SimpleRAGDemo()

    # 演示问题
    questions = [
        "什么是 LangChain？",
        "RAG 有什么优势？",
    ]

    for question in questions:
        demo.run(question)
        print("\n" * 2)

    # 交互模式
    print("=" * 50)
    print("进入交互模式（输入 'quit' 退出）")
    print("=" * 50)

    while True:
        query = input("\n请输入问题: ").strip()

        if query.lower() in ["quit", "exit", "退出", "q"]:
            print("再见！")
            break

        if not query:
            continue

        demo.run(query)


if __name__ == "__main__":
    main()
