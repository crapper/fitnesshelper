import tkinter as tk
import tkinter.font as tkFont

from .page import *

class ConfigPage(Page):
    def __init__(self, parent: tk.Canvas, controller):
        Page.__init__(self, parent)
        self.controller = controller
        self.panel = []
        self.BgTop_x = 688
        self.BgTop_y = 188
        self.BgDown_x = 1088
        self.BgDown_y = 488
        self.shape_tri_pointer={'bounds': [1152, 352, self.BgDown_x, 320, self.BgDown_x, 384], 'kind': 'tri', 'fill': True}
        self.panel.append(self.parent.create_polygon(list(self.shape_tri_pointer.values())[0],fill='white',outline='blue', width = 5)) #[0] : widget background panel triangle
        self.panel.append(self.parent.create_rectangle(self.BgTop_x, self.BgTop_y,self.BgDown_x,self.BgDown_y,fill='white',outline='blue', width = 5)) #[1] : widget background panel rectangle
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1), text="Weight: ", font=("Helvetica", 16), fill="black", anchor=tk.NW)) 
        v_cmd = (self.register(self.validate_entry))
        size = tkFont.Font(size=16, family='Helvetica').measure('Weight: ')

        self.weight_entry = tk.Entry(self.controller, validate='all', validatecommand=(v_cmd, '%P'))
        self.weight_entry.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + size, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1))
        self.weight_entry.place_forget()

        self.pixel = tk.PhotoImage(width=1, height=1)
        self.save_btn = tk.Button(self.controller, image=self.pixel, text="Save", state='normal', width=int((self.BgDown_x-self.BgTop_x)*0.2), height =int((self.BgDown_y-self.BgTop_y)*0.1), compound='c', command=lambda: self.save(int(self.weight_entry.get())))
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        self.save_btn.place_forget()
        self.active = False
        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')

    def save(self, weight):
        self.controller.weight = weight
        tk.messagebox.showinfo("Success", "Weight update successful to "+str(weight))
        self.toggle_visible()

    def validate_entry(self, P):
        try:
            if P == ""  or float(P):
                pass
        except:
            return False
        return True

    def show_page(self):
        self.active = True
        for item in self.panel:
            self.parent.itemconfig(item, state='normal')
            self.parent.tag_raise(item, 'all')
        size = tkFont.Font(size=16, family='Helvetica').measure('Weight: ')
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        self.weight_entry.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + size, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1))

        for item in self.panel:
            self.parent.tag_raise(item, 'all')

    def hide_page(self):
        self.active = False
        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')
        self.save_btn.place_forget()
        self.weight_entry.place_forget()
