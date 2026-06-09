import unittest

from response_parser import parse_braces_dict


class MyTestCase(unittest.TestCase):
    def test_something(self):
        text = '{"name": "blah_blah_blah", "args": "[\'first\': \'value\']"}'
        result = parse_braces_dict(text)
        self.assertEqual('blah_blah_blah', result["name"])  # add assertion here
    def test_something_else(self):
        text = '{"file_path": "pkg/calculator.py", "content": "# calculator/pkg/calculator.py\n\nfrom collections.abc import Callable\n\n\nclass Calculator:\n    def __init__(self) -> None:\n        self.operators: dict[str, Callable[[float, float], float]] = {\n            \"+\": lambda a, b: a + b,\n            \"-\": lambda a, b: a - b,\n            \"*\": lambda a, b: a * b,\n            \"/\": lambda a, b: a / b,\n        }\n        self.precedence: dict[str, int] = {\n            \"+\": 1,\n            \"-\": 1,\n            \"*\": 2,\n            \"/\": 2,\n        }\n\n    def evaluate(self, expression: str) -> float | None:\n        if not expression or expression.isspace():\n            return None\n        tokens = expression.strip().split()\n        return self._evaluate_infix(tokens)\n\n    def _evaluate_infix(self, tokens: list[str]) -> float:\n        values: list[float] = []\n        operators: list[str] = []\n\n        for token in tokens:\n            if token in self.operators:\n                while (\n                    operators\n                    and operators[-1] in self.operators\n                    and self.precedence[operators[-1]] >= self.precedence[token]\n                ):\n                    self._apply_operator(operators, values)\n                operators.append(token)\n            else:\n                try:\n                    values.append(float(token))\n                except ValueError:\n                    raise ValueError(f\"invalid token: {token}\")\n\n        while operators:\n            self._apply_operator(operators, values)\n\n        if len(values) != 1:\n            raise ValueError(\"invalid expression\")\n\n        return values[0]\n\n    def _apply_operator(self, operators: list[str], values: list[float]) -> None:\n        if not operators:\n            return\n\n        operator = operators.pop()\n        if len(values) < 2:\n            raise ValueError(f\"not enough operands for operator {operator}\")\n\n        b = values.pop()\n        a = values.pop()\n        values.append(self.operators[operator](a, b))\n"}'
        result = parse_braces_dict(text, debug=True)
        if result:
            print(len(result['content']))

if __name__ == '__main__':
    unittest.main()
