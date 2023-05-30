import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
import os

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def openf():
    return filedialog.askopenfilename(initialdir='~', title="select powerpoint file")




class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Powerpoint Gestures")
        self.geometry("400x100")
        self.label = customtkinter.CTkLabel(self, text="Please select a powerpoint file(ppt,pptx,pptm)")
        self.label.pack(padx=20, pady=20)



class SidebarFrame (customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.open_button = customtkinter.CTkButton(self,text="Open..",command=master.get_file)
        self.open_button.grid(row=2,column=0,padx=20,pady=20,sticky="nsw")
        self.toplevel_window = None


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.file_dir = None
        self.title("Powerpoint Gestures")
        self.geometry(f"{1100}x{580}")
        customtkinter.set_widget_scaling(1.25)

        self.sidebarframe = SidebarFrame(self)
        self.grid_rowconfigure(0,weight=1)
        self.sidebarframe.grid(row=0,column=0,sticky='nsw')

    def get_file(self):
        file_dir = openf()
        if file_dir.lower().endswith(("pptx","pptm","ppt")):
            self.file_dir = file_dir
        else:
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.focus()

        



if __name__ == "__main__":
    app = App()
    app.mainloop()