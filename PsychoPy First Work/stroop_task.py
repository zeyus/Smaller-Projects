#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Stroop Task
# @ Kristian Tylén
# Feb 2017

# import modules
from psychopy import visual, event, core, data, gui
import numpy as np 
import random
import pandas as pd
from random import randint
import glob, os, shutil

# Create popup information box
popup = gui.Dlg(title = "The Stroop Experiment")
popup.addField("Alias: ") # Empty box
popup.addField("Age: ")
popup.addField("Gender: ", choices=["Male", "Female", "Other" ]) # Dropdown menu
popup.show()
if popup.OK: # To retrieve data from popup window
    ID = popup.data
elif popup.Cancel: # To cancel the experiment if popup is closed
    core.quit()

#########################################################################################
################################## Stroop Task ##########################################
#########################################################################################


NUM_REP = 10 # repetitions * 4 trials

intro = '''
Welcome to the first experiment!

This is a "Stroop Task". Please read the instructions very carefully.

Use the keys r, g, b, and y to indicate if the words on the screen are printed
in red, green, blue or yellow ink. Ignore the meaning of the words.

Example: if you see the word "red" printed in green ink, you should press 'g' (and NOT 'r').
Please try to be as fast as possible. 

If you make a mistake, please do not try to correct it by pushing a second key. Just wait for the next trial.  

press any key when you are ready...
'''

outro = '''
The experiment is done. Thank you for your participation!
'''

# define window
win = visual.Window(fullscr=True, color = 'Black')

# define a stop watch
stopwatch = core.Clock()                                  

# prepare stimuli
Word = ['red', 'green', 'blue', 'yellow']
Word = Word*NUM_REP
random.shuffle(Word)

Colours = ['red', 'green', 'blue', 'yellow'] 
Colours = Colours*NUM_REP
random.shuffle(Colours)

# prepare pandas data frame for recorded data
columns = ['ID', 'Age', 'Gender', 'Word', 'Colour', 'Response', 'Congruent', 'Correct', 'Reaction_time']
index = np.arange(0)
STROOP_DATA = pd.DataFrame(columns=columns, index = index)

# define function that shows text
def msg(txt):
    instructions = visual.TextStim(win, text=txt, color = 'white', height = 0.05) # create an instruction text
    instructions.draw() # draw the text stimulus in a "hidden screen" so that it is ready to be presented 
    win.flip() # flip the screen to reveal the stimulus
    event.waitKeys() # wait for any key press


# show instructions
msg(intro)

# loop through trials
for i in range(len(Word)):
    # prepare stimulus
    stimulus = visual.TextStim(win, text=Word[i], color = Colours[i])
    # draw stimulus
    stimulus.draw()
    win.flip()
    # reset stop watch
    stopwatch.reset()                              #reset the clock to 0:0:0 
    # record key press
    key = event.waitKeys(keyList = ['escape', 'r', 'g', 'b', 'y'])                  # wait for any key press
    # get reaction time at key press
    reaction_time = stopwatch.getTime()            # asks the stopwatch for the time since reset and save to the variable reation_time
    
    # check if response is correct and if it is congruent 
    if key[0] == 'r' and Colours[i] == 'red':
        correct = 1
        if Word[i] == 'red':
            congruent = 1
        else:
            congruent = 0
    elif key[0] == 'g' and Colours[i] == 'green':
        correct = 1
        if Word[i] == 'green':
            congruent = 1
        else:
            congruent = 0
    elif key[0] == 'b' and Colours[i] == 'blue':
        correct = 1
        if Word[i] == 'blue':
            congruent = 1
        else:
            congruent = 0
    elif key[0] == 'y' and Colours[i] == 'yellow':
        correct = 1
        if Word[i] == 'yellow':
            congruent = 1
        else:
            congruent = 0
    elif key[0] == 'escape':
        core.quit()
        win.close()
    else: 
        correct = 0
        congruent = 0
    
    
    # append all recorded data to the pandas DATA 
    STROOP_DATA = STROOP_DATA.append({
        'ID': ID[0],
        'Age': ID[1],
        'Gender': ID[2],
        'Word': Word[i], 
        'Colour': Colours[i], 
        'Response': key[0], 
        'Congruent': congruent, 
        'Correct': correct, 
        'Reaction_time': reaction_time
        }, ignore_index=True)
    
    # show blank screen
    stimulus = visual.TextStim(win, '')
    stimulus.draw()
    win.flip()
    core.wait(0.5)

print(STROOP_DATA)

logfile_name = 'logfile_' + ID[0] + '.csv'
STROOP_DATA.to_csv(logfile_name)

msg(outro)
core.quit()
