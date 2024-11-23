from django.urls import path
from flight import views


app_name = 'reports'

urlpatterns = [
    
    path('',views.home,name='home'),
    path('details/<int:pk>/', views.report_details, name='details'),
    path('add_report/',views.add_report,name='add_report'),
    path('list/', views.report_list, name='report_list'),
    path('compare-reports/', views.compare_reports, name='compare_reports'),
    path('note/', views.add_note, name='add_note'),
]
