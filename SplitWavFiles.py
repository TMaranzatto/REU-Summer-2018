"""
File Name:      splitter.py

Author Name:    Jordan Edward Shea <https://github.com/JShea232>

Revised By: Victoria Kraj

Revision Date:   07/31/18 

Description:    This script splits a given WAV file into smaller WAV files, which will ideally be given to a
                transcription service like IBM Watson for annotation. By default, the maximum duration for each
                split file is 20 seconds, but this can be modified depending on the task at hand.

                In addition to splitting files, this script will also notify the user about relevant statistics
                regarding their submitted WAV file (e.g. number of channels, duration, sample rate, bit rate, file
                size, etc).

                After a WAV file is split into smaller files, these smaller files are then stored within the
                Montreal Forced Aligner directory.
"""

import math
import os
import warnings
from GSRTimes import participantGSRTimeDict as theDict 

warnings.filterwarnings("ignore")  # Suppresses a warning thrown by the pydub package

from pydub import AudioSegment

"""
analyzeWindows is the number of windows wanted to be analyzed, should be int
windowDuration in seconds
startTimes is an array of the starting times in milliseonds
"""

def split_wav(participant, analyzeWindows, windowDuration, startTimes):
    filePathwayRead = os.path.expanduser("~/Desktop/SilenceTracker/TrimmedAudioFiles/Participant"+str(participant)+"Trim.wav")
    print("Opening participant " + str(participant) + " file. . . " + filePathwayRead)
    original_audio = AudioSegment.from_file(filePathwayRead)
    print("Duration: " + str(round(original_audio.duration_seconds, 2)))
    name = "Participant" + str(participant) + "Split"
    newDestination = "SplitFiles/" + name
    
    for i in range(analyzeWindows):

        #creating start and end times for clipping
        start = (int(startTimes[i]) - 5000) #decided I wanted to look 5 seconds before the given time value
        end = start + (windowDuration * 1000)

        # This "splits" the WAV file based on two indices
        small_wav = original_audio[start:end]

        # File names continually increment upwards
        newName = name + "_" + str(i + 1)

        # Makes a new folder for each subjects' split WAV files
        if not os.path.exists(newDestination):
            os.makedirs(newDestination)

        newFile = newDestination + "/" + newName + ".wav"
        small_wav.export(newFile, format="wav")

    print(name + ".wav has been successfully split into " + str(analyzeWindows) + " new files that are " + str(windowDuration) + " sec each...")

    return analyzeWindows

def automate():
    for participant in theDict:
        timeList = []
        if theDict[participant] == [] or participant == 11:
            continue
        else:
            for index in range(0, len(theDict[participant])): 
                timeList.append(theDict[participant][index][0]*1000) #multiply by 1000 to get into milliseconds for usage with split_wav function
            split_wav(participant, len(theDict[participant]), 15, timeList)

automate()

"""
To run I need:
    -  the number of time windows we are analyzing
    -  the duration size of these windows
    -  an array of the start times of these windows
"""

