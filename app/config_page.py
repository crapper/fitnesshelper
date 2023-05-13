import tkinter as tk
from tkinter import *
import tkinter.font as tkFont

class ConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.panel = []
        self.BgTopx = 688
        self.BgTopy = 188
        self.BgDownx = 1088
        self.BgDowny = 488
        self.shapetripointer={'bounds': [1152, 352, self.BgDownx, 320, self.BgDownx, 384], 'kind': 'tri', 'fill': True}
        self.panel.append(self.parent.create_polygon(list(self.shapetripointer.values())[0],fill='white',outline='blue', width = 5)) #[0] : widget background panel triangle
        self.panel.append(self.parent.create_rectangle(self.BgTopx, self.BgTopy,self.BgDownx,self.BgDowny,fill='white',outline='blue', width = 5)) #[1] : widget background panel rectangle
        self.panel.append(self.parent.create_text(self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1), self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1), text="Weight: ", font=("Helvetica", 16), fill="black", anchor=NW)) 
        vcmd = (self.register(self.validate_entry))
        size = tkFont.Font(size=16, family='Helvetica').measure('Weight: ')

        self.weightentry = Entry(self.controller, validate='all', validatecommand=(vcmd, '%P'))
        self.weightentry.place(x= self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1) + size, y = self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1))
        self.weightentry.place_forget()

        self.pixel = tk.PhotoImage(width=1, height=1)
        self.savebtn = Button(self.controller, image=self.pixel, text="Save", state='normal', width=int((self.BgDownx-self.BgTopx)*0.2), height =int((self.BgDowny-self.BgTopy)*0.1), compound='c', command=lambda: self.save(int(self.weightentry.get())))
        self.savebtn.place(x= self.BgDownx - int((self.BgDownx-self.BgTopx)*0.3), y = ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.1) )+16+16)
        self.savebtn.place_forget()
        self.active = False
        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')

    def save(self, weight):
        self.controller.weight = weight
        tk.messagebox.showinfo("Success", "Weight update successful to "+str(weight))
        self.disableswitch()

    def validate_entry(self, P):
        try:
            if P == ""  or float(P):
                pass
        except:
            return False
        return True

    def disableswitch(self):
        if self.active == False:
            self.active = True
            for item in self.panel:
                self.parent.itemconfig(item, state='normal')
                self.parent.tag_raise(item, 'all')
            size = tkFont.Font(size=16, family='Helvetica').measure('Weight: ')
            self.savebtn.place(x= self.BgDownx - int((self.BgDownx-self.BgTopx)*0.3), y = ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.1) )+16+16)
            self.weightentry.place(x= self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1) + size, y = self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1))
        else:
            self.active = False
            for item in self.panel:
                self.parent.itemconfig(item, state='hidden')
            self.savebtn.place_forget()
            self.weightentry.place_forget()

    def movetop(self):
        for item in self.panel:
            self.parent.tag_raise(item, 'all')
