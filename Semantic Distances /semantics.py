# Script that records word association lists, get semantic distances from http://swoogle.umbc.edu/SimService/GetSimilarity 
# and plot the distances

# import modules

from psychopy import visual, event, core, gui
import pandas as pd
import numpy as np
from requests import get


# create dialogue box for time entry
V = {'subject_ID':'', 'age': '', 'gender':['m', 'f', 'o'], 'category': ['animals', 'foods'], 'Insert time in secs (e.g. 120):':int()}
if not gui.DlgFromDict(V, order=['subject_ID', 'age', 'gender', 'Insert time in secs (e.g. 120):']).OK:
    core.quit()

# create empty panda matrix 

columns = ['subject', 'age', 'gender', 'word', 'word_nr', 'distance', 'cumulative', 'time']
index = np.arange(0) # array of numbers for the number of samples
word_list = pd.DataFrame(columns=columns, index = index)
word_nr = 0

# make word entry function 

# -*- coding: utf-8 -*-
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Set up window and text field

win = visual.Window(fullscr = True)
text = visual.TextStim(win, text='')


#display info text and wait for key press
def info(string, end = False):
    disp = visual.TextStim(win, text=string, height=.08)
    disp.draw()
    win.flip()
    event.waitKeys()[0]
    win.flip()
    event.clearEvents()

#pull up a screen that lets them start the experiment
txt="You now have {} seconds to name as many different {} as you can think of. Press any key when you are ready.".format(V["Insert time in secs (e.g. 120):"], V["category"])
info(txt)


# initialize abort option
endTrial = False
# initialize clock
clock = core.Clock()
stopwatch = core.Clock()

while not endTrial:
    # Wait for response...
    if clock.getTime() > int(V['Insert time in secs (e.g. 120):']):
        endTrial = True
    response = event.waitKeys()
    if response:
        # If backspace, delete last character
        if response[0] == 'backspace':
            text.setText(text.text[:-1])
            
        # Insert space
        elif response[0] == 'space':
            text.setText(text.text + ' ')

        # Else if a letter, append to text:
        elif response[0] in chars:
            text.setText(text.text + response[0])

        # If return, save word to panda and reset inputw
        elif response[0] == 'return':
            time = stopwatch.getTime()
            word_nr += 1
            word_list = word_list.append({'subject':V['subject_ID'], 'age':V['age'], 'gender':V['gender'], 'category':V['category'], 'word': text.text, 'word_nr': word_nr, 'time': time}, ignore_index=True)
            text.setText(text='')
            stopwatch.reset()
        
        # If esc key - end experiment
        elif response[0] == 'escape': 
            endTrial = True
        

    # Display updated text
    text.draw()
    win.flip()
win.close()

print word_list
    

# get semantic similarities by quering website

sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"

def sss(s1, s2, type='similarity', corpus='webbase'):
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0

        
# Initialize values 

word_list['distance'][0] = float(0)
word_list['cumulative'][0] = float(0)




# loop through word_list and add semantic distances between words
i_prev = 1
for i in range(1,len(word_list)):
    distance = sss(word_list['word'][i], word_list['word'][i-i_prev], 'similarity')
    if str(distance) == "-inf":
        word_list['distance'][i] = None
        word_list['cumulative'][i] = None
        i_prev += 1 #skip this row on the next turn
    else:
        word_list['distance'][i] = ((1 - distance)*10)*((1 - distance)*10) # (distance*distance) # square the distances to enhance effect for plotting
        # create cumulative vector of semantic distances for plotting
        word_list['cumulative'][i] = word_list['distance'][i] + word_list['cumulative'][i-i_prev]
        i_prev = 1 #set back to 1 if a match is found

# print the resulting list
print word_list
word_list.to_csv(str(V['subject_ID'])+'.csv')
