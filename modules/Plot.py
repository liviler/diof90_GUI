import customtkinter
from modules.style import *
from PIL import Image,ImageTk
import pathlib

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scienceplots

ui_images_path = pathlib.Path(__file__).parent.resolve().joinpath("images","ui")
style1={
    "font" : bold18,
    "text_color": "#444",
}

style2 = {
    "font" : bold16,
    "text_color": "#666",
}
placeholder_font ={
    "font" : italic16,
    "text_color": "#999",
    "width": 400,
    "border_color": bordercolor,
    "corner_radius": 0

}


class WorkDir(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        label = customtkinter.CTkLabel(self, text='Work Directory:',**style1)
        self.work_dir = customtkinter.CTkEntry(self, **placeholder_font,placeholder_text="work directory of dio result" )
        img_dir = customtkinter.CTkImage(Image.open(ui_images_path.joinpath("folder.png")), size = (30,30))
        file_button = customtkinter.CTkButton(self, text = "", image=img_dir, command=self.open_directory, width = 40, fg_color = "transparent")
        label.grid(row=0, column=0,sticky="w",pady = 10)
        self.work_dir.grid(row=0, column=1,padx=10)
        file_button.grid(row=0, column=2)
    def open_directory(self):
        directory_path = customtkinter.filedialog.askdirectory(
            title="Select Output Directory"
        )
        if directory_path:
            try:
                self.work_dir.delete(0, "end")
                self.work_dir.insert(0, directory_path) 
                self.work_dir.configure(font= italic16,text_color='black')
            except Exception as e:
                print(f"Error opening directory: {e}")


class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master,fg_color='transparent')
        self.values = values
        self.checkboxes = []
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value, **style2)
            checkbox.grid(row=0, column=i, padx=10, sticky="w")
            self.checkboxes.append(checkbox)
    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class DisPlay(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        # items 
        self.items = MyCheckboxFrame(self, values=["Energy", "value 2", "value 3"])
        self.items.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        # button
        self.plot_button = customtkinter.CTkButton(self, text="Plot",command=self.plot_figure,width=80,height=50, font=bold18)
        self.plot_button.grid(row=0, column=1, padx=10, pady=(10, 0),sticky="w")
    
    def check_work_dir(self):
        def flash_border(widget):
            original_color = bordercolor
            flash_color = "red"
            def toggle_color(count=4):
                nonlocal flash_color
                if count > 0:
                    current_color = widget.cget("border_color")
                    next_color = flash_color if current_color == original_color else original_color
                    widget.configure(border_color=next_color)
                    widget.after(300, toggle_color, count - 1)

            toggle_color()
        work_dir_widget = self.parent.workdir.work_dir
        work_dir = work_dir_widget.get()
        if not os.path.exists(os.path.join(work_dir, "output")):
            flash_border(work_dir_widget)
            work_dir = ''
        return work_dir
    
    def plot_figure(self):
        # check work_dir
        checked_dir = self.check_work_dir()
        if checked_dir == '': 
            return
        else:
            self.work_dir = checked_dir
        # Create a directory to store figures if not exist
        self.figure_dir = os.path.join(self.work_dir,'figures')
        if not os.path.exists(self.figure_dir):
            os.makedirs(self.figure_dir)
        # plot items
        selected_items = self.items.get()
        row_index = 1
        if("Energy" in selected_items):
            show_data =self.plot_energy()
            self.energy = customtkinter.CTkLabel(self, **show_data)
            self.energy.grid(row=row_index, column=0, columnspan=2)
            row_index += 1

    def plot_energy(self):
        dio_dat_path = os.path.join(self.work_dir,"input/dio.dat")
        expection_path = os.path.join(self.work_dir,"output/Expectation.out")
        df = pd.read_csv(expection_path, sep=r'\s+')
        # plot case
        with open(dio_dat_path, 'r') as file:
            for line in file:
                if 'icstr' in line:
                    constraint_type = int(line.split()[2])
        if(constraint_type==0):
            return {
                "text": f"Energy: {df['Etot']}",
                "font": bold18,
                "text_color": "#444",
            }
        elif(constraint_type==1):
            beta2 = df['beta2']
            Energy = df['Etot']
            with plt.style.context(['science', 'ieee', 'notebook']):
                plt.figure(figsize=(12, 9))
                plt.plot(beta2, Energy)
                plt.xlabel(r'$\beta_2$',fontsize=18)
                plt.ylabel('Energy (MeV)',fontsize=18)
            figure_path = os.path.join(self.figure_dir,'Energy.png')
            plt.savefig(figure_path, dpi=100)
            img = Image.open(figure_path)
            img_tk = customtkinter.CTkImage(img,size = (400,300))
            return {
                "text":'',
                "image": img_tk
            }
        elif(constraint_type==2):
            levels = np.linspace(min(df['Etot']),max(df['Etot']),20)
            # Create a meshgrid for contour plot
            beta2 = df['beta2'].unique()
            beta3 = df['beta3'].unique()
            X, Y = np.meshgrid(beta2, beta3)
            Z = np.array(df.pivot_table(index='beta3', columns='beta2', values='Etot').values)
            with plt.style.context(['science', 'ieee', 'notebook']):
                # Plotting
                plt.figure(figsize=(12, 9))
                plt.contour(X, Y, Z, levels=levels,colors='black', linestyles='solid')
                plt.gca().tick_params(axis='both', which='minor', length=0) 
                plt.contourf(X, Y, Z, levels=levels, cmap='rainbow',vim=min(levels),vmax=max(levels))
                cbar = plt.colorbar()
                cbar.set_label('MeV',fontsize=18)
                cbar.ax.tick_params(which='both', length=0)
                cbar.ax.tick_params(which='minor', length=0)
                # plt.text(0.15,0.47,r'$^{164}$Dy',fontsize=18,bbox=dict(facecolor='white', alpha=1))
                plt.xlabel(r'$\beta_2$',fontsize=18)
                plt.ylabel(r'$\beta_3$',fontsize=18)
                # store
            figure_path = os.path.join(self.figure_dir,'Energy.png')
            plt.savefig(figure_path, dpi=100)
            img = Image.open(figure_path)
            img_tk = customtkinter.CTkImage(img,size = (400,300))
            return {
                "text":'',
                "image": img_tk
            }

class Plot(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.workdir = WorkDir(self, fg_color="transparent")
        self.workdir.grid(row=0, column=0)
        self.display = DisPlay(self, fg_color= "transparent")
        self.display.grid(row=2, column=0, sticky="nsew")
        
