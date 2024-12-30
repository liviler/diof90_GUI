import customtkinter
import json

from modules.Configuration import Configuration
from modules.Workspace import Workspace
from modules.Plot import Plot
from modules.style import *

customtkinter.set_default_color_theme("blue") 
customtkinter.set_appearance_mode("light")

class multiTabs(customtkinter.CTkTabview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._segmented_button.configure(font=bold18)
        self._segmented_button.grid(ipadx=100,ipady=18)
        
        tab1 = self.add("Configuration")
        tab1.grid_columnconfigure(0, weight=1)
        tab1.grid_rowconfigure(0, weight=1)
        self.configuration = Configuration(tab1, width = 900, height=500, corner_radius=0,fg_color="transparent")
        self.configuration.grid(row=0, column=0, padx=20, pady=20,sticky="ns")
        
        tab2 = self.add("Workspace")
        tab2.grid_columnconfigure(0, weight=1)
        tab2.grid_rowconfigure(0, weight=1)
        self.workspace = Workspace(tab2, width = 900, height=500,corner_radius=0,fg_color="transparent")
        self.workspace.grid(row=0, column=0, padx=20, pady=20,sticky="ns")
        self.workspace.grid_propagate(0) # make width of workspace(Frame) work!
        
        tab3 = self.add("Plot")
        tab3.grid_columnconfigure(0, weight=1)
        tab3.grid_rowconfigure(0, weight=1)
        self.plot = Plot(tab3, width = 900, height=500, corner_radius=0,fg_color="transparent")
        self.plot.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        self.plot.grid_propagate(0) # make width of workspace(Frame) work!
        # self.set("Workspace")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('DIO F90')
        self.iconbitmap('code.ico')
        self.set_geometry(width=1200, height=675, min_width=650,min_height=350)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.multiTabs = multiTabs(self)
        self.multiTabs.grid(row=0, column=0, sticky="nsew")

    def set_geometry(self,width,height, min_width, min_height):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        left, top = int((window_width -width)/2), int((window_height - height)/2)
        self.geometry(f'{width}x{height}+{left}+{top}')
        self.minsize(min_width, min_height)

if __name__ == '__main__':
    
    app = App()
    app.mainloop()
    