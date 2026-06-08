import unittest

from functions.run_python_file import run_python_file


class TestRunScript(unittest.TestCase):
    def test_run_python(self):
        project_working_directory = "calculator"
        test_cases = [
            ["main.py"],
            ["main.py", ["3 + 5"]],
            ["tests.py"],
            ["../main.py"],
            ["nonexistent.py"],
            ["lorem.txt"],
        ]
        for test_case in test_cases:
            if len(test_case) == 1:
                file = test_case[0]
                run_info = run_python_file(project_working_directory, file)
            elif len(test_case) == 2:
                file, args = test_case
                run_info = run_python_file(project_working_directory, file, args)
            else:
                print(f"test case {test_case} is not valid. ")
                continue

            print(f"Result for '{file}':\n\t{run_info}")



if __name__ == '__main__':
    unittest.main()
