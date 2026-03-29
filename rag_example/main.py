"""
RAG 系统主程序
演示如何使用 RAGSystem 进行问答
"""

import os
from dotenv import load_dotenv

from rag import RAGSystem

load_dotenv()


def main():
    """主程序"""
    # 检查 API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请在 .env 文件中设置你的 API Key")
        print("格式: OPENAI_API_KEY=your-api-key")
        print("\n如果使用智谱AI，还需要设置:")
        print("OPENAI_BASE_URL=https://open.bigmodel.cn/api/pas/v1")
        return

    # 创建 RAG 系统实例
    rag = RAGSystem(
        data_path="./data",           # 文档目录
        persist_directory="./chroma_db",  # 向量数据库目录
        use_simple_embeddings=True,   # 使用简单嵌入（演示版）
    )

    # 选择模式
    print("\n" + "=" * 50)
    print("RAG 问答系统")
    print("=" * 50)
    print("1. 从零构建（首次使用或文档更新后）")
    print("2. 加载已存在的系统")
    print("=" * 50)

    choice = input("\n请选择模式 (1/2): ").strip()

    if choice == "1":
        # 从零构建
        rag.build_from_scratch()
    elif choice == "2":
        # 加载已存在的
        try:
            rag.load_existing()
        except Exception as e:
            print(f"加载失败: {e}")
            print("将尝试从零构建...")
            rag.build_from_scratch()
    else:
        print("无效选择，退出程序")
        return

    # 问答循环
    print("\n" + "=" * 50)
    print("进入问答模式（输入 'quit' 退出）")
    print("=" * 50)

    while True:
        question = input("\n请输入问题: ").strip()

        if question.lower() in ["quit", "exit", "退出", "q"]:
            print("再见！")
            break

        if not question:
            continue

        print("\n查询中...")
        result = rag.query(question)

        print("\n" + "-" * 50)
        print(f"问题: {result['question']}")
        print(f"回答: {result['answer']}")
        print("-" * 50)

        # 显示来源
        if result['source_documents']:
            print("\n参考来源:")
            for i, doc in enumerate(result['source_documents'], 1):
                source = doc.metadata.get('source', '未知来源')
                page = doc.metadata.get('page', '未知页码')
                content = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                print(f"  [{i}] {source} (页码: {page})")
                print(f"      内容片段: {content}")


if __name__ == "__main__":
    main()
