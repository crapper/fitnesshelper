import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
import tkinter as tk
from app import *

class TestConfigPage(unittest.TestCase):
    def setUp(self):
        self.c = tk.Canvas(None)
        self.config_page = ConfigPage(self.c, None)

    def tearDown(self):
        pass

    def test_show_page(self):
        self.assertFalse(self.config_page.active)
        self.config_page.show_page()
        self.assertTrue(self.config_page.active)

    def test_hide_page(self):
        self.config_page.show_page()
        self.assertTrue(self.config_page.active)
        self.config_page.hide_page()
        self.assertFalse(self.config_page.active)

    def test_request_open_page(self):
        self.assertFalse(self.config_page.active)
        self.config_page.request_open_page()
        self.assertTrue(self.config_page.active)
        self.assertTrue(self.config_page.request_open_page())
    
    def test_request_close_page(self):
        self.config_page.show_page()
        self.assertTrue(self.config_page.active)
        self.config_page.request_close_page()
        self.assertFalse(self.config_page.active)
        self.assertTrue(self.config_page.request_close_page())

    def test_validate_entry(self):
        self.assertFalse(self.config_page.validate_entry("a"))
        self.assertTrue(self.config_page.validate_entry("1"))
        self.assertTrue(self.config_page.validate_entry("1.0"))
        self.assertTrue(self.config_page.validate_entry("1.0e-10"))
        self.assertTrue(self.config_page.validate_entry(""))
    
    
if __name__ == '__main__':
    unittest.main()


