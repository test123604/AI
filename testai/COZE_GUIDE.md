# Coze 工作流测试指南

## 一、Coze 平台配置

### 1. 获取 API Key

1. 访问 [Coze 官网](https://www.coze.cn)
2. 登录/注册账号
3. 进入「开发者设置」→「API Key」
4. 创建新的 API Key

### 2. 创建工作流或 Bot

#### 方式 A: 使用工作流 API（推荐用于自动化流程）

1. 在 Coze 创建一个工作流
2. 配置输入参数（如 `query` 字符串类型）
3. 配置输出参数（如 `answer` 字符串类型）
4. 发布工作流
5. 获取工作流 ID

**工作流输入示例：**
```
输入参数名: query
类型: String
必填: 是
```

#### 方式 B: 使用 Bot API（推荐用于对话）

1. 在 Coze 创建一个 Bot
2. 配置工作流或插件
3. 发布 Bot
4. 获取 Bot ID

## 二、配置环境变量

```bash
cd E:/Auto/testai

# 编辑 .env 文件，添加 Coze 配置
```

```env
# Coze API Key
COZE_API_KEY=你的Coze_API_Key

# 工作流方式（二选一）
COZE_WORKFLOW_ID=7384xxxxx

# Bot 方式（二选一）
COZE_BOT_ID=7384xxxxx
```

## 三、运行测试

### 快速验证（单问题测试）

```bash
pytest tests/test_coze.py::TestCozeWorkflow::test_coze_single_question -v
```

### 抽样测试（5个用例）

```bash
pytest tests/test_coze.py::TestCozeWorkflow::test_coze_workflow_sample -v
```

### 鲁棒性测试

```bash
pytest tests/test_coze.py::TestCozeWorkflow::test_coze_robustness -v
```

### 所有 Coze 测试

```bash
pytest tests/test_coze.py -v
```

## 四、Coze API 说明

### 工作流 API 调用

```
POST https://api.coze.cn/v1/workflow/run

Headers:
  Authorization: Bearer {COZE_API_KEY}
  Content-Type: application/json

Body:
{
  "workflow_id": "your_workflow_id",
  "parameters": {
    "query": "用户问题"
  }
}
```

### Bot API 调用

```
POST https://api.coze.cn/v3/chat

Headers:
  Authorization: Bearer {COZE_API_KEY}
  Content-Type: application/json

Body:
{
  "bot_id": "your_bot_id",
  "user": "test_user",
  "query": "用户问题",
  "stream": false
}
```

## 五、测试框架适配说明

### 1. 输入适配

Coze 工作流的输入参数需要与测试用例匹配。如果工作流期望的参数名不是 `query`，需要修改 `real_llm.py` 中的调用代码：

```python
# src/real_llm.py 中修改
data = {
    "workflow_id": workflow_id,
    "parameters": {
        "input": prompt  # 根据工作流配置调整参数名
    }
}
```

### 2. 输出适配

Coze 的响应格式可能有多种：

- **标准响应**: `{"code": 0, "data": {"answer": "回答内容"}}`
- **聊天响应**: `{"messages": [{"content": "回答内容"}]}`

框架已处理多种格式，如果工作流返回格式不同，可以修改解析逻辑：

```python
# src/real_llm.py 中修改
if result.get('code') == 0:
    # 根据实际返回格式调整
    return result.get('data', {}).get('output', str(result))
```

## 六、常见问题

### Q1: API 调用失败 "401 Unauthorized"

A: 检查 API Key 是否正确，是否有调用权限

### Q2: API 调用失败 "workflow_id not found"

A:
- 确认工作流 ID 是否正确
- 确认工作流是否已发布
- 确认 API Key 是否有该工作流的访问权限

### Q3: 返回结果为空

A:
- 检查工作流输出配置
- 检查输入参数是否匹配
- 查看 Coze 平台的日志

### Q4: 如何自定义测试用例？

A: 编辑 `test_cases/accuracy.json` 或创建新的 JSON 文件，格式如下：

```json
{
  "description": "自定义测试用例",
  "test_cases": [
    {
      "id": "CUSTOM_001",
      "name": "测试用例名称",
      "query": "你的问题",
      "expected_keywords": ["关键词1", "关键词2"],
      "priority": "high"
    }
  ]
}
```

## 七、与真实大模型测试的对比

| 特性 | 大模型 API | Coze 工作流 |
|------|----------|-------------|
| 配置方式 | API Key | API Key + Workflow/Bot ID |
| 输入格式 | 纯文本提示 | 结构化参数 |
| 输出格式 | 纯文本回答 | 结构化数据 |
| 适用场景 | 通用问答测试 | 特定业务流程测试 |
| 灵活性 | 高 | 中（需要在 Coze 平台配置）|

## 八、推荐使用场景

### 适合用 Coze 工作流测试的场景：

1. **企业内部 Bot**：测试客服、问答机器人
2. **业务流程自动化**：审批、填报、查询等
3. **多步骤任务**：涉及多个工具插件的复杂流程
4. **RAG 应用**：结合知识库的问答系统

### 适合用大模型 API 测试的场景：

1. **通用问答测试**：知识问答、开放域对话
2. **模型对比**：测试不同模型的表现
3. **性能测试**：测试响应速度、并发能力
4. **算法研究**：测试新的提示词技巧
