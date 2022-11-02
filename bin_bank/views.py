from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from bin_bank.models import Article, Feedback, MyUser, SupportMessage, Transaction
from django.views.decorators.csrf import csrf_exempt
from bin_bank.forms import RegisterForm, SupportMessageForm
from bin_bank.forms import FeedbackForm, RegisterForm, FindTransactionForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('bin_bank:login')

    context = {'form': form}
    return render(request, 'register.html', context)


# Fungsi untuk menampilkan homepage
def homepage(request):
    username = request.user.username
    total_feedback = Feedback.objects.count()
    data_transaction = Transaction.objects.all()
    data_article = Article.objects.all()

    total_waste = 0
    for transaction in data_transaction:
        total_waste += transaction.amountKg

    context = {
        'username': username,
        'shared_story': total_feedback,
        'waste_collected': total_waste, 
        'articles': data_article,
    }

    return render(request, 'homepage.html', context)


def add_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get("feedback")
        name = request.POST.get("name")
        if name == "":
            new_feedback = Feedback(feedback=feedback,name="ANONYM")
        else:
            new_feedback = Feedback(feedback=feedback,name=name)
        new_feedback.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

# Fungsi untuk mengembalikan seluruh data task dalam bentuk JSON
def show_feedback_json(request):
    data_feedback = Feedback.objects.all()
    return HttpResponse(serializers.serialize('json', data_feedback), content_type='application/json')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bin_bank:homepage')
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('bin_bank:login')


# @login_required(login_url='/login/')
def show_history(request):
    # context = {
    #     'username': request.user.username,
    #     'last_login': request.COOKIES['last_login'],
    # }
    form = FindTransactionForm()
    context = {'form': form}
    return render(request, "history.html", context)


# @login_required(login_url='/login/')
def update_transaction(request, id):
    transaction_list = Transaction.objects.filter(id=id)
    transaction = transaction_list[0]
    transaction.isFinished = True
    transaction.save()
    return redirect('bin_bank:show_history')


# @login_required(login_url='/login/')
def show_transaction_user(request):
    transactions = Transaction.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


# @login_required(login_url='/login/')
def show_transaction_user_ongoing(request):
    transactions = Transaction.objects.filter(isFinished=False)  # TODO: Add filter user
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


# @login_required(login_url='/login/')
def show_transaction_user_success(request):
    transactions = Transaction.objects.filter(isFinished=True)  # TODO: Add filter user
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


# @login_required(login_url='/login/')
def show_transaction_user_range(request):
    if request.method == "POST":
        # transaction = Transaction(
        #     amountKg = 4,
        #     branchName = "New York"
        # )
        # transaction.save()
        transactions = Transaction.objects.filter(
            amountKg__range=(request.POST["Min"], request.POST["Max"]))  # TODO: Add filter user
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)


# @login_required(login_url='/login/')
def show_transaction_user_specific(request):
    print(request)
    form = FindTransactionForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        transactions = Transaction.objects.filter(amountKg=form.amountKg,
                                                  branchName=form.branchName)  # TODO: Add filter user
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method")


def deposit_sampah(request):
    return render(request, "deposit_sampah.html")


def add_transaction(request):
    if request.method != 'POST':
        return redirect('bin_bank:deposit_sampah')

    form = request.POST
    if form.is_valid():
        new_transaction = form.save(commit=False)
        new_transaction.user = request.user
        new_transaction.save()
        form.save_m2m()
        return JsonResponse({
            'user': new_transaction.user,
            'pk': new_transaction.pk,
            'date': new_transaction.date,
            'amountKg': new_transaction.amountKg,
            'branchName': new_transaction.branchName,
            'isFinished': new_transaction.isFinished,
        })


def show_leaderboard(request):
    user_data = MyUser.objects.all().order_by('-points')
    return HttpResponse(serializers.serialize("json", user_data), content_type="application/json")


def leaderboard(request):
    form = SupportMessageForm
    context = {
        'username':request.user.username,
        'form':form
        }
    return render(request, "leaderboard.html", context)

def show_support_message(request):
    message_data = SupportMessage.objects.all().order_by('?')[:12]
    data = []
    for item in message_data:
        data.append({
            'username':item.user.username,
            'date':item.date,
            'message':item.message
        })
    data = {'data':data}
    return JsonResponse(data)

def add_support_message(request):
    if request.method == 'POST':
        user = request.user
        message = request.POST.get("message")

        new_message = SupportMessage(user=user, message=message)
        new_message.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
