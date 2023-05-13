import tkinter as tk

class HelloButton:
    def __init__(self, master):
        self.master = master
        self.hello_button = tk.Button(self.master, text="Hello", command=self.print_hello)
        self.hello_button.pack()

    def print_hello(self):
        print("Hello")


root = tk.Tk()
hello_button = HelloButton(root)
root.mainloop()
