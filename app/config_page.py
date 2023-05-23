import tkinter as tk

from .page import *

import locale
locale.setlocale(locale.LC_NUMERIC, 'pl_PL.UTF8')

class NewScale(tk.Frame):
    def __init__(self, master=None, **options):
        tk.Frame.__init__(self, master)

        # Disable normal value display...
        options['showvalue'] = False
        # ... and use custom display instead
        options['command'] = self._on_scale

        # Set resolution to 1 and adjust to & from value 
        self.res = options.get('resolution', 1)
        from_ = int(options.get('from_', 0) / self.res)
        to = int(options.get('to', 100) / self.res)
        options.update({'resolution': 1, 'to': to, 'from_': from_})

        # This could be improved...
        if 'digits' in options:
            self.digits = ['digits']
            del options['digits']
        else:
            self.digits = 2

        self.scale = tk.Scale(self, **options)
        self.scale_label = tk.Label(self)
        orient = options.get('orient', tk.VERTICAL)
        if orient == tk.VERTICAL:
            side, fill = 'right', 'y'
        else:
            side, fill = 'top', 'x'
        self.scale.pack(side=side, fill=fill)
        self.scale_label.pack(side=side)

    def _on_scale(self, value):
        value = locale.atof(value) * self.res
        value = locale.format_string('%.*f', (self.digits, value))
        self.scale_label.configure(text=value)

    def get(self):
        return self.scale.get() * self.res

    def set(self, value):   
        self.scale.set(int(0.5 + value / self.res))


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

        #Dropdown menu for model complexity selection
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight), text="ModelComplexity: ", font=("Helvetica", 16), fill="black", anchor=tk.NW)) 
        width_model_complexity, height_model_complexity = self.get_width_height(self.panel[3])
        options = [0, 1, 2]
        clicked = tk.IntVar()
        clicked.set(options[1])
        self.drop_model_complexity = tk.OptionMenu(self.controller, clicked , *options)
        self.drop_model_complexity.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_model_complexity, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight))
        self.drop_model_complexity.place_forget()

        #Drag bar for model confidence
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity), text="ModelConf: ", font=("Helvetica", 16), fill="black", anchor=tk.NW)) 
        width_model_conf, height_model_conf = self.get_width_height(self.panel[4])
        self.drag_model_conf = NewScale(self.controller, from_=0, to=1, orient=tk.HORIZONTAL, tickinterval=0.1, resolution =0.01, width=5)
        self.drag_model_conf.set(0.5)
        self.drag_model_conf.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_model_conf, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity))
        self.drag_model_conf.place_forget()

        #Drag bar for tracking confidence
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+16), text="TrackingConf: ", font=("Helvetica", 16), fill="black", anchor=tk.NW))
        width_track_conf, height_track_conf = self.get_width_height(self.panel[5])
        self.drag_track_conf = NewScale(self.controller, from_=0, to=1, orient=tk.HORIZONTAL, tickinterval=0.1, resolution =0.01, width=5)
        self.drag_track_conf.set(0.5)
        self.drag_track_conf.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_track_conf, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+16))
        self.drag_track_conf.place_forget()

        self.pixel = tk.PhotoImage(width=1, height=1)
        self.save_btn = tk.Button(self.controller, image=self.pixel, text="Save", state='normal', width=int((self.BgDown_x-self.BgTop_x)*0.2), height =int((self.BgDown_y-self.BgTop_y)*0.1), compound='c', command=lambda: self.save(int(self.weight_entry.get())))
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        
        self.hide_page()

    def save(self, weight):
        message = ""
        if self.controller.weight != weight:
            message += "Weight update successful to "+str(weight)+"\n"
        if self.controller.model_complexity != int(self.drop_model_complexity.cget("text")):
            message += "Model Complexity update successful to "+self.drop_model_complexity.cget("text")+"\n"
        if self.controller.model_conf != self.drag_model_conf.get():
            message += "Model Confidence update successful to "+str(self.drag_model_conf.get())+"\n"
        if self.controller.track_conf != self.drag_track_conf.get():
            message += "Tracking Confidence update successful to "+str(self.drag_track_conf.get())+"\n"
        self.controller.weight = weight
        self.controller.model_complexity = int(self.drop_model_complexity.cget("text"))
        self.controller.model_conf = self.drag_model_conf.get()
        self.controller.track_conf = self.drag_track_conf.get()
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
        width_model_conf, height_model_conf = self.get_width_height(self.panel[4])
        self.drag_model_conf.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_model_conf, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity))
        width_track_conf, height_track_conf = self.get_width_height(self.panel[5])
        self.drag_track_conf.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_track_conf, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+16))

    def hide_page(self):
        self.active = False

        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')
        self.save_btn.place_forget()
        self.weight_entry.place_forget()
        self.drop_model_complexity.place_forget()
        self.drag_model_conf.place_forget()
        self.drag_track_conf.place_forget()

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
