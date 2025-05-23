import sys, os
import pytest
from unittest.mock import MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.pinecone_checker import get_existing_vector_info

# 假設 Pinecone 的 Index 是一個物件，我們用 mock 模擬它
class MockPineconeIndex:
    def describe_index_stats(self):
        return {
            "namespaces": {
                "test-namespace": {
                    "vector_count": 2
                }
            }
        }

    def fetch(self, ids, namespace):
        return MagicMock(
            vectors={
                "faq_1": MagicMock(metadata={"question": "什麼時候打掃？"}),
                "faq_2": MagicMock(metadata={"question": "如何處理客訴？"}),
            }
        )


def test_get_existing_vector_info_returns_correct_sets():
    index = MockPineconeIndex()
    namespace = "test-namespace"

    ids, questions = get_existing_vector_info(index, namespace)

    assert isinstance(ids, set)
    assert isinstance(questions, set)
    assert "faq_1" in ids
    assert "faq_2" in ids
    assert "什麼時候打掃？" in questions
    assert "如何處理客訴？" in questions


def test_get_existing_vector_info_returns_empty_when_zero_vectors():
    class EmptyMockIndex:
        def describe_index_stats(self):
            return {"namespaces": {"test-namespace": {"vector_count": 0}}}
        def fetch(self, ids, namespace):
            return MagicMock(vectors={})

    index = EmptyMockIndex()
    namespace = "test-namespace"

    ids, questions = get_existing_vector_info(index, namespace)

    assert ids == set()
    assert questions == set()
