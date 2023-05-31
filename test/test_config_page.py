import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from unittest.mock import patch
import tkinter as tk
from app import *
import tkinter.messagebox as mb

from test_setup import root

class TestConfigPage(unittest.TestCase):
    def setUp(self):
        global root
        self.c = tk.Canvas(root)
        self.config_page = ConfigPage(self.c, root)

    def tearDown(self):
        self.config_page.model_conf_value.set(0.5)
        self.config_page.track_conf_value.set(0.5)
        self.config_page.entry_text.set("")
        self.config_page.drop_model_complexity.current(1)
        self.config_page.drop_statistic_unit.current(0)
        del self.config_page
        del self.c
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
        self.assertFalse(self.config_page.validate_entry("1.0.0"))
        self.assertTrue(self.config_page.validate_entry(""))
        self.assertFalse(self.config_page.validate_entry("1000000"))

    def test_enter_leave(self):
        self.assertIsNone(self.config_page.tips)
        self.config_page.Update_Model_Track_Tip(tk.Button(self.c), "test")
        self.assertIsNotNone(self.config_page.tips)
        self.assertEqual(self.config_page.tips.text, "test")
        self.config_page.leave()
        self.assertIsNone(self.config_page.tips)
        floatvar = tk.DoubleVar()
        floatvar.set(0.5)
        testentry = tk.Entry(self.c, textvariable=floatvar)
        self.config_page.Update_Model_Track_Tip(testentry, "test")
        self.assertIsNotNone(self.config_page.tips)
        self.assertEqual(self.config_page.tips.text, "test0.5")
        self.config_page.leave()
        self.assertIsNone(self.config_page.tips)

    def test_save_no_update(self):
        def mock_showinfo(title, message):
            return True
        with patch.object(mb, 'showinfo', side_effect=mock_showinfo):
            self.assertEqual(self.config_page.save(), "No update")
    
    def test_save_update_overweight(self):
        def mock_showinfo(title, message):
            return True
        root.statistic_page = None # To avoid error, set up dummy statistic page
        self.config_page.model_conf_value.set(0.7)
        self.config_page.track_conf_value.set(0.7)
        self.config_page.entry_text.set("1000")
        self.config_page.drop_model_complexity.current(2)
        self.config_page.drop_statistic_unit.current(2)
        with patch.object(mb, 'showinfo', side_effect=mock_showinfo):
            self.config_page.save()
            self.assertEqual(root.model_conf, 0.7)
            self.assertEqual(root.track_conf, 0.7)
            self.assertEqual(root.model_complexity, 2)
            self.assertEqual(root.statistic_unit, 2)
            self.assertEqual(root.weight, 999)
    
    def test_save_update_underweight(self):
        def mock_showinfo(title, message):
            return True
        root.statistic_page = None # To avoid error, set up dummy statistic page
        self.config_page.model_conf_value.set(0.7)
        self.config_page.track_conf_value.set(0.7)
        self.config_page.entry_text.set("100")
        self.config_page.drop_model_complexity.current(2)
        self.config_page.drop_statistic_unit.current(2)
        with patch.object(mb, 'showinfo', side_effect=mock_showinfo):
            self.config_page.save()
            self.assertEqual(root.model_conf, 0.7)
            self.assertEqual(root.track_conf, 0.7)
            self.assertEqual(root.model_complexity, 2)
            self.assertEqual(root.statistic_unit, 2)
            self.assertEqual(root.weight, 100)
    
if __name__ == '__main__':
    unittest.main()



