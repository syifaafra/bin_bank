from django.shortcuts import render
from bin_bank.models import Transaction
from django.http import HttpResponse
from django.core import serializers


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