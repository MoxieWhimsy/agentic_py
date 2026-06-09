import unittest

from response_parser import parse_braces_dict


class MyTestCase(unittest.TestCase):
    def test_something(self):
        text = '{"name": "blah_blah_blah", "args": "[\'first\': \'value\']"}'
        result = parse_braces_dict(text)
        self.assertEqual('blah_blah_blah', result["name"])  # add assertion here


if __name__ == '__main__':
    unittest.main()
