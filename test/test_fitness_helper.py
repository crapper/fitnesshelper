import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
import tkcalendar as tkc
from unittest.mock import patch, MagicMock
from app import *
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from test_setup import root

class TestFitnessHelper(unittest.TestCase):
    def setUp(self):
        global root
        root.statistic_page = StatisticPage(root.c, root)
        root.camera_page = CameraPage(root.c, root)
        root.video_page = VideoPage(root.c, root)
        root.config_page = ConfigPage(root.c, root)
        root.initialize_attribute()
        pass

    def tearDown(self):
        root.statistic_page = StatisticPage(root.c, root)
        root.camera_page = CameraPage(root.c, root)
        root.video_page = VideoPage(root.c, root)
        root.config_page = ConfigPage(root.c, root)
        root.initialize_attribute()
        pass

    def test_create_hover_tip(self):
        def has_binding(widget, event):
            for tag in widget.bindtags():
                if widget.bind_class(tag, event):
                    return True
            return False
        test_btn = tk.Button(None)
        root.create_hover_tip(test_btn, 'test')
        self.assertTrue(has_binding(test_btn, '<Enter>'))
        self.assertTrue(has_binding(test_btn, '<Leave>'))
        root.enter(test_btn, 'test')
        self.assertTrue(root.tips != None)
        root.leave()
        self.assertTrue(root.tips == None)

    def test_pick_date(self):
        mock_toplevel = MagicMock()
        mock_toplevel.grab_set.return_value = None
        
        with patch.object(tk, 'Toplevel', return_value=mock_toplevel):
            with patch.object(tkc, 'Calendar'):
                root.pick_date()
                mock_toplevel.wait_window.assert_called_once()

    def test_update_date(self):
        mocktkc = tkc.Calendar(None, date_pattern='yyyy-mm-dd')
        mocktkc.selection_set(datetime.date(2020, 1, 1))
        root.temp_date = ""
        mock_toplevel = MagicMock()
        root.update_date(mock_toplevel, mocktkc)
        self.assertEqual(root.temp_date, "2020-01-01")

    def test_switch_camera_page(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        root.weight = -1
        with patch.object(messagebox, 'showinfo') as mock_showinfo:
            root.switchCameraPage()
            mock_showinfo.assert_called_once_with('Warning', 'Please enter your weight in the config page')
        root.weight = 1
        root.statistic_page.active = True
        root.config_page.active = True
        self.assertFalse(root.camera_page.active)
        root.switchCameraPage()
        self.assertTrue(root.camera_page.active)
        self.assertFalse(root.statistic_page.active)
        self.assertFalse(root.config_page.active)
        def mock_askquestion(title, message, **options):
            return 'no'
        with patch.object(mb, 'askquestion', side_effect=mock_askquestion):
            root.switchCameraPage()
            self.assertFalse(root.camera_page.active)

    def test_switch_video_page(self):
        # test if the weight is not entered
        root.weight = -1
        with patch.object(messagebox, 'showinfo') as mock_showinfo:
            root.switchVideoPage()
            mock_showinfo.assert_called_once_with('Warning', 'Please enter your weight in the config page')

        # test if the file is not selected
        root.weight = 1
        with patch.object(fd, 'askopenfilename', return_value=""):
            root.switchVideoPage()
            self.assertFalse(root.video_page.active)

        # test if the date is not selected
        root.temp_date = ""
        with patch.object(fd, 'askopenfilename', return_value="test.mp4"):
            with patch.object(tk, 'Toplevel'):
                with patch.object(tkc, 'Calendar'):
                    root.switchVideoPage()
                    self.assertFalse(root.video_page.active)

        # test if the date is future date
        root.temp_date = datetime.date.today() + datetime.timedelta(days=1)
        root.temp_date = root.temp_date.strftime("%Y-%m-%d")
        with patch.object(fd, 'askopenfilename', return_value="test.mp4"):
            with patch.object(tk, 'Toplevel'):
                with patch.object(tkc, 'Calendar'):
                    with patch.object(messagebox, 'showinfo') as mock_showinfo:
                        root.switchVideoPage()
                        self.assertFalse(root.video_page.active)
                        mock_showinfo.assert_called_once_with('Warning', 'Please enter a date before today')

        # test success case
        root.temp_date = "2020-01-01"
        with patch.object(fd, 'askopenfilename', return_value="test.mp4"):
            with patch.object(tk, 'Toplevel'):
                with patch.object(tkc, 'Calendar'):
                    root.switchVideoPage()
                    self.assertTrue(root.video_page.active)
                    self.assertEqual(root.video_page.date, "2020-01-01")
                    def mock_askquestion_yes(title, message, **options):
                        return 'yes'
                    with patch.object(mb, 'askquestion', side_effect=mock_askquestion_yes):
                        root.switchVideoPage()
                        self.assertFalse(root.video_page.active)
        
    def test_switch_statistic_page(self):
        def mock_askquestion(title, message, **options):
            return 'no'
        root.video_page.active = True
        root.pick_date = MagicMock()
        root.switchStatisticPage() # should not switch when video page is active
        self.assertFalse(root.statistic_page.active)
        root.video_page.active = False
        root.camera_page.active = True
        root.temp_date = "2020-01-01"
        with patch.object(mb, 'askquestion', side_effect=mock_askquestion):
            with patch.object(tk, 'Toplevel'):
                with patch.object(tkc, 'Calendar'):
                    root.switchStatisticPage()
                    self.assertTrue(root.statistic_page.active)
                    root.switchStatisticPage()
                    self.assertFalse(root.statistic_page.active)

    def test_switch_config_page(self):
        root.video_page.active = True
        root.switchConfigPage() # should not switch when video page is active
        self.assertFalse(root.config_page.active)
        root.video_page.active = False

        root.camera_page.active = True
        root.switchConfigPage() # should not switch when camera page is active
        self.assertFalse(root.config_page.active)
        root.camera_page.active = False

        root.statistic_page.active = True
        root.switchConfigPage() # should be able to switch when statistic page is active
        self.assertTrue(root.config_page.active)
        root.statistic_page.active = False

        root.switchConfigPage()
        self.assertFalse(root.config_page.active)

    def test_update_frame(self):
        root.after_keeper = None
        root.update_frame()
        self.assertIsNotNone(root.after_keeper)

    def test_before_destroy(self):
        root.update_frame()
        root.before_destroy()
        with patch.object(root, 'after_cancel') as mock_after_cancel:
            with patch.object(root, 'quit') as mock_quit:
                root.before_destroy()
                self.assertTrue(mock_after_cancel.called)
                self.assertTrue(mock_quit.called)

if __name__ == '__main__':
    unittest.main()
