import tkinter as tk

from .page import *

class ConfigPage(Page):
    def __init__(self, parent: tk.Canvas, controller: App):
        Page.__init__(self, parent, controller)
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
        width_weight, height_weight = self.get_width_height(self.panel[2])
        self.weight_entry = tk.Entry(self.controller, validate='all', validatecommand=(v_cmd, '%P'))
        self.weight_entry.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_weight, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1))
        self.weight_entry.place_forget()

        #Dropdowm menu for model complexity selection
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight), text="ModelComplexity: ", font=("Helvetica", 16), fill="black", anchor=tk.NW)) 
        width_model_complexity, height_model_complexity = self.get_width_height(self.panel[3])
        options = [0, 1, 2]
        clicked = tk.IntVar()
        clicked.set(options[1])
        self.drop_model_complexity = tk.OptionMenu(self.controller, clicked , *options)
        self.drop_model_complexity.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_model_complexity, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight))
        self.drop_model_complexity.place_forget()

        self.pixel = tk.PhotoImage(width=1, height=1)
        self.save_btn = tk.Button(self.controller, image=self.pixel, text="Save", state='normal', width=int((self.BgDown_x-self.BgTop_x)*0.2), height =int((self.BgDown_y-self.BgTop_y)*0.1), compound='c', command=lambda: self.save(int(self.weight_entry.get())))
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        self.save_btn.place_forget()
        
        self.hide_page()

    def save(self, weight):
        message = ""
        if self.controller.weight != weight:
            message += "Weight update successful to "+str(weight)+"\n"
        if self.controller.model_complexity != int(self.drop_model_complexity.cget("text")):
            message += "Model Complexity update successful to "+self.drop_model_complexity.cget("text")+"\n"
        self.controller.weight = weight
        self.controller.model_complexity = int(self.drop_model_complexity.cget("text"))
        tk.messagebox.showinfo("Success", message)
        self.toggle_visible()

    def get_width_height(self, id):
        bounds = self.parent.bbox(id)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        return width, height

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
        
        width_weight, height_weight = self.get_width_height(self.panel[2])
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        width_model_complexity, height_model_complexity = self.get_width_height(self.panel[3])
        self.drop_model_complexity.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_model_complexity, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight))
        self.weight_entry.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_weight, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1))

    def hide_page(self):
        self.active = False

        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')
        self.save_btn.place_forget()
        self.weight_entry.place_forget()
        self.drop_model_complexity.place_forget()

    def request_open_page(self):
        if self.active:
            return True

        self.show_page()
        return True

    def request_close_page(self):
        if self.active == False:
            return True

        self.hide_page()
        return True
