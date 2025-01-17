import customtkinter
import json
from modules.style import *
from functools import partial
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from PIL import Image
import io
import periodictable
import pathlib

ui_images_path = pathlib.Path(__file__).parent.resolve().joinpath("images","ui")
pady_section = 20
pady_section_title = 5
padx_section_title = 5
padx_right_to_scroll = 10


padx_left = 20
padx_right = 30
pady_widget = 10


section_title_style = {
    "font" : bold18,
    "text_color": "#333",
}

label_style={
    "font" : bold18,
    "text_color": "#444",
}

sublabel_style={
    "font" : bold18,
    "text_color": "#666",
}
entry_style ={
    "font" : bold16,
    "text_color": "#555",
    "width": 116,
    "border_color": bordercolor

}
hint_style ={
    "font" : italic14,
    "text_color": "#666",
}


global_n0f_variable = None
def on_focus_in(event,master):
    master.configure(border_color="#ADD8E6")

def on_focus_out(event,master):
    master.configure(border_color=bordercolor)

def focus_inout(widgetList):
    for widget in widgetList:
        widget.bind("<FocusIn>", partial(on_focus_in, master=widget))
        widget.bind("<FocusOut>",partial(on_focus_out,master=widget))

def render_latex_to_image(latex_formula, fontsize=20, length=10):
    fig = Figure(figsize=(length,1), dpi=400,facecolor='none')
    ax = fig.add_subplot(111,facecolor='none')
    ax.text(0.5, 0.5, latex_formula, fontsize=60, ha='center', va='center', usetex=True)
    ax.axis('off')
    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    buf.seek(0)
    image = Image.open(buf)
    return customtkinter.CTkImage(image,size=(fontsize*length,fontsize))

def get_proton_number(element_symbol):
    try:
        element = periodictable.elements.symbol(element_symbol)
        return element.number
    except KeyError:
        return None

class Nuclear(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent,**kwargs)
        index = 0
        self.grid_columnconfigure(0, weight=1)
        label = customtkinter.CTkLabel(self, text='Nuclear Name:', **label_style)
        self.nuclear_name = customtkinter.CTkEntry(self, **entry_style)
        label.grid(row=index, column=0, padx = (padx_left,0), pady = (pady_widget,pady_widget/2),sticky="w")
        self.nuclear_name.grid(row=index, column=3,sticky="e",padx=(0,padx_right))
        
        index +=1
        label = customtkinter.CTkLabel(self, text='Mass Number:',**label_style)
        self.nuclear_mass_number = customtkinter.CTkEntry(self, **entry_style)
        label.grid(row=index, column=0, padx = (padx_left,0), pady = (pady_widget/2,pady_widget),sticky="w")
        self.nuclear_mass_number.grid(row=index, column=3,sticky="e",padx=(0,padx_right))
        
        focus_inout([self.nuclear_name, self.nuclear_mass_number])
        self.nuclear_name.bind("<Leave>", command=self.set_Z)
        self.nuclear_mass_number.bind("<Leave>", command=self.set_according_to_nuclear_mass_number)
        
        index +=1
        hline = customtkinter.CTkFrame(self, height=2, fg_color=bordercolor)
        hline.grid(row=index, column=0, columnspan=4, sticky="ew", padx=20)
        
        index+=1
        label = customtkinter.CTkLabel(self, text="Block Type", **label_style)
        self.block_type = customtkinter.IntVar(value=0)
        radiobutton1 = customtkinter.CTkRadioButton(self, text="No",**entry_style, value=0, variable=self.block_type)
        radiobutton2 = customtkinter.CTkRadioButton(self, text="Given level",**entry_style, value=1, variable=self.block_type)
        radiobutton3 = self.RadioButton_latex(self,text=r"$K^\pi$", value=2,variable=self.block_type,length=1)
        label.grid(row=index, column=0, padx=(padx_left,0), pady=(pady_widget,pady_widget/2), sticky="w")
        radiobutton1.grid(row=index, column=1, padx=(0,padx_right), sticky="w")
        radiobutton2.grid(row=index, column=2, padx=(0,padx_right), sticky="w")
        radiobutton3.grid(row=index, column=3, padx=(0,padx_right), sticky="w")
        
        index+=1
        self.neutron_level_label = customtkinter.CTkLabel(self, text='Blocked energy level (Neutron):',**sublabel_style)
        self.neutron_level = customtkinter.CTkEntry(self, **entry_style)
        self.neutron_level_label.grid(row=index, column=0, padx = (padx_left+20,0), pady = (pady_widget/2,pady_widget),sticky="w")
        self.neutron_level.grid(row=index, column=3,sticky="e",padx=(0,padx_right))
        self.neutron_level.insert(0,"0")
        index+=1
        self.proton_level_label = customtkinter.CTkLabel(self, text='Blocked energy level (Proton):',**sublabel_style)
        self.proton_level = customtkinter.CTkEntry(self, **entry_style)
        self.proton_level_label.grid(row=index, column=0, padx = (padx_left+20,0), pady = (pady_widget/2,pady_widget),sticky="w")
        self.proton_level.grid(row=index, column=3,sticky="e",padx=(0,padx_right))
        self.proton_level.insert(0,"0")
        
        index+=1
        self.neutron_KPi_label = customtkinter.CTkLabel(self, text='Neutron:',**sublabel_style)
        self.neutron_K = self.KSpinbox(self)
        self.neutron_Pi = customtkinter.CTkComboBox(self, values=["+", "-"],
                                                        font = bold18,
                                                        justify="center",
                                                        text_color = '#555',
                                                        width=80,
                                                        border_color=bordercolor,
                                                        height = 35,
                                                        dropdown_font= normal16)
        self.neutron_Pi.set("+")
        self.neutron_KPi_label.grid(row=index, column=0, padx = (padx_left+20,0), pady = (pady_widget/2,pady_widget),sticky="w")
        self.neutron_K.grid(row=index, column=2,sticky="e",padx=(0,padx_right))
        self.neutron_Pi.grid(row=index, column=3,sticky="w",padx=(0,padx_right))
        index+=1
        self.proton_KPi_label = customtkinter.CTkLabel(self, text='Proton:',**sublabel_style)
        self.proton_K = self.KSpinbox(self)
        self.proton_Pi = customtkinter.CTkComboBox(self, values=["+", "-"],
                                                        font = bold20,
                                                        justify="center",
                                                        text_color = '#555',
                                                        width=80,
                                                        border_color=bordercolor,
                                                        height = 35,
                                                        dropdown_font= normal16)
        self.proton_KPi_label.grid(row=index, column=0, padx = (padx_left+20,0), pady = (pady_widget/2,pady_widget),sticky="w")
        self.proton_K.grid(row=index, column=2,sticky="e",padx=(0,padx_right))
        self.proton_Pi.grid(row=index, column=3,sticky="w",padx=(0,padx_right))
        
        
        index+=1
        self.block_method_label = customtkinter.CTkLabel(self, text="Block Method", **label_style)
        self.block_method = customtkinter.IntVar(value=2)
        self.block_method_radiobutton1 = customtkinter.CTkRadioButton(self, text="BC",**entry_style, value=1, variable=self.block_method)
        self.block_method_radiobutton2 = customtkinter.CTkRadioButton(self, text="CB",**entry_style, value=2, variable=self.block_method)
        self.block_method_radiobutton3 = customtkinter.CTkRadioButton(self, text="CBC",**entry_style, value=3, variable=self.block_method)
        self.block_method_label.grid(row=index, column=0, padx=(padx_left,0), pady=(pady_widget,pady_widget/2), sticky="w")
        self.block_method_radiobutton1.grid(row=index, column=1, padx=(0,0), sticky="w")
        self.block_method_radiobutton2.grid(row=index, column=2, padx=(0,padx_right), sticky="w")
        self.block_method_radiobutton3.grid(row=index, column=3, padx=(0,padx_right), sticky="w")
        
        self.update_block_visibility()
        self.block_type.trace_add("write", lambda *args: self.update_block_visibility())
        
    def set_Z(self,event):
        self.Z = get_proton_number(event.widget.get())

    def set_according_to_nuclear_mass_number(self,event):
        self.A = int(event.widget.get() or '0')
        # set N0f
        A = self.A
        if(A>0 and A<50):
            global_n0f_variable.set(8)
        elif(A>=50 and A<100):
            global_n0f_variable.set(10)
        elif(A>=100):
            global_n0f_variable.set(12)
        
        # set block action
        self.N = self.A -self.Z
        if (self.N%2==1 or self.Z%2==1):
            self.block_type.set(2)
        else:
            self.block_type.set(0)

    def RadioButton_latex(self,master, value,text,variable,fontsize=20,length=10):
        frame = customtkinter.CTkFrame(master,fg_color="transparent")
        radiobutton = customtkinter.CTkRadioButton(frame, text="", value=value, variable=variable,width=20)
        latex_text = customtkinter.CTkLabel(frame,text="",image=render_latex_to_image(text,fontsize=fontsize,length=length))
        radiobutton.grid(row=0, column=0,padx=0)
        latex_text.grid(row=0, column=1,padx=0)
        return frame

    class KSpinbox(customtkinter.CTkFrame):
        def __init__(self, *args,
                    width: int = 100,
                    height: int = 26,
                    **kwargs):
            super().__init__(*args, width=width, height=height, **kwargs,border_width=2,border_color=bordercolor)
            self.configure(fg_color=("#fff", "gray28"))  # set frame color
            self.grid_columnconfigure(1, weight=1)  # entry expands
            
            self.K = customtkinter.IntVar(value=0)
            self.K_text=customtkinter.StringVar(value="-/-")
            
            left_png = customtkinter.CTkImage(Image.open(ui_images_path.joinpath("left.png")), size = (10,20))
            self.subtract_button = customtkinter.CTkButton(self, text="",image=left_png, width=10, height=20,
                                                        command=self.subtract_button_callback,fg_color="transparent")
            self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
           
            self.label = customtkinter.CTkLabel(self, textvariable=self.K_text, width=40, height=20
                                                ,fg_color="white",font=bold16, text_color="#555")
            self.label.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
            
            right_png = customtkinter.CTkImage(Image.open(ui_images_path.joinpath("right.png")), size = (10,20))
            self.add_button = customtkinter.CTkButton(self, text="", image=right_png, width=20, height=20,
                                                    command=self.add_button_callback,fg_color="transparent")
            self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        def add_button_callback(self):
            try:
                value = int(self.K.get()) + 1
                self.K_text.set(f"{value*2-1}/2")
                self.K.set(value)
            except ValueError:
                return

        def subtract_button_callback(self):
            try:
                value = int(self.K.get()) - 1
                if(value > 0):
                    self.K_text.set(f"{value*2-1}/2")
                    self.K.set(value)
            except ValueError:
                return

        def get(self):
            try:
                return int(self.K.get())
            except ValueError:
                return None
        
        
    def update_block_visibility(self):
        value = self.block_type.get()
        if value == 0:  # no block
            self.neutron_level_label.grid_remove()
            self.neutron_level.grid_remove()
            self.proton_level_label.grid_remove()
            self.proton_level.grid_remove()
            self.neutron_KPi_label.grid_remove()
            self.neutron_K.grid_remove()
            self.neutron_Pi.grid_remove()
            self.proton_KPi_label.grid_remove()
            self.proton_K.grid_remove()
            self.proton_Pi.grid_remove()
            self.block_method_label.grid_remove()
            self.block_method_radiobutton1.grid_remove()
            self.block_method_radiobutton2.grid_remove()
            self.block_method_radiobutton3.grid_remove()
            
            
        elif  value==1:
            if(self.N %2==1):
                self.neutron_level_label.grid()
                self.neutron_level.grid()
            if(self.Z %2==1):
                self.proton_level_label.grid()
                self.proton_level.grid()
            self.neutron_KPi_label.grid_remove()
            self.neutron_K.grid_remove()
            self.neutron_Pi.grid_remove()
            self.proton_KPi_label.grid_remove()
            self.proton_K.grid_remove()
            self.proton_Pi.grid_remove()
            self.block_method_label.grid()
            self.block_method_radiobutton1.grid()
            self.block_method_radiobutton2.grid()
            self.block_method_radiobutton3.grid()
        elif  value==2:
            self.neutron_level_label.grid_remove()
            self.neutron_level.grid_remove()
            self.proton_level_label.grid_remove()
            self.proton_level.grid_remove()
            if(self.N %2==1):
                self.neutron_KPi_label.grid()
                self.neutron_K.grid()
                self.neutron_Pi.grid()
            if(self.Z %2==1):
                self.proton_KPi_label.grid()
                self.proton_K.grid()
                self.proton_Pi.grid()
            self.block_method_label.grid()
            self.block_method_radiobutton1.grid_remove()
            self.block_method_radiobutton2.grid()
            self.block_method_radiobutton3.grid()
class Force(customtkinter.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_columnconfigure(0, weight=1)
        label = customtkinter.CTkLabel(self, text='Force Set:',**label_style)
        hint  = customtkinter.CTkLabel(self, text='Only support Point-Coupling parameter sets now.', **hint_style)
        self.force_option = customtkinter.CTkComboBox(self, values=["PC-PK1", "PC-F1"],
                                                        **entry_style,
                                                        height = 35,
                                                        dropdown_font= normal16,
                                                        command=self.force_option_callback)
        self.force_option.set("PC-PK1")
        label.grid(row=0, column=0, padx = (padx_left,0), pady=(pady_widget,0),sticky="w")
        hint.grid(row=1, column=0, padx = (padx_left,0), pady=(0,pady_widget/2),sticky="w")
        self.force_option.grid(row=0, column=2, rowspan=2, sticky="e",padx=(0,padx_right))
        
        label = customtkinter.CTkLabel(self, text='V0:', **label_style)
        hint  = customtkinter.CTkLabel(self, text='pairing strength for delta pairing',**hint_style)
        self.V0_neutron = customtkinter.DoubleVar(value=349.500)
        self.V0_proton = customtkinter.DoubleVar(value=330.000)
        V0_neutron = customtkinter.CTkEntry(self,**entry_style,textvariable=self.V0_neutron)
        V0_proton = customtkinter.CTkEntry(self,**entry_style,textvariable=self.V0_proton)
        label.grid(row=2, column=0, padx=(padx_left,0), pady=(pady_widget/2,0), sticky="w")
        hint.grid(row=3, column=0, padx =(padx_left,0), pady=(0,pady_widget),sticky="w")
        V0_neutron.grid(row=2, column=1,rowspan=2, padx=(0,10),sticky="e")
        V0_proton.grid(row=2, column=2,rowspan=2, padx=(0,padx_right),sticky="e")
        focus_inout([self.force_option,V0_neutron,V0_proton])
    def force_option_callback(self,choice):
        if(choice=="PC-PK1"):
            self.V0_neutron.set(349.500)
            self.V0_proton.set(330.000)
        elif(choice=="PC-F1"):
            self.V0_neutron.set(308.000)
            self.V0_proton.set(321.000)        
        
class Basis_config(customtkinter.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        global global_n0f_variable
        self.grid_columnconfigure(0, weight=1)
        label = customtkinter.CTkLabel(self, text='Nf:',**label_style)
        hint  = customtkinter.CTkLabel(self, text='Set to an even number.The larger the value, the more accurate the calculation, but it takes more time.', **hint_style)
        self.n0f = customtkinter.IntVar(value=8)
        global_n0f_variable = self.n0f
        n0f = customtkinter.CTkEntry(self,**entry_style,textvariable=self.n0f)
        label.grid(row=0, column=0, padx = (padx_left,0), pady=(pady_widget,0),sticky="w")
        hint.grid(row=1, column=0, padx = (padx_left,0), pady=(0,pady_widget/2),sticky="w")
        n0f.grid(row=0,column=1,rowspan=2,padx=(0,padx_right),sticky="e")
        
        self.b0 = customtkinter.DoubleVar(value=-2.448)
        label = customtkinter.CTkLabel(self, text = "b0:", **label_style)
        hint  = customtkinter.CTkLabel(self, text='The value will be replaced with the empirical formula if it is set to be less than zero.', **hint_style)
        b0 = customtkinter.CTkEntry(self,**entry_style, textvariable=self.b0)
        label.grid(row=2, column=0, padx = (padx_left,0), pady=(pady_widget/2,0),sticky="w")
        hint.grid(row=3, column=0, padx = (padx_left,0), pady=(0,pady_widget/2),sticky="w")
        b0.grid(row=2,column=1,rowspan=2,padx=(0,padx_right),sticky="e")
        
        self.beta0 = customtkinter.DoubleVar(value=0.0)
        label = customtkinter.CTkLabel(self, text = "beta0:", **label_style)
        hint  = customtkinter.CTkLabel(self, text="The difference between the radial and axial harmonic oscillator frequencies increases as the value increases.", **hint_style)
        beta0 = customtkinter.CTkEntry(self,**entry_style,textvariable=self.beta0)
        label.grid(row=4, column=0, padx = (padx_left,0), pady=(pady_widget/2,0),sticky="w")
        hint.grid(row=5, column=0, padx = (padx_left,0), pady=(0,pady_widget),sticky="w")
        beta0.grid(row=4,column=1,rowspan=2,padx=(0,padx_right),sticky="e")
        focus_inout([n0f, b0, beta0])

class Initial_Potential(customtkinter.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_columnconfigure(0, weight=1)
        label = customtkinter.CTkLabel(self, text='Init:', **label_style)
        hint  = customtkinter.CTkLabel(self, text='Choose the input potential field for the initial iteration.', **hint_style)
        self.inin = customtkinter.IntVar(value=1)
        radiobutton1 = customtkinter.CTkRadioButton(self, text="Woods–Saxon", value=1, **entry_style, variable=self.inin)
        radiobutton2 = customtkinter.CTkRadioButton(self, text="Read saved Potential", value=0, **entry_style, variable=self.inin, state="disabled")
        label.grid(row=0, column=0, padx=(padx_left,0), pady=(pady_widget,0), sticky="w")
        hint.grid(row=1, column=0, padx = (padx_left,0), pady=(0,pady_widget/2),sticky="w")
        radiobutton1.grid(row=0, column=1, rowspan=2,padx=(0,10), sticky="e")
        radiobutton2.grid(row=0, column=2, rowspan=2,padx=(0,padx_right), sticky="e")
        
        # Woods-Saxon setting
        label = customtkinter.CTkLabel(self, text = "beta2:", **label_style)
        hint  = customtkinter.CTkLabel(self, **hint_style,wraplength=460,justify="left",
                                        text='The beta2 for woods-saxon potential. When the nuclear beta2 deformation constraint is set (beta2 or beta2+beta3), this value has no effect and is replaced by the constrained beta2 value. Different deformed Woods-Saxon potentials may lead to convergence at different deformation minima.',)
        self.beta2 = customtkinter.DoubleVar(value=0.5)
        beta2 = customtkinter.CTkEntry(self,**entry_style,textvariable=self.beta2)
        label.grid(row=2, column=0, padx=(padx_left,0), pady=(pady_widget/2,0), sticky="w")
        hint.grid(row=3, column=0, padx = (padx_left,0), pady=(0,pady_widget/2),sticky="w")
        beta2.grid(row=2, column=2, rowspan=2, padx=(0,padx_right), sticky="e")
        
        label = customtkinter.CTkLabel(self, text = "beta3:",  **label_style)
        hint  = customtkinter.CTkLabel(self, **hint_style,wraplength=460,justify="left",
                                        text='The beta3 for woods-saxon potential. When the nuclear beta3 deformation constraint is set (beta2+beta3), this value has no effect and is replaced by the constrained beta3 value. Different deformed Woods-Saxon potentials may lead to convergence at different deformation minima.',)
        self.beta3 = customtkinter.DoubleVar(value=0)
        beta3 = customtkinter.CTkEntry(self,**entry_style,textvariable=self.beta3)
        label.grid(row=4, column=0, padx=(padx_left,0), pady=(pady_widget/2,0), sticky="w")
        hint.grid(row=5, column=0, padx = (padx_left,0), pady=(0,pady_widget),sticky="w")
        beta3.grid(row=4, column=2, rowspan=2, padx=(0,padx_right), sticky="e")
        
class Constraint(customtkinter.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_columnconfigure(0, weight=1)
        label = customtkinter.CTkLabel(self, text='Constraint Type:',**label_style)
        self.icstr = customtkinter.IntVar(value=0)
        radiobutton1 = customtkinter.CTkRadioButton(self, text="no",**entry_style, value=0, variable=self.icstr)
        radiobutton2 = customtkinter.CTkRadioButton(self, text="beta2",**entry_style, value=1, variable=self.icstr)
        radiobutton3 = customtkinter.CTkRadioButton(self, text="beta2+beta3",**entry_style, value=2, variable=self.icstr)
        label.grid(row=0, column=0, padx=(padx_left,0), pady=(pady_widget,pady_widget/2), sticky="w")
        radiobutton1.grid(row=0, column=1, padx=(0,0), sticky="e")
        radiobutton2.grid(row=0, column=2, padx=(0,0), sticky="e")
        radiobutton3.grid(row=0, column=3, padx=(0,padx_right), sticky="e")
        
        # beta2 range
        self.beta2_label = customtkinter.CTkLabel(self, text='beta2:',font=bold16,text_color="#555")
        self.beta2 = self.range_bar(self)
        self.beta2_label.grid(row=1, column=0, padx=(padx_left+86,0), pady=(pady_widget/2,0), sticky="w")
        self.beta2.grid(row=1, column=1, columnspan=3, padx=(0,padx_right), sticky="e")
        # beta3 range
        self.beta3_label = customtkinter.CTkLabel(self, text='beta3:',font=bold16,text_color="#555")
        self.beta3 = self.range_bar(self)
        self.beta3_label.grid(row=2, column=0, padx=(padx_left+86,0), pady=(0,pady_widget/2), sticky="w")
        self.beta3.grid(row=2, column=1, columnspan=3,padx=(0,padx_right), sticky="e")
        # Hide beta2 and beta3 initially
        self.update_beta_visibility()
        # Trace changes in icstr
        self.icstr.trace_add("write", lambda *args: self.update_beta_visibility())
        
        self.cspr = customtkinter.DoubleVar(value=10.00)
        label = customtkinter.CTkLabel(self, text='Spring constant:',**label_style)
        cspr = customtkinter.CTkEntry(self,**entry_style,textvariable=self.cspr)
        label.grid(row=3, column=0, padx=(padx_left,0), pady=(pady_widget,pady_widget/2), sticky="w")
        cspr.grid(row=3, column=3, padx=(0,padx_right), sticky="e")
        
        self.cmax = customtkinter.DoubleVar(value=1.000)
        label = customtkinter.CTkLabel(self, text='cutoff for dE/db:',**label_style)
        cmax = customtkinter.CTkEntry(self,**entry_style,textvariable=self.cmax)
        label.grid(row=4, column=0, padx=(padx_left,0), pady=(pady_widget/2,pady_widget), sticky="w")
        cmax.grid(row=4, column=3, padx=(0,padx_right), sticky="e")

    def range_bar(self,master):
        style1 = {
        "font" : italic16,
        "text_color": "#555",
        }
        style2 ={
        "font" : bold16,
        "text_color": "#555",
        "width": 58,
        "border_color": bordercolor
        }
        frame = customtkinter.CTkFrame(master, fg_color="transparent")
        start_text = customtkinter.CTkLabel(frame, text='Start:',**style1)
        frame.start = customtkinter.CTkEntry(frame,**style2)
        end_text = customtkinter.CTkLabel(frame, text='End:',**style1)
        frame.end = customtkinter.CTkEntry(frame,**style2)
        step_text = customtkinter.CTkLabel(frame, text='Step:',**style1)
        frame.step = customtkinter.CTkEntry(frame,**style2)
        start_text.grid(row=0, column=0, padx=(15,6))
        frame.start.grid(row=0, column=1)
        end_text.grid(row=0, column=2, padx=(15,6))
        frame.end.grid(row=0, column=3)
        step_text.grid(row=0, column=4, padx=(15,6))
        frame.step.grid(row=0, column=5)
        return frame
    def update_beta_visibility(self):
        """Show or hide beta2 and beta3 sections based on icstr."""
        value = self.icstr.get()
        if value == 0:  # no constraint
            self.beta2_label.grid_remove()
            self.beta2.grid_remove()
            self.beta3_label.grid_remove()
            self.beta3.grid_remove()
        elif value == 1:  # beta2 only
            self.beta2_label.grid()
            self.beta2.grid()
            self.beta3_label.grid_remove()
            self.beta3.grid_remove()
        elif value == 2:  # beta2 + beta3
            self.beta2_label.grid()
            self.beta2.grid()
            self.beta3_label.grid()
            self.beta3.grid()
class Iteration_config(customtkinter.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.maxi = customtkinter.IntVar(value=100)
        label = customtkinter.CTkLabel(self, text='Maximal number of Iterations:',**label_style)
        hint  = customtkinter.CTkLabel(self, text= "When the iteration cannot converge, the maximum number of iterations is limited to this value.", **hint_style)
        maxi = customtkinter.CTkEntry(self,**entry_style,textvariable=self.maxi)
        label.grid(row=0, column=0, padx = (padx_left,0), pady=(pady_widget,0),sticky="w")
        hint.grid(row=1, column=0, padx = (padx_left,0), pady=(0,pady_widget/2),sticky="w")
        maxi.grid(row=0, column=1, rowspan=2,padx=(0,padx_right),sticky="e")
        
        self.xmix = customtkinter.DoubleVar(value=0.5)
        label = customtkinter.CTkLabel(self, text='mixing parameter:', **label_style)
        hint  = customtkinter.CTkLabel(self, text='The retention ratio of the field in the current iteration calculation, with a range from 0 to 1. ', **hint_style)
        xmix = customtkinter.CTkEntry(self,**entry_style,textvariable=self.xmix)
        label.grid(row=2, column=0, padx = (padx_left,0), pady=(pady_widget/2,0),sticky="w")
        hint.grid(row=3, column=0, padx = (padx_left,0), pady=(0,pady_widget/2),sticky="w")
        xmix.grid(row=2, column=1, rowspan=2, padx=(0,padx_right),sticky="e")

class OutputOption(customtkinter.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_columnconfigure(0, weight=1)
        label = customtkinter.CTkLabel(self, text='RCE:',**label_style)
        self.Erot_option = customtkinter.CTkComboBox(self, values=["No", "EE: IB", "EE: NP", "OA: F(regulator)"],
                                                        **entry_style,
                                                        height = 35,
                                                        dropdown_font= normal16)
        label.grid(row=0, column=0, padx = (padx_left,0), pady=(pady_widget,pady_widget),sticky="w")
        self.Erot_option.grid(row=0, column=1, padx=(0,padx_right),sticky="e")
        
class Configuration(customtkinter.CTkScrollableFrame):
    def __init__(self,  parent, **kwargs):
        super().__init__(parent,**kwargs)
        row_index = 0
        self.grid_columnconfigure(0, weight=1)
        self.nuclei = Nuclear(self,fg_color="transparent", border_width=2, border_color=bordercolor)
        self.nuclei.grid(row=row_index, column=0, padx =(0,padx_right_to_scroll), pady=(pady_section_title,pady_section),sticky="nsew")
        
        row_index+=1
        label = customtkinter.CTkLabel(self,text="Force Parameter",**section_title_style)
        label.grid(row= row_index, column = 0, padx= (padx_section_title,0), sticky="w")
        row_index+=1
        self.force = Force(self, fg_color="transparent", border_width=2, border_color=bordercolor)
        self.force.grid(row=row_index, column=0, padx =(0,padx_right_to_scroll), pady=(pady_section_title,pady_section),sticky="nsew")

        row_index+=1
        label = customtkinter.CTkLabel(self,text="Basis Set", **section_title_style)
        label.grid(row= row_index, column = 0,padx= (padx_section_title,0), sticky="w")
        row_index+=1
        self.basis = Basis_config(self,fg_color="transparent", border_width=2, border_color=bordercolor)
        self.basis.grid(row=row_index, column=0, padx =(0,padx_right_to_scroll), pady=(pady_section_title,pady_section),sticky='nsew')
        
        row_index+=1
        label = customtkinter.CTkLabel(self,text="Initial Potential", **section_title_style)
        label.grid(row= row_index, column = 0,padx= (padx_section_title,0), sticky="w")
        row_index+=1
        self.initPot = Initial_Potential(self,fg_color="transparent", border_width=2, border_color=bordercolor)
        self.initPot.grid(row=row_index, column=0, padx =(0,padx_right_to_scroll), pady=(pady_section_title,pady_section),sticky='nsew')

        row_index+=1
        label = customtkinter.CTkLabel(self,text="Nuclear deformation constraint", **section_title_style)
        label.grid(row= row_index, column = 0, padx= (padx_section_title,0),sticky="w")
        row_index+=1
        self.constraint = Constraint(self,fg_color="transparent", border_width=2, border_color=bordercolor)
        self.constraint.grid(row=row_index, column=0, padx =(0,padx_right_to_scroll), pady=(pady_section_title,pady_section),sticky='nsew')

        row_index+=1
        label = customtkinter.CTkLabel(self,text="Iteration Setting", **section_title_style)
        label.grid(row= row_index, column = 0, padx= (padx_section_title,0),sticky="w")
        row_index+=1
        self.interation = Iteration_config(self,fg_color="transparent", border_width=2, border_color=bordercolor)
        self.interation.grid(row=row_index, column=0, padx =(0,padx_right_to_scroll), pady=(pady_section_title,pady_section),sticky='nsew')
        
        row_index+=1
        label = customtkinter.CTkLabel(self,text="Output Setting", **section_title_style)
        label.grid(row= row_index, column = 0, padx= (padx_section_title,0),sticky="w")
        row_index+=1
        self.output = OutputOption(self,fg_color="transparent", border_width=2, border_color=bordercolor)
        self.output.grid(row=row_index, column=0, padx =(0,padx_right_to_scroll), pady=(pady_section_title,pady_section),sticky='nsew')

        row_index+=1
        self.runButton = customtkinter.CTkButton(self, text="Save",font=bold18, command = self.save_configuration)
        self.runButton.grid(row= row_index, column = 0, pady=(pady_section,pady_section))
    
    def save_configuration(self):
        if len(self.nuclei.nuclear_name.get()) == 1:
            nuclear_name = "_"+self.nuclei.nuclear_name.get()
        else:
            nuclear_name = self.nuclei.nuclear_name.get()
        #
        if self.nuclei.neutron_Pi.get() =="+":
            neutron_Pi = 1
        else:
            neutron_Pi = -1
        if self.nuclei.proton_Pi.get() =="+":
            proton_Pi = 1
        else:
            proton_Pi = -1
        # 
        if self.output.Erot_option.get() == "EE: IB":
            Erot_option = 1
        elif self.output.Erot_option.get() == "EE: NP":
            Erot_option = 2
        elif self.output.Erot_option.get() == "OA: F(regulator)":
            Erot_option = 3
        else :
            Erot_option = 0
            
        configuration_data = {
            "nuclear_name" : nuclear_name,
            "nuclear_mass_number" : self.nuclei.nuclear_mass_number.get(),
            "block_type": self.nuclei.block_type.get(),
            "neutron_level":self.nuclei.neutron_level.get(),
            "proton_level":self.nuclei.proton_level.get(),
            "neutron_K": self.nuclei.neutron_K.get(),
            "neutron_Pi": neutron_Pi,
            "proton_K": self.nuclei.proton_K.get(),
            "proton_Pi": proton_Pi,
            "block_method":self.nuclei.block_method.get(),
            "force_option" : self.force.force_option.get(),
            "V0" : [self.force.V0_neutron.get(), self.force.V0_proton.get()],
            "n0f" : self.basis.n0f.get(),
            "b0" : self.basis.b0.get(),
            "beta0" : self.basis.beta0.get(),
            "inin" : self.initPot.inin.get(),
            "beta2_ws" : self.initPot.beta2.get(),
            "beta3_ws" : self.initPot.beta3.get(),
            "maxi" : self.interation.maxi.get(),
            "xmix" : self.interation.xmix.get(),
            "icstr" : self.constraint.icstr.get(),
            "cspr" : self.constraint.cspr.get(),
            "cmax" : self.constraint.cmax.get(),
            "Erot" : Erot_option,
            "beta2":{
                "start": self.constraint.beta2.start.get(),
                "end": self.constraint.beta2.end.get(),
                "step": self.constraint.beta2.step.get()
            },
            "beta3":{
                "start": self.constraint.beta3.start.get(),
                "end": self.constraint.beta3.end.get(),
                "step": self.constraint.beta3.step.get()
            }
        }
        file_path = customtkinter.filedialog.asksaveasfilename(
            initialfile=f"{configuration_data["nuclear_name"]}{configuration_data["nuclear_mass_number"]}.json",
            defaultextension=".json",
            filetypes=[("Text files", "*.json"), ("All files", "*.*")],
            title="Save File As" 
        )
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(configuration_data, file, indent=4)
            except Exception as e:
                print(f"Error saving file: {e}")
