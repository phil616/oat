import unittest
from io_tools import systeminfo

class TestWindows(unittest.TestCase):
    controller = None
    ADMIN_ENV = False
    notepad_path = "C:\\Windows\\System32\\notepad.exe"
    WeChat_path = "C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    @classmethod
    def setUpClass(cls):
        cls.controller = systeminfo.WindowsProcessOperate()
        print("setUpClass")

    def test_privileges(self):
        flag = self.controller.is_runas_administrator()
        self.assertEqual(flag,self.ADMIN_ENV)

    def test_app_start(self):
        if self.ADMIN_ENV:
            self.controller.start_executable(self.notepad_path)
    def test_call_front(self):
        self.controller.load_process_to_front("notepad.exe")

    # no more test cases
    