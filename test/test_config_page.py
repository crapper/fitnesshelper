import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import tkinter as tk
from app import *



configpage = ConfigPage(tk.Canvas(None), None)
print(configpage.active)
configpage.show_page()
print(configpage.active)
