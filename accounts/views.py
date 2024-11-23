from django.shortcuts import HttpResponse, render,redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def signup(request):
   if request.method=='POST':
      form=UserCreationForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('/flights')
   
   context={
      'form':form,
   }
   return render(request,'registration/signup.html',context)

