import unittest
from functions.write_file import write_file

class TestWriteFile(unittest.TestCase):
    def test_write_file(self):
        project_working_directory = "calculator"
        test_cases = {
            "lorem.txt": "wait, this isn't lorem ipsum",
            "pkg/morelorem.txt": "lorem ipsum dolor sit amet",
            "/tmp/temp.txt": "this should not be allowed",
        }
        print("running test")
        for path in test_cases:
            write_result = write_file(project_working_directory, path, test_cases[path])
            print(f"Result for '{path}':\n\t{write_result}")


if __name__ == '__main__':
    unittest.main()
