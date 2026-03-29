"""
通义千问 API 测试脚本
用于验证 API Key 是否有效
"""

import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# 加载环境变量
load_dotenv()


def test_qwen_api():
    """测试通义千问 API"""
    print("=" * 50)
    print("通义千问 API 测试")
    print("=" * 50)

    # 获取 API Key
    api_key = os.getenv('DASHSCOPE_API_KEY')

    if not api_key or api_key == 'your-dashscope-api-key-here' or api_key == 'your_dashscope_api_key_here':
        print("\n❌ 未配置 API Key")
        print("\n请按以下步骤获取免费 API Key:")
        print("1. 访问: https://dashscope.console.aliyun.com/apiKey")
        print("2. 登录阿里云账号（免费注册）")
        print("3. 创建 API Key")
        print("4. 将 Key 填入 .env 文件的 DASHSCOPE_API_KEY")
        return False

    print(f"\n📝 API Key: {api_key[:8]}...{api_key[-4:]}")
    print("\n🚀 正在测试 API 连接...\n")

    # 设置 API Key
    dashscope.api_key = api_key

    # 测试问题
    test_prompt = "请用一句话介绍一下你自己。"

    print(f"📋 测试问题: {test_prompt}\n")
    print("-" * 50)

    try:
        # 调用 API
        response = Generation.call(
            model='qwen-turbo',
            prompt=test_prompt,
            max_tokens=500,
            temperature=0.7,
        )

        # 检查响应
        if response.status_code == 200:
            print("✅ API 调用成功!\n")
            print("📦 模型回答:")
            print(response.output.text)
            print("\n" + "=" * 50)
            print("✨ API Key 有效，可以正常使用!")
            print("=" * 50)
            return True
        else:
            print(f"❌ API 调用失败")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.message}")
            print(f"   请求ID: {response.request_id}")

            # 根据错误码给出建议
            if response.code == 'InvalidApiKey':
                print("\n💡 建议: API Key 无效，请检查是否正确复制")
            elif response.code == 'Unauthorized':
                print("\n💡 建议: API Key 未授权或已过期")
            return False

    except Exception as e:
        print(f"❌ 连接错误: {e}")
        print("\n💡 可能的原因:")
        print("   1. 网络连接问题（防火墙/代理）")
        print("   2. API Key 格式错误")
        print("   3. API 服务暂时不可用")
        return False


if __name__ == "__main__":
    success = test_qwen_api()
    exit(0 if success else 1)
