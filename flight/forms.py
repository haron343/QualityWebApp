from django import forms
from django.forms import ModelForm
from .models import Report, Notes


class ReportForm(forms.ModelForm):
    # Notess = forms.ModelMultipleChoiceField(queryset=Notes.objects.all(), widget=forms.CheckboxSelectMultiple)
    date=forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date','placeholder':'yyyy-mm-dd (DOB)','class':'form-control col-sm-4 col-lg'}))
    time=forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type':'time','class':'form-control'}))
    
    
    class Meta:
        model = Report
        # fields='__all__'
        fields = [
                'date',
                'time',
                'company',
                'flight_number',
                'f_from',
                'f_to',
                'stand',
                'carrier_reg',
                'carrier_type',
                'statues',
                'author',
                'observations'
                
                ]
        widgets={
            'company':forms.TextInput(attrs={'type':'text','placeholder':'Carrier','class':'form-control row col-sm-4 col-lg'}),
            'flight_number':forms.TextInput(attrs={'type':'text','placeholder':'Flight Number','class':'form-control'}),
            'f_from':forms.TextInput(attrs={'type':'text','placeholder':'Flight from','class':'form-control'}),
            'f_to':forms.TextInput(attrs={'type':'text','placeholder':'Flight to','class':'form-control'}),
            'stand':forms.TextInput(attrs={'type':'text','placeholder':'stand','class':'form-control'}),
            'carrier_reg':forms.TextInput(attrs={'type':'text','placeholder':'Rigester','class':'form-control'}),
            'carrier_type':forms.TextInput(attrs={'type':'text','placeholder':'Type','class':'form-control'}),
            'statues':forms.Select(attrs={'class':'form-control',} ),
            'author':forms.Select(attrs={'class':'form-control'}),
            'observations':forms.CheckboxSelectMultiple(choices=(Notes.objects.all()))
            

            
        }

class NoteForm(forms.ModelForm):
    
    class Meta:
        model = Notes
        fields='__all__'
        widgets={
            'notes':forms.TextInput(attrs={'type':'text','placeholder':'Add-Note','class':'form-control row col-sm-4 col-lg'}),
        }