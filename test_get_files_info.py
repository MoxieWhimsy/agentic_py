import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_get_files_info(self):
        info_result = get_files_info("calculator", ".")
        print(f'Result for current directory:\n\t{info_result}')
        info_result = get_files_info("calculator", "pkg")
        print(f"Result for 'pkg' directory:\n\t{info_result}")
        info_result = get_files_info("calculator", "/bin")
        print(f"Result for '/bin' directory:\n\t{info_result}")
        info_result = get_files_info("calculator", "../")
        print(f"Result for '../' directory:\n\t{info_result}")
        info_result = get_files_info("calculator", "main.py")
        print(f"Result for 'main.py' file:\n\t{info_result}")

if __name__ == "__main__":
    unittest.main()