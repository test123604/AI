"""
pytest 配置文件
配置 Allure 报告路径和公共 fixtures
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def pytest_configure(config):
    """pytest 配置钩子"""
    # 注册 Allure 插件
    config.addinivalue_line(
        "markers", "accuracy: 准确性测试标记"
    )
    config.addinivalue_line(
        "markers", "robustness: 鲁棒性测试标记"
    )
    config.addinivalue_line(
        "markers", "format: 格式规范测试标记"
    )
    config.addinivalue_line(
        "markers", "rag: RAG 检索测试标记"
    )


@pytest.fixture(scope="session")
def test_data_dir():
    """获取测试数据目录路径"""
    return Path(__file__).parent / "test_cases"


@pytest.fixture(scope="session")
def evaluator():
    """评估器 fixture"""
    from src.evaluator import AnswerEvaluator
    return AnswerEvaluator()


@pytest.fixture(scope="session")
def mock_llm():
    """Mock LLM fixture"""
    from src.mock_llm import MockLLM
    return MockLLM()
