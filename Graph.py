import plotly.plotly as py
import plotly
from plotly.graph_objs import *
import surveyAnalysis as sa

list1 = sa.averageListVR
list2 = sa.averageListCM
list3 = sa.STDVR
list4 = sa.STDCM

print(len(list1))
print(len(list2))


plotly.tools.set_credentials_file(username='pA1nt1tblAck', api_key='rqy813x2YekWfh0ERUWu')

trace1 = {
    "x": ['Interested', 'Distressed', 'Excited', 'Upset', 'Strong', 'Guilty', 'Scared', 'Hostile', 'Enthusiastic', 'Proud', 'Irritable', 'Alert', 'Ashamed', 'Inspired', 'Nervous', 'Determined', 'Attentive', 'Jittery', 'Active', 'Afraid' ],
    "y": list1,
    "error_y": {"array": list3},
    "name": "VR",
    "type": "bar",
    "uid": "629895"
}
trace2 = {
    "x": ['Interested', 'Distressed', 'Excited', 'Upset', 'Strong', 'Guilty', 'Scared', 'Hostile', 'Enthusiastic', 'Proud', 'Irritable', 'Alert', 'Ashamed', 'Inspired', 'Nervous', 'Determined', 'Attentive', 'Jittery', 'Active', 'Afraid' ],
    "y": list2,
    "error_y": {"array": list4},
    "name": "Computer Monitor",
    "type": "bar",
    "uid": "629895"
}
data = Data([trace1, trace2])
layout = {
  "autosize": True, 
  "height": 536, 
  "title": "Changes in PANAS Score from Watching a Performance", 
  "width": 1099, 
  "xaxis": {
    "title": "Rated Emotions"
  }, 
  "yaxis": {
    "autorange": False, 
    "range": [-4, 3], 
    "title": "Average of Change in Emotion", 
    "type": "linear"
  }
}
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)

