"""
格式规范测试模块
测试模型回答格式是否符合要求
"""

import pytest
import json
from pathlib import Path
import allure


@allure.epic("大模型测试")
@allure.feature("格式规范测试")
class TestFormat:
    """格式规范测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, test_data_dir, mock_llm, evaluator):
        """测试前置条件"""
        self.test_data_dir = test_data_dir
        self.mock_llm = mock_llm
        self.evaluator = evaluator

        # 加载测试用例
        format_file = self.test_data_dir / "format.json"
        with open(format_file, 'r', encoding='utf-8') as f:
            self.test_cases = json.load(f)['test_cases']

    @pytest.mark.format
    def test_all_format_cases(self):
        """
        运行所有格式规范测试用例
        """
        pass_count = 0
        results = []

        for case in self.test_cases:
            with allure.step(f"执行测试用例: {case['name']}"):
                allure.attach(
                    json.dumps(case, ensure_ascii=False, indent=2),
                    name="测试用例详情",
                    attachment_type=allure.attachment_type.JSON
                )

                # 获取问题和格式要求
                query = case['query']
                format_req = case.get('format_requirements', {})

                # 生成回答
                response = self.mock_llm.generate(query)

                allure.attach(
                    query,
                    name="问题",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    response,
                    name="模型回答",
                    attachment_type=allure.attachment_type.TEXT
                )

                # 评估格式
                eval_result = self.evaluator.evaluate_format(response, format_req)

                allure.attach(
                    json.dumps(eval_result, ensure_ascii=False, indent=2),
                    name="格式评估结果",
                    attachment_type=allure.attachment_type.JSON
                )

                test_passed = eval_result['pass']
                if test_passed:
                    pass_count += 1

                results.append({
                    'id': case['id'],
                    'name': case['name'],
                    'passed': test_passed,
                    'details': eval_result.get('details', {})
                })

        # 生成测试报告
        allure.attach(
            json.dumps(results, ensure_ascii=False, indent=2),
            name="格式测试结果",
            attachment_type=allure.attachment_type.JSON
        )

        allure.attach(
            f"通过: {pass_count}/{len(self.test_cases)} ({pass_count/len(self.test_cases)*100:.1f}%)",
            name="格式测试统计",
            attachment_type=allure.attachment_type.TEXT
        )

        # 格式测试至少60%应该通过
        assert pass_count / len(self.test_cases) >= 0.6, (
            f"格式测试通过率过低: {pass_count}/{len(self.test_cases)}"
        )

    @pytest.mark.format
    @pytest.mark.length
    def test_length_constraints(self):
        """测试长度限制"""
        length_cases = [
            case for case in self.test_cases
            if case.get('category') == 'length_limit'
        ]

        for case in length_cases:
            with allure.step(f"长度测试: {case['name']}"):
                query = case['query']
                format_req = case.get('format_requirements', {})

                response = self.mock_llm.generate(query)
                eval_result = self.evaluator.evaluate_format(response, format_req)

                assert eval_result['pass'], (
                    f"长度限制测试失败 [{case['id']}]: {case['name']}\n"
                    f"要求: {format_req}\n"
                    f"实际长度: {len(response)}\n"
                    f"结果: {eval_result.get('details', {})}"
                )

    @pytest.mark.format
    @pytest.mark.content
    def test_content_requirements(self):
        """测试内容要求"""
        content_cases = [
            case for case in self.test_cases
            if case.get('category') in ['content_requirement', 'content_restriction']
        ]

        for case in content_cases:
            with allure.step(f"内容要求测试: {case['name']}"):
                query = case['query']
                format_req = case.get('format_requirements', {})

                response = self.mock_llm.generate(query)
                eval_result = self.evaluator.evaluate_format(response, format_req)

                assert eval_result['pass'], (
                    f"内容要求测试失败 [{case['id']}]: {case['name']}\n"
                    f"要求: {format_req}\n"
                    f"结果: {eval_result.get('details', {})}"
                )

    @pytest.mark.format
    @pytest.mark.pattern
    def test_pattern_matching(self):
        """测试正则表达式匹配"""
        pattern_cases = [
            case for case in self.test_cases
            if case.get('category') == 'pattern'
        ]

        for case in pattern_cases:
            with allure.step(f"正则匹配测试: {case['name']}"):
                query = case['query']
                format_req = case.get('format_requirements', {})

                response = self.mock_llm.generate(query)
                eval_result = self.evaluator.evaluate_format(response, format_req)

                assert eval_result['pass'], (
                    f"正则匹配测试失败 [{case['id']}]: {case['name']}\n"
                    f"模式: {format_req.get('pattern')}\n"
                    f"回答: {response}"
                )

    @pytest.mark.format
    @pytest.mark.response_quality
    def test_response_quality(self):
        """测试响应质量"""
        # 测试不能为空或全空格
        non_empty_cases = [
            case for case in self.test_cases
            if case.get('category') in ['non_empty', 'non_whitespace']
        ]

        for case in non_empty_cases:
            with allure.step(f"响应质量测试: {case['name']}"):
                response = self.mock_llm.generate(case['query'])

                format_req = case.get('format_requirements', {})
                eval_result = self.evaluator.evaluate_format(response, format_req)

                assert eval_result['pass'], (
                    f"响应质量测试失败 [{case['id']}]: {case['name']}\n"
                    f"回答: '{response}'"
                )

    @pytest.mark.format
    def test_structured_output(self):
        """测试结构化输出格式"""
        structured_cases = [
            case for case in self.test_cases
            if case.get('category') == 'structured_output'
        ]

        for case in structured_cases:
            with allure.step(f"结构化输出测试: {case['name']}"):
                query = case['query']
                format_req = case.get('format_requirements', {})

                response = self.mock_llm.generate(query)
                eval_result = self.evaluator.evaluate_format(response, format_req)

                assert eval_result['pass'], (
                    f"结构化输出测试失败 [{case['id']}]: {case['name']}\n"
                    f"要求: {format_req}\n"
                    f"回答: {response}"
                )

    @pytest.mark.format
    @pytest.mark.high_priority
    def test_high_priority_format_cases(self):
        """只运行高优先级的格式测试"""
        high_priority_cases = [
            case for case in self.test_cases
            if case.get('priority') == 'high'
        ]

        pass_count = 0
        for case in high_priority_cases:
            with allure.step(f"高优先级格式测试: {case['name']}"):
                query = case['query']
                format_req = case.get('format_requirements', {})

                response = self.mock_llm.generate(query)
                eval_result = self.evaluator.evaluate_format(response, format_req)

                if eval_result['pass']:
                    pass_count += 1

        # 高优先级测试至少75%应该通过
        assert pass_count / len(high_priority_cases) >= 0.75, (
            f"高优先级格式测试通过率过低: {pass_count}/{len(high_priority_cases)}"
        )
