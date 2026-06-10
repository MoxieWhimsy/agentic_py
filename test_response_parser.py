import unittest

from response_parser import get_within_curly_braces


class MyTestCase(unittest.TestCase):
    def test_something(self):
        text = '{"name": "blah_blah_blah", "args": "[\'first\': \'value\']"}'
        result = get_within_curly_braces(text)
        self.assertEqual(text, result)
    def test_something_else(self):
        text = 'abcdefgh{ijk{lmno}pq}rstuvwxyz'
        result = get_within_curly_braces(text)
        self.assertEqual('{ijk{lmno}pq}', result)
    def test_open(self):
        text = '{{}{'
        try:
            get_within_curly_braces(text)
        except Exception as e:
            print("The following exception should have something to do with the braces being open or the level not being zero.")
            print(e)


if __name__ == '__main__':
    unittest.main()
