#Import all neccessary features to code.
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import random

def playSequence(seq):
    note = 0
    for i in seq :
        print(i)
        #if fraction set note length
        if not isinstance(i, int) :
            note = i
        #next, if not an on or off must be tempo!
        elif i > 1 :
            tempo = i
        else :
            playNote(i, tempo, note)
        
def playNote(on, tempo, note):
    #say tempo at 90 2/3 * 1/8 = 1/6 of a second
    duration = (60/tempo) * note
    # if note length is to short to hear strike 
    if duration < 0.2 :
        duration = 0.2
    if on:
        #Turns Relay On. Brings Voltage to Min GPIO can output ~0V.
        GPIO.output(18, 0)
        #10ms on
        strike = 0.1
        sleep(strike)
        GPIO.output(18, 1)
        if duration - strike == 0 :
            sleep(duration)
        else :
            sleep(duration-strike)
    else :
        sleep(duration)

#If code is stopped during active it will stay active
#This may produce a warning if restarted, this
#line prevents that.
GPIO.setwarnings(False)
#This means we will refer to the GPIO
#by the number after GPIO.
GPIO.setmode(GPIO.BCM)
#This sets up the GPIO 18 pin as an output pin
GPIO.setup(18, GPIO.OUT)

#Broken into quarter notes, 1 = note 0 = rest
#Lets do 2 bar first value represents note length
seqs = [
    [1/8, 80, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1/8, 60, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
    [1/8, 80, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1/8, 60, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0],
    
    #[1/4, 90, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    #[1/4, 90, 1, 0, 0, 1, 0, 0, 0, 1],
    #[1/4, 40, 1, 0, 0, 1, 1, 0, 1, 1],
    #[1/4, 60, 1, 0, 1, 0, 0, 0, 1, 0],
    #[1/4, 60, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0]
]
#How many dings? get hour
hour = datetime.now().hour
#starts at 6 ends at 10
half_hour  = ( 29 <= datetime.now().minute <= 59 ) 
chosen_seq = ((hour - 2) % 4)
# chosen_seq = random.randint(0, len(seqs)-1)
reps = 4
if half_hour :
    reps = reps - 2
# chosen_seq = 0
seq = seqs[chosen_seq]

for i in range(reps):
    playSequence(seq)
    #sleep(1)
    
#This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
GPIO.output(18, 1)
    
