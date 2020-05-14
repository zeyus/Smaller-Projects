#!/usr/bin/env python2
# -*- coding: utf-8 -*-
""" DESCRIPTION:
This is a version of the classic visual search paradigm: 
Treisman, A. M., & Gelade, G. (1980). A feature-integration theory of attention. Cognitive psychology, 12, 97-136.

The task is to find the red T among a variable set of other Ts and Is that can be either red or green.

/Mikkel Wallentin 2017 (with some code adapted from Jonas LindeLoev: https://github.com/lindeloev/psychopy-course/blob/master/ppc_template.py)

Structure: 
    SET VARIABLES
    GET PARTICIPANT INFO USING GUI
    SPECIFY TIMING AND MONITOR
    STIMULI
    OUTPUT
    FUNCTIONS FOR EXPERIMENTAL LOOP
    DISPLAY INTRO TEXT AND AWAIT SCANNER TRIGGER
    CALL FUNCTION RUNNING THE EXPERIMENTAL LOOP
    END EXPERIMENT

"""

# Import the modules that we need in this script
from __future__ import division
from psychopy import core, visual, event, gui, monitors, event
import ppc
import random
import numpy as np
import math
import numpy.matlib

"""
SET VARIABLES
"""
# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor 
MON_WIDTH = 34  # Width of your monitor in cm
MON_SIZE = [1440, 900]  # Pixel-dimensions of your monitor
FRAME_RATE=60 # Hz
SAVE_FOLDER = 'visual_search_data'  # Log is saved to this folder. The folder is created if it does not exist.


"""
GET PARTICIPANT INFO USING GUI
"""
# Intro-dialogue. Get subject-id and other variables.
# Save input variables in "V" dictionary (V for "variables")
V= {'ID':'','age':'','gender':['female','male','other'],'handedness':['right','left','ambidextrous']}
if not gui.DlgFromDict(V, order=['ID', 'age', 'gender','handedness']).OK: # dialog box; order is a list of keys 
    core.quit()

"""
SPECIFY TIMING AND MONITOR
"""

# Clock and timer
clock = core.Clock()  # A clock wich will be used throughout the experiment to time events on a trial-per-trial basis (stimuli and reaction times).

# Create psychopy window
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)
win = visual.Window(monitor=my_monitor, units='deg', fullscr=False, allowGUI=False, color='black')  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

"""
STIMULI
"""
delay=(1*FRAME_RATE)# 1 sec between stimuli.
dur=int(3*FRAME_RATE) # duration in seconds multiplied by 60 Hz and made into integer
presence=[1,0]# Is the target present or not
conjunction=[1,0,1,0] #Is it a conjunction or feature search (i.e. are there also green Ts)
rowsizes=[3,5,7,9] # Setsize. How many letters per row
REPETITIONS = 4 # 3 reps* 4 different setsizes * 2 (presence) * 4 (conjunction) = 128 trials
condition='visual_search' #Just a variable. If the script can run several exp. then this can be called in GUI. Not relevant here.


""" OUTPUT """

#KEYS
KEYS_present=['t']#T is response key for target present.
KEYS_absent=['y','r']#Y and R (present next to T) are response key for target absent. One can be used for righthanders, the other for lefthanders

#response keys for quitting and starting
KEYS_QUIT = ['escape']  # Keys that quits the experiment
KEYS_start=['space'] # press space to start
   # Prepare a csv log-file using the ppc script
writer = ppc.csvWriter(str(V['ID']), saveFolder=SAVE_FOLDER)  # writer.write(trial) will write individual trials with low latency

""" FUNCTIONS FOR EXPERIMENTAL LOOP"""
#Generate a trial list with different combinations of the experimental factors
def make_trial_list(condition):
# Factorial design
    trial_list = []
    for rowsize in rowsizes: # number of letters in stim rows
        for conjunct in conjunction:
            for present in presence:
                    for rep in range(REPETITIONS):
                    # Add a dictionary for every trial
                        trial_list += [{
                            'ID': V['ID'],
                            'age': V['age'],
                            'gender': V['gender'],
                            'condition': condition,
                            'rowsize': rowsize,
                            'setsize': rowsize*rowsize,
                            'conjunct': conjunct,
                            'present': present,
                            'onset':'' ,# a place to note onsets
                            'offset': '',
                            'duration_measured':'',
                            'duration_frames': dur,
                            'delay_frames': delay,
                            'response': '',
                            'key_t':'',
                            'rt': '',
                            'correct_resp': ''
                    }]
    
   # Randomize order
    from random import sample
    trial_list = sample(trial_list, len(trial_list))

    # Add trial numbers and return
    for i, trial in enumerate(trial_list):
        trial['no'] = i + 1  # start at 1 instead of 0
        if i is 0:
            writer.writeheader(trial) # An added line to give headers to the log-file (see ppc.py)
    return trial_list

#Function for looping over trials
    
def run_condition(condition):
    """
    Runs a block of trials. This is the presentation of stimuli,
    collection of responses and saving the trial
    """
    # Loop over trials
    for trial in make_trial_list(condition):
        event.clearEvents(eventType='keyboard')# clear keyboard input to make sure that no responses are logged that do not belong to stimulus
        
        if trial['present'] ==1:
            if trial['conjunct'] ==0:
            #Feature present
                Ts=1
                Is=trial['setsize']-1
                Reds1=trial['setsize']
                Reds2=0
                Greens=0
            elif trial['conjunct'] ==1: 
                #Conjunction present
                Ts=math.ceil(trial['setsize']/2)
                Is=math.floor(trial['setsize']/2)
                Reds1=1
                Greens=math.floor(trial['setsize']/2)
                Reds2=math.floor(trial['setsize']/2)
        elif trial['present'] ==0:
            if trial['conjunct'] ==0:
            #Easy absent
                Ts=0
                Is=trial['setsize']
                Reds1=trial['setsize']
                Reds2=0
                Greens=0
            elif trial['conjunct'] ==1: 
                #Hard absent
                Ts=math.ceil(trial['setsize']/2)
                Is=math.floor(trial['setsize']/2)
                Reds1=0
                Greens=math.ceil(trial['setsize']/2)
                Reds2=math.floor(trial['setsize']/2)
        
        sstim1=np.repeat('T',Ts,axis=0)
        sstim2=np.repeat('I',Is,axis=0)
        sstim=np.concatenate((sstim1, sstim2), axis=0)
        
        #Create matrices to use for showing different colors in rgb space
        col1=np.matlib.repmat([1,0],int(Reds1),1)#one for the target, if present
        col2=np.matlib.repmat([0,1],int(Greens),1)
        col3=np.matlib.repmat([1,0],int(Reds2),1)
        col4=np.concatenate((col1,col2, col3), axis=0)
        
        #A fancy method for shuffling both letters and color together
        c = list(zip(sstim, col4))
        random.shuffle(c)
        sstim, col = zip(*c)
        #Make arrays that can be used to display stimuli at different positions
        xcoords=[0,-1, 1,-2,2,-3,3,-4,4]
        ycoords=[0,-1,1,-2,2,-3,3,-4,4]
        #Adapt display coordinates to the rowsize
        xcoords=xcoords[0:trial['rowsize']]
        ycoords=ycoords[0:trial['rowsize']]
        stim=[]
        counter=-1
        for xpos in xcoords:
            for ypos in ycoords:
                counter=counter+1
                coltemp=col[counter]
                stim = visual.TextStim(win=win, text=sstim[counter], pos=[xpos,ypos], height=textHeight,color=(coltemp[0], coltemp[1], 0), colorSpace='rgb')
                # Display image and monitor time
                stim.draw()
        time_flip=core.monotonicClock.getTime() #onset of stimulus
        for frame in range(trial['duration_frames']):
            win.flip(clearBuffer=False)          # Show the stimuli on next monitor update and ...
        win.clearBuffer()  #empty screen
        
        offset = core.monotonicClock.getTime()  # offset of stimulus
                   
        #Log time information
        trial['onset']=time_flip-exp_start
        trial['offset'] = offset-exp_start
        trial['duration_measured']=offset-time_flip
        
        # Log responses
        try:
            key, time_key = event.getKeys(keyList=('t','y','r','escape'), timeStamped=True)[0]# timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.

        except IndexError:  #if no responses were given, the getKeys function produces an IndexError
            trial['response']=''
            trial['key_t']=''
            trial['rt']=''
            trial['correct_resp']=''
         
        else: #if responses were given, find RT and correct responses
            trial['response']=key
            trial['key_t']=time_key-exp_start
            trial['rt'] = time_key-time_flip
            #check if responses are correct
            if trial['response']=='t':
                trial['correct_resp'] = 1 if trial['present']==1 else 0
            elif trial['response']=='y' or 'r':
                trial['correct_resp'] = 1 if trial['present']==0 else 0

            if key in KEYS_QUIT:  # Look at first reponse [0]. Quit everything if quit-key was pressed
                core.quit()
        
        # Save trials to csv file
        writer.write(trial) 
    


"""
DISPLAY INTRO TEXT AND AWAIT PARTICIPANT
"""    
textHeight=0.75 # height in degrees
introText1=[u'In this experiment you have to finde the red T',
                    u'',
                    u'Sometimes there is a red T, sometimes not',# some blanks here to create line shifts
                    u'Press T as fast as possible',
                    u'if the red T is present',
                    u'Press Y (righthanders) or R (lefthanders)',
                    u'if the red T is absent',
                    u'Press SPACE to start the experiment']

# Loop over lines in Intro Text1
ypos=6
xpos=0
for intro in introText1:
    ypos=ypos-1
    introText1 = visual.TextStim(win=win, text=intro, pos=[xpos,ypos], height=textHeight, alignHoriz='center')
    introText1.draw()
win.flip()          # Show the stimuli on next monitor update and ...


#Wait for SPACE to continue
event.waitKeys(keyList=KEYS_start)
stim = visual.TextStim(win=win,text='') #empty screen
stim.draw()
win.flip()
exp_start=core.monotonicClock.getTime()

""" CALL FUNCTION RUNNING THE EXPERIMENTAL LOOP"""

run_condition('visual_search')

""" END EXPERIMENT"""

textHeight=0.75 # height in degrees
endText1=[u'The experiment is over.',
                    u'',
                    u'Thank you for participating',# some blanks here to create line shifts
                    u'Press SPACE to end the experiment']

# Loop over lines in End Text1
ypos=2
xpos=0
for end in endText1:
    ypos=ypos-1
    endText1 = visual.TextStim(win=win, text=end, pos=[xpos,ypos], height=textHeight, alignHoriz='center')
    endText1.draw()
win.flip()          # Show the stimuli on next monitor update and ...

#Wait for SPACE to continue
event.waitKeys(keyList=KEYS_start)
core.quit()
