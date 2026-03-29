"""
RAG (Retrieval-Augmented Generation) 系统实现
使用 LangChain 框架构建 - 简化版演示
"""

import os
from typing import List, Optional

from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import FakeEmbeddings

load_dotenv()


class SimpleEmbeddings(FakeEmbeddings):
    """简单的基于词频的嵌入（仅用于演示）"""

    def __init__(self, size: int = 384):
        super().__init__(size=size)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """生成简单的嵌入向量"""
        # 使用文本长度和字符特征生成固定长度向量
        vectors = []
        for text in texts:
            # 简单特征：文本长度 + 字符分布
            vec = [0.0] * self.size
            for i, char in enumerate(text[:self.size]):
                vec[i] = float(ord(char)) / 1000.0
            vectors.append(vec)
        return vectors

    def embed_query(self, text: str) -> List[float]:
        """生成查询的嵌入向量"""
        return self.embed_documents([text])[0]


class RAGSystem:
    """RAG 检索增强生成系统"""

    def __init__(
        self,
        data_path: str = "./data",
        persist_directory: str = "./chroma_db",
        use_openai: bool = False,
        use_simple_embeddings: bool = True,
    ):
        """
        初始化 RAG 系统

        Args:
            data_path: 文档数据目录路径
            persist_directory: 向量数据库持久化目录
            use_openai: 是否使用 OpenAI 嵌入模型
            use_simple_embeddings: 是否使用简单嵌入（演示用）
        """
        self.data_path = data_path
        self.persist_directory = persist_directory

        # 初始化嵌入模型
        if use_simple_embeddings:
            print("使用简单嵌入模型（演示版）")
            self.embeddings = SimpleEmbeddings()
        elif use_openai:
            print("使用 OpenAI 兼容的嵌入模型")
            self.embeddings = OpenAIEmbeddings(
                base_url=os.getenv("OPENAI_BASE_URL"),
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            raise ValueError("需要指定嵌入模型")

        # 初始化 LLM（支持智谱AI等兼容服务）
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        # 根据不同的服务商选择模型
        if "bigmodel.cn" in base_url:
            model = "glm-4"  # 智谱AI模型
        elif "deepseek" in base_url:
            model = "deepseek-r1-distill-qwen-7b"  # DeepSeek模型
        elif "dashscope" in base_url:
            model = "qwen-turbo"  # 通义千问模型
        else:
            model = "gpt-3.5-turbo"  # OpenAI默认

        self.llm = ChatOpenAI(
            model=model,
            temperature=0,
            base_url=base_url,
            api_key=os.getenv("OPENAI_API_KEY", "")
        )

        self.vectorstore: Optional[Chroma] = None
        self.qa_chain = None
        self.retriever = None

    def load_documents(self) -> List[Document]:
        """
        从目录加载文档

        Returns:
            文档列表
        """
        documents = []

        # 加载 PDF 文件
        try:
            pdf_loader = DirectoryLoader(
                self.data_path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader
            )
            raw_docs = pdf_loader.load()
            # 清理文档内容
            for doc in raw_docs:
                doc.page_content = self._clean_text(doc.page_content)
                documents.append(doc)
        except Exception as e:
            print(f"加载 PDF 文件时出错: {e}")

        # 加载 TXT 文件
        try:
            txt_loader = DirectoryLoader(
                self.data_path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={"autodetect_encoding": True}
            )
            raw_docs = txt_loader.load()
            # 清理文档内容
            for doc in raw_docs:
                doc.page_content = self._clean_text(doc.page_content)
                documents.append(doc)
        except Exception as e:
            print(f"加载 TXT 文件时出错: {e}")

        print(f"共加载 {len(documents)} 个文档片段")
        return documents

    def _clean_text(self, text: str) -> str:
        """清理文本，移除问题字符"""
        if not text:
            return ""
        # 更彻底的清理：移除所有非ASCII可打印字符（保留中文）
        cleaned = []
        for char in text:
            code = ord(char)
            # 保留：ASCII可打印字符、中文字符范围、基本控制符
            if (32 <= code <= 126) or (0x4E00 <= code <= 0x9FFF) or char in '\n\t':
                cleaned.append(char)
        return ''.join(cleaned)

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        将文档分割成小块

        Args:
            documents: 原始文档列表

        Returns:
            分割后的文档列表
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )

        splits = text_splitter.split_documents(documents)
        print(f"文档被分割为 {len(splits)} 个块")
        return splits

    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        创建向量数据库

        Args:
            documents: 文档列表

        Returns:
            Chroma 向量数据库
        """
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        print(f"向量数据库已创建并保存到 {self.persist_directory}")
        return self.vectorstore

    def load_vectorstore(self) -> Chroma:
        """
        加载已存在的向量数据库

        Returns:
            Chroma 向量数据库
        """
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        print(f"已从 {self.persist_directory} 加载向量数据库")
        return self.vectorstore

    def format_docs(self, docs):
        """格式化文档用于提示"""
        # 清理文本，移除可能导致编码问题的字符
        cleaned_texts = []
        for doc in docs:
            text = doc.page_content
            # 更彻底的清理：移除所有非ASCII可打印字符（保留中文）
            cleaned = []
            for char in text:
                code = ord(char)
                # 保留：ASCII可打印字符、中文字符范围、基本控制符
                if (32 <= code <= 126) or (0x4E00 <= code <= 0x9FFF) or char in '\n\t':
                    cleaned.append(char)
            text = ''.join(cleaned)
            cleaned_texts.append(text.strip())
        return "\n\n".join(cleaned_texts)

    def create_qa_chain(self, retrieval_kwargs: Optional[dict] = None):
        """
        创建问答链

        Args:
            retrieval_kwargs: 检索参数

        Returns:
            问答链
        """
        if self.vectorstore is None:
            raise ValueError("向量数据库未初始化，请先创建或加载向量数据库")

        # 创建检索器
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4} if retrieval_kwargs is None else retrieval_kwargs
        )

        # 定义提示模板
        template = """你是一个有帮助的AI助手。使用以下上下文片段来回答用户的问题。
如果你不知道答案，就说你不知道，不要试图编造答案。

上下文:
{context}

问题: {question}

回答:"""

        prompt = ChatPromptTemplate.from_template(template)

        # 创建 RAG 链
        self.qa_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        print("问答链已创建")
        return self.qa_chain

    def query(self, question: str) -> dict:
        """
        查询问题

        Args:
            question: 用户问题

        Returns:
            包含答案和来源文档的字典
        """
        if self.qa_chain is None:
            raise ValueError("问答链未初始化，请先创建问答链")

        # 清理问题文本
        cleaned_question = self._clean_text(question)

        # 获取答案
        answer = self.qa_chain.invoke(cleaned_question)

        # 获取来源文档
        source_docs = self.retriever.invoke(cleaned_question)

        return {
            "question": question,
            "answer": answer,
            "source_documents": source_docs
        }

    def build_from_scratch(self) -> None:
        """从零构建 RAG 系统"""
        print("=" * 50)
        print("开始构建 RAG 系统...")
        print("=" * 50)

        # 1. 加载文档
        print("\n[步骤 1/4] 加载文档...")
        documents = self.load_documents()

        if not documents:
            print("警告: 没有找到任何文档！")
            return

        # 2. 分割文档
        print("\n[步骤 2/4] 分割文档...")
        splits = self.split_documents(documents)

        # 3. 创建向量数据库
        print("\n[步骤 3/4] 创建向量数据库...")
        self.create_vectorstore(splits)

        # 4. 创建问答链
        print("\n[步骤 4/4] 创建问答链...")
        self.create_qa_chain()

        print("\n" + "=" * 50)
        print("RAG 系统构建完成！")
        print("=" * 50)

    def load_existing(self) -> None:
        """加载已存在的 RAG 系统"""
        print("=" * 50)
        print("加载已存在的 RAG 系统...")
        print("=" * 50)

        # 加载向量数据库
        self.load_vectorstore()

        # 创建问答链
        self.create_qa_chain()

        print("\n" + "=" * 50)
        print("RAG 系统加载完成！")
        print("=" * 50)
