# -*- coding: utf-8 -*-
""" DESCRIPTION:
An experiment for investigating system 1 and system 2 emotions.
Participants view images and judge whether they have any emotional content.
20 images are system 1
20 are system 2
40 are neutral

/Mikkel Wallentin 2017 (with most of the code adapted from Jonas LindeLoev: https://github.com/lindeloev/psychopy-course/blob/master/ppc_template.py)

Structure: 
    SET VARIABLES
    GET PARTICIPANT INFO USING GUI
    SPECIFY TIMING AND MONITOR
    STIMULI
    OUTPUT
    FUNCTIONS FOR EXPERIMENTAL LOOP
    DISPLAY INTRO TEXT AND AWAIT PARTICIPANT
    CALL FUNCTION RUNNING THE EXPERIMENTAL LOOP

"""

# Import the modules that we need in this script
from __future__ import division
from psychopy import core, visual, event, gui, monitors
import ppc
import glob
import random
import numpy as np
"""
SET VARIABLES
"""
# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor 
MON_WIDTH = 34  # Width of your monitor in cm
MON_SIZE = [1440, 900]  # Pixel-dimensions of your monitor
FRAME_RATE=60 # Hz
SAVE_FOLDER = 'emotion_systems_data'  # Log is saved to this folder. The folder is created if it does not exist.


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
win = visual.Window(size=(1100, 800),monitor=my_monitor, units='deg', fullscr=False, allowGUI=False, color='#404040')  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

#Prepare Fixation cross
stim_fix = visual.TextStim(win, '+')#, height=FIX_HEIGHT)  # Fixation cross is just the character "+". Units are inherited from Window when not explicitly specified.
"""
STIMULI

"""
#EXPERIMANTAL DETAILS

#iMAGE FILES
img_neu = glob.glob("images_neutral/neutral_*") 
img_tp1 = glob.glob("images_type1_emotion/type1_*")
img_tp2 = glob.glob("images_type2_emotion/type2_*")

all_stimuli = img_neu + img_tp1 + img_tp2

catN=np.repeat('N',len(img_neu),axis=0)
catTp1=np.repeat('tp1',len(img_tp1),axis=0)
catTp2=np.repeat('tp2',len(img_tp2),axis=0)
categories=np.concatenate((catN, catTp1,catTp2), axis=0)

#random.shuffle(all_stimuli)
delay=(1*FRAME_RATE)
dur=int(2*FRAME_RATE) # duration in seconds multiplied by 60 Hz and made into integer
condition='emotion_systems' #Just a variable. If the script can run several exp. then this can be called in GUI. Not relevant here.

# The image size and position using ImageStim, file info added in trial list sbelow.
stim_image = visual.ImageStim(win,  # you don't have to use new lines for each attribute, but sometime it's easier to read that way
     mask=None)
     #size=(10,10))

""" 
OUTPUT 
"""

#KEYS
KEYS_emotion =['e']#T is response key for target present.
KEYS_neutral =['w','r']#Y and R (present next to T) are response key for target absent. One can be used for righthanders, the other for lefthanders

#response keys for quitting and starting
KEYS_QUIT = ['escape']  # Keys that quits the experiment
KEYS_start=['space'] # press space to start
   # Prepare a csv log-file using the ppc script
writer = ppc.csvWriter(str(V['ID']), saveFolder=SAVE_FOLDER)  # writer.write(trial) will write individual trials with low latency

""" FUNCTIONS FOR EXPERIMENTAL LOOP"""

def make_trial_list(condition):
# Factorial design
    trial_list = []
    for i, image in enumerate(all_stimuli): # images
                    # Add a dictionary for every trial
                    trial_list += [{
                        'ID': V['ID'],
                        'age': V['age'],
                        'gender': V['gender'],
                        'condition': condition,
                        'img': image, #image file
                        'onset':'' ,# a place to note onsets
                        'offset': '',
                        'duration_measured':'',
                        'duration_frames': dur,
                        'delay_frames': delay,
                        'category': categories[i],                       
                        'emotion_judge':'',                        
                        'response': '',
                        'key_t':'',
                        'rt': '',
                    }]
#    for cat in categories: # add category info
#        trial_list += [{
#            'category': cat,
#        }]
      
   # Randomize order
    from random import sample
    trial_list = sample(trial_list, len(trial_list))

    # Add trial numbers and return
    for i, trial in enumerate(trial_list):
        trial['no'] = i + 1  # start at 1 instead of 0
        if i is 0:
            writer.writeheader(trial) # An added line to give headers to the log-file (see ppc.py)
    return trial_list
    



    
def run_condition(condition):
    """
    Runs a block of trials. This is the presentation of stimuli,
    collection of responses and saving the trial
    """    
    
    # Loop over trials
    for trial in make_trial_list(condition):
        for frame in range(trial['delay_frames']):
            stim_fix.draw()
            win.flip()
        event.clearEvents(eventType='keyboard')# clear keyboard input to make sure that no responses are logged that do not belong to stimulus
        key=[]# Prepare image
        stim_image.image = trial['img']

        # Display image and monitor time
        time_flip=core.monotonicClock.getTime() #onset of stimulus
        for frame in range(trial['duration_frames']):
            if len(key)==0:
                stim_image.draw()
                win.flip()
            else:
                stim_fix.draw()
                win.flip()
            try:
                key, time_key = event.getKeys(keyList=('e','r','w','escape'), timeStamped=True)[0]# timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.
    
            except IndexError:  #if no responses were given, the getKeys function produces an IndexError
                if not trial['rt'] >0:                
                    trial['response']=''
                    trial['key_t']=''
                    trial['rt']=''
             
            else: #if responses were given, find RT and correct responses
                trial['response']=key
                trial['key_t']=time_key-exp_start
                trial['rt'] = time_key-time_flip
                #check if responses are correct
                if trial['response']=='e':
                    trial['emotion_judge'] = 1
                elif trial['response']=='r' or 'w':
                    trial['emotion_judge'] = 0
    
                if key in KEYS_QUIT:  # Look at first reponse [0]. Quit everything if quit-key was pressed
                    core.quit()

        # Display fixation cross
        offset = core.monotonicClock.getTime()  # offset of stimulus
        # Get actual duration at offset
                   

        #Log values
        trial['onset']=time_flip-exp_start
        trial['offset'] = offset-exp_start
        trial['duration_measured']=offset-time_flip


        # Save trials to csv file
        writer.write(trial) 
        print trial
 
"""
DISPLAY INTRO TEXT AND AWAIT PARTICIPANT
"""    
textHeight=0.75 # height in degrees
introText1=[u'In this experiment you have to judge',
                    u'if the images contain something emotional.',
                    u'Sometimes it is obvious, sometimes subtle',# some blanks here to create line shifts
                    u'Press E as fast as possible',
                    u'if the image is EMOTIONAL',
                    u'Press R (righthanders) or W (lefthanders)',
                    u'if the image is NEUTRAL',
                    u'',
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

run_condition('emotion_systems')

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