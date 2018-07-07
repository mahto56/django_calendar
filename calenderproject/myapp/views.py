from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Entry
from .forms import EntryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(req):
    if req.user.is_authenticated:
        return HttpResponseRedirect("/calendar")
    return render(req,'myapp/index.html')

@login_required  
def calender(req):
    entries = Entry.objects.filter(author=req.user)
    return render(req,'myapp/calender.html',{'entries':entries})
    
@login_required  
def details(request, pk):
    entry = Entry.objects.get(id=pk)
    return render(request,'myapp/details.html',{'entry':entry})

@login_required  
def add(req):
    if req.method == 'POST':
        form = EntryForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            
            description = form.cleaned_data['description']
            
            Entry.objects.create(
                name=name,
                date=date,
                author = req.user,
                description=description,
            ).save()
            
            return HttpResponseRedirect("/calendar")
    else:
        form = EntryForm()
        
    return render(req,'myapp/form.html',{'form':form})

@login_required  
def delete(req,pk):
    if req.method == 'DELETE':
        entry = get_object_or_404(Entry,pk=pk)
        entry.delete()
        
    return HttpResponseRedirect('/')

def signup(req):
    if req.method== 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(req,user)
            return HttpResponseRedirect('/calendar')
    else:
        form = UserCreationForm()
        
    return render(req,'registration/signup.html',{'form':form})
