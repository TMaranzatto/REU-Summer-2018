import os
import numpy as np

filePathwayRead = os.path.expanduser("~/Desktop/surveyAnalysis/SurveyResponseEditedNice.txt")
filePathwayWrite = os.path.expanduser("~/Desktop/surveyAnalysis/Results.txt")

print("Reading file. . . ", filePathwayRead)
print("Writing to file. . . ", filePathwayWrite)

myfile = open(filePathwayRead, "r")
linelist = myfile.readlines()
myfile.close()

counter = 0
num = 0

#the twenty feelings on the PANAS assessment 
feelings = {'feeling1': 'Interested', 'feeling2': 'Distressed', 'feeling3': 'Excited', 'feeling4': 'Upset', 'feeling5': 'Strong', 'feeling6': 'Guilty', 'feeling7': 'Scared', 'feeling8': 'Hostile', 'feeling9': 'Enthusiastic', 'feeling10': 'Proud', 'feeling11': 'Irritable', 'feeling12': 'Alert', 'feeling13': 'Ashamed', 'feeling14': 'Inspired', 'feeling15': 'Nervous', 'feeling16': 'Determined', 'feeling17': 'Attentive', 'feeling18': 'Jittery', 'feeling19': 'Active', 'feeling20': 'Afraid'} 

participant_feelings = {}
twenty_feelings = {}
twenty_feelings_pre = {}
twenty_feelings_post = {}
platform = {}
infoList = []
#pre_panas_list was used to create standard deviation of participants answers
#This was to see if people picked extremes, or if people just picked 1 answer
#over and over again. Results ranged from 0.539 to 1.749
#pre_panas_list = []

#huge dictionary of the differences in Pre/Post PANAS feelings for each participant
for line in linelist:
    chunks = line.split(" ")
    for feeling in range(20):
        counter += 1
        first_num = chunks[2][num]
        #pre_panas_list.append(int(first_num))
        second_num = chunks[2][num+80]
        difference_in_nums = int(second_num) - int(first_num)
        print(difference_in_nums)
        twenty_feelings_pre[feelings['feeling'+str(counter)]] = first_num
        twenty_feelings_post[feelings['feeling'+str(counter)]] = second_num
        twenty_feelings[feelings['feeling'+str(counter)]] = difference_in_nums
        num += 4
        if counter == 20:
            num = 0
            counter = 0
    platform["viewing_platform"] = chunks[1][1:3]
    infoList = [platform, twenty_feelings, twenty_feelings_pre, twenty_feelings_post]
    participant_feelings[chunks[0]] = infoList
    #print("std " + str(round(np.std(pre_panas_list), 3)))
    twenty_feelings = {}
    twenty_feelings_pre = {}
    twenty_feelings_post = {}
    platform = {}
    infoList = []
    #pre_panas_list = []

counter = 0
feelingListVR = []
feelingListCM = []
#these were created to write graphs in Graph.py
averageListVR = []
averageListCM = []
STDVR = []
STDCM = []

total = 0

#writing to Response file
myfile2 = open(filePathwayWrite, "w")

for num in range(20): #loops through all of the emotions
    for num3 in range(1, 4): #loops through differences in PANAS values, PANAS Pre values, and PANAS Post values
        for num2 in range(31): #loops through all of the participants
            if num2+1 == 7:
                continue
            if participant_feelings[str(num2+1)][0]["viewing_platform"] == "VR":
                feelingListVR.append(int(participant_feelings[str(num2+1)][num3][feelings['feeling'+str(num+1)]]))
            if participant_feelings[str(num2+1)][0]["viewing_platform"] == "CM":
                feelingListCM.append(int(participant_feelings[str(num2+1)][num3][feelings['feeling'+str(num+1)]]))
    #we have made the long list of 3 sets of values: differences, pre, post
    #need to reset at this point as well as compute data/write to file
    counter1VR = 0
    counter2VR = 16
    counter1CM = 0
    counter2CM = 15
    writingTitles = ["Differences", "Pre-PANAS", "Post-PANAS"]
    for title in range(3):
        averageVR = sum(feelingListVR[counter1VR:counter2VR])/len(feelingListVR[counter1VR:counter2VR])
        aVR = np.array(feelingListVR[counter1VR:counter2VR])
        standardDeviationVR = np.std(aVR)
        #to create graphs in different script
        if counter1VR == 0:
            averageListVR.append(str(round(averageVR, 3)))
            STDVR.append(str(round(standardDeviationVR, 3)))
        myfile2.write("VR " + writingTitles[title] + " " + feelings['feeling'+str(num+1)] + "\nAverage: " + str(round(averageVR,3)) + "\nStandard Deviation: " + str(round(standardDeviationVR, 3)) + "\n\n")
        counter1VR += 16
        counter2VR += 16
    for title in range(3):
        averageCM = sum(feelingListCM[counter1CM:counter2CM])/len(feelingListCM[counter1CM:counter2CM])
        aCM = np.array(feelingListCM[counter1CM:counter2CM])
        standardDeviationCM = np.std(aCM)
        #to create graphs in different script
        if counter1CM == 0:
            averageListCM.append(str(round(averageCM,3)))
            STDCM.append(str(round(standardDeviationCM, 3)))
        myfile2.write("CM " + writingTitles[title] + " " + feelings['feeling'+str(num+1)] + "\nAverage: " + str(round(averageCM,3)) + "\nStandard Deviation: " + str(round(standardDeviationCM, 3)) + "\n\n")
        counter1CM += 15
        counter2CM += 15
    feelingListVR = []
    feelingListCM = []

myfile2.close()
print("Computing Complete!")
