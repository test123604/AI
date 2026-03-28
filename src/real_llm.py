"""
真实大模型调用模块
支持通义千问、DeepSeek 等多种 API
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class RealLLM:
    """真实大模型调用类"""

    def __init__(self, provider: str = "dashscope"):
        """
        初始化真实 LLM

        Args:
            provider: 提供商，支持 "dashscope"(通义千问)、"deepseek"、"openai"、"coze" 等
        """
        self.provider = provider
        self.call_count = 0

    def generate(self, prompt: str, **kwargs) -> str:
        """
        调用真实大模型生成回答

        Args:
            prompt: 输入提示词
            **kwargs: 其他参数 (temperature, max_tokens 等)

        Returns:
            模型回答
        """
        self.call_count += 1

        if self.provider == "dashscope":
            return self._call_dashscope(prompt, **kwargs)
        elif self.provider == "deepseek":
            return self._call_deepseek(prompt, **kwargs)
        elif self.provider == "openai":
            return self._call_openai(prompt, **kwargs)
        elif self.provider == "coze":
            return self._call_coze(prompt, **kwargs)
        else:
            raise ValueError(f"不支持的提供商: {self.provider}")

    def _call_dashscope(self, prompt: str, **kwargs) -> str:
        """调用通义千问 API"""
        try:
            from dashscope import Generation

            api_key = os.getenv('DASHSCOPE_API_KEY')
            if not api_key:
                raise ValueError("未配置 DASHSCOPE_API_KEY")

            import dashscope
            dashscope.api_key = api_key

            response = Generation.call(
                model='qwen-turbo',
                prompt=prompt,
                max_tokens=kwargs.get('max_tokens', 1500),
                temperature=kwargs.get('temperature', 0.7),
            )

            if response.status_code == 200:
                return response.output.text
            else:
                raise Exception(f"API 调用失败: {response.message}")

        except ImportError:
            raise ImportError("请安装 dashscope: pip install dashscope")

    def _call_deepseek(self, prompt: str, **kwargs) -> str:
        """调用 DeepSeek API"""
        try:
            from openai import OpenAI

            api_key = os.getenv('DEEPSEEK_API_KEY')
            if not api_key:
                raise ValueError("未配置 DEEPSEEK_API_KEY")

            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get('max_tokens', 1500),
                temperature=kwargs.get('temperature', 0.7),
            )

            return response.choices[0].message.content

        except ImportError:
            raise ImportError("请安装 openai: pip install openai")

    def _call_openai(self, prompt: str, **kwargs) -> str:
        """调用 OpenAI API"""
        try:
            from openai import OpenAI

            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("未配置 OPENAI_API_KEY")

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get('max_tokens', 1500),
                temperature=kwargs.get('temperature', 0.7),
            )

            return response.choices[0].message.content

        except ImportError:
            raise ImportError("请安装 openai: pip install openai")

    def _call_coze(self, prompt: str, **kwargs) -> str:
        """
        调用 Coze 工作流 API

        Coze API 文档: https://www.coze.cn/docs/developer_guid/api_reference
        """
        try:
            api_key = os.getenv('COZE_API_KEY')
            if not api_key:
                raise ValueError("未配置 COZE_API_KEY")

            # Coze 工作流 API 端点
            # 需要提供工作流 ID 或 Bot ID
            workflow_id = kwargs.get('workflow_id') or os.getenv('COZE_WORKFLOW_ID')
            bot_id = kwargs.get('bot_id') or os.getenv('COZE_BOT_ID')

            if not workflow_id and not bot_id:
                raise ValueError("需要配置 workflow_id 或 bot_id")

            import requests

            # 方式1: 调用工作流 API
            if workflow_id:
                url = f"https://api.coze.cn/v1/workflow/run"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "workflow_id": workflow_id,
                    "parameters": {
                        "query": prompt  # 根据工作流输入参数调整
                    }
                }
            # 方式2: 调用 Bot API
            else:
                url = f"https://api.coze.cn/v3/chat"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "bot_id": bot_id,
                    "user": "test_user",
                    "query": prompt,
                    "stream": False
                }

            response = requests.post(url, json=data, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()

            # 解析 Coze 响应
            if workflow_id:
                # 工作流响应格式
                if result.get('code') == 0:
                    return result.get('data', {}).get('answer', str(result))
                else:
                    raise Exception(f"Coze API 错误: {result.get('msg')}")
            else:
                # Bot 聊天响应格式
                messages = result.get('messages', [])
                if messages:
                    return messages[-1].get('content', '')
                return result.get('data', str(result))

        except ImportError:
            raise ImportError("请安装 requests: pip install requests")
        except Exception as e:
            raise Exception(f"Coze API 调用失败: {str(e)}")

    def get_call_count(self) -> int:
        """获取调用次数"""
        return self.call_count


# 创建全局实例
_real_llm = None


def get_real_llm(provider: str = "dashscope") -> RealLLM:
    """获取真实 LLM 实例"""
    global _real_llm
    if _real_llm is None:
        _real_llm = RealLLM(provider)
    return _real_llm
