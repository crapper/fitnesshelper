import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from unittest.mock import patch
import tkinter as tk
from app import *
import matplotlib.pyplot
import tkinter.messagebox as mb

root = App()

class TestStatisticPage(unittest.TestCase):
    def setUp(self):
        global root
        self.c = tk.Canvas(root)
        self.statistic_page = StatisticPage(self.c,root)
        root.withdraw()
        self.statistic_page.start_date = "2019-01-01"
        self.statistic_page.end_date = "2019-01-01"
        self.sql_conn = SQLconnector()
        if os.path.exists(self.sql_conn.db_path):
            os.remove(self.sql_conn.db_path)
        self.sql_conn.date = "2019-01-01"
        self.sql_conn.save("pushup", 10, 5, 60, 3)
        self.sql_conn.save("situp", 10, 5, 60, 3)

    def tearDown(self):
        matplotlib.pyplot.close('all')
        del self.statistic_page
        del self.c
        os.remove(self.sql_conn.db_path)
        del self.sql_conn

    def test_show_page(self):
        self.assertFalse(self.statistic_page.active)
        self.statistic_page.show_page()
        self.assertTrue(self.statistic_page.active)

    def test_hide_page(self):
        self.statistic_page.show_page()
        self.assertTrue(self.statistic_page.active)
        self.statistic_page.hide_page()
        self.assertFalse(self.statistic_page.active)
    
    def test_request_open_page(self):
        self.assertFalse(self.statistic_page.active)
        self.statistic_page.show_page()

        # Define a mock function to replace tkMessageBox.showinfo
        def mock_showinfo(title, message):
            return True

        # Use patch to replace tkMessageBox.showinfo with the mock function
        with patch.object(mb, 'showinfo', side_effect=mock_showinfo):
            self.assertTrue(self.statistic_page.request_open_page())

        self.statistic_page.hide_page()
        self.statistic_page.start_date = "2020-01-01"
        self.statistic_page.end_date = "2019-01-01"

        # Use patch again to replace tkMessageBox.showinfo with the mock function
        with patch.object(mb, 'showinfo', side_effect=mock_showinfo):
            self.assertFalse(self.statistic_page.request_open_page())

        self.assertEqual(self.statistic_page.start_date, "")
        self.assertEqual(self.statistic_page.end_date, "")

        self.statistic_page.start_date = "2019-01-01"
        self.statistic_page.end_date = "2019-01-01"

        # Use patch again to replace tkMessageBox.showinfo with the mock function
        with patch.object(mb, 'showinfo', side_effect=mock_showinfo):
            self.assertTrue(self.statistic_page.request_open_page())

    def test_request_close_page(self):
        self.assertTrue(self.statistic_page.request_close_page()) # close the page when the page is not active
        self.statistic_page.show_page()
        self.assertTrue(self.statistic_page.active)
        self.assertTrue(self.statistic_page.request_close_page())
        self.assertFalse(self.statistic_page.active)

    def test_change_state(self):
        self.assertEqual(self.statistic_page.state, 0)
        self.statistic_page.change_state(1)
        self.assertEqual(self.statistic_page.state, 1)
        self.statistic_page.change_state(-1)
        self.assertEqual(self.statistic_page.state, 0)
        self.statistic_page.change_state(-1)
        self.assertEqual(self.statistic_page.state, 3)
        self.statistic_page.change_state(1)
        self.assertEqual(self.statistic_page.state, 0)

    def test_update_plot(self):
        self.statistic_page.start_date = "2019-01-01"
        self.statistic_page.end_date = "2019-01-01"
        self.assertIsNone(self.statistic_page.plot_graph_list[0])
        self.assertIsNone(self.statistic_page.plot_graph_list[1])
        self.assertIsNone(self.statistic_page.plot_graph_list[2])
        self.assertIsNone(self.statistic_page.plot_graph_list[3])
        self.statistic_page.update_plot()
        self.assertIsNotNone(self.statistic_page.plot_graph_list[0])
        self.assertIsNotNone(self.statistic_page.plot_graph_list[1])
        self.assertIsNotNone(self.statistic_page.plot_graph_list[2])
        self.assertIsNotNone(self.statistic_page.plot_graph_list[3])

        root.statistic_unit = 1 # dummy for coverage
        self.statistic_page.update_plot()

        root.statistic_unit = 2 # dummy for coverage
        self.statistic_page.update_plot()


if __name__ == '__main__':
    unittest.main()