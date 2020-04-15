from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
# Include the `fusioncharts.py` file that contains functions to embed the charts.

from .fusioncharts import FusionCharts



import pandas as pd
import numpy as np

df = pd.read_excel('fusioncharts/data/covid_19_data_switzerland.xlsx') 

def myFirstChart(request):
    # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "COVID-Cases in Switzerland"
    chartConfig["subCaption"] = "Peoples died of covid per canton"
    chartConfig["xAxisName"] = "canton"
    chartConfig["yAxisName"] = "fatalities"
    chartConfig["numberSuffix"] = "K"
    chartConfig["theme"] = "fusion"

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    for canton, value in zip(df.columns[1:], df.iloc[-3, 1:].values): 
        if pd.isnull(value):
            continue
        if canton == 'CH':
            continue
        dataSource["data"].append({"label": canton, "value": str(value)})

    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)
    return render(request, 'index.html', {
        'output': column2D.render()}
    )