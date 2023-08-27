from tkinter import *
from enum import IntFlag
import pandas as pd
import matplotlib.pyplot as plt

                                    # FILES + QUESTIONS

file = 'ChatGPT (Responses).csv' 
df = pd.read_csv(file)
df = df.drop('Timestamp', axis=1) # Deleting the time stamps column

# Getting String values of questions

# Independent
Iq1 = "How old are you?"
Iq2 = "What is your gender?"
Iq3 = "What is your University role?"
Iq4 = "What is your field of study?"
Iq5 = "How busy are you outside of University? (jobs, other commitments, etc.)"
Iq6 = "How much time do you spend working on your University role(s)? (studying, classes, etc.)"

# Dependent
Dq1 = "How experienced are you with ChatGPT?"
Dq2 = "In what circumstances have you used ChatGPT? (multi-select)" # Multi select --> split answers for data frame
Dq3 = "On a scale of 1-5, how strongly do you believe that using ChatGPT for academics is a form of plagiarism?"
Dq4 = "If you have used ChatGPT, how satisfied were you with the depth of and accuracy of the information?"
Dq5 = "How helpful do you think ChatGPT is for the learning environment?"
choices = [Iq1, Iq2, Iq3, Iq4, Iq5, Iq6, Dq1, Dq2, Dq3, Dq4, Dq5] # Questions

df[Iq2] = df[Iq2].fillna('Prefer not to say')  #No data --> about 30 of the responses are missing the gender question due to a problem with the form
        #fillna --> replaces all mising data in column 'What is your gender' with 'Prefer Not to Say


                                    # UI PART

                    # Flag Enums for Each Independent Question
class AGE(IntFlag): # Enums must be assigned in unique powers of two so that they can be combined with bitwise operations!!!!!!
    _17To23 = 1     # By assigning unique powers of two values to each flag, we can represent any combination of flags using a single integer value
    _24To28 = 2
    _29To35 = 4
    _36To50 = 8
    _50Plus = 16

class GENDER(IntFlag):
    MALE = 1
    FEMALE = 2
    PREFER_NOT_SAY = 4
    OTHERGENDER = 8

class UNIROLE(IntFlag):
    UNDERGRAD = 1
    GRAD = 2
    TA = 4
    PROFESSOR = 8

class FIELD(IntFlag):
    SCIENCES = 1
    MATH = 2
    SOCIAL_SCIENCES = 4
    ARTS_AND_MUSIC = 8
    LAW = 16
    LANGUAGES = 32
    SPORTS = 64
    BUSINESS = 128
    OTHERFIELD = 256

class BUSY_OUT(IntFlag):
    ONE = 1
    TWO = 2
    THREE = 4
    FOUR = 8
    FIVE = 16

class BUSY_IN(IntFlag):
    ONE = 1
    TWO = 2
    THREE = 4
    FOUR = 8
    FIVE = 16

# Functions


def place_checkbuttons(frame, values, checkboxes, function): # Frame is the current frame. Values are the possible result (the labels of each checkbox --> labels based on thier flag enums). Function is the specific command for all checkboxes in a specific frame. Checkboxes is a dictionary of all checkboxes
    vars = [IntVar(value=1) for _ in range(len(values))] # Creating an array of intVariables the same size as values. This is a VARIABLE CLASS, and useful to bind functions to be called when values change (such as in lambda functions)
    index_vars = 0 # Keeping track of each IntVar --> each is an Object (all are unique).
    row = Frame(frame) # Creating Frame for a row, in the current frame
    row.pack(anchor = "w") # Rows anchoring to the left of the frame
    for enum in values: # Looping the number of checkboxes we need. Each loop is directed by a specific enum of the flag enumerator given in values
        checkbutton = Checkbutton(row, variable=vars[index_vars], text=values[enum], command = function) # Creating the checkbox. Starts on with intvar = 1. As int vars are separated, each check box is unaffected by the other checkboxes. In addition, values is a dictionary --> getting the value at key enum
        checkbutton.pack(side=LEFT) # Packing left to right
        checkboxes[enum] = vars[index_vars] # Each frame has a specific checkbox dictionary to keep track of checkboxes and their state (on/off). States are IntVars, so changing them change their values in checkboxes
        if ((index_vars + 1) % 5  == 0):
            row = Frame(frame)
            row.pack(anchor = "w")# Creates a new row when too many instances of checkboxes in one row happen (5 max). Anchoring at left again
        index_vars += 1 
    select_all_button = Button(frame, text="Select All", command=lambda vars=vars: ([var.set(1) for var in vars], function())) # Select all button, that has a lambda command to set all Int vars in the frame to 1 (on). It also has a second lambda function, function, that calls the update_state updating the varaible holding the enum values
    select_all_button.pack(side=LEFT) # Packing the button
    deselect_all_button = Button(frame, text="Deselect All", command=lambda vars=vars: ([var.set(0) for var in vars], function())) # Select all button, that has a lambda command to set all Int vars in the frame to 1 (on). It also has a second lambda function, function, that calls the update_state updating the varaible holding the enum values
    deselect_all_button.pack(side=LEFT) # Packing the button

# Updates the variables holding the enums based on which checkboxes are on
def update_state(checkboxes, current_var): # Checkboxes is a dictionary of checkboxes in a specific frame. current_var is the variable holding the enums for the specific frame (like age, gender, etc.). current_enums is the current flag class we are looking at
    value = 0
    for key, var in checkboxes.items(): #.items() splits the dictionary of checkboxes into an array list of tuple (key, value) --> (checkbox, value(on/off))
        if var.get(): # Getting the value of var --> var is a booleanVariable. This is a VARIABLE CLASS, and useful to bind functions to be called when values change (such as in lambda functions)
            value |= key.value # As per the use of flags, we OR(|) --> allows the combination of flags!! Ex: 2 | 4 == 6 (binary bitwise operation). This also works with AND (&)
                                    # Each number has a unique set of value to make it 
    if (value == 0):
        print("One option must be selected!")
        canPlot.set(False) # If all checkboxes of a frame are off, canPlot, this booleanVar will be set to false, and nothing will plot until at least one box is on
    else:
        canPlot.set(True)
    current_var.set(value) 



#window.mainloop()
root = Tk(className = " ChatGPT") # Creates window and sets window name. root is default name for the 'main' window
root.geometry("1000x600") # Sets window size

                                # Independent Questions

general = Frame(root, width = 200, height = root.winfo_height()) #Creating a general frame to containg other frames
general.pack() # Packs the frame into the main (root) window
general.place(x=0, y=0) # Placing frame top-left

# Plot boolean variable
canPlot = BooleanVar(value = True) # False if all buttons in a frame are not clicked, because then all data will filter out. Can only plot when true


# AGE
age_frame = Frame(general) # Creates a frame
age_frame.pack(anchor="w") # Anchor the frame to the left of the general frame
age_label = Label(age_frame, text="AGE", font=("Arial", 10), anchor="n") #Creates a label and anchors it at the top of this frame
age_label.pack(padx=10, pady=5) # Packs the label

age_checkboxes = {} # Dictionary of checkboxes and their values(on/off)
age_labels = {AGE._17To23: "17-23", AGE._24To28: "24-28", AGE._29To35: "29-35", AGE._36To50: "36-50", AGE._50Plus: "50+"} # Creates labels based on the flag enums for each checkbox (the possible responses)
age_var = IntVar(value=0) # This variable represents the value of the enum flags. Because of how the flags are set up, each value is made of a unique set of flags. 
age_function = lambda :update_state(age_checkboxes, age_var)     # This function controls the parameters of the checkboxes when they call the update_state function
place_checkbuttons(age_frame, age_labels, age_checkboxes, age_function) # Calls the method to place all the checkbuttons in the frame (on screen)
update_state(age_checkboxes, age_var) # Must call to update age_var when the program starts




                    #Rest of UI Independent Questions follow same structure!!!

# Gender
gender_frame = Frame(general) 
gender_frame.pack(anchor="w")
gender_label = Label(gender_frame, text="GENDER", font=("Arial", 10), anchor="n") 
gender_label.pack(padx=10, pady=5)


gender_checkboxes = {} 
gender_labels = {GENDER.MALE: "Male", GENDER.FEMALE:"Female", GENDER.PREFER_NOT_SAY: "Prefer not to say", GENDER.OTHERGENDER: "Other"} 
gender_var = IntVar(value=0) 
gender_function = lambda :update_state(gender_checkboxes, gender_var)
place_checkbuttons(gender_frame, gender_labels, gender_checkboxes, gender_function) 
update_state(gender_checkboxes, gender_var)

# University Role
role_frame = Frame(general) # Creates a frame
role_frame.pack(anchor="w")
role_label = Label(role_frame, text="UNIVERSITY ROLE", font=("Arial", 10), anchor="n") #Creates a label and anchors it at the top
role_label.pack(padx=10, pady=5)

role_checkboxes = {} 
role_labels = {UNIROLE.UNDERGRAD: "Undergraduate", UNIROLE.GRAD: "Graduate", UNIROLE.TA: "TA", UNIROLE.PROFESSOR: "Professor"} 
role_var = IntVar(value=0) 
role_function = lambda :update_state(role_checkboxes, role_var)
place_checkbuttons(role_frame, role_labels, role_checkboxes, role_function) 
update_state(role_checkboxes, role_var)

# Field of Study
field_frame = Frame(general) # Creates a frame
field_frame.pack(anchor="w")
field_label = Label(field_frame, text="FIELD OF STUDY", font=("Arial", 10), anchor="n") #Creates a label and anchors it at the top
field_label.pack(padx=10, pady=5)

field_checkboxes = {} 
field_labels = {FIELD.SCIENCES: "Sciences (Physics, Med, Comp Sci, etc.)", FIELD.MATH: "Math", FIELD.SOCIAL_SCIENCES: "Social Sciences", FIELD.ARTS_AND_MUSIC: "Arts and Music", FIELD.LAW: "Law", FIELD.LANGUAGES: "Languages", FIELD.SPORTS: "Sports", FIELD.BUSINESS: "Business", FIELD.OTHERFIELD: "Other"} 
field_var = IntVar(value=0) 
field_function = lambda :update_state(field_checkboxes, field_var)
place_checkbuttons(field_frame, field_labels, field_checkboxes, field_function) 
update_state(field_checkboxes, field_var)

# Busy outside Uni
busyOut_frame = Frame(general) # Creates a frame
busyOut_frame.pack(anchor="w")
busyOut_label = Label(busyOut_frame, text="HOW BUSY OUTSIDE UNI (SCALE)", font=("Arial", 10), anchor="n") #Creates a label and anchors it at the top
busyOut_label.pack(padx=10, pady=5)

busyOut_checkboxes = {} 
busyOut_labels = {BUSY_OUT.ONE: 1, BUSY_OUT.TWO: 2, BUSY_OUT.THREE: 3, BUSY_OUT.FOUR: 4, BUSY_OUT.FIVE: 5} 
busyOut_var = IntVar(value=0) 
busyOut_function = lambda :update_state(busyOut_checkboxes, busyOut_var)
place_checkbuttons(busyOut_frame, busyOut_labels, busyOut_checkboxes, busyOut_function) 
update_state(busyOut_checkboxes, busyOut_var)

# Busy in Uni
busyIn_frame = Frame(general) # Creates a frame
busyIn_frame.pack(anchor="w")
busyIn_label = Label(busyIn_frame, text="HOW BUSY IN UNI (SCALE)", font=("Arial", 10), anchor="n") #Creates a label and anchors it at the top
busyIn_label.pack(padx=10, pady=5)

busyIn_checkboxes = {} 
busyIn_labels = {BUSY_IN.ONE: 1, BUSY_IN.TWO: 2, BUSY_IN.THREE: 3, BUSY_IN.FOUR: 4, BUSY_IN.FIVE: 5} 
busyIn_var = IntVar(value=0) 
busyIn_function = lambda :update_state(busyIn_checkboxes, busyIn_var)
place_checkbuttons(busyIn_frame, busyIn_labels, busyIn_checkboxes, busyIn_function) 
update_state(busyIn_checkboxes, busyIn_var)


                    # Which question to graph?


def text_limit(*args): # Works with var to have a text limit for the dropdown menu
    text = var.get() # Gets the value of var --> the question
    question_var.set(text)
    if len(text) > 20:
        text = text[:17] + '...'
    var.set(text) # Limits the question to 20 characters and sets it back into var

var = StringVar(value=Iq1) # Original Choice of question
var.trace("w", text_limit) # Attaches a callback function to var using trace. text_limit limits the size of the text displayed on the menu. Whenever var changes, the function is called

option_menu = OptionMenu(root, var, *choices) # Dropdown menu to select question
option_menu.config(width = 20, anchor = "w") # Menu selection cant increase the size(width) of the menu. Anchor set to left to width starts from left to right
option_menu.pack()
question_var = StringVar(value = choices[0])

question_label = Label(root, text="QUESTION SELECT:", font=("Arial", 10), anchor="n") #Creates a label and anchors it at the top
question_label.pack(padx=10, pady=5)
question_label.place(x=280, y= 7)


important_vars = [age_var, gender_var, role_var, field_var, busyOut_var, busyIn_var, question_var]

# Reversing dictionaries above to go from labels to keys. Need both dictionaries for two different processes
# In this case, we need labels to enums so that all the data in the data frame can easily convert to enums
# Reversing: age_labels, gender_labels, role_labels, field_labels, busyOut_labels, busyIn_labels
def reverse(original): # Function to reverse dictionaries
    reversed = dict()
    for key in original:
        val = original[key]
        reversed[val] = key
    return reversed

age_dict = reverse(age_labels)
gender_dict = reverse(gender_labels)
role_dict = reverse(role_labels)
field_dict= reverse(field_labels)
busyOut_dict = reverse(busyOut_labels)
busyIn_dict = reverse(busyIn_labels)

dictionary_list = [age_dict, gender_dict, role_dict, field_dict, busyOut_dict, busyIn_dict]


                        # WHAT TYPE OF GRAPH?


graph_choices = ["Pie Chart", 'Bar Graph']
graph_var = StringVar(value = graph_choices[0])

graph_menu = OptionMenu(root, graph_var, *graph_choices)
graph_menu.config(width = 20, anchor = "e") 
graph_menu.pack()

graph_label = Label(root, text="GRAPH SELECT:", font=("Arial", 10), anchor="n") #Creates a label and anchors it at the top
graph_label.pack(padx=10, pady=5)
graph_label.place(x=280, y= 37)

                        # FILTERING

def multiSelect(dictionary, data, flags, question, callNum):# One independent question has multi-select
    ## Iq3 is the only independent question that is multiselect --> responses must be split
    parts_data = data.split(", ")
    parts_var = [dictionary.get(x) for x in parts_data]
    binary_values = [bin(int(part)) for part in parts_var]
    value = 0
    for binary in binary_values:
        value |= int(binary, 2) # The two specifies that the value converted to int is binary and the converstion takes care of this
    
    if (value & flags == value): # If all the values in common between data and flags is data: no point in continuing, we are good
        return 1 if callNum == 1 else data
    
    if (value & flags != 0): # If there is some value in common between data and the flags when value contains some value(s) not in flags
        if (question == Iq3):
            flag_list = [UNIROLE.UNDERGRAD, UNIROLE.GRAD, UNIROLE.TA, UNIROLE.PROFESSOR]
            possible_responses = ["Undergraduate", "Graduate", "TA", "Professor"]
            for i in range(len(flag_list)):
                current_flag = flag_list[i]
                current_response = possible_responses[i]
                if not (flags & current_flag):
                    try:
                        parts_data.remove(current_response)
                    except:
                        continue
        # for i in range(value.bit_length()): # Looping the number of bits that value has
        #     bit = (value >> i) & 1 # Shifs i bits to the right, and anding by 1 to set all other bits to 0 --> Gets the rightmost bit, to the leftmost
        #     flag_bit = (flags >> i) & 1
        #     if (bit == 1) and (flag_bit == 0): # If the flag isn't set for a part of the response, and the response contains that part, then:
        #         del parts_data[value.bit_length() - i - 2] # remove that part of the response from data (an object)
        #         binary_value += int(bin(flag_bit), 2)
        #     else:
        #         binary_value += int(bin(bit), 2)
        data = ', '.join(parts_data) # data changed accordingly
        if not data == "": # If data in empty, just return data for the first pass. Why? Because the second pass will remove it
            return 1 if callNum == 1 else data
    return 0 if callNum == 1 else data

    
def convertToInt(dictionary, data): 
    return int(bin(int(dictionary.get(data))), 2) # Converts the value given by the dictionary (converted to an int), and converting it to binary, then to a binary int representation
    

def PLOT(): # Uses choices and important_vars

    if (not canPlot.get()): # If the boolean Variable canPlot is false (only when all checkbuttons in a frame are off), don't do anything (end plotting)
        return

    filtered_df = df.copy() # Copying the data frame into another data frame
    size = len(important_vars) - 1 # important_vars --> amount of variables is amount of filtering needed
    for i in range(size): 
        current_column = choices[i] # Current column takes the questions from choices
        current_filter = important_vars[i] # Containes all the filtering --> values containing flag enums 1/0 for each bit in binary form
        current_dict = dictionary_list[i] # Contains the needed dictionary for each question in the same order
        # For every single filter but the last one (6 times)                                          # If the returned binary value of the data AND the current_filter(flag) == 0 --> flag not set to accept this data, filter data out                                        
        if (current_column in [Iq3]): # If multi select question
            filtered_df[current_column] = filtered_df[current_column].apply(lambda x: multiSelect(current_dict, x, current_filter.get(), current_column, 2)) # Setting every value in the series to the value given by the function. This only affects data that contains multiple responses, removing all parts of a response that are to be filtered out
            filtered_df = filtered_df[filtered_df[current_column].apply(lambda x: multiSelect(current_dict, x, current_filter.get(), current_column, 1) != 0)] # Filters the data out (after the multi-select responses have been filtered out)      
        else:
            filtered_df = filtered_df[filtered_df[current_column].apply(lambda x: convertToInt(current_dict, x) & current_filter.get() != 0)] # Filters out all values in a column one column at a time if the data in their respective rows do not match any of the flags in their respective var variable. 
        if filtered_df.shape[0] == 0: # Shape returns a tuple of (# of rows, # of columns). If # of rows = 0, end plot
            return
    # Last filter, only question column needed
    #filtered_df = filtered_df[current_filter.get()] #Filters out all columns except the one with the question we are looking at. This happens at the end after all the other filtering
    
   # Graph_var is a StringVar containing the string representation of the graph we want to draw
    graph_type = graph_var.get()
    title = question_var.get()

    if title in [Iq3, Dq2]: # Only multiselect questions
        filtered_df = filtered_df.assign(**{title: filtered_df[title].str.split(', ')})# If multiselect, go to each row, and split up the multi responses via ', ' and create new rows for them
        filtered_df = filtered_df.explode(title)
        filtered_df[title] = filtered_df[title].apply(lambda x: x.strip())

    
    # Graph_choices containes all the possible combinations in an array
    if (graph_type == graph_choices[0]): # Pie Chart
        filtered_df.groupby(title).size().plot(kind='pie', autopct='%.1f%%', ) # Graphing the column directed by question_var.
        
    elif (graph_type == graph_choices[1]): # Bar Graph
        filtered_df.groupby(title).size().plot(kind='bar') # Graphing the column directed by question_var. 
        
        

    if title in [Dq1, Dq4, Dq5]: # These three questions need to add (Scale) to make it clear that the data value labels are on scales (1-5)
        title += " (Scale)"
    plt.title(title, wrap = True) #Sets the title and Wrap wraps the title within the screen


    plt.show()
    

                    
                    
                    # Plot Graph button

plot = Button(root, text = "PLOT", command = PLOT) # Passing the PLOT function inself as the command option (without the () at the end, else that would immediately call the function and return a value, which would be assigned to command instead of the function itself)
plot.pack(side = TOP)

root.mainloop()