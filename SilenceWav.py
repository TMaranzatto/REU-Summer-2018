from pylab import *
import pylab
from scipy.io import wavfile
import os
import more_itertools as mit

soundTime = []
participantSoundTime = {}

counter = 0
threshold = 1000

#obtaining file
for num in range(1, 33):
    if num == 11 or num == 13 or num == 14 or num == 16 or num == 21 or num == 22 or num == 26 or num == 27:
        continue
    else:
        filePathwayRead = os.path.expanduser("~/Desktop/SilenceTracker/TrimmedAudioFiles/Participant"+str(num)+"Trim.wav")
        sampFreq, theSoundFile = wavfile.read(filePathwayRead)
        print("Opening participant " + str(num) + " file. . . " + filePathwayRead)
    for index, amp in enumerate(theSoundFile):
        if index % 10 == 0: 
            if abs(amp) > threshold:
                theSecond = round(index/100000, 0)
                if counter == 0: #starting counter
                    previousSecond = theSecond
                    counter += 1
                elif theSecond == 0:
                    if num == 15:
                        continue
                    threshold+=100
                elif theSecond == previousSecond: #continuing counter if the current time second is equal to the previous
                    counter += 1
                else:
                    if counter > 50: #threshold being that if there are 50 .00001 seconds with sound
                        soundTime.append(previousSecond) #appending a list of the times (s) a participant spoke
                    counter = 0
    if previousSecond > theSecond:
        participantSoundTime[str(num)-1].append(previousSecond)
    participantSoundTime[str(num)] = soundTime #adding completed list of times to a dictionary where participant # is key
    soundTime = []
    threshold = 1000 

print(participantSoundTime)

#if you want to see graphs of soundwave

#timeArray = (arange(0, theSoundFile.shape[0], 1)/sampFreq)
#plot(timeArray, theSoundFile, color='k')
#ylabel('Amplitude')
#xlabel('Time (s)')
#pylab.show()
