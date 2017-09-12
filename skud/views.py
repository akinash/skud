from django.shortcuts import render_to_response
import datetime

def hello(request):
    now = datetime.datetime.now()
    name = 'ARTEM'
    return render_to_response('date/current_datetime.html', locals())