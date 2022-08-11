import tkinter as tk


class guiTk(tk.Frame):

    def __init__(self, parent:tk.Tk, *args, **kwargs):

        # ----------------------------------------------------------------------
        #  Setup
        # ----------------------------------------------------------------------
        # Setup TK Frame
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Get Handle to Main Frame
        self.parent = parent

        # ----------------------------------------------------------------------
        #  Generate GUI
        # ----------------------------------------------------------------------
        self.setup_gui()

    def setup_gui(self):
        self.parent.title('MIKE')

if __name__ == "__main__":
    root = tk.Tk()
    guiTk(root)
    root.mainloop()
