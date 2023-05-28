from collections.abc import Callable
import sys
import os
from typing import Any
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
import tkinter as tk
from app import *

class TestConfigPage(unittest.TestCase):
    def setUp(self):
        self.c = tk.Canvas(None)
        self.configpage = ConfigPage(self.c, None)

    def tearDown(self):
        pass

    def test_show_page(self):
        self.assertFalse(self.configpage.active)
        self.configpage.show_page()
        self.assertTrue(self.configpage.active)

    def test_hide_page(self):
        self.configpage.show_page()
        self.assertTrue(self.configpage.active)
        self.configpage.hide_page()
        self.assertFalse(self.configpage.active)

    def test_request_open_page(self):
        self.assertFalse(self.configpage.active)
        self.configpage.request_open_page()
        self.assertTrue(self.configpage.active)
        self.assertTrue(self.configpage.request_open_page())
    
    def test_request_close_page(self):
        self.configpage.show_page()
        self.assertTrue(self.configpage.active)
        self.configpage.request_close_page()
        self.assertFalse(self.configpage.active)
        self.assertTrue(self.configpage.request_close_page())

    def test_validate_entry(self):
        self.assertFalse(self.configpage.validate_entry("a"))
        self.assertTrue(self.configpage.validate_entry("1"))
        self.assertTrue(self.configpage.validate_entry("1.0"))
        self.assertTrue(self.configpage.validate_entry("1.0e-10"))
        self.assertTrue(self.configpage.validate_entry(""))
    
    
if __name__ == '__main__':
    unittest.main()


