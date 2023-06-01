import os
import subprocess
import tkinter
import cv2
import numpy as np
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
from PIL import Image, ImageTk

from mp_utils import annotate_hands, annotate_body


customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


# global cam


def openf():
    return filedialog.askopenfilename(initialdir="~", title="select powerpoint file")


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Powerpoint Gestures")
        self.geometry("400x100")
        self.label = customtkinter.CTkLabel(
            self, text="Please select a powerpoint file(ppt,pptx,pptm)"
        )
        self.label.pack(padx=20, pady=20)


class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=140, corner_radius=0)

        self.logo_label = customtkinter.CTkLabel(
            self,
            text="Powerpoint Gestures",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self, text="Open...", command=master.get_file
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        frame = np.random.randint(0, 255, [100, 100, 3], dtype="uint8")
        # configure window
        self.title("Powerpoint Hand Gestures")
        self.geometry(f"{1100}x{580}")
        self.timeline_text = "Gesture Recording Timeline\n"
        self.cam = None
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = SidebarFrame(self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10)),
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create frame to view images
        self.feed_frame = customtkinter.CTkLabel(self, text="")
        self.feed_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(
            master=self,
            width=150,
            height=40,
            text="start",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.start_cam,
        )

        self.main_button_1.grid(
            row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Configure Gestures")
        self.tabview.add("Configure Pointer")
        self.tabview.tab("Configure Gestures").grid_columnconfigure(
            0, weight=1
        )  # configure grid of individual tabs
        self.tabview.tab("Configure Pointer").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(
            self.tabview.tab("Configure Gestures"),
            dynamic_resizing=False,
            values=["Value 1", "Value 2", "Value Long Long Long"],
        )
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(
            self.tabview.tab("Configure Gestures"),
            values=["Value 1", "Value 2", "Value Long....."],
        )
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(
            self.tabview.tab("Configure Gestures"),
            text="Open CTkInputDialog",
            command=self.open_input_dialog_event,
        )
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(
            self.tabview.tab("Configure Pointer"), text="CTkLabel on Tab 2"
        )
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(
            row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(
            master=self.radiobutton_frame, text="Select Mode"
        )
        self.label_radio_group.grid(
            row=0, column=2, columnspan=1, padx=10, pady=10, sticky=""
        )
        self.radio_button_1 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            text="Long Distance",
            variable=self.radio_var,
            value=0,
        )
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            text="Short Distance",
            variable=self.radio_var,
            value=1,
        )
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="#191717")
        self.slider_progressbar_frame.grid(
            row=0, column=1, padx=(20, 0), rowspan=4, pady=(20, 0), sticky="nsew"
        )
        self.rowconfigure(1, weight=1)
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(
            self.slider_progressbar_frame, fg_color="#282424"
        )
        self.seg_button_1.grid(
            row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
        )
        self.timeline = customtkinter.CTkLabel(
            self.slider_progressbar_frame, text=self.timeline_text
        )
        self.timeline.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="w")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self, label_text="Toggle Gestures"
        )
        self.scrollable_frame.grid(
            row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(18):
            switch = customtkinter.CTkSwitch(
                master=self.scrollable_frame, text=f"Gesture {i}"
            )
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(
            row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.checkbox_1 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="Enable Pointer"
        )
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")

        # set default values
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.seg_button_1.configure(values=["View 1", "View 2", "View 3"])
        self.seg_button_1.set("View 2")

    def start_cam(self):
        subprocess.run(["python", "short_distance.py"])
        # self.cam = cv2.VideoCapture(0)
        # while True:
        #     ret, frame = self.cam.read()
        #     if self.radio_var.get() == 1:
        #         annotate_hands(frame)
        #     elif self.radio_var.get() == 0:
        #         annotate_body(frame)
        #     frame = cv2.flip(frame, 1)
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     image_update = customtkinter.CTkImage(
        #         Image.fromarray(frame), size=(900, 600)
        #     )
        #     self.feed_frame.configure(image=image_update)
        #     self.feed_frame.update()

        #     if not ret:
        #         # add better error handling here
        #         print("failed to grab frame")
        #     k = cv2.waitKey(1)
        #     if k % 256 == 27:
        #         print("closing feed")
        #         self.cam.release()
        #         cv2.destroyAllWindows()
        #         break

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog"
        )
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def get_file(self):
        file_dir = openf()
        if file_dir.lower().endswith(("pptx", "pptm", "ppt")):
            self.file_dir = file_dir
        else:
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.focus()


if __name__ == "__main__":
    app = App()
    app.mainloop()
