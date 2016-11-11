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
    #band
    #values of the band are stored as string to allow concantation of the numbers.
    'black': "0",
    'brown': "1",
    'red': "2",
    'orange': "3",
    'yellow': "4",
    'green': "5",
    'blue': "6",
    'violet': "7",
    'gray': "8",
    'white': "9",
    #multiplier
    'black_multiplier': 1,
    'brown_multiplier': 10,
    'red_multiplier': 100,
    'orange_multiplier': 1000,
    'yellow_multiplier': 10000,
    'green_multiplier': 100000,
    'blue_multiplier': 1000000,
    'violet_multiplier': 10000000,
    #tolerance
    'brown_tolerance': 0.01,
    'red_tolerance': 0.02,
    'green_tolerance': 0.005,
    'blue_tolerance': 0.025,
    'violet_tolerance': 0.010,
    'grey_tolerance': 0.005,
    'gold_tolerance': 0.05,
    'silver_tolerance': 0.10
    }

#enable dot notation on the dictionary
d = dotdict(d)

#function to calculate 
def calculate_resistor(band1, band2, band3, multiplier, tolerance): 
    #if there are only 2 bands to add, change the formula to skip the band3
    bands = band1 + band2 if band3 == 0 else band1 + band2 + band3
    #convert string into int so we can do mathematical operations on it
    int_bands = int(bands)
    #calculate the resistance based on the formula
    formula = (int_bands * multiplier) * tolerance
    #initialize empty variable to hold our result
    result = ''
    if formula < 1000:
        result = formula, "Ω"
        var.set(result)     #set our result to display in our GUI program
    # if result of formula exceeds 1000 concate "k" to the result.
    elif formula > 1000 and formula < 1000000:
        result = formula / multiplier, "kΩ"
        var.set(result)
    else:
        result = formula / multiplier, "MΩ"
        var.set(result)

calculate_resistor(d.green, d.violet, d.violet, d.green_multiplier, d.gold_tolerance)

class ResistorCalculator:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.close_program)

        self.build_window()
    def combobox_handler(self, event): #function called when '<<ComboboxSelected>>' event is triggered
        #current = self.combobox.current()
        #self.entNumber.delete(0, END)
        print(self.get()) #how to access to combobox selected item

    def build_window(self):
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=tk.YES)

        # status bar, displayed at the bottom of a program
        self.statusBar = tk.Label(main_frame, text="by Namax0r", relief=tk.SUNKEN, bd=1) 
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)

        # Band 1
        label = tk.Label(main_frame, text="Band 1" )
        label.pack()
        self.band1_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center')
        self.band1_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                               'Yellow', 'Green', 'Blue', 'Violet',
                               'Gray', 'White',)
        self.band1_combo.pack()

        # Band 2
        label = tk.Label( main_frame, text="Band 2")
        label.pack()
        band2_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center')
        band2_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                               'Yellow', 'Green', 'Blue', 'Violet',
                               'Gray', 'White',)
        band2_combo.pack()

        # Band 3
        label = tk.Label( main_frame, text="Band 3" )
        label.pack()
        band3_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center')
        band3_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                               'Yellow', 'Green', 'Blue', 'Violet',
                               'Gray', 'White',)
        band3_combo.pack()

        # Multiplier
        label = tk.Label( main_frame, text="Multiplier" )
        label.pack()
        multiplier_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center')
        multiplier_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                                    'Yellow', 'Green', 'Blue', 'Violet')
        multiplier_combo.pack()

        # Tolerance
        label = tk.Label( main_frame, text="Tolerance" )
        label.pack()
        tolerance_var = tk.StringVar() #a string variable to hold user selection
        tolerance_combo = Combobox(main_frame, state='readonly', height = '6', justify = 'center', textvariable=tolerance_var)
        tolerance_combo['values']=('Brown', 'Red', 'Green', 'Blue',
                                   'Violet', 'Gray', 'Gold', 'Silver')
        #tolerance_combo.bind('<<ComboboxSelected>>', self.combobox_handler)
        tolerance_combo.pack()

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
