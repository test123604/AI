"""
Mock 大模型模块
模拟真实 LLM 的响应，用于测试
不消耗真实 API 额度
"""

from typing import Dict, List, Optional, Any
import random
import time


class MockLLM:
    """模拟大语言模型"""

    def __init__(self):
        """初始化 Mock LLM"""
        self.call_count = 0
        self.response_delay = 0.01  # 模拟网络延迟（秒）

        # 预定义的响应模板库
        self.templates = {
            # 问答类
            "qa_default": "根据我的了解，{query}是一个很好的问题。{extra_info}",

            # 是否类问题
            "yes_answer": "是的，{topic}确实如此。根据相关资料显示，{detail}。",
            "no_answer": "不是的，{topic}并不正确。实际上{detail}。",

            # 时间相关
            "time_answer": "{time}，{event}如期举行/发生了。",

            # 数量相关
            "number_answer": "根据统计，大约有{number}{unit}。",

            # 解释说明类
            "explanation": "{concept}是指{definition}。它的主要特点包括{features}。",

            # RAG 检索类
            "rag_answer": "根据检索到的文档，关于{topic}的相关信息如下：{content}",
        }

        # 鲁棒性测试的异常响应
        self.error_responses = {
            "empty": "",
            "very_short": "好的。",
            "very_long": "这是一个非常复杂的问题，需要从多个角度来分析。首先，我们需要了解问题的背景和历史..." * 20,
            "gibberish": "xkcd fj123 乱码 %#@！测试",
            "repetition": "回答。回答。回答。重复的内容。" * 10,
        }

    def generate(self, prompt: str, **kwargs) -> str:
        """
        生成回答（模拟 LLM 调用）

        Args:
            prompt: 输入提示词
            **kwargs: 其他参数（temperature, max_tokens 等）

        Returns:
            模型回答
        """
        self.call_count += 1
        time.sleep(self.response_delay)

        # 根据提示词内容选择合适的响应
        response = self._analyze_and_respond(prompt, kwargs)

        return response

    def _analyze_and_respond(self, prompt: str, params: Dict[str, Any]) -> str:
        """
        分析提示词并生成相应回答

        Args:
            prompt: 输入提示词
            params: 生成参数

        Returns:
            模拟回答
        """
        prompt_lower = prompt.lower()

        # 检测是否是是否类问题
        if any(word in prompt for word in ["是否", "是不是", "有没有", "对吗"]):
            if "不" in prompt or "没" in prompt or "无" in prompt:
                return self.templates["no_answer"].format(
                    topic=self._extract_topic(prompt),
                    detail="实际情况与问题描述相反"
                )
            else:
                return self.templates["yes_answer"].format(
                    topic=self._extract_topic(prompt),
                    detail="这已经是被确认的事实"
                )

        # 检测年份/时间问题
        if "年" in prompt or "时间" in prompt:
            import re
            year_match = re.search(r'(\d{4})年', prompt)
            if year_match:
                return self.templates["time_answer"].format(
                    time=year_match.group(0),
                    event="该事件"
                )

        # 检测数量问题
        if "多少" in prompt or "几" in prompt:
            return self.templates["number_answer"].format(
                number=random.randint(1, 100),
                unit="个"
            )

        # 检测定义/解释类问题
        if "是什么" in prompt or "什么是" in prompt or "定义" in prompt:
            return self.templates["explanation"].format(
                concept=self._extract_topic(prompt),
                definition="这是一个专业术语或概念",
                features="特性1、特性2、特性3"
            )

        # RAG 类问题（包含上下文）
        if "上下文" in prompt or "context" in prompt_lower:
            return self.templates["rag_answer"].format(
                topic=self._extract_topic(prompt),
                content="这是从知识库中检索到的相关信息..."
            )

        # 默认回答
        return self.templates["qa_default"].format(
            query=self._extract_topic(prompt),
            extra_info="希望能帮到你！"
        )

    def _extract_topic(self, text: str) -> str:
        """
        从文本中提取主题词

        Args:
            text: 输入文本

        Returns:
            主题词
        """
        # 简单提取：去除常见的问句词和标点
        topic = text
        for word in ["什么是", "是什么", "请问", "能否", "如何", "怎么", "?", "？", "的", "是", "了", "在"]:
            topic = topic.replace(word, "")
        return topic.strip()[:20]  # 限制长度

    def generate_with_error(self, error_type: str) -> str:
        """
        生成特定类型的错误响应（用于鲁棒性测试）

        Args:
            error_type: 错误类型
                - empty: 空响应
                - very_short: 过短响应
                - very_long: 过长响应
                - gibberish: 乱码
                - repetition: 重复内容
                - timeout: 超时（抛出异常）
                - api_error: API 错误（抛出异常）

        Returns:
            错误响应（或抛出异常）

        Raises:
            TimeoutError: 当 error_type 为 timeout 时
            ConnectionError: 当 error_type 为 api_error 时
        """
        self.call_count += 1
        time.sleep(self.response_delay)

        if error_type == "timeout":
            raise TimeoutError("模拟 API 超时")

        if error_type == "api_error":
            raise ConnectionError("模拟 API 连接错误")

        if error_type in self.error_responses:
            return self.error_responses[error_type]

        return ""

    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """
        批量生成回答

        Args:
            prompts: 提示词列表
            **kwargs: 其他参数

        Returns:
            回答列表
        """
        return [self.generate(prompt, **kwargs) for prompt in prompts]

    def get_call_count(self) -> int:
        """获取调用次数"""
        return self.call_count

    def reset(self):
        """重置调用计数器"""
        self.call_count = 0


class MockRAGSystem:
    """模拟 RAG 检索系统"""

    def __init__(self):
        """初始化 Mock RAG 系统"""
        self.call_count = 0

        # 模拟文档库
        self.document_store = {
            "langchain": "LangChain 是一个用于开发由语言模型驱动的应用程序的框架。它提供了一套全面的工具和组件。",
            "rag": "RAG（检索增强生成）是一种将信息检索与生成式 AI 相结合的技术，可以提高回答的准确性。",
            "python": "Python 是一种高级编程语言，以其简洁的语法和强大的功能而闻名。",
            "2025": "2025 年是世界足球锦标赛年，这将是全球足球爱好者的盛会。",
            "世界杯": "世界杯是世界上最具影响力的足球比赛，每四年举办一次。2026 年将在美国、加拿大和墨西哥联合举办。",
        }

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        """
        模拟检索相关文档

        Args:
            query: 查询问题
            top_k: 返回文档数量

        Returns:
            检索到的文档列表
        """
        self.call_count += 1

        # 简单的关键词匹配
        results = []
        for keyword, doc in self.document_store.items():
            if keyword.lower() in query.lower() or query.lower() in doc.lower():
                results.append(doc)

        return results[:top_k]

    def generate_with_rag(self, query: str) -> str:
        """
        使用 RAG 生成回答

        Args:
            query: 查询问题

        Returns:
            生成的回答
        """
        retrieved_docs = self.retrieve(query)

        if not retrieved_docs:
            return f"抱歉，我没有找到与「{query}」相关的信息。"

        context = " ".join(retrieved_docs)
        return f"根据检索到的文档：{context}\n\n针对您的问题，以上是相关信息。"

    def get_call_count(self) -> int:
        """获取检索调用次数"""
        return self.call_count
