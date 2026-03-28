"""
准确性测试模块
测试模型回答是否准确、正确
"""

import pytest
import json
from pathlib import Path
import allure


@allure.epic("大模型测试")
@allure.feature("准确性测试")
class TestAccuracy:
    """准确性测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, test_data_dir, mock_llm, evaluator):
        """测试前置条件"""
        self.test_data_dir = test_data_dir
        self.mock_llm = mock_llm
        self.evaluator = evaluator

        # 加载测试用例
        accuracy_file = self.test_data_dir / "accuracy.json"
        with open(accuracy_file, 'r', encoding='utf-8') as f:
            self.test_cases = json.load(f)['test_cases']

    @pytest.mark.accuracy
    def test_all_accuracy_cases(self):
        """
        运行所有准确性测试用例
        使用pytest动态生成测试用例
        """
        for case in self.test_cases:
            with allure.step(f"执行测试用例: {case['name']}"):
                allure.attach(
                    json.dumps(case, ensure_ascii=False, indent=2),
                    name="测试用例详情",
                    attachment_type=allure.attachment_type.JSON
                )

                # 使用预定义的 mock_response（确保测试可控）
                response = case.get('mock_response', self.mock_llm.generate(case['query']))

                allure.attach(
                    case['query'],
                    name="问题",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    response,
                    name="模型回答",
                    attachment_type=allure.attachment_type.TEXT
                )

                # 获取预期关键词
                expected_keywords = set(case.get('expected_keywords', []))

                # 评估回答
                eval_result = self.evaluator.evaluate(
                    expected=" ".join(expected_keywords),
                    actual=response
                )

                allure.attach(
                    json.dumps(eval_result, ensure_ascii=False, indent=2),
                    name="评估结果",
                    attachment_type=allure.attachment_type.JSON
                )

                # 断言测试通过
                assert eval_result['pass'], (
                    f"准确性测试失败 [{case['id']}]: {case['name']}\n"
                    f"问题: {case['query']}\n"
                    f"预期关键词: {expected_keywords}\n"
                    f"回答: {response}\n"
                    f"语义相似度: {eval_result['semantic_similarity']:.2f}\n"
                    f"关键词命中率: {eval_result['keyword_hit_rate']:.2f}"
                )

    @pytest.mark.accuracy
    @pytest.mark.high_priority
    def test_high_priority_accuracy_cases(self):
        """只运行高优先级的准确性测试"""
        high_priority_cases = [
            case for case in self.test_cases
            if case.get('priority') == 'high'
        ]

        for case in high_priority_cases:
            with allure.step(f"高优先级测试: {case['name']}"):
                response = self.mock_llm.generate(case['query'])
                expected_keywords = set(case.get('expected_keywords', []))

                eval_result = self.evaluator.evaluate(
                    expected=" ".join(expected_keywords),
                    actual=response
                )

                assert eval_result['pass'], (
                    f"高优先级测试失败 [{case['id']}]: {case['name']}"
                )

    @pytest.mark.accuracy
    def test_factual_qa_accuracy(self):
        """测试事实性问答的准确性"""
        factual_cases = [
            case for case in self.test_cases
            if case.get('category') == 'factual_qa'
        ]

        pass_count = 0
        for case in factual_cases:
            with allure.step(f"事实问答: {case['name']}"):
                response = self.mock_llm.generate(case['query'])
                expected_keywords = set(case.get('expected_keywords', []))

                eval_result = self.evaluator.evaluate(
                    expected=" ".join(expected_keywords),
                    actual=response
                )

                if eval_result['pass']:
                    pass_count += 1

        allure.attach(
            f"通过: {pass_count}/{len(factual_cases)}",
            name="事实问答统计",
            attachment_type=allure.attachment_type.TEXT
        )

        # 至少50%的事实问答应该通过
        assert pass_count / len(factual_cases) >= 0.5, (
            f"事实问答准确率过低: {pass_count}/{len(factual_cases)}"
        )

    @pytest.mark.accuracy
    def test_numerical_accuracy(self):
        """测试数值型问题的准确性"""
        numerical_cases = [
            case for case in self.test_cases
            if 'expected_numbers' in case
        ]

        for case in numerical_cases:
            with allure.step(f"数值测试: {case['name']}"):
                response = self.mock_llm.generate(case['query'])

                # 检查是否包含预期的数字
                expected_numbers = set(case['expected_numbers'])
                keyword_result = self.evaluator.check_keywords_match(
                    expected=" ".join(expected_numbers),
                    actual=response
                )

                allure.attach(
                    f"预期数字: {expected_numbers}, 实际包含: {keyword_result['actual_numbers']}",
                    name="数字匹配结果",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert keyword_result['number_match'], (
                    f"数字匹配失败 [{case['id']}]: "
                    f"预期 {expected_numbers}, 回答: {response}"
                )
