"""
RAG 演示 - 输出到文件
"""

import sys
from simple_demo import SimpleRAGDemo

def main():
    demo = SimpleRAGDemo()
    demo.load_documents()
    demo.split_documents(demo.documents)

    # 运行查询
    questions = ["什么是 LangChain？", "RAG 有什么优势？"]

    results = []
    for question in questions:
        relevant_docs = demo.simple_search(question)
        answer = demo.generate_answer(question, relevant_docs)
        results.append({
            "question": question,
            "context": [doc.page_content[:200] for doc in relevant_docs],
            "answer": answer
        })

    # 输出到文件
    with open("rag_result.txt", "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("RAG 系统运行结果\n")
        f.write("=" * 60 + "\n\n")

        for i, result in enumerate(results, 1):
            f.write(f"[查询 {i}] {result['question']}\n")
            f.write("-" * 60 + "\n")
            f.write("检索到的相关文档:\n")
            for j, ctx in enumerate(result['context'], 1):
                f.write(f"  [{j}] {ctx}...\n")
            f.write("\n")
            f.write("生成的回答:\n")
            f.write(f"  {result['answer']}\n")
            f.write("\n" + "=" * 60 + "\n\n")

    print("结果已保存到 rag_result.txt")

    # 同时打印到控制台
    with open("rag_result.txt", "r", encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    main()
