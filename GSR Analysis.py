#engagement while immersed in a virtual world

##look at facial analysis engagement, suprise, excitement
##look at pulse
##command + space -- 'managed software center' -- install

#what do we need to do
#1- get top n gsr peaks from each participant
#DONEDONE
#2- do analysis on data in a 20 second window around the top n peaks
#3- transplant this analysis into the excel sheet

#building blocks for first goal

#make box and whisker plot
#get gsr baseline



# get first and second half gsr values across groups
import openpyxl
import pandas as pd
from openpyxl import load_workbook
import os
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#importing the workbook.  Change this filepath for where the data is on your machine.
wb = openpyxl.load_workbook('C:\\Users\\Jake From State Farm\\Desktop\\Peaks pr respondent.xlsx')
data_folder = 'C:/Users/Jake From State Farm/AppData/Local/Programs/Python/Python36-32/Sensor Data'
sheet = wb['Peaks pr respondent']

####################################DEPRECATED########################################
###generic function that can work for times, amplitudes, etc.
##def getSinglePeak(val_list, participant):
##    value = 0
##    for val in val_list:
##        if val > value:
##            value = val
##    return value
##
##def peakToTime(val, participant):
##    for cell in sheet['E']:
##        if cell.value == ('Participant ' + str(participant)):
##            row = cell.row
##            if sheet['L' + str(row)].value == val:
##                return sheet['J' + str(row)].value
##    return(-1)
##
##def getAnalysisRange(value):
##    if value == -1:
##        return (-1, -1)
##    min_time = 0
##    #need to update this later, this is just placeholder
##    max_time = 336000
##    lower_bound = max(min_time, value - 10000)
##    upper_bound = min(max_time, value + 10000)
##    return (lower_bound, upper_bound)
##
##
###returns the highest peak amplitudes for each participant in a dictionary format {participant: peaks}
##def getPeaks(participant, num_of_peaks):
##    value_list = []
##    for cell in sheet['E']:
##        if cell.value == ('Participant ' + str(participant)):
##            row = cell.row
##            value_list.append(sheet['L' + str(row)].value)
##
##    peak_list = []
##    for i in range(num_of_peaks):
##        temp_val = getSinglePeak(value_list, participant)
##
##        if len(value_list) == 0:
##            peak_list.append(-1)
##
##        else:
##            peak_list.append(temp_val)
##            value_list.remove(temp_val)
##
##    return {participant: peak_list}
##
##
##def getAllPeaks(num_of_peaks):
##    #assumming we have 32 participants..
##    peak_list_complete = {}
##    for i in range(1, 33):
##        temp_peaks = getPeaks(i, num_of_peaks)
##        peak_list_complete.update(temp_peaks)
##
##    return peak_list_complete
##
##def getAllTimes(num_of_peaks):
##    #this first implementation works with the overanalyze paradigm we discussed
##    #will try the other implementation after this works
##    peak_dict = getAllPeaks(num_of_peaks)
##    for i in range(1, 33):
##        peak_dict[i] = [getAnalysisRange(peakToTime(x, i)) for x in peak_dict[i]]
##    #peak_dict = {x: getAnalysisRange(x) for x in peak_dict}
##    return peak_dict

###########################################################################
#################GETTING HEARTRATE DERIVATIVE#############################
###########################################################################

#yvals is a list or tuple of 2 values
def getSlope(yvals, xdist):
    return (yvals[1] - yvals[0]) / xdist

#many_yvals is a list of arbitrary size
def getDerivative(many_yvals, xdist):
    #returns a list, may make it just write to file to save memory
    deriv = []
    previous = 0
    for v in many_yvals:
        if v != None and v > 0:
            deriv.append(getSlope((previous, v), xdist))
            previous = v
        else:
            deriv.append(0)
            previous = 0

    deriv_dict = {}
    for i, d in enumerate(deriv):
        if d != 0:
            #making dictionary of structure {time(ms) : derivitive}
            #this shows us when the derivitive changes and by how much
            deriv_dict[i] = d
    return deriv_dict

def getSingleDer(file, xdist):
        data = []
        path = data_folder + '/' +  file
        wrkbk = load_workbook(filename=path)
        sheet = wrkbk.sheetnames[0]
        sheet = wrkbk[sheet]

        prev = 0
        for cell in sheet['FJ']:
            try:
                cell.value += 1
            except TypeError:
                continue
            data.append(cell.value)
        print(data[0])
        return getDerivative(data, xdist)

def getAllDer(xdist):
        #this may complain about double \\ in data_folder dir name
        for file in os.listdir(data_folder):
                getSingleDer(file, 1)
                
if 0:
    min_to_ms = 1.66 * (10**-5)
    print(getSingleDer('001_Participant 1.xlsx', 1))

###########################################################################
########################FINDING GSR PEAKS##################################
###########################################################################


performance_length = 336000
def makeBins(n_bins):
    bin_length = performance_length / n_bins
    bins = []
    cur_val = 0
    for i in range(n_bins):
        bins.append((cur_val, cur_val + bin_length))
        cur_val += bin_length
    return bins

def getCondition(participant):
    #0 for monitor, 1 for VR
     for cell in sheet['E']:
        if cell.value == ('Participant ' + str(participant)):
            row = cell.row
            if sheet['H' + str(row)].value == 'Virtual Reality':
                return 1
            else:
                return 0


def isPeak(participant, time_range, activation_threshold,single_or_total):
    #time_range is a 2-tuple, like how makeBins outputs
    val = 0
    for cell in sheet['E']:
        if cell.value == ('Participant ' + str(participant)):
            row = cell.row
            #checking if peakMs is within time_range
            if sheet['K' + str(row)].value > time_range[0] and sheet['k' + str(row)].value < time_range[1]:
                if sheet['L' + str(row)].value > activation_threshold:
    #data is returned as (peak signal, study group) tuple
                    if single_or_total == 0:
                        return 1
                    else:
                        val += 1
    if single_or_total == 0:
        return 0
    else:
        return val

def histogramData(condition, activation_threshold, n_bins, single_or_total):
    #loop through participants
    bins = makeBins(n_bins)
    data = [0 for x in range(len(bins))]
    for participant in range(1, 33):
        #check if we are in the right condition
        if getCondition(participant) == condition:
            for j in range(len(bins)):
                data[j] += isPeak(participant, bins[j], activation_threshold, single_or_total)
    return data


if 0:
    ##PARAMETERS##
    single_or_total = 0
    timestep = 10
    threshold = 0.25
    ################

    my_bins = int(336/timestep)
    x1 = histogramData(1, threshold, my_bins, single_or_total)
    x2 = histogramData(0, threshold, my_bins, single_or_total)
    bar_width = .3* timestep

    bins = makeBins(my_bins)
    y1 = [int(i[0] / 1000) for i in bins]
    y2 = [i + bar_width for i in y1]

    ##y1 = [i for i in range(my_bins)]
    ##y2 = [i + bar_width for i in y1]


    error_config = {'ecolor': '0.3'}

    fig, ax = plt.subplots()
    opacity = 0.4
    rects1 = ax.bar(y1, x1, bar_width, error_kw=error_config, label='VR')
    rects2 = ax.bar(y2 , x2, bar_width, error_kw=error_config, label='Monitor')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Participant Peaks (Threshold = ' + str(threshold) + ')')
    ax.set_title('GSR Peaks per ' + str(timestep) + ' Second Bin')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend()

    fig.tight_layout()
    plt.show()



###print(getCondition(1))
###print(makeBins(10))
##bins = int(336/10)
##thresholds = [.25, .5, .75]
##for i in range(len(thresholds)):
##    print('monitor condition with threshold of ' + str(thresholds[i]) + ' ' + str(histogramData(0, thresholds[i], bins)))
##    print('VR condition with threshold of ' + str(thresholds[i]) +  ' ' + str(histogramData(1, thresholds[i], bins)))

###########################GSR MEAN SCORES###########################################
##using pandas library here, trying out different libraries to see which ones i prefer


def getSingleGSRAvg(file, startTIme, endTime):
        path = data_folder + '/' +  file
        df = pd.read_excel(path, header = None, usecols = [167])
        vals = df.iloc[startTIme:endTime].mean()
        try:
            print(vals[0])
            return vals[0]
        except:
            print(-1)
            return -1

def getAllAvg(startTIme, endTime, condition):
        #this may complain about double \\ in data_folder dir name
        arr = []
        for i, file in enumerate(os.listdir(data_folder)):
                if getCondition(i) == condition:
                    arr.append(getSingleGSRAvg(file, startTIme, endTime))
        return arr
    
print(getAllAvg(5, 10000, 0))







