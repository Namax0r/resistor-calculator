# TODO:
# - Remake the dictionary to allow selecting key by simple color names (get rid of _multiplier, _tolerance)
# - Fix the formula to account for changes done to dictionary.
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
root.minsize(500,300)
root.maxsize(550,310)
# var is used to store our result
var = tk.StringVar()

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
        'violet': 0.010, 'grey': 0.005, 'gold': 0.05, 'silver': 0.10
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
        bands = d[self.band1_var_result] + d[self.band2_var_result] if d[self.band3_var_result] == 0 else d[self.band1_var_result] + d[self.band2_var_result] + d[self.band3_var_result]
        #convert string into int so we can do mathematical operations on it
        int_bands = int(bands)
        int_multiplier = int(d[self.multiplier_var_result])
        int_tolerance = int(d[self.tolerance_var_result])
        #calculate the resistance based on the formula
        formula = (int_bands * int_multiplier) * int_tolerance
        #initialize empty variable to hold our result
        result = ''
        if formula < 1000:
            result = formula, "Ω"
            var.set(result)     #set our result to display in our GUI program
        # if result of formula exceeds 1000 concate "k" to the result.
        elif formula > 1000 and formula < 1000000:
            result = formula / int_multiplier, "kΩ"
            var.set(result)
        else:
            result = formula / int_multiplier, "MΩ"
            var.set(result)
    #function to build a GUI window and all of it's widgets.
    def build_window(self):
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=tk.YES)

        # status bar, displayed at the bottom of a program
        self.statusBar = tk.Label(main_frame, text="by Namax0r", relief=tk.SUNKEN, bd=1) 
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)

        # Band 1
        label = tk.Label(main_frame, text="Band 1" )
        label.pack()
        self.band1_var = tk.StringVar() #a string variable to hold user selection
        band1_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center', textvariable=self.band1_var)
        band1_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band1_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band1_combo.pack()

        # Band 2
        label = tk.Label( main_frame, text="Band 2")
        label.pack()
        self.band2_var = tk.StringVar() 
        band2_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center', textvariable=self.band2_var)
        band2_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band1_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band2_combo.pack()

        # Band 3
        label = tk.Label( main_frame, text="Band 3" )
        label.pack()
        self.band3_var = tk.StringVar()
        band3_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center', textvariable=self.band3_var)
        band3_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band1_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band3_combo.pack()

        # Multiplier
        label = tk.Label( main_frame, text="Multiplier" )
        label.pack()
        self.multiplier_var = tk.StringVar()
        multiplier_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center', textvariable=self.multiplier_var)
        multiplier_combo['values']=('black', 'brown', 'red', 'orange',
                                    'yellow', 'green', 'blue', 'violet')
        band1_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        multiplier_combo.pack()

        # Tolerance
        label = tk.Label( main_frame, text="Tolerance" )
        label.pack()
        self.tolerance_var = tk.StringVar()
        tolerance_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center', textvariable=self.tolerance_var)
        tolerance_combo['values']=('brown', 'red', 'green', 'blue',
                                   'violet', 'gray', 'gold', 'silver')
        tolerance_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        tolerance_combo.pack()
            
        self.calculate_button = tk.Button(main_frame, text ="Calculate", command = self.calculate_resistor)
        self.calculate_button.pack()

        # Result
        label = tk.Message( main_frame, text="Result: ", pady=50)
        label.pack( side = tk.LEFT ) 

        label = tk.Message( main_frame, textvariable=var, relief=tk.RAISED, width=55, padx=5 )
        label.pack( side = tk.RIGHT )

    def close_program(self, event=None):
        self.parent.destroy()
    
if __name__ == '__main__':
    app = ResistorCalculator(root, "Resistor Calculator")
    root.mainloop()
    print(d.axa.red)