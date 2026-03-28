# 大模型测试框架 (LLM Testing Framework)

> **基于 Python + Pytest + LangChain 的 AI 大模型自动化测试框架**
> 支持准确性、鲁棒性、格式规范和 RAG 检索四个维度的全面测试

## 🎯 项目亮点

### 技术实现
- ✅ **100+ 自动化测试用例**：JSON 驱动，覆盖准确性、鲁棒性、格式规范、RAG 检索四个维度
- ✅ **智能评估算法**：关键词匹配 (jieba) + 语义相似度 (SentenceTransformer) 双重验证，解决大模型回答泛化性问题
- ✅ **提示词工程优化**：结构化提示词 + Few-shot + 思维链，准确率提升至 100%
- ✅ **多平台适配**：统一接口支持通义千问、DeepSeek、OpenAI、Coze 工作流

### 项目成果
| 指标 | Mock 测试 | 真实 API 测试 |
|------|----------|--------------|
| 测试通过率 | 85% | 100% |
| 平均响应时间 | <0.1s | ~4s/次 |
| 测试用例数 | 105条 | 可配置 |

### 匹配岗位技能
- 🎯 **AI 模型测试**：全面的测试维度，智能评估算法
- 🎯 **提示词工程**：结构化提示词设计，Few-shot 示例，思维链优化
- 🎯 **测试框架设计**：模块化架构，可扩展的 JSON 驱动设计
- 🎯 **API 集成**：多种大模型 API 和工作流平台的统一适配

## 功能特点

- ✅ **105+ 测试用例**：覆盖准确性、鲁棒性、格式规范、RAG 检索四个维度
- ✅ **关键词匹配 + 语义相似度**：双重评估机制，确保回答质量
- ✅ **Mock 模拟**：不消耗真实 API 额度，快速测试
- ✅ **Allure 报告**：生成美观的测试报告
- ✅ **JSON 配置**：测试用例从 JSON 文件读取，易于维护和扩展

## 项目结构

```
testai/
├── test_cases/              # 测试用例 JSON 文件
│   ├── accuracy.json        # 准确性测试 (30条)
│   ├── robustness.json      # 鲁棒性测试 (30条)
│   ├── format.json          # 格式规范测试 (20条)
│   └── rag.json            # RAG 检索测试 (25条)
├── src/
│   ├── evaluator.py        # 评估器（关键词匹配 + 语义相似度）
│   ├── mock_llm.py         # Mock 大模型和 RAG 系统
│   └── __init__.py
├── tests/
│   ├── test_accuracy.py    # 准确性测试
│   ├── test_robustness.py  # 鲁棒性测试
│   ├── test_format.py      # 格式规范测试
│   ├── test_rag.py         # RAG 检索测试
│   └── __init__.py
├── reports/                # Allure 报告目录
├── conftest.py             # pytest 配置
├── requirements.txt        # 依赖包
└── README.md              # 说明文档
```

## 评估方法

### 1. 关键词匹配

从预期答案中提取关键词，检查实际回答是否包含：

- **普通关键词**：使用 jieba 分词提取
- **数字**：提取年份数字、数量等
- **否定词**：检测"不"、"没"、"无"等

### 2. 语义相似度

使用 SentenceTransformer 计算余弦相似度：

- 模型：`paraphrase-multilingual-MiniLM-L12-v2`（支持中文）
- 阈值：0.7（可配置）
- 相似度 ≥ 0.7 视为通过

### 3. 综合判断

```
通过条件 = (关键词命中率 ≥ 0.4) AND (语义相似度 ≥ 0.7 OR 数字匹配 AND 否定词匹配)
```

## 🛠️ 技术栈

### 核心框架
- **pytest**: 测试框架，支持参数化、fixture、标记、并行测试
- **pytest-cov**: 代码覆盖率统计
- **pytest-xdist**: 并行测试加速
- **allure-pytest**: 可视化 HTML 测试报告

### NLP 与机器学习
- **jieba**: 中文分词，关键词提取
- **SentenceTransformer**: 多语言语义编码，支持中文
- **scikit-learn**: 余弦相似度计算，数值分析
- **numpy**: 数值计算

### LLM 框架与 API
- **LangChain**: RAG 系统、提示词模板管理
- **dashscope**: 通义千问 API (阿里云)
- **openai**: OpenAI / DeepSeek / 兼容接口

### 工具库
- **python-dotenv**: 环境变量管理
- **requests**: HTTP 请求，API 调用
- **pandas**: 数据处理（可选）

## 🚀 快速开始

### 1. 安装依赖

```bash
cd E:/Auto/testai
pip install -r requirements.txt
```

### 2. 运行所有测试

```bash
# 运行所有测试
pytest

# 运行指定维度的测试
pytest tests/test_accuracy.py    # 准确性测试
pytest tests/test_robustness.py  # 鲁棒性测试
pytest tests/test_format.py      # 格式规范测试
pytest tests/test_rag.py         # RAG 检索测试

# 运行高优先级测试
pytest -m "high_priority"

# 并行运行（加快测试速度）
pytest -n auto
```

### 3. 生成 Allure 报告

```bash
# 运行测试并生成结果
pytest --alluredir=reports/allure-results

# 生成 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开报告
allure open reports/allure-report
```

### 4. 查看测试覆盖率

```bash
pytest --cov=src --cov-report=html
```

## 测试用例格式

测试用例存储在 JSON 文件中，格式如下：

```json
{
  "description": "测试用例描述",
  "test_cases": [
    {
      "id": "TEST_001",
      "name": "测试用例名称",
      "category": "测试类别",
      "query": "测试问题",
      "expected_keywords": ["关键词1", "关键词2"],
      "expected_numbers": ["2024"],
      "mock_response": "模拟的回答",
      "priority": "high"
    }
  ]
}
```

## 扩展测试用例

1. 在 `test_cases/` 目录下创建新的 JSON 文件
2. 按照上述格式添加测试用例
3. 在 `tests/` 目录下创建对应的测试模块
4. 运行 `pytest` 自动加载新测试

## 配置说明

### 修改相似度阈值

在 `src/evaluator.py` 中修改：

```python
evaluator = AnswerEvaluator(similarity_threshold=0.7)  # 修改阈值
```

### 添加新的评估维度

1. 在 `src/evaluator.py` 中添加新的评估方法
2. 在测试模块中调用新方法
3. 在 JSON 文件中添加对应的测试用例

## 常见问题

### Q: 如何测试真实的 LLM API？

A: 将 `mock_llm.py` 中的 `MockLLM` 替换为真实的 API 调用，例如：

```python
import dashscope
from dashscope import Generation

def generate(self, prompt: str, **kwargs) -> str:
    response = Generation.call(
        model='qwen-turbo',
        prompt=prompt,
        **kwargs
    )
    return response.output.text
```

### Q: 如何调整测试速度？

A: 使用并行运行：

```bash
pytest -n auto  # 自动检测 CPU 核心数并行运行
```

### Q: 测试失败怎么办？

A: 查看 Allure 报告中的详细信息，包括：
- 测试用例详情
- 模型回答
- 评估结果
- 失败原因

## 测试维度说明

| 维度 | 测试内容 | 用例数量 |
|------|---------|---------|
| 准确性 | 回答是否正确、准确 | 30 |
| 鲁棒性 | 异常输入处理能力 | 30 |
| 格式规范 | 回答格式是否符合要求 | 20 |
| RAG 检索 | 检索和生成质量 | 25 |

## License

MIT

---

**项目描述**：

设计并实现了一套基于 **Python + Pytest + LangChain** 的大模型自动化测试框架，支持通义千问、DeepSeek、OpenAI、Coze 工作流等多种平台的测试评估。

**核心成果**：

1. **智能评估算法**：设计关键词匹配 (jieba 分词) + 语义相似度 (SentenceTransformer) 双重验证机制，有效解决大模型回答泛化性问题，实现自动化质量评估

2. **提示词工程优化**：设计结构化提示词模板，结合 Few-shot 示例和思维链技术，针对不同场景优化提示词策略，将回答准确率提升至 100%

3. **多平台 API 适配**：统一封装多种大模型 API (通义千问、DeepSeek、OpenAI) 和工作流平台 (Coze)，支持工作流和对话两种调用模式

4. **测试工程实践**：采用 JSON 驱动的测试用例设计，实现数据与代码分离；集成 Allure 生成可视化测试报告，支持 CI/CD 集成

**技术亮点**：

- ✅ **105+ 测试用例**：覆盖准确性、鲁棒性、格式规范、RAG 检索四个维度
- ✅ **双重验证机制**：关键词匹配 + 语义相似度，平衡准确性和泛化能力
- ✅ **自适应评估**：根据问题类型（数值型、否定型、定义型）动态调整评估标准
- ✅ **Mock + 实测双模式**：支持无消耗的 Mock 测试和真实的 API 测试

**项目成果**：

| 指标 | 数值 |
|------|------|
| 测试通过率 | Mock 85% / 真实 API 100% |
| 测试用例数 | 105+ 条 |
| 平均响应时间 | <5 秒/次 |
| 代码覆盖率 | 可配置 |

**相关技能**：

- Python、Pytest、测试框架设计
- LangChain、RAG 系统、提示词工程
- NLP 处理 (jieba、SentenceTransformer)
- API 集成 (通义千问、DeepSeek、Coze)
- 机器学习 (scikit-learn、语义相似度)
