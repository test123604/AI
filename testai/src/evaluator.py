"""
答案评估器模块
使用关键词匹配 + 语义相似度相结合的方法评估大模型回答质量
"""

import re
import jieba
from typing import List, Dict, Tuple, Set
import numpy as np


class AnswerEvaluator:
    """大模型答案评估器"""

    def __init__(self, similarity_threshold: float = 0.7, model_name: str = None, offline_mode: bool = True):
        """
        初始化评估器

        Args:
            similarity_threshold: 语义相似度阈值，默认 0.7
            model_name: SentenceTransformer 模型名称（暂不使用，避免网络下载）
            offline_mode: 离线模式，只使用关键词匹配
        """
        self.similarity_threshold = similarity_threshold
        self.offline_mode = offline_mode
        self.model = None

        # 如果不是离线模式，尝试加载模型
        if not offline_mode and model_name:
            try:
                from sentence_transformers import SentenceTransformer
                from sklearn.metrics.pairwise import cosine_similarity
                self.SentenceTransformer = SentenceTransformer
                self.cosine_similarity = cosine_similarity
                self.model = SentenceTransformer(model_name)
            except Exception as e:
                print(f"[警告] 无法加载 SentenceTransformer 模型: {e}")
                print("[提示] 将使用纯关键词匹配模式")
                self.offline_mode = True

    def extract_keywords(self, text: str) -> Set[str]:
        """
        从文本中提取关键词

        Args:
            text: 输入文本

        Returns:
            关键词集合
        """
        # 使用 jieba 分词
        words = jieba.cut(text)

        # 过滤停用词和单字词
        stop_words = {
            '的', '是', '了', '在', '和', '有', '我', '你', '他', '她', '它',
            '什么', '怎么', '如何', '吗', '吧', '呢', '啊', '哦', '呀',
            '这个', '那个', '一个', '一些', '可以', '能够', '应该',
            '?', '？', '!', '！', '.', '。', ',', '，', ':', '：', ';', '；'
        }

        keywords = set()
        for word in words:
            word = word.strip()
            # 保留长度>=2的词，且不在停用词中
            if len(word) >= 2 and word not in stop_words:
                keywords.add(word)

        return keywords

    def extract_numbers(self, text: str) -> Set[str]:
        """
        从文本中提取数字（包括年份数字、数量等）

        Args:
            text: 输入文本

        Returns:
            数字字符串集合
        """
        # 匹配数字（包括整数、小数、年份数字）
        pattern = r'\b\d+(\.\d+)?\b'
        numbers = set(re.findall(pattern, text))
        return numbers

    def extract_negation_words(self, text: str) -> Set[str]:
        """
        提取否定词

        Args:
            text: 输入文本

        Returns:
            否定词集合
        """
        negation_words = {'不', '没', '无', '非', '未', '否', '不是', '没有', '无法', '不能'}
        found = set()
        for word in negation_words:
            if word in text:
                found.add(word)
        return found

    def check_keywords_match(self, expected: str, actual: str) -> Dict[str, any]:
        """
        检查关键词匹配情况

        Args:
            expected: 预期答案
            actual: 实际答案

        Returns:
            包含匹配结果的字典
        """
        # 提取关键词
        expected_keywords = self.extract_keywords(expected)
        actual_keywords = self.extract_keywords(actual)

        # 提取数字
        expected_numbers = self.extract_numbers(expected)
        actual_numbers = self.extract_numbers(actual)

        # 提取否定词
        expected_negations = self.extract_negation_words(expected)
        actual_negations = self.extract_negation_words(actual)

        # 计算关键词命中率
        if len(expected_keywords) > 0:
            hit_count = len(expected_keywords & actual_keywords)
            keyword_hit_rate = hit_count / len(expected_keywords)
        else:
            keyword_hit_rate = 1.0  # 没有关键词要求，默认满分

        # 检查数字是否匹配
        number_match = expected_numbers == actual_numbers or expected_numbers.issubset(actual_numbers)

        # 检查否定词是否匹配
        negation_match = True
        if expected_negations:
            negation_match = bool(expected_negations & actual_negations)

        return {
            "expected_keywords": expected_keywords,
            "actual_keywords": actual_keywords,
            "keyword_hit_rate": keyword_hit_rate,
            "keyword_match": keyword_hit_rate >= 0.6,  # 关键词命中率阈值 0.6
            "number_match": number_match,
            "negation_match": negation_match,
            "expected_numbers": expected_numbers,
            "actual_numbers": actual_numbers
        }

    def calculate_semantic_similarity(self, expected: str, actual: str) -> float:
        """
        计算语义相似度（余弦相似度）

        Args:
            expected: 预期答案
            actual: 实际答案

        Returns:
            相似度分数 (0-1)
        """
        # 离线模式：基于关键词重叠计算相似度
        if self.offline_mode or self.model is None:
            expected_keywords = self.extract_keywords(expected)
            actual_keywords = self.extract_keywords(actual)

            if not expected_keywords:
                return 1.0

            # 计算关键词重叠率
            intersection = expected_keywords & actual_keywords
            union = expected_keywords | actual_keywords

            if not union:
                return 0.0

            # Jaccard 相似度
            jaccard = len(intersection) / len(union)

            # 加权：考虑关键词命中率
            hit_rate = len(intersection) / len(expected_keywords)

            # 综合相似度
            similarity = jaccard * 0.6 + hit_rate * 0.4

            return float(similarity)

        # 在线模式：使用 SentenceTransformer
        expected_embedding = self.model.encode([expected])
        actual_embedding = self.model.encode([actual])

        # 计算余弦相似度
        similarity = self.cosine_similarity(expected_embedding, actual_embedding)[0][0]

        return float(similarity)

    def evaluate(self, expected: str, actual: str) -> Dict[str, any]:
        """
        综合评估答案

        Args:
            expected: 预期答案
            actual: 实际答案

        Returns:
            评估结果字典，包含是否通过、相似度分数、关键词匹配情况等
        """
        # 关键词匹配检查
        keyword_result = self.check_keywords_match(expected, actual)

        # 语义相似度计算
        semantic_similarity = self.calculate_semantic_similarity(expected, actual)

        # 综合判断：
        # 1. 关键词匹配 OR
        # 2. 语义相似度达标
        keyword_pass = keyword_result["keyword_match"]
        semantic_pass = semantic_similarity >= self.similarity_threshold

        # 最终通过条件：关键词命中 且（数字匹配 且 否定词匹配） 或 语义相似度达标
        number_match = keyword_result["number_match"]
        negation_match = keyword_result["negation_match"]

        # 简化评估逻辑：
        # 1. 关键词命中率 >= 60% 直接通过
        # 2. 或：关键词命中率 >= 40% 且（语义相似度 >= 0.5 或（有数字且数字匹配 且有否定词且否定词匹配））
        keyword_hit_rate = keyword_result["keyword_hit_rate"]

        # 条件1：关键词命中率足够高
        if keyword_hit_rate >= 0.6:
            final_pass = True
        else:
            # 条件2：需要额外验证
            has_number_requirement = len(keyword_result["expected_numbers"]) > 0
            has_negation_requirement = any(neg in keyword_result["expected_keywords"]
                                          for neg in {'不', '没', '无', '非', '未', '不是', '没有'})

            # 基本要求：关键词命中率 >= 30%
            basic_keyword_hit = keyword_hit_rate >= 0.3

            if has_number_requirement and has_negation_requirement:
                final_pass = basic_keyword_hit and (semantic_pass or (number_match and negation_match))
            elif has_number_requirement:
                final_pass = basic_keyword_hit and (semantic_pass or number_match)
            elif has_negation_requirement:
                final_pass = basic_keyword_hit and (semantic_pass or negation_match)
            else:
                # 没有特殊要求：关键词命中率 >= 30% 或 语义相似度 >= 0.4
                final_pass = basic_keyword_hit or semantic_similarity >= 0.4

        return {
            "pass": final_pass,
            "semantic_similarity": semantic_similarity,
            "semantic_pass": semantic_pass,
            "keyword_hit_rate": keyword_result["keyword_hit_rate"],
            "keyword_pass": keyword_pass,
            "number_pass": keyword_result["number_match"],
            "negation_pass": negation_match,
            "expected_keywords": list(keyword_result["expected_keywords"]),
            "actual_keywords": list(keyword_result["actual_keywords"]),
            "expected_numbers": list(keyword_result["expected_numbers"]),
            "actual_numbers": list(keyword_result["actual_numbers"]),
            "threshold": self.similarity_threshold
        }

    def evaluate_format(self, response: str, format_requirements: Dict[str, any]) -> Dict[str, any]:
        """
        评估回答格式是否符合要求

        Args:
            response: 模型回答
            format_requirements: 格式要求，如：
                {
                    "max_length": 500,
                    "min_length": 10,
                    "contains": ["关键词1", "关键词2"],
                    "not_contains": ["禁止词"],
                    "pattern": r"\\d+年"  # 正则表达式
                }

        Returns:
            格式检查结果
        """
        result = {
            "pass": True,
            "details": {}
        }

        # 检查长度
        if "max_length" in format_requirements:
            max_ok = len(response) <= format_requirements["max_length"]
            result["details"]["max_length"] = {
                "pass": max_ok,
                "actual": len(response),
                "expected": f"<={format_requirements['max_length']}"
            }
            result["pass"] = result["pass"] and max_ok

        if "min_length" in format_requirements:
            min_ok = len(response) >= format_requirements["min_length"]
            result["details"]["min_length"] = {
                "pass": min_ok,
                "actual": len(response),
                "expected": f">={format_requirements['min_length']}"
            }
            result["pass"] = result["pass"] and min_ok

        # 检查必须包含的内容
        if "contains" in format_requirements:
            contains_all = all(keyword in response for keyword in format_requirements["contains"])
            result["details"]["contains"] = {
                "pass": contains_all,
                "keywords": format_requirements["contains"]
            }
            result["pass"] = result["pass"] and contains_all

        # 检查不能包含的内容
        if "not_contains" in format_requirements:
            contains_none = not any(keyword in response for keyword in format_requirements["not_contains"])
            result["details"]["not_contains"] = {
                "pass": contains_none,
                "keywords": format_requirements["not_contains"]
            }
            result["pass"] = result["pass"] and contains_none

        # 检查正则表达式模式
        if "pattern" in format_requirements:
            pattern_match = bool(re.search(format_requirements["pattern"], response))
            result["details"]["pattern"] = {
                "pass": pattern_match,
                "pattern": format_requirements["pattern"]
            }
            result["pass"] = result["pass"] and pattern_match

        return result

    def evaluate_rag_retrieval(self, query: str, retrieved_docs: List[str], expected_keywords: Set[str]) -> Dict[str, any]:
        """
        评估 RAG 检索质量

        Args:
            query: 查询问题
            retrieved_docs: 检索到的文档列表
            expected_keywords: 预期应该检索到的关键词

        Returns:
            检索质量评估结果
        """
        result = {
            "pass": True,
            "details": {}
        }

        # 检查是否检索到文档
        has_docs = len(retrieved_docs) > 0
        result["details"]["has_documents"] = {
            "pass": has_docs,
            "count": len(retrieved_docs)
        }
        result["pass"] = result["pass"] and has_docs

        # 检查文档是否包含预期关键词
        if expected_keywords and has_docs:
            all_retrieved_text = " ".join(retrieved_docs)
            found_keywords = set()
            for keyword in expected_keywords:
                if keyword in all_retrieved_text:
                    found_keywords.add(keyword)

            keyword_coverage = len(found_keywords) / len(expected_keywords) if expected_keywords else 1.0
            result["details"]["keyword_coverage"] = {
                "pass": keyword_coverage >= 0.4,
                "coverage": keyword_coverage,
                "found": list(found_keywords),
                "expected": list(expected_keywords)
            }
            result["pass"] = result["pass"] and (keyword_coverage >= 0.4)

        return result
