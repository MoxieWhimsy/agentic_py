import unittest
from functions.get_file_content import get_file_content


class MyTestCase(unittest.TestCase):
    def test_get_lorem_content(self):
        result = get_file_content("calculator", "lorem.txt")
        print(f"Result for 'lorem.txt': Success == {result.startswith('SUCCESS')}")
        print(f"lorem.txt length: {len(result)}")
        print(f"lorem.txt truncated: {'truncated' in result}")

    def test_get_multiple_file_contents_in_calculator_working_dir(self):
        for file_path in [
            "main.py",
            "pkg/calculator.py",
            "/bin/cat",
            "pkg/does_not_exist.py"
        ]:
            content = get_file_content("calculator", file_path)

            print(f"Result for '{file_path}':\n\t{content}")
            if content.startswith("Error:"):
                continue
            print(f"\t{file_path} length: {len(content)}")
            print(f"\t{file_path} truncated: {'truncated' in content}")


if __name__ == '__main__':
    unittest.main()
