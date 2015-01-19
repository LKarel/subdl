import tkinter as tk

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.resizable(0, 0)
        self.geometry("%dx%d" % (426, 320))

        self.label = tk.Label(text="Hello, world")
        self.label.pack(padx=10, pady=10)

if __name__ == "__main__":
    app = Application();
    app.mainloop()
