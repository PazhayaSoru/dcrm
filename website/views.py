from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record

# Create your views here.


def home(request):
  records = Record.objects.all()

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    #authenticate 

    user = authenticate(request,username=username,password = password)
    if user is not None:
      login(request,user)
      messages.success(request,'You have been logged In')
      return redirect('home')
    else:
      messages.success(request,'There was an error logging In..')
      return redirect('home')
  else:
    return render(request,'website\home.html',{'records':records})

def login_user(request):
  pass

def logout_user(request):
  logout(request)
  messages.success(request,'You have been logged out...')
  return redirect('home')

def register_user(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      #authenticate and login
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username,password=password)
      login(request,user)
      messages.success(request,'You have successfully created an Account')
      return redirect('home')
  else:
    form = SignUpForm()
    return render(request,'register.html',{'form':form})
  return render(request,'register.html',{'form':form})


def customer_record(request,pk):
  if request.user.is_authenticated:
    record = get_object_or_404(Record,id=pk)
    return render(request,'record.html',{'record':record})
  else:
    messages.success(request,'You must be logged in to view Records')
    return redirect('home')

def delete_record(request,pk):
  if request.user.is_authenticated:
    record = get_object_or_404(Record,id=pk)
    record.delete()
    messages.success(request,"Record Deleted Successfully")
    return redirect('home')
  else:
    messages.success(request,'You must be Logged In to Delete Records')
    return redirect('home')

def add_record(request):
  form = AddRecordForm(request.POST or None)
  if request.user.is_authenticated:
    if request.method == 'POST':
      if form.is_valid():
        record = form.save()
        messages.success(request,'Record Added')
        return redirect('home')
    return render(request,'add.html',{'form':form})
  else:
    messages.success(request,'You must be Logged In')
    return redirect('home')

def update_record(request,pk):
  if request.user.is_authenticated:
    curr_record = get_object_or_404(Record,id=pk)
    form = AddRecordForm(request.POST or None,instance=curr_record)
    if form.is_valid():
      form.save()
      messages.success(request,'Record has been Updated')
      return redirect('home')
    return render(request,'update.html',{'form':form})
  else:
    messages.success(request,'You must be Logged In')
    return redirect('home')