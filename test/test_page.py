import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from app import *

class TestPage(unittest.TestCase):
    def setUp(self):
        self.page = Page(None, None)

    def test_dummy(self):
        self.page.show_page()
        self.page.hide_page()
        self.page.request_open_page()
        self.page.request_close_page()
        self.page.update_frame()

if __name__ == '__main__':
    unittest.main()
