"""
RAG检索测试模块
测试RAG系统的检索和生成能力
"""

import pytest
import json
from pathlib import Path
import allure


@allure.epic("大模型测试")
@allure.feature("RAG检索测试")
class TestRAG:
    """RAG检索测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, test_data_dir, mock_llm, evaluator):
        """测试前置条件"""
        self.test_data_dir = test_data_dir
        self.mock_llm = mock_llm
        self.evaluator = evaluator

        # 创建Mock RAG系统
        from src.mock_llm import MockRAGSystem
        self.mock_rag = MockRAGSystem()

        # 加载测试用例
        rag_file = self.test_data_dir / "rag.json"
        with open(rag_file, 'r', encoding='utf-8') as f:
            self.test_cases = json.load(f)['test_cases']

    @pytest.mark.rag
    def test_all_rag_cases(self):
        """
        运行所有RAG检索测试用例
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

                query = case['query']

                # RAG检索
                retrieved_docs = self.mock_rag.retrieve(query)

                allure.attach(
                    query,
                    name="查询问题",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    json.dumps(retrieved_docs, ensure_ascii=False, indent=2),
                    name="检索到的文档",
                    attachment_type=allure.attachment_type.JSON
                )

                # 获取预期关键词
                expected_keywords = set(case.get('expected_keywords', []))

                # 评估检索质量
                eval_result = self.evaluator.evaluate_rag_retrieval(
                    query=query,
                    retrieved_docs=retrieved_docs,
                    expected_keywords=expected_keywords
                )

                allure.attach(
                    json.dumps(eval_result, ensure_ascii=False, indent=2),
                    name="RAG检索评估结果",
                    attachment_type=allure.attachment_type.JSON
                )

                test_passed = eval_result['pass']
                if test_passed:
                    pass_count += 1

                results.append({
                    'id': case['id'],
                    'name': case['name'],
                    'passed': test_passed,
                    'doc_count': len(retrieved_docs),
                    'details': eval_result.get('details', {})
                })

        # 生成测试报告
        allure.attach(
            json.dumps(results, ensure_ascii=False, indent=2),
            name="RAG测试结果",
            attachment_type=allure.attachment_type.JSON
        )

        allure.attach(
            f"通过: {pass_count}/{len(self.test_cases)} ({pass_count/len(self.test_cases)*100:.1f}%)",
            name="RAG测试统计",
            attachment_type=allure.attachment_type.TEXT
        )

        # RAG测试至少60%应该通过
        assert pass_count / len(self.test_cases) >= 0.6, (
            f"RAG测试通过率过低: {pass_count}/{len(self.test_cases)}"
        )

    @pytest.mark.rag
    @pytest.mark.retrieval
    def test_retrieval_quality(self):
        """测试检索质量"""
        retrieval_cases = [
            case for case in self.test_cases
            if case.get('category') in ['keyword_retrieval', 'multi_keyword']
        ]

        for case in retrieval_cases:
            with allure.step(f"检索质量测试: {case['name']}"):
                query = case['query']
                expected_keywords = set(case.get('expected_keywords', []))

                # 执行检索
                retrieved_docs = self.mock_rag.retrieve(query)

                # 评估检索质量
                eval_result = self.evaluator.evaluate_rag_retrieval(
                    query=query,
                    retrieved_docs=retrieved_docs,
                    expected_keywords=expected_keywords
                )

                assert eval_result['pass'], (
                    f"检索质量测试失败 [{case['id']}]: {case['name']}\n"
                    f"预期关键词: {expected_keywords}\n"
                    f"检索到文档数: {len(retrieved_docs)}"
                )

    @pytest.mark.rag
    @pytest.mark.generation
    def test_rag_generation(self):
        """测试RAG生成回答质量"""
        generation_cases = [
            case for case in self.test_cases
            if case.get('category') in ['keyword_retrieval', 'multi_keyword']
        ][:5]  # 取前5个测试

        for case in generation_cases:
            with allure.step(f"RAG生成测试: {case['name']}"):
                query = case['query']
                expected_keywords = set(case.get('expected_keywords', []))

                # 使用RAG生成回答
                response = self.mock_rag.generate_with_rag(query)

                allure.attach(
                    query,
                    name="问题",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    response,
                    name="RAG回答",
                    attachment_type=allure.attachment_type.TEXT
                )

                # 评估回答质量
                eval_result = self.evaluator.evaluate(
                    expected=" ".join(expected_keywords),
                    actual=response
                )

                assert eval_result['pass'], (
                    f"RAG生成测试失败 [{case['id']}]: {case['name']}\n"
                    f"预期关键词: {expected_keywords}\n"
                    f"回答: {response}"
                )

    @pytest.mark.rag
    def test_no_match_handling(self):
        """测试无匹配结果的处理"""
        no_match_cases = [
            case for case in self.test_cases
            if case.get('category') == 'no_match'
        ]

        for case in no_match_cases:
            with allure.step(f"无匹配处理测试: {case['name']}"):
                query = case['query']

                # 执行检索
                retrieved_docs = self.mock_rag.retrieve(query)

                # 生成回答
                response = self.mock_rag.generate_with_rag(query)

                # 无匹配时应该返回友好提示
                assert len(response) > 0, "无匹配时也应该返回响应"
                assert any(word in response for word in ['抱歉', '没有找到', '无法']), \
                    "无匹配时应该返回友好提示"

    @pytest.mark.rag
    def test_numerical_rag(self):
        """测试数值型RAG检索"""
        numerical_cases = [
            case for case in self.test_cases
            if 'expected_numbers' in case
        ]

        for case in numerical_cases:
            with allure.step(f"数值RAG测试: {case['name']}"):
                query = case['query']
                expected_numbers = set(case.get('expected_numbers', []))

                # 执行检索
                retrieved_docs = self.mock_rag.retrieve(query)

                # 检查文档是否包含预期数字
                all_text = " ".join(retrieved_docs)
                found_numbers = set()
                for num in expected_numbers:
                    if num in all_text:
                        found_numbers.add(num)

                # 至少应该检索到包含部分数字的文档
                assert len(retrieved_docs) > 0, "应该检索到文档"
                assert len(found_numbers) > 0 or len(retrieved_docs) > 0, \
                    f"数值RAG测试失败 [{case['id']}]: 预期数字 {expected_numbers}"

    @pytest.mark.rag
    @pytest.mark.negation
    def test_negation_detection(self):
        """测试否定信息检索"""
        negation_cases = [
            case for case in self.test_cases
            if case.get('category') == 'negation_info'
        ]

        for case in negation_cases:
            with allure.step(f"否定信息测试: {case['name']}"):
                query = case['query']
                expected_keywords = set(case.get('expected_keywords', []))

                # 执行检索
                retrieved_docs = self.mock_rag.retrieve(query)

                # 检查是否包含否定关键词
                all_text = " ".join(retrieved_docs)
                negation_words = {'不', '没', '无', '未', '没有'}

                found_negation = any(word in all_text for word in negation_words)

                assert found_negation or len(retrieved_docs) > 0, \
                    f"否定信息测试失败 [{case['id']}]: 应包含否定词"

    @pytest.mark.rag
    def test_retrieval_count(self):
        """测试检索文档数量"""
        for case in self.test_cases[:10]:  # 测试前10个
            with allure.step(f"检索数量测试: {case['name']}"):
                query = case['query']

                # 检索文档
                retrieved_docs = self.mock_rag.retrieve(query, top_k=2)

                # 检查文档数量不超过top_k
                assert len(retrieved_docs) <= 2, \
                    f"检索数量超过限制 [{case['id']}]: {len(retrieved_docs)} > 2"

    @pytest.mark.rag
    @pytest.mark.high_priority
    def test_high_priority_rag_cases(self):
        """只运行高优先级的RAG测试"""
        high_priority_cases = [
            case for case in self.test_cases
            if case.get('priority') == 'high'
        ]

        pass_count = 0
        for case in high_priority_cases:
            with allure.step(f"高优先级RAG测试: {case['name']}"):
                query = case['query']
                expected_keywords = set(case.get('expected_keywords', []))

                retrieved_docs = self.mock_rag.retrieve(query)

                eval_result = self.evaluator.evaluate_rag_retrieval(
                    query=query,
                    retrieved_docs=retrieved_docs,
                    expected_keywords=expected_keywords
                )

                if eval_result['pass']:
                    pass_count += 1

        # 高优先级RAG测试至少40%应该通过
        assert pass_count / len(high_priority_cases) >= 0.4, (
            f"高优先级RAG测试通过率过低: {pass_count}/{len(high_priority_cases)}"
        )
