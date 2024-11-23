from django.shortcuts import render,redirect
from django.db.models import Count
from .models import Report,Notes
from datetime import datetime,timedelta,date
from .forms import ReportForm, NoteForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import requests
# Create your views here.

#main page with all reports and charts

@login_required
def home(request):
    report = Report.objects.all()
    current_date = datetime.now()
    current_year= current_date.year
    current_month = current_date.month
    start_date = None
    end_date = None
    
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date_str = request.GET['start_date']
        end_date_str = request.GET['end_date']
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            # يتم رمي استثناء إذا كان التنسيق غير صحيح
            # يمكنك إضافة رسالة خطأ هنا أو تنفيذ إجراء آخر حسب الحاجة
            pass
    context={
       
        'current_date': current_date,
        'current_year':current_year,
        'current_month':current_month,
        'report':report,
        'ms' : Report.objects.filter(company='Egyptair').count,
        'ara' : Report.objects.filter(company='Arabia').count,
        'sau' : Report.objects.filter(company='Saudi airlines').count,
        'afr' : Report.objects.filter(company='Afriqya').count,
        'cai' : Report.objects.filter(company='Air Cairo').count,
    
    }
    return render(request,'pages/home.html',context)

@login_required
def report_list(request):
    reports = Report.objects.all()
    top_notes = Notes.objects.all()
    start_date = None
    end_date = None
    
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date_str = request.GET['start_date']
        end_date_str = request.GET['end_date']
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            # يتم رمي استثناء إذا كان التنسيق غير صحيح
            # يمكنك إضافة رسالة خطأ هنا أو تنفيذ إجراء آخر حسب الحاجة
            pass
        
        if start_date and end_date:
            reports = reports.filter(date__range=[start_date, end_date]).order_by('date')
            top_notes = Notes.objects.filter(report__date__range=[start_date, end_date]).values('notes').annotate(count=Count('notes')).order_by('-count')[:10]
            counts= reports.filter(date__range=[start_date, end_date]).count
            total_notes = Notes.objects.filter(report__date__range=[start_date, end_date]).count()
            cunt=reports.filter(date__range=[start_date, end_date]).count()
            
            for note in top_notes:
                percentage =((note['count'] / cunt) * 100) 
                
                note['percentage'] = round(percentage,ndigits=0)
        
    context = {'reports': reports, 'top_notes': top_notes,
                'start_date':start_date,'end_date':end_date,
                'counts':counts,
                'total_notes':total_notes,
                'top_notes':top_notes,
                
    
    }
    return render(request, 'pages/report_list.html', context)

@login_required
def report_details(request, pk):
    # احصل على تفاصيل تقرير معين بناءً على معرفه
    report = Report.objects.get(pk=pk)
    context = {'report': report}
    return render(request, 'pages/report_details.html', context)

@login_required
def add_report(request):
    eform=ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pages/add_flight.html',{'eform': eform})
        # redirect('/')
        
        else:
            # طباعة رسائل الخطأ في واجهة المستخدم
            print(form.errors)
    else:
        form = ReportForm()
    return render(request, 'pages/add_flight.html', {'form': form})


@login_required
def compare_reports(request):

    reports = Report.objects.all()
    top_notes_current = []
    top_notes_previous = []
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # الفترة المطلوبة في العام الحالي
        reports_current = reports.filter(date__range=[start_date, end_date])
        top_notes_current = Notes.objects.filter(report__date__range=[start_date, end_date]).values('notes').annotate(count=Count('notes')).order_by('-count')[:4]
        total_notes_current = reports.filter(date__range=[start_date, end_date]).count()
        
        # الفترة المطلوبة في العام السابق
        start_date_previous = start_date - timedelta(days=365)  # 365 يومًا = سنة واحدة
        end_date_previous = end_date - timedelta(days=365)
        reports_previous = reports.filter(date__range=[start_date_previous, end_date_previous])
        top_notes_previous = Notes.objects.filter(report__date__range=[start_date_previous, end_date_previous]).values('notes').annotate(count=Count('notes')).order_by('-count')[:4]
        total_notes_previous = reports.filter(date__range=[start_date_previous, end_date_previous]).count()
        
        # مقارنة النسبة بين العامين
        for note_current, note_previous in zip(top_notes_current, top_notes_previous):
            note_current['percentage'] = round((note_current['count'] / total_notes_current) * 100 )
            note_previous['percentage'] =round((note_previous['count'] / total_notes_previous) * 100 ) 
            note_current['improvement_percentage'] = round(note_current['percentage'] - note_previous['percentage'])
    
    context = {'reports_current': reports_current, 'top_notes_current': top_notes_current,
               'reports_previous': reports_previous, 'top_notes_previous': top_notes_previous,
               'start_date':start_date,'start_date_previous':start_date_previous,
               
               
               }
    return render(request, 'pages/compare_reports.html', context)

@login_required
def add_note(request):
    eform=NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pages/note.html',{'eform': eform})
        # redirect('/')
        
        else:
            # طباعة رسائل الخطأ في واجهة المستخدم
            print(form.errors)
    else:
        form = NoteForm()
    return render(request, 'pages/note.html', {'form': form})

