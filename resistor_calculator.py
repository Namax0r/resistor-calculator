#!/usr/bin/env python

# Basic version handling
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

from tkinter.ttk import Combobox
from tkinter import messagebox

# Small utility that adds dot notation access to dictionary attributes
class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# Main view window
root = tk.Tk()
# Store width and height in variable for ease of change
window_width = 300
window_height = 380
# Set min and max size of a GUI window
root.minsize(window_width, window_height)
root.maxsize(window_width, window_height)

# Var is used to store our result
var_result = tk.StringVar()
var_max = tk.StringVar()
var_min = tk.StringVar()

# Create dictionary of colors and values
d = {
    #Values of the band are stored as string to allow concatenation of the numbers.
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

# Enable dot notation on the dictionary
d = dotdict(d)

class ResistorCalculator:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.close_program)
        # Define variables to store values of comboboxes 
        self.band1_var_result = 0
        self.band2_var_result = 0
        self.band3_var_result = 0
        self.multiplier_var_result = 0
        self.tolerance_var_result = 0

        self.build_window()

    # Function to destroy the window when [X] is pressed
    def close_program(self, event=None):
        self.parent.destroy()

    # Function called when '<<ComboboxSelected>>' event is triggered
    def combobox_handler(self, event): 
        #store values of comboboxes in variables.
        self.band1_var_result = self.band1_var.get()
        self.band2_var_result = self.band2_var.get()
        self.band3_var_result = self.band3_var.get()
        self.multiplier_var_result = self.multiplier_var.get()
        self.tolerance_var_result = self.tolerance_var.get() 

    # Function to handle error, when there are not enough arguments for formula to calculate properly.
    def error_not_enough_args(self):
        tk.messagebox.showinfo("Error", "Not enough arguments to calculate. Please select more values.")

    # Function to add a mark at the end of a result
    def add_mark(self, val, mark):
        return val, mark

    # Function to calculate the resistors
    def calculate_resistor(self):
        try:
            # If there are only 2 bands to add, change the formula to skip the band3
            if self.band3_var_result == " ":
                bands = d.band[self.band1_var_result] + d.band[self.band2_var_result]
            else:
                bands = d.band[self.band1_var_result] + d.band[self.band2_var_result] + d.band[self.band3_var_result]
            # Convert string into int so we can do mathematical operations on it
            int_bands = int(bands)       
            # Set multiplier and tolerance
            multiplier = d.multiplier[self.multiplier_var_result]
            tolerance = d.tolerance[self.tolerance_var_result]
            # Calculate the resistance based on the formula
            formula = (int_bands * multiplier)
            max_resistance = formula + (formula *  tolerance)
            min_resistance = formula - (formula *  tolerance)

            result_max = max_resistance / multiplier
            result_min = min_resistance / multiplier
            result_normal = formula / multiplier
            if formula < 1000:
                result_max = max_resistance
                result_min = min_resistance
                result_normal = formula
            # if result of formula exceeds 1000 add "k" after the result.
            elif formula > 1000 and formula < 1000000:
                result_max = self.add_mark(result_max, "kΩ")
                result_min = self.add_mark(result_min, "kΩ")
                result_normal = self.add_mark(result_normal, "kΩ")
            else:
                result_max = self.add_mark(result_max, "MΩ")
                result_min = self.add_mark(result_min, "MΩ")
                result_normal = self.add_mark(result_normal, "MΩ")
            # Set the variables that display result in the GUI
            var_result.set(result_normal)
            var_max.set(result_max)
            var_min.set(result_min)
        # KeyError exception when there are not enough values to calculate 
        except KeyError:
            self.error_not_enough_args()

    # Function to build a GUI window and all of it's widgets.
    def build_window(self):
        # Band 1
        band1_label = tk.Label(self.parent, text="Band 1" )
        band1_label.grid(row=0, column=0, ipadx=30, pady=5)
        self.band1_var = tk.StringVar() 
        band1_combo = Combobox(self.parent, state='readonly', height = '10', justify = 'center', textvariable=self.band1_var)
        band1_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band1_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band1_combo.grid(row=0, column=1, padx=10)

        # Band 2
        band2_label = tk.Label( self.parent, text="Band 2")
        band2_label.grid(row=2, column=0, pady=5)
        self.band2_var = tk.StringVar() 
        band2_combo = Combobox(self.parent, state='readonly', height = '10', justify = 'center', textvariable=self.band2_var)
        band2_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band2_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band2_combo.grid(row=2, column=1)

        # Band 3
        band3_label = tk.Label( self.parent, text="Band 3" )
        band3_label.grid(row=4, column=0, pady=5)
        self.band3_var = tk.StringVar()
        # Setting band3 to " " helps with modification of calculation formula based on this value
        self.band3_var.set(" ")
        band3_combo = Combobox(self.parent, state='readonly', height = '10', justify = 'center', textvariable=self.band3_var)
        band3_combo['values']=('black', 'brown', 'red', 'orange',
                               'yellow', 'green', 'blue', 'violet',
                               'gray', 'white')
        band3_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        band3_combo.grid(row=4, column=1)

        # Multiplier
        multiplier_label = tk.Label( self.parent, text="Multiplier" )
        multiplier_label.grid(row=6, column=0, pady=5)
        self.multiplier_var = tk.StringVar()
        multiplier_combo = Combobox(self.parent, state='readonly', height = '10', justify = 'center', textvariable=self.multiplier_var)
        multiplier_combo['values']=('black', 'brown', 'red', 'orange',
                                    'yellow', 'green', 'blue', 'violet')
        multiplier_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        multiplier_combo.grid(row=6, column=1)

        # Tolerance
        tolerance_label = tk.Label( self.parent, text="Tolerance" )
        tolerance_label.grid(row=8, column=0, pady=5)
        self.tolerance_var = tk.StringVar()
        tolerance_combo = Combobox(self.parent, state='readonly', height = '10', justify = 'center', textvariable=self.tolerance_var)
        tolerance_combo['values']=('brown', 'red', 'green', 'blue',
                                   'violet', 'gray', 'gold', 'silver')
        tolerance_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        tolerance_combo.grid(row=8, column=1)

        # Calculate button
        self.calculate_button = tk.Button(self.parent, text ="Calculate", command = self.calculate_resistor)
        self.calculate_button.grid(row=9, column=1, pady=5, ipadx=40)

        # Results section
        result_label = tk.Message( self.parent, text="Result:")
        result_label.grid(row=12, column=0, pady=10)
        result_value = tk.Message( self.parent, textvariable=var_result, relief=tk.RAISED )
        result_value.grid(row=12, column=1)

        max_result_label = tk.Message( self.parent, text="Max:")
        max_result_label.grid(row=13, column=0, pady=10, ipadx=20)
        max_result_value = tk.Message( self.parent, textvariable=var_max, relief=tk.RAISED)
        max_result_value.grid(row=13, column=1)

        min_result_label = tk.Message( self.parent, text="Min:")
        min_result_label.grid(row=14, column=0, pady=10)
        min_result_value = tk.Message( self.parent, textvariable=var_min, relief=tk.RAISED )
        min_result_value.grid(row=14, column=1)

        # Author name, displayed at the bottom of a program
        author_name = tk.Label(self.parent, text="by Namax0r", relief=tk.SUNKEN, bd=1) 
        author_name.place(x=window_width - 70, y=window_height - 20)
    
if __name__ == '__main__':
    app = ResistorCalculator(root, "Resistor Calculator")
    root.mainloop()
