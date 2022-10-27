from django.shortcuts import render, redirect
from bin_bank.models import Transaction
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')

    context = {'form':form}
    return render(request, 'register.html', context)

def homepage(request):
    return render(request, "test_page.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todolist:show_todo')
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('todolist:login')

@login_required(login_url='/bin_bank/login/')
def show_transaction_user(request):
    tasks = Transaction.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", tasks), content_type="application/json")

@login_required(login_url='/bin_bank/login/')
def show_transaction_user_ongoing(request):
    tasks = Transaction.objects.filter(user=request.user, status=1)
    return HttpResponse(serializers.serialize("json", tasks), content_type="application/json")

@login_required(login_url='/bin_bank/login/')
def show_transaction_user_success(request):
    tasks = Transaction.objects.filter(user=request.user, status=2)
    return HttpResponse(serializers.serialize("json", tasks), content_type="application/json")

@login_required(login_url='/bin_bank/login/')
def show_transaction_user_failed(request):
    tasks = Transaction.objects.filter(user=request.user, status=3)
    return HttpResponse(serializers.serialize("json", tasks), content_type="application/json")