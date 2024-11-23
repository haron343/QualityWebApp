from django.http import HttpResponse
import pandas as pd
from .models import Report
from django.shortcuts import render

def test(request):
    data=Report.objects.values('company','date')
    df = pd.DataFrame(list(data))
    df=pd.DataFrame.from_records(data).describe()
    
    return HttpResponse(df)

