import unittest

from codemode_eval.token_budget import (
    codemode_tokens,
    estimate_tokens,
    reduction_ratio,
    schema_dump_tokens,
)


def _tools(n: int) -> list[dict]:
    return [
        {"name": f"endpoint_{i}", "schema": {"type": "object", "properties": {"a": {"type": "string"}, "b": {"type": "integer"}}}}
        for i in range(n)
    ]


class TestEstimateTokens(unittest.TestCase):
    def test_empty_is_one(self):
        self.assertEqual(estimate_tokens(""), 1)

    def test_deterministic(self):
        self.assertEqual(estimate_tokens("hello"), estimate_tokens("hello"))


class TestTokenBudget(unittest.TestCase):
    def test_dump_grows_with_tool_count(self):
        self.assertGreater(schema_dump_tokens(_tools(50)), schema_dump_tokens(_tools(5)))

    def test_codemode_is_constant(self):
        self.assertEqual(codemode_tokens(), codemode_tokens())

    def test_reduction_grows_with_tool_count(self):
        small = reduction_ratio(schema_dump_tokens(_tools(5)))
        large = reduction_ratio(schema_dump_tokens(_tools(500)))
        self.assertGreater(large, small)

    def test_reduction_high_for_large_catalog(self):
        # ~2500 endpoints -> schema dump should dwarf the fixed codemode baseline
        self.assertGreater(reduction_ratio(schema_dump_tokens(_tools(2500))), 0.9)


if __name__ == "__main__":
    unittest.main()
