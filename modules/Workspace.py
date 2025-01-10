import customtkinter
import pathlib
import json
from PIL import Image
import os
import subprocess
import threading
from tkinter import messagebox
from modules.style import *
import numpy as np
import sys 
from datetime import datetime
ui_images_path = pathlib.Path(__file__).parent.resolve().joinpath("images","ui")

style1={
    "font" : bold18,
    "text_color": "#444",
}
placeholder_font ={
    "font" : italic16,
    "text_color": "#999",
    "width": 400,
    "border_color": bordercolor,
    "corner_radius": 0

}

stdout_style = {
    "font": Cambria16
}

constraint_type = 0

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file) 
            return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
        
class Configurator_select_Run(customtkinter.CTkFrame):
    def __init__(self,  parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.parent = parent
        self.grid_columnconfigure(1, weight=1)
        label = customtkinter.CTkLabel(self, text='DIO exe:',**style1)
        self.dio_path = customtkinter.CTkEntry(self, **placeholder_font,placeholder_text="dio.exe path")
        img_file = customtkinter.CTkImage(Image.open(ui_images_path.joinpath("exe.png")), size = (35,35))
        file_button = customtkinter.CTkButton(self, text = "", image=img_file, command=self.open_exe, width = 40, fg_color = "transparent")
        label.grid(row=0, column=0,sticky="w",pady = 10)
        self.dio_path.grid(row=0, column=1,padx=10)
        file_button.grid(row=0, column=2)
        
        label = customtkinter.CTkLabel(self, text='Configuration File:',**style1)
        self.configuration_path = customtkinter.CTkEntry(self, **placeholder_font,placeholder_text="configuration json file")
        img_file = customtkinter.CTkImage(Image.open(ui_images_path.joinpath("configure_setting.png")), size = (30,30))
        file_button = customtkinter.CTkButton(self, text = "", image=img_file, command=self.open_configuration, width = 40, fg_color = "transparent")
        label.grid(row=1, column=0,sticky="w",pady = 10)
        self.configuration_path.grid(row=1, column=1,padx=10)
        file_button.grid(row=1, column=2)

        label = customtkinter.CTkLabel(self, text='Output Directory:',**style1)
        self.work_dir = customtkinter.CTkEntry(self, **placeholder_font,placeholder_text="Path to store running results" )
        img_dir = customtkinter.CTkImage(Image.open(ui_images_path.joinpath("folder.png")), size = (30,30))
        file_button = customtkinter.CTkButton(self, text = "", image=img_dir, command=self.open_directory, width = 40, fg_color = "transparent")
        label.grid(row=2, column=0,sticky="w",pady = 10)
        self.work_dir.grid(row=2, column=1,padx=10)
        file_button.grid(row=2, column=2)
        
        
        img_run = customtkinter.CTkImage(Image.open(ui_images_path.joinpath("run_solid_white.png")), size = (30,30))
        self.run_button = customtkinter.CTkButton(self, text='Run', image=img_run, command = self.run, width =100, height=60, font= bold18, text_color="#fff")
        self.run_button.grid(row=0, column=3, rowspan=2, padx=(30,10))
    
    def open_exe(self):
        file_path = customtkinter.filedialog.askopenfilename(
            defaultextension=".exe",
            filetypes=[("Text files", "*.exe"), ("All files", "*.*")],
            title="Open File" 
        )
        if file_path:
            try:
                self.dio_path.delete(0, "end")
                self.dio_path.insert(0, file_path) 
                self.dio_path.configure(font= italic16,text_color='black')
                
            except Exception as e:
                print(f"Error opening file: {e}")
    def open_configuration(self):
        file_path = customtkinter.filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("Text files", "*.json"), ("All files", "*.*")],
            title="Open File" 
        )
        if file_path:
            try:
                self.configuration_path.delete(0, "end")
                self.configuration_path.insert(0, file_path) 
                self.configuration_path.configure(font= italic16,text_color='black')
                
            except Exception as e:
                print(f"Error opening file: {e}")

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

    def generate_dio_dat(self):
        configuration_data = read_json(self.configuration_path.get())
        work_dir = self.work_dir.get()
        work_dir_input = os.path.join(work_dir, "input")
        if not os.path.exists(work_dir_input):
            os.makedirs(work_dir_input)
        with open(os.path.join(work_dir_input,'dio.dat'), "w") as f:
            f.write(f"n0f,n0b  = {int(configuration_data["n0f"]):02}  8\n")
            f.write(f"b0       = {configuration_data["b0"]}\n")
            f.write(f"beta0    =  {configuration_data['beta0']}\n")
            f.write(f"betas    =  {configuration_data['beta2_ws']}\n")
            f.write(f"bet3s    =  {configuration_data['beta3_ws']}\n")
            f.write(f"maxi     =  {configuration_data['maxi']}\n")
            f.write(f"xmix     =  {configuration_data['xmix']}\n")
            f.write(f"inin     =  {configuration_data['inin']}\n")
            f.write(f"{configuration_data["nuclear_name"]}  {configuration_data["nuclear_mass_number"]}\n")
            f.write( "Ide      =  4  4  \n")
            f.write( "Delta    =  0.000000  0.000000 \n")
            f.write( "Ga       =  0.000000  0.000000 \n")
            f.write( "Delta-0  =  2.000000  2.000000\n")
            f.write(f"Vpair    =  {configuration_data["V0"][0]}   {configuration_data["V0"][1]}\n")
            f.write(f"Force    =  {configuration_data["force_option"]}\n")
            global constraint_type
            constraint_type = int(configuration_data["icstr"])
            f.write(f"icstr    =  {configuration_data["icstr"]}\n")
            f.write(f"cspr     =  {configuration_data["cspr"]}\n")
            f.write(f"cmax     =  {configuration_data["cmax"]}\n")
            f.write( "iRHB     =  0\n")
            f.write(f"iBlock   =  {configuration_data["block_type"]}\n")
            f.write(f"bln      =  {configuration_data["neutron_level"]}\n")
            f.write(f"blp      =  {configuration_data["proton_level"]}\n")
            f.write(f"Kn       =  {configuration_data["neutron_K"]}\n")
            f.write(f"Pin      =  {configuration_data["neutron_Pi"]}\n")
            f.write(f"Kp       =  {configuration_data["proton_K"]}\n")
            f.write(f"Pip      =  {configuration_data["proton_Pi"]}\n")
            f.write(f"bMethod  =  {configuration_data["block_method"]}\n")
            f.write(f"Erot     =  {configuration_data["Erot"]}\n")

    def generate_b23_dat(self):
        configuration_data = read_json(self.configuration_path.get())
        work_dir = self.work_dir.get()
        work_dir_input = os.path.join(work_dir, "input")
        if not os.path.exists(work_dir_input):
            os.makedirs(work_dir_input)
        with open(os.path.join(work_dir_input,'b23.dat'), "w") as f:
            beta2_range_start = float(configuration_data["beta2"]["start"] or 0)
            beta2_range_step = float(configuration_data["beta2"]["step"] or 0.1)
            beta2_range_end = float(configuration_data["beta2"]["end"] or 0) + beta2_range_step
            beta3_range_start = float(configuration_data["beta3"]["start"] or 0)
            beta3_range_step = float(configuration_data["beta3"]["step"] or 0.1)
            beta3_range_end = float(configuration_data["beta3"]["end"] or 0) + beta3_range_step
            for beta2 in np.arange(beta2_range_start, beta2_range_end, beta2_range_step):
                for beta3 in np.arange(beta3_range_start, beta3_range_end, beta3_range_step):
                    f.write(f"{beta2:.2f}   {beta3:.2f}  0.00\n")
    
    def check_path_empty(self):
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
        state = 1
        if (self.dio_path.get()==""):
            # self.configuration_path.configure(border_color="red")
            flash_border(self.dio_path)
            state = 0
        else:
            self.dio_path.configure(border_color=bordercolor)
        if (self.configuration_path.get()==""):
            # self.configuration_path.configure(border_color="red")
            flash_border(self.configuration_path)
            state = 0
        else:
            self.configuration_path.configure(border_color=bordercolor)
        if (self.work_dir.get()==""):
            # self.work_dir.configure(border_color="red")
            flash_border(self.work_dir)
            state = 0
        else:
            self.configuration_path.configure(border_color=bordercolor)
        return state
    
    def run_exe(self):
        def target():
            # run environment
            work_dir = self.work_dir.get()
            try:
                exe_path = self.dio_path.get() # os.path.join(work_dir,"dio.exe")
                process = subprocess.Popen([exe_path], 
                                        cwd = work_dir,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
                for stdout_line in iter(process.stdout.readline, ""):
                    global constraint_type
                    if (constraint_type == 2):
                        print(stdout_line, end='')
                    elif (constraint_type == 1):
                        if("Constraint" in  stdout_line):
                            print(stdout_line[:-15], end='')
                        else:
                            print(stdout_line, end='')
                    elif (constraint_type == 0):
                        if("Constraint" in  stdout_line):
                            print("Unconstraint",end='')
                        else:
                            print(stdout_line, end='')
                    if("Constraint" in stdout_line):
                        data = stdout_line.split()[1].split('/')
                        count = int(data[0])
                        total = int(data[1])
                        self.parent.Show_running_progress.progress_bar.bar.set(count/total)
                        self.parent.Show_running_progress.progress_bar.count.configure(text=f"{count}/{total}")
                for stderr_line in iter(process.stderr.readline, ""):
                    print(stderr_line, end='', file=sys.stderr)
                process.stdout.close()
                process.stderr.close()
                process.wait()
            except Exception as e:
                print(f"Error run dio.exe file: {e}")
                self.run_button.configure(state="standard",fg_color=run_button_original_color)
                return None
            # messagebox.showinfo("Notice", "Code Finish!")
            self.run_button.configure(state="standard",fg_color=run_button_original_color)
        run_button_original_color = self.run_button.cget("fg_color")
        self.run_button.configure(state="disabled",fg_color="grey")
        threading.Thread(target=target).start()       

    def run(self):
        if self.check_path_empty()==0: return
        # generate dio.dat 
        self.generate_dio_dat()
        # generate b23.dat
        self.generate_b23_dat()
        # mkdir output directory
        work_dir_output = os.path.join(self.work_dir.get(), "output")
        if not os.path.exists(work_dir_output):
            os.makedirs(work_dir_output)
        # run
        self.run_exe()

class Show_running_progress(customtkinter.CTkFrame):
    def __init__(self, parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.progress_bar = self.set_progress_bar(self)
        self.progress_bar.grid(row=0, column=1)

    def set_progress_bar(self,parent):
        progress_bar = customtkinter.CTkFrame(parent,fg_color="transparent")
        progress_bar.grid_columnconfigure(0, weight=1)
        progress_bar.bar = customtkinter.CTkProgressBar(progress_bar, width=600, height=16)
        progress_bar.bar.set(0)
        progress_bar.bar.grid(row=0, column=0, sticky='ew')
        progress_bar.count = customtkinter.CTkLabel(progress_bar, text=f"-/-", font=bold16)
        progress_bar.count.grid(row=0,column=1,padx=10)
        return progress_bar

class StdoutRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, message):
        message = message.rstrip()
        if message.strip():
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  # 格式化时间
            formatted_message = f"{timestamp} {message}\n"
            self.textbox.insert("end", formatted_message)
            self.textbox.see("end") 

    def flush(self):
        pass
    
class Show_running_stdout(customtkinter.CTkFrame):
    def __init__(self, parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_columnconfigure(0, weight=1)
        output_textbox = customtkinter.CTkTextbox(self, width = 900, height=300,**stdout_style)
        sys.stdout = StdoutRedirector(output_textbox)
        sys.stderr = StdoutRedirector(output_textbox)
        output_textbox.grid(row=0, column=0)

class Workspace(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.configurator_select_run =  Configurator_select_Run(self, fg_color="transparent")
        self.configurator_select_run.grid(row=0, column=0)
        self.Show_running_progress =  Show_running_progress(self, fg_color="transparent")
        self.Show_running_progress.grid(row=1, column=0, pady=10)
        self.Show_running_stdout =  Show_running_stdout(self, fg_color="transparent")
        self.Show_running_stdout.grid(row=2, column=0)


