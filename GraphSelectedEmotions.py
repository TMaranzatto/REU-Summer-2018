import plotly.plotly as py
import plotly
from plotly.graph_objs import *

"""
#Male Data
list1 = [-2.5, -0.833, -1.333, -0.833, 0.333] #VR Male Averages
list2 = [-0.333, -1.333, -1.333, -1.333, -0.667] #CM Male Averages
list3 = [1.258, 1.067, 1.374, 1.067, 1.491] #VR Male Standard Deviations
list4 = [0.816, 0.943, 0.943, 0.471, 0.943] #CM Male Standard Deviations
"""

#Female Data
list1 = [-1.667, -0.5, -2, -2.167, 0.167] #VR Female Averages
list2 = [-2, -1, -2.2, -1.8, 0.6] #CM Female Averaeges
list3 = [1.247, 1.118, 1.633, 1.462, 0.687] #VR Female Standard Deviations
list4 = [1.265, 0.632, 0.98, 1.47, 1.625] #CM Female Standard Deviations 

plotly.tools.set_credentials_file(username='ToriKraj', api_key='kbrQffinF25JfzOkSMil')

trace1 = {
    "x": ['Distressed', 'Excited', 'Upset', 'Irritable', 'Attentive' ],
    "y": list1,
    "error_y": {"array": list3},
    "name": "VR",
    "type": "bar",
    "uid": "629895"
}
trace2 = {
    "x": ['Distressed', 'Excited', 'Upset', 'Irritable', 'Attentive' ],
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



