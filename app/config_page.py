import tkinter as tk

from .page import *
from .tips_window import *

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
        self.model_conf_value = tk.DoubleVar()
        self.model_conf_value.set(0.5)
        self.track_conf_value = tk.DoubleVar()
        self.track_conf_value.set(0.5)
        self.entry_text = tk.StringVar()
        self.entry_text.set("")
        self.tips: TipWindow = None

        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1), text="Weight: ", font=("Helvetica", 16), fill="black", anchor=tk.NW)) 
        v_cmd = (self.register(self.validate_entry))
        width_weight, height_weight = self.get_width_height(self.panel[2])
        self.weight_entry = tk.Entry(self.controller, validate='all', validatecommand=(v_cmd, '%P'), textvariable=self.entry_text)
        self.weight_entry.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_weight, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1))
        self.weight_entry.place_forget()

        #Dropdown menu for model complexity selection
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight), text="ModelComplexity: ", font=("Helvetica", 16), fill="black", anchor=tk.NW)) 
        width_model_complexity, height_model_complexity = self.get_width_height(self.panel[3])
        options = [0, 1, 2]
        self.drop_model_complexity = tk.ttk.Combobox(self.controller, values=options, state="readonly", width=2, font=("Helvetica", 10))
        self.drop_model_complexity.current(1)
        self.drop_model_complexity.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_model_complexity, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight))
        self.drop_model_complexity.place_forget()

        #Drag bar for model confidence
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity), text="ModelConf: ", font=("Helvetica", 16), fill="black", anchor=tk.NW)) 
        width_model_conf, height_model_conf = self.get_width_height(self.panel[4])
        self.drag_model_conf = tk.ttk.Scale(self.controller, from_=0, to=1, orient="horizontal", command=lambda x: self.Update_Model_Track_Tip(self.drag_model_conf, "min_detection_confidence: "), variable=self.model_conf_value)
        self.create_hover_tip(self.drag_model_conf, "min_detection_confidence: ")
        self.drag_model_conf.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_model_conf, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity))
        self.drag_model_conf.place_forget()

        #Drag bar for tracking confidence
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+10), text="TrackingConf: ", font=("Helvetica", 16), fill="black", anchor=tk.NW))
        width_track_conf, height_track_conf = self.get_width_height(self.panel[5])
        self.drag_track_conf = tk.ttk.Scale(self.controller, from_=0, to=1, orient="horizontal", command=lambda x: self.Update_Model_Track_Tip(self.drag_track_conf, "min_tracking_confidence: "), variable=self.track_conf_value)
        self.create_hover_tip(self.drag_track_conf, "min_tracking_confidence: ")
        self.drag_track_conf.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_track_conf, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+10))
        self.drag_track_conf.place_forget()

        #Dropdown menu for statistic unit selection
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+height_track_conf+16), text="StatisticUnit: ", font=("Helvetica", 16), fill="black", anchor=tk.NW))
        width_statistic_unit, height_statistic_unit = self.get_width_height(self.panel[6])
        options = ['Day', 'Month', 'Year']
        self.drop_statistic_unit = tk.ttk.Combobox(self.controller, values=options, state="readonly", font=("Helvetica", 10))
        self.drop_statistic_unit.current(0)
        self.drop_statistic_unit.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_statistic_unit, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+height_track_conf+18))
        self.drop_statistic_unit.place_forget()

        self.pixel = tk.PhotoImage(width=1, height=1)
        self.save_btn = tk.Button(self.controller, image=self.pixel, text="Save", state='normal', width=int((self.BgDown_x-self.BgTop_x)*0.2), height =int((self.BgDown_y-self.BgTop_y)*0.1), compound='c', command=lambda: self.save())
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        
        self.hide_page()

    def save(self):
        message = ""
        if self.weight_entry.get() != "" and self.controller.weight != float(self.weight_entry.get()):
            if float(self.weight_entry.get()) >= 1000:
                self.entry_text.set("999")
            self.controller.weight = float(self.weight_entry.get())
            message += "Weight update successful to "+str(float(self.weight_entry.get()))+"\n"
        if self.controller.model_complexity != int(self.drop_model_complexity.get()):
            self.controller.model_complexity = int(self.drop_model_complexity.get())
            message += "Model Complexity update successful to "+self.drop_model_complexity.get()+"\n"
        if self.controller.model_conf != round(float(self.drag_model_conf.get()), 2):
            self.controller.model_conf = round(float(self.drag_model_conf.get()), 2)
            message += "Model Confidence update successful to "+str(round(float(self.drag_model_conf.get()), 2))+"\n"
        if self.controller.track_conf != round(float(self.drag_track_conf.get()), 2):
            self.controller.track_conf = round(float(self.drag_track_conf.get()), 2)
            message += "Tracking Confidence update successful to "+str(round(float(self.drag_track_conf.get()), 2))+"\n"
        if self.controller.statistic_unit != self.drop_statistic_unit.current():
            self.controller.statistic_unit = self.drop_statistic_unit.current()
            message += "Statistic Unit update successful to "+self.drop_statistic_unit.get()+"\n"
            if self.controller.statistic_page and self.controller.statistic_page.active:
                self.controller.statistic_page.update_plot()
        if message == "":
            message = "No update"
        tk.messagebox.showinfo("Success", message)
        self.toggle_visible()
        return message

    def leave(self):
        if self.tips != None:
            self.tips.hidetip()
            self.tips = None
    
    def enter(self, widget, text):
        self.leave()
        self.tips = TipWindow(widget)
        try:
            value = str(round(float(widget.get()), 2))
            self.tips.showtip(text + value)
        except:
            self.tips.showtip(text)

    def create_update_tip(self, widget, text):
        self.enter(widget, text)
        widget.bind('<Leave>',lambda event: self.leave())

    def create_hover_tip(self, widget, text):
        widget.bind('<Enter>',lambda event, widget=widget, text=text: self.enter(widget, text))
        widget.bind('<Leave>',lambda event: self.leave())

    def get_width_height(self, id):
        bounds = self.parent.bbox(id)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        return width, height

    def validate_entry(self, P):
        try:
            if P == ""  or float(P):
                pass
            if len(P) > 6:
                return False
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
        self.drag_track_conf.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_track_conf, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+10))
        width_statistic_unit, height_statistic_unit = self.get_width_height(self.panel[6])
        self.drop_statistic_unit.place(x= self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) + width_statistic_unit, y = self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1+height_weight+height_model_complexity+height_model_conf+height_track_conf+18))

    def hide_page(self):
        self.active = False

        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')
        self.save_btn.place_forget()
        self.weight_entry.place_forget()
        self.drop_model_complexity.place_forget()
        self.drag_model_conf.place_forget()
        self.drag_track_conf.place_forget()
        self.drop_statistic_unit.place_forget()

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
