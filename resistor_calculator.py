from tkinter import *
from tkinter.ttk import Combobox

root = Tk()
var = StringVar()

# Band 1
label = Label( root, text="Band 1" )
label.pack()

band1_combo = Combobox(root, state='readonly', height = '6',justify = 'center')

band1_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                                  'Yellow', 'Green', 'Blue', 'Violet','Gray',
                                  'White',)
band1_combo.pack( anchor = E )

# Band 2
label = Label( root, text="Band 2" )
label.pack()


band2_combo = Combobox(root, state='readonly', height = '6',justify = 'center')

band2_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                                  'Yellow', 'Green', 'Blue', 'Violet','Gray',
                                  'White',)
band2_combo.pack( anchor = E )

# Band 3
label = Label( root, text="Band 3" )
label.pack()


band3_combo = Combobox(root, state='readonly', height = '6',justify = 'center')

band3_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                                  'Yellow', 'Green', 'Blue', 'Violet','Gray',
                                  'White',)
band3_combo.pack( anchor = E )

# Multiplier
label = Label( root, text="Multiplier" )
label.pack()


multiplier_combo = Combobox(root, state='readonly', height = '6',justify = 'center')

multiplier_combo['values']=('Black', 'Brown', 'Red', 'Orange',
                                  'Yellow', 'Green', 'Blue', 'Violet')
multiplier_combo.pack( anchor = E )

# Tolerance
label = Label( root, text="Tolerance" )
label.pack()


tolerance_combo = Combobox(root, state='readonly', height = '6',justify = 'center')

tolerance_combo['values']=('Brown', 'Red', 'Green', 'Blue', 'Violet', 'Gray', 'Gold',
                                  'Silver')
tolerance_combo.pack( anchor = E )

root.mainloop()

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
    
    if formula < 1000:
        print(formula, "Ω")
    # if result of formula exceeds 1000 concate "k" to the result.
    elif formula > 1000 and formula < 1000000:
        print(formula / multiplier, "kΩ")
    else:
        print(formula / multiplier, "MΩ")

calculate_resistor(d.green, d.violet, d.violet, d.green_multiplier, d.gold_tolerance)

