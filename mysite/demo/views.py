from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Avg
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from .models import *
from qsstats import QuerySetStats
from django.utils import timezone
#from .populatedb import
from time import mktime

def home(request):
    ##Receives all snr and temp data, structure it to a 
    series = {'snr': [],'temp': []}
    #SNR
    tag_filter = tagDetection.objects.all() #TODO: Actually filter, based on timeframe
    for i in range(0, len(tag_filter)):
        series['snr'].append([tag_filter[i].timestamp,tag_filter[i].snr])
    #Temperature
    tbr_filter = TBRsensorData.objects.all()
    for i in range(0, len(tbr_filter)):
        series['temp'].append([tbr_filter[i].timestamp,float(tbr_filter[i].temp)])
    
    return render(request, 'demo/home_test.html', {'series': series})
        
