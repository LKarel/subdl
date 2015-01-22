import tkinter as tk
from tkinter import ttk

def _lang(string):
    return string

def _save_lang(value): # Save the language
    pass

def _search(target): # Movie/serial to search
    print(target)

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.resizable(0, 0)
        self.geometry("%dx%d" % (426, 320))
        self.title("Subtitle downloader")

        self.lang = tk.Label(text=_lang("Vali keel:"))
        self.lang.place(x=15, y=25)

        options = ("Eesti", "English")

        self.var = tk.StringVar(self)
        self.var.set(options[0])

        self.dropdown = ttk.OptionMenu(self, self.var, options[0], *options)
        self.dropdown.place(x=85, y=25)

        self.save_button = ttk.Button(self, text=_lang("salvesta"), command= lambda: _save_lang(self.var.get()))
        self.save_button.place(x=175, y=25)

        self.help = tk.Label(text=_lang("Kuidas seda persekukkunud programmi kasutada..."))
        self.help.place(x=15, y=75)

        self.search = tk.Label(text=_lang("Faili või filmi nimi, mida otsiad:"))
        self.search.place(x=15, y=125)

        self.searchbox = ttk.Entry(self, width=40)
        self.searchbox.place(x=15, y=150)

        self.search_button = ttk.Button(self, text=_lang("otsi"), command= lambda: _search(self.searchbox.get()))
        self.search_button.place(x=280, y=150)

        self.footer = tk.Label(text="Ragnis Armus, Karel Liiv \n Github - https://github.com/Ragnis/subdl")
        self.footer.place(x=100,y=250)


if __name__ == "__main__":
    app = Application();
    app.mainloop()
