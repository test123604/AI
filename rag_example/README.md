# LangChain RAG 示例项目

这是一个使用 LangChain 框架构建的 RAG（检索增强生成）完整示例。

## 目录结构

```
rag_example/
├── rag/                    # RAG 模块
│   ├── __init__.py
│   └── rag_system.py      # RAG 系统核心实现
├── data/                   # 文档数据目录
│   └── sample_text.txt    # 示例文档
├── chroma_db/             # 向量数据库（运行后生成）
├── main.py                # 主程序
├── requirements.txt       # 依赖列表
├── .env.example           # 环境变量示例
└── README.md              # 本文档
```

## 什么是 RAG？

RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合**信息检索**和**生成式 AI**的技术：

```
用户提问
    │
    ▼
┌─────────────┐
│ 向量检索    │ → 从知识库中找到相关文档
└─────────────┘
    │
    ▼
┌─────────────┐
│ LLM 生成    │ → 基于检索到的文档生成回答
└─────────────┘
    │
    ▼
带有引用的回答
```

### RAG 的优势

| 优势 | 说明 |
|------|------|
| **减少幻觉** | 基于真实文档回答，减少模型编造 |
| **知识更新** | 更新文档即可更新知识，无需重新训练模型 |
| **可解释性** | 可以查看引用的文档来源 |
| **成本效益** | 相比微调模型，成本更低 |

## 安装步骤

### 1. 安装依赖

```bash
cd E:/Auto/rag_example
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的 API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 使用 OpenAI
OPENAI_API_KEY=sk-your-openai-key
OPENAI_BASE_URL=https://api.openai.com/v1

# 或使用智谱AI（推荐国内用户）
OPENAI_API_KEY=your-zhipu-api-key
OPENAI_BASE_URL=https://open.bigmodel.cn/api/pas/v1
```

## 使用方法

### 方式一：交互式运行

```bash
python main.py
```

程序会提示你选择模式：
- **模式 1**：从零构建（首次使用或文档更新后选择）
- **模式 2**：加载已存在的系统（后续使用选择此模式更快）

### 方式二：代码中使用

```python
from rag import RAGSystem

# 创建 RAG 实例
rag = RAGSystem(
    data_path="./data",
    persist_directory="./chroma_db",
    use_openai=False  # 使用本地嵌入模型
)

# 首次使用：构建系统
rag.build_from_scratch()

# 后续使用：直接加载
# rag.load_existing()

# 查询
result = rag.query("什么是 LangChain？")
print(result['answer'])
```

## RAG 工作流程详解

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RAG 系统工作流程                              │
└─────────────────────────────────────────────────────────────────────┘

  阶段 1: 索引构建（一次性）

  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
  │ 文档加载│ →  │ 文档分割│ →  │ 向量化  │ →  │ 存储到  │
  │         │    │         │    │         │    │ 向量库  │
  └─────────┘    └─────────┘    └─────────┘    └─────────┘
  PDF/TXT      500字符/块     Embedding      ChromaDB

  阶段 2: 问答（每次查询）

  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
  │ 用户问题│ →  │ 向量检索│ →  │ 组合上下│ →  │ LLM生成 │
  │         │    │ Top K=4 │    │ 文+问题 │    │   回答  │
  └─────────┘    └─────────┘    └─────────┘    └─────────┘
                 相似度搜索      Prompt模板
```

### 关键参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `chunk_size` | 500 | 每个文本块的字符数 |
| `chunk_overlap` | 50 | 块之间的重叠字符数 |
| `search_kwargs.k` | 4 | 检索时返回的相关文档数量 |
| `temperature` | 0 | LLM 温度，0 使回答更确定 |

## 扩展功能

### 添加更多文档

将 PDF 或 TXT 文件放入 `data/` 目录，然后重新构建系统。

### 自定义提示词

编辑 `rag_system.py` 中的 `prompt_template`：

```python
prompt_template = """你是一个专业的客服助手。
请根据以下上下文回答用户问题，保持友好和专业的语气。

上下文: {context}
问题: {question}

回答:"""
```

### 使用不同的嵌入模型

```python
# 使用 OpenAI 嵌入（需要付费）
rag = RAGSystem(use_openai=True)

# 使用其他本地模型
rag = RAGSystem(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## 常见问题

**Q: 首次运行很慢？**
A: 首次运行会下载嵌入模型（约 200MB），之后会缓存。

**Q: 如何添加 PDF 文档？**
A: 将 PDF 文件放入 `data/` 目录，选择模式 1 重新构建。

**Q: 向量数据库存在哪里？**
A: 默认在 `chroma_db/` 目录，可以删除重建。

**Q: 支持中文吗？**
A: 完全支持！使用的是多语言嵌入模型。

## 进阶方向

- [ ] 支持更多文档格式（Word、Markdown）
- [ ] 添加文档来源追踪
- [ ] 实现流式输出
- [ ] 添加 Web UI 界面
- [ ] 支持多轮对话记忆

## 参考资源

- [LangChain 官方文档](https://python.langchain.com/)
- [ChromaDB 文档](https://docs.trychroma.com/)
- [OpenAI API 文档](https://platform.openai.com/docs/)
