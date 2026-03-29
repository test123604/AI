"""
真实大模型测试模块
测试实际的 LLM API 调用
"""

import pytest
import json
from pathlib import Path
import allure
import time


# 结果保存路径
RESULT_FILE = Path(__file__).parent.parent / "result.txt"


@allure.epic("大模型测试")
@allure.feature("真实API测试")
class TestRealLLM:
    """真实大模型测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, test_data_dir, evaluator):
        """测试前置条件"""
        self.test_data_dir = test_data_dir
        self.evaluator = evaluator

        # 延迟导入，避免没有配置 API Key 时初始化失败
        from src.real_llm import get_real_llm
        self.real_llm = get_real_llm(provider="dashscope")  # 可改为 "deepseek"

        # 加载测试用例
        accuracy_file = self.test_data_dir / "accuracy.json"
        with open(accuracy_file, 'r', encoding='utf-8') as f:
            self.test_cases = json.load(f)['test_cases']

    @pytest.mark.accuracy
    @pytest.mark.real_api
    def test_real_llm_accuracy_sample(self):
        """
        测试真实大模型的准确性（抽样测试）
        只运行前10个用例，避免消耗过多 API 额度
        """
        # 清空并初始化结果文件
        with open(RESULT_FILE, 'w', encoding='utf-8') as f:
            f.write(f"{'='*60}\n")
            f.write("真实大模型测试结果\n")
            f.write(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"提供商: dashscope (通义千问)\n")
            f.write(f"{'='*60}\n\n")

        sample_cases = self.test_cases[:10]

        pass_count = 0
        results = []

        for case in sample_cases:
            with allure.step(f"测试: {case['name']}"):
                allure.attach(
                    json.dumps(case, ensure_ascii=False, indent=2),
                    name="测试用例",
                    attachment_type=allure.attachment_type.JSON
                )

                try:
                    start_time = time.time()
                    response = self.real_llm.generate(case['query'])
                    elapsed_time = time.time() - start_time

                    # 写入结果文件
                    with open(RESULT_FILE, 'a', encoding='utf-8') as f:
                        f.write(f"\n{'='*60}\n")
                        f.write(f"测试用例: {case['id']} - {case['name']}\n")
                        f.write(f"{'='*60}\n")
                        f.write(f"问题: {case['query']}\n")
                        f.write(f"回答: {response}\n")
                        f.write(f"耗时: {elapsed_time:.2f}秒\n")
                        f.write(f"API 调用次数: {self.real_llm.get_call_count()}\n")

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

                    # 评估回答
                    expected_keywords = set(case.get('expected_keywords', []))
                    eval_result = self.evaluator.evaluate(
                        expected=" ".join(expected_keywords),
                        actual=response
                    )

                    allure.attach(
                        f"耗时: {elapsed_time:.2f}秒\n调用次数: {self.real_llm.get_call_count()}",
                        name="API 调用信息",
                        attachment_type=allure.attachment_type.TEXT
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

        # 生成报告
        allure.attach(
            json.dumps(results, ensure_ascii=False, indent=2),
            name="测试结果详情",
            attachment_type=allure.attachment_type.JSON
        )

        allure.attach(
            f"通过: {pass_count}/{len(sample_cases)}\n"
            f"总 API 调用次数: {self.real_llm.get_call_count()}",
            name="测试统计",
            attachment_type=allure.attachment_type.TEXT
        )

        # 写入摘要到结果文件
        with open(RESULT_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write("测试摘要\n")
            f.write(f"{'='*60}\n")
            f.write(f"通过: {pass_count}/{len(sample_cases)} ({pass_count/len(sample_cases)*100:.1f}%)\n")
            f.write(f"总 API 调用次数: {self.real_llm.get_call_count()}\n")
            f.write(f"测试结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n")

        # 真实 API 测试通过率要求较低（60%）
        assert pass_count / len(sample_cases) >= 0.6, (
            f"真实 API 测试通过率过低: {pass_count}/{len(sample_cases)}"
        )

    @pytest.mark.accuracy
    @pytest.mark.real_api
    @pytest.mark.single
    def test_real_llm_single_question(self):
        """
        单个问题测试
        用于快速验证 API 配置是否正确
        """
        test_case = {
            "id": "REAL_001",
            "name": "测试 API 连接",
            "query": "天空是什么颜色的？",
            "expected_keywords": ["蓝色", "蓝天"]
        }

        with allure.step("测试真实 API 连接"):
            try:
                response = self.real_llm.generate(test_case['query'])

                # 写入结果文件
                with open(RESULT_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"测试用例: {test_case['id']} - {test_case['name']}\n")
                    f.write(f"{'='*60}\n")
                    f.write(f"问题: {test_case['query']}\n")
                    f.write(f"回答: {response}\n")
                    f.write(f"API 调用次数: {self.real_llm.get_call_count()}\n")

                allure.attach(
                    f"问题: {test_case['query']}\n"
                    f"回答: {response}\n"
                    f"API 调用次数: {self.real_llm.get_call_count()}",
                    name="测试结果",
                    attachment_type=allure.attachment_type.TEXT
                )

                # 基本检查：回答不为空
                assert len(response) > 0, "API 返回空响应"

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
                pytest.fail(f"真实 API 调用失败: {e}")

    @pytest.mark.robustness
    @pytest.mark.real_api
    def test_real_llm_robustness(self):
        """测试真实大模型的鲁棒性（抽样测试）"""
        robustness_file = self.test_data_dir / "robustness.json"
        with open(robustness_file, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)['test_cases']

        # 只测试特殊字符和边界情况
        sample_cases = [
            case for case in test_cases[:5]
            if case.get('category') in ['empty_input', 'special_chars', 'emoji']
        ]

        pass_count = 0
        for case in sample_cases:
            with allure.step(f"鲁棒性测试: {case['name']}"):
                try:
                    response = self.real_llm.generate(case['query'])
                    # 基本检查：有响应即可
                    if len(response) > 0:
                        pass_count += 1
                except Exception as e:
                    allure.attach(
                        str(e),
                        name="错误",
                        attachment_type=allure.attachment_type.TEXT
                    )

        allure.attach(
            f"鲁棒性测试通过: {pass_count}/{len(sample_cases)}",
            name="鲁棒性测试结果",
            attachment_type=allure.attachment_type.TEXT
        )

        # 鲁棒性测试至少 60% 通过
        assert pass_count / len(sample_cases) >= 0.6 if sample_cases else True
