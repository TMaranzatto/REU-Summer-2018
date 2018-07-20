from pylab import *
import pylab
from scipy.io import wavfile
import os
import more_itertools as mit



def find_ranges(iterable):
    """Yield range of consecutive numbers."""
    for group in mit.consecutive_groups(iterable):
        group = list(group)
        if len(group) == 1:
            yield 1000 * group[0], 1000 + 1000 * group[0]
        else:
            yield 1000* group[0], 1000 + 1000*group[-1]

def signalAboveThresh(audioSnip, threshold):
    continuousSignal = True
    #list comprehension from current position to 50 places out
    for amp in audioSnip:
        if amp < threshold:
                #if our amplitude drops below threshold, our signal is not continuous
                continuousSignal = False
                break
    #only append to list if this is true!!!!
    return continuousSignal

def singleParRange(num):
        soundTime = []
        counter = 0
        maxCount = 50
        threshold = 1000
    
     #tori path:
        filePathwayRead = os.path.expanduser("~/Desktop/SilenceTracker/TrimmedAudioFiles/Participant"+str(num)+"Trim.wav")
        #Jake path, just comment this out for the code to work on your end.  
        filePathwayRead = os.path.expanduser("C:/Users/Jake From State Farm\Desktop/TrimmedAudioFiles/Participant"+str(num)+"Trim.wav")
        sampFreq, theSoundFile = wavfile.read(filePathwayRead)
        print("Opening participant " + str(num) + " file. . . " + filePathwayRead)
            
        for index, amp in enumerate(theSoundFile):
            #checking every 10th ms
            if index % 10 == 0:
                
                if abs(amp) > threshold:
                    theSecond = round(index/100000, 0)
                    
                    #checking if our second is already in the list.  Should speed things up considerably
                    if theSecond in soundTime:
                        continue
                    
                    elif signalAboveThresh(theSoundFile[index: index + maxCount], threshold) == True:
                        soundTime.append(theSecond)
                            
        #Changing the list format
        return list(find_ranges(soundTime))

    
#obtaining file
def getParRanges():
    
    participantSoundTime = {}

    for num in range(1, 4):
        if num == 11 or num == 13 or num == 14 or num == 16 or num == 21 or num == 22 or num == 26 or num == 27:
            continue
        else:
        #adding completed list of times to a dictionary where participant # is key      
            participantSoundTime[str(num)] = singleParRange(num)
            #resetting everything
        
    return participantSoundTime


print(getParRanges())
#if you want to see graphs of soundwave

#timeArray = (arange(0, theSoundFile.shape[0], 1)/sampFreq)
#plot(timeArray, theSoundFile, color='k')
#ylabel('Amplitude')
#xlabel('Time (s)')
#pylab.show()
