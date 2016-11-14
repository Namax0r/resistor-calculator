# TODO:
# - Remake the dictionary to allow selecting key by simple color names (get rid of _multiplier, _tolerance) -- DONE
# - Fix the formula to account for changes done to dictionary. -- DONE
# - Fix the positioning of the widgets inside a window -- PARTLY DONE
# - Fix overwriting of self.band3_var_result when any of the other combo boxes are selected
# More to be added when problems and ideas arise.


# basic version handling
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

from tkinter.ttk import Combobox

root = tk.Tk()
root.minsize(300,300)
#root.maxsize(550,310)
# var is used to store our result
var_result = tk.StringVar()
var_max = tk.StringVar()
var_min = tk.StringVar()

#small utility that adds dot.notation access to dictionary attributes
class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

#create dictionary of colors and values
d = {
    #values of the band are stored as string to allow concantation of the numbers.
    'band':{
        'black': "0", 'brown': "1", 'red': "2", 'orange': "3",
        'yellow': "4", 'green': "5", 'blue': "6", 'violet': "7",
        'gray': "8", 'white': "9"
        },
    'multiplier':{ 
        'black': 1, 'brown': 10, 'red': 100, 'orange': 1000,
        'yellow': 10000, 'green': 100000, 'blue': 1000000,
        'violet': 10000000
        },
    'tolerance':{
        'brown': 0.01, 'red': 0.02, 'green': 0.005, 'blue': 0.025,
        'violet': 0.010, 'gray': 0.005, 'gold': 0.05, 'silver': 0.10
        }  
    }

#enable dot notation on the dictionary
d = dotdict(d)

class ResistorCalculator:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.close_program)
        #define variables to store values of comboboxes 
        self.band1_var_result = 0
        self.band2_var_result = 0
        self.band3_var_result = 0
        self.multiplier_var_result = 0
        self.tolerance_var_result = 0

        self.build_window()
    def combobox_handler(self, event): #function called when '<<ComboboxSelected>>' event is triggered
        #store values of comboboxes in variables.
        self.band1_var_result = self.band1_var.get()
        self.band2_var_result = self.band2_var.get()
        self.band3_var_result = self.band3_var.get()
        self.multiplier_var_result = self.multiplier_var.get()
        self.tolerance_var_result = self.tolerance_var.get() 

    #function to calculate the resistors
    def calculate_resistor(self):
        #if there are only 2 bands to add, change the formula to skip the band3
        #bands = d.band[self.band1_var_result] + d.band[self.band2_var_result] if self.band3_var_result == 0 else d.band[self.band1_var_result] + d.band[self.band2_var_result] + d.band[self.band3_var_result]
        if self.band3_var_result == " ":
            bands = d.band[self.band1_var_result] + d.band[self.band2_var_result]
        else:
            bands = d.band[self.band1_var_result] + d.band[self.band2_var_result] + d.band[self.band3_var_result]
        #convert string into int so we can do mathematical operations on it
        int_bands = int(bands)       
        multiplier = d.multiplier[self.multiplier_var_result]
        tolerance = d.tolerance[self.tolerance_var_result]
        #calculate the resistance based on the formula
        formula = (int_bands * multiplier)
        max_resistance = formula + (formula *  tolerance)
        min_resistance = formula - (formula *  tolerance)
        print(max_resistance)
        print(min_resistance)

        if formula < 1000:
            result_max = max_resistance, "Ω"
            result_min = min_resistance, "Ω"
            result_normal = formula, "Ω"
            var_result.set(result_normal)
            var_max.set(result_max)     #set our result to display in our GUI program
            var_min.set(result_min)
        # if result of formula exceeds 1000 concate "k" to the result.
        elif formula > 1000 and formula < 1000000:
            result_max = max_resistance / multiplier, "kΩ"
            result_min = min_resistance / multiplier, "kΩ"
            result_normal = formula / multiplier, "kΩ"
            var_result.set(result_normal)
            var_max.set(result_max)
            var_min.set(result_min)
        else:
            result_max = max_resistance / multiplier, "MΩ"
            result_min = min_resistance / multiplier, "MΩ"
            result_normal = formula / multiplier, "MΩ"
            var_result.set(result_normal)
            var_max.set(result_max)
            var_min.set(result_min)
    #function to build a GUI window and all of it's widgets.
    def build_window(self):
        #main_frame = tk.Frame(self.parent)
        #main_frame.pack(fill=tk.BOTH, expand=tk.YES)

        # status bar, displayed at the bottom of a program
        self.statusBar = tk.Label(self.parent, text="by Namax0r", relief=tk.SUNKEN, bd=1) 
        self.statusBar.grid(row=15, column=2)

        # Band 1
        label = tk.Label(self.parent, text="Band 1" )
        label.grid(row=0, column=0)
        self.band1_var = tk.StringVar() #a string variable to hold user selection
        band1_combo = Combobox(self.parent, state='readonly', height = '6', justify = 'center', textvariable=self.band1_var)
        band1_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band1_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band1_combo.grid(row=0, column=1)

        # Band 2
        label = tk.Label( self.parent, text="Band 2")
        label.grid(row=2, column=0)
        self.band2_var = tk.StringVar() 
        band2_combo = Combobox(self.parent, state='readonly', height = '6', justify = 'center', textvariable=self.band2_var)
        band2_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band2_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band2_combo.grid(row=2, column=1)

        # Band 3
        label = tk.Label( self.parent, text="Band 3" )
        label.grid(row=4, column=0)
        self.band3_var = tk.StringVar()
        self.band3_var.set(" ")
        band3_combo = Combobox(self.parent, state='readonly', height = '6', justify = 'center', textvariable=self.band3_var)
        band3_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band3_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band3_combo.grid(row=4, column=1)

        # Multiplier
        label = tk.Label( self.parent, text="Multiplier" )
        label.grid(row=6, column=0)
        self.multiplier_var = tk.StringVar()
        multiplier_combo = Combobox(self.parent, state='readonly', height = '6', justify = 'center', textvariable=self.multiplier_var)
        multiplier_combo['values']=('black', 'brown', 'red', 'orange',
                                    'yellow', 'green', 'blue', 'violet')
        multiplier_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        multiplier_combo.grid(row=6, column=1)

        # Tolerance
        label = tk.Label( self.parent, text="Tolerance" )
        label.grid(row=8, column=0)
        self.tolerance_var = tk.StringVar()
        tolerance_combo = Combobox(self.parent, state='readonly', height = '6', justify = 'center', textvariable=self.tolerance_var)
        tolerance_combo['values']=('brown', 'red', 'green', 'blue',
                                   'violet', 'gray', 'gold', 'silver')
        tolerance_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        tolerance_combo.grid(row=8, column=1)
            
        self.calculate_button = tk.Button(self.parent, text ="Calculate", command = self.calculate_resistor)
        self.calculate_button.grid(row=9, column=1)

        # Result
        label = tk.Message( self.parent, text="Result:")
        label.grid(row=11, column=1) 

        label = tk.Message( self.parent, text="Basic:")
        label.grid(row=12, column=0)
        label = tk.Message( self.parent, textvariable=var_result, relief=tk.RAISED )
        label.grid(row=12, column=1)

        label = tk.Message( self.parent, text="Max:")
        label.grid(row=13, column=0)
        label = tk.Message( self.parent, textvariable=var_max, relief=tk.RAISED)
        label.grid(row=13, column=1)

        label = tk.Message( self.parent, text="Min:")
        label.grid(row=14, column=0)
        label = tk.Message( self.parent, textvariable=var_min, relief=tk.RAISED )
        label.grid(row=14, column=1)

    def close_program(self, event=None):
        self.parent.destroy()
    
if __name__ == '__main__':
    app = ResistorCalculator(root, "Resistor Calculator")
    root.mainloop()
