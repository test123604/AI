"""
Coze 工作流测试模块
测试 Coze 平台配置的 AI 工作流
"""

import pytest
import json
from pathlib import Path
import allure
import time


@allure.epic("大模型测试")
@allure.feature("Coze工作流测试")
class TestCozeWorkflow:
    """Coze 工作流测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, test_data_dir, evaluator):
        """测试前置条件"""
        self.test_data_dir = test_data_dir
        self.evaluator = evaluator

        # 导入真实 LLM（Coze）
        from src.real_llm import get_real_llm
        self.coze_llm = get_real_llm(provider="coze")

        # 加载测试用例
        accuracy_file = self.test_data_dir / "accuracy.json"
        with open(accuracy_file, 'r', encoding='utf-8') as f:
            self.test_cases = json.load(f)['test_cases']

        # 结果文件
        self.result_file = Path(__file__).parent.parent / "coze_result.txt"

    @pytest.mark.accuracy
    @pytest.mark.coze
    def test_coze_workflow_sample(self):
        """
        测试 Coze 工作流（抽样测试）
        只运行前5个用例，避免消耗过多额度
        """
        # 初始化结果文件
        with open(self.result_file, 'w', encoding='utf-8') as f:
            f.write(f"{'='*60}\n")
            f.write("Coze 工作流测试结果\n")
            f.write(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n\n")

        sample_cases = self.test_cases[:5]

        pass_count = 0
        results = []

        for case in sample_cases:
            with allure.step(f"测试: {case['name']}"):
                try:
                    start_time = time.time()
                    response = self.coze_llm.generate(case['query'])
                    elapsed_time = time.time() - start_time

                    # 写入结果文件
                    with open(self.result_file, 'a', encoding='utf-8') as f:
                        f.write(f"\n{'='*60}\n")
                        f.write(f"测试用例: {case['id']} - {case['name']}\n")
                        f.write(f"{'='*60}\n")
                        f.write(f"问题: {case['query']}\n")
                        f.write(f"回答: {response}\n")
                        f.write(f"耗时: {elapsed_time:.2f}秒\n")

                    # 评估回答
                    expected_keywords = set(case.get('expected_keywords', []))
                    eval_result = self.evaluator.evaluate(
                        expected=" ".join(expected_keywords),
                        actual=response
                    )

                    test_passed = eval_result['pass']
                    if test_passed:
                        pass_count += 1

                    results.append({
                        'id': case['id'],
                        'name': case['name'],
                        'passed': test_passed,
                        'elapsed_time': elapsed_time,
                        'similarity': eval_result['semantic_similarity'],
                        'keyword_hit_rate': eval_result['keyword_hit_rate']
                    })

                except Exception as e:
                    allure.attach(
                        str(e),
                        name="错误信息",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    results.append({
                        'id': case['id'],
                        'name': case['name'],
                        'passed': False,
                        'error': str(e)
                    })

        # 写入摘要
        with open(self.result_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write("测试摘要\n")
            f.write(f"{'='*60}\n")
            f.write(f"通过: {pass_count}/{len(sample_cases)}\n")
            f.write(f"API 调用次数: {self.coze_llm.get_call_count()}\n")
            f.write(f"{'='*60}\n")

        # Coze 工作流测试通过率要求 50%
        assert pass_count / len(sample_cases) >= 0.5, (
            f"Coze 工作流测试通过率过低: {pass_count}/{len(sample_cases)}"
        )

    @pytest.mark.accuracy
    @pytest.mark.coze
    @pytest.mark.single
    def test_coze_single_question(self):
        """
        单个问题测试
        用于快速验证 Coze 配置是否正确
        """
        test_case = {
            "id": "COZE_001",
            "name": "测试 Coze 连接",
            "query": "天空是什么颜色的？",
            "expected_keywords": ["蓝色", "蓝天"]
        }

        with allure.step("测试 Coze 工作流连接"):
            try:
                response = self.coze_llm.generate(test_case['query'])

                # 写入结果文件
                with open(self.result_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"单问题测试: {test_case['id']}\n")
                    f.write(f"{'='*60}\n")
                    f.write(f"问题: {test_case['query']}\n")
                    f.write(f"回答: {response}\n")
                    f.write(f"API 调用次数: {self.coze_llm.get_call_count()}\n")

                # 基本检查：回答不为空
                assert len(response) > 0, "Coze API 返回空响应"

                # 检查是否包含预期关键词
                expected_keywords = set(test_case['expected_keywords'])
                eval_result = self.evaluator.evaluate(
                    expected=" ".join(expected_keywords),
                    actual=response
                )

                allure.attach(
                    json.dumps(eval_result, ensure_ascii=False, indent=2),
                    name="评估结果",
                    attachment_type=allure.attachment_type.JSON
                )

            except Exception as e:
                pytest.fail(f"Coze API 调用失败: {e}")

    @pytest.mark.robustness
    @pytest.mark.coze
    def test_coze_robustness(self):
        """测试 Coze 工作流的鲁棒性"""
        test_queries = [
            {"query": "", "name": "空输入"},
            {"query": "     ", "name": "纯空格"},
            {"query": "你好😊", "name": "表情符号"},
            {"query": "test input for 你好", "name": "混合语言"},
        ]

        pass_count = 0
        for test in test_queries:
            with allure.step(f"鲁棒性测试: {test['name']}"):
                try:
                    response = self.coze_llm.generate(test['query'])
                    if len(response) > 0:
                        pass_count += 1
                except Exception as e:
                    allure.attach(
                        str(e),
                        name="错误",
                        attachment_type=allure.attachment_type.TEXT
                    )

        allure.attach(
            f"鲁棒性测试通过: {pass_count}/{len(test_queries)}",
            name="鲁棒性测试结果",
            attachment_type=allure.attachment_type.TEXT
        )

        # 鲁棒性测试至少 50% 通过
        assert pass_count / len(test_queries) >= 0.5
