# 真实大模型测试指南

## 配置步骤

### 1. 获取 API Key

#### 通义千问（推荐，有免费额度）
1. 访问：https://dashscope.console.aliyun.com/apiKey
2. 登录阿里云账号
3. 创建 API Key
4. 复制 Key

#### DeepSeek（推荐，性价比高）
1. 访问：https://platform.deepseek.com/api_keys
2. 注册/登录账号
3. 创建 API Key

#### OpenAI
1. 访问：https://platform.openai.com/api-keys
2. 登录账号
3. 创建 API Key

### 2. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# 例如：
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx
```

### 3. 安装额外依赖

```bash
# 通义千问
pip install dashscope

# DeepSeek / OpenAI
pip install openai
```

## 运行真实 API 测试

### 单个问题测试（快速验证）

```bash
# 测试 API 连接是否正常
pytest tests/test_real_llm.py::TestRealLLM::test_real_llm_single_question -v
```

### 抽样测试（前10个用例）

```bash
# 测试准确性（只运行前10个，节省额度）
pytest tests/test_real_llm.py::TestRealLLM::test_real_llm_accuracy_sample -v
```

### 完整测试（所有用例）

```bash
# 运行所有真实 API 测试（会消耗较多额度）
pytest tests/test_real_llm.py -v
```

## 切换不同的模型

### 使用通义千问
```python
# 在测试文件中修改
self.real_llm = get_real_llm(provider="dashscope")
```

### 使用 DeepSeek
```python
self.real_llm = get_real_llm(provider="deepseek")
```

### 使用 OpenAI
```python
self.real_llm = get_real_llm(provider="openai")
```

## 测试策略建议

### 1. 分阶段测试
- **阶段 1**：先运行 `test_real_llm_single_question` 验证配置
- **阶段 2**：运行抽样测试，检查基本质量
- **阶段 3**：运行完整测试，获取全面评估

### 2. 控制 API 调用次数
```bash
# 只运行特定标记的测试
pytest tests/test_real_llm.py -m "real_api and single" -v

# 限制测试数量
pytest tests/test_real_llm.py::TestRealLLM::test_real_llm_accuracy_sample -v
```

### 3. 查看调用统计
测试报告中会显示：
- API 调用次数
- 每次调用的耗时
- 通过率统计

## 与 Mock 测试对比

| 特性 | Mock 测试 | 真实 API 测试 |
|------|----------|--------------|
| 成本 | 免费 | 消耗 API 额度 |
| 速度 | 快速 | 较慢（网络延迟） |
| 稳定性 | 完全可控 | 依赖网络和 API |
| 真实性 | 模拟数据 | 真实模型输出 |
| 适用场景 | 开发、CI/CD | 验收、质量评估 |

## 常见问题

### Q: API 调用失败怎么办？
A: 检查以下几点：
1. API Key 是否正确配置
2. 网络连接是否正常
3. API 额度是否充足
4. 防火墙是否阻止了请求

### Q: 如何减少 API 调用次数？
A:
1. 使用抽样测试
2. 先运行 Mock 测试，再运行真实测试
3. 使用 `@pytest.mark.skip` 跳过不需要的测试

### Q: 测试太慢怎么办？
A:
1. 减少测试用例数量
2. 使用并行测试：`pytest -n auto`
3. 将耗时测试标记为 `@pytest.mark.slow`，然后排除：`pytest -m "not slow"`

## 生成报告

```bash
# 生成 Allure 报告
pytest tests/test_real_llm.py --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allage-report
```
