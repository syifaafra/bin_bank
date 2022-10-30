from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bin_bank.models import Article, Feedback, MyUser, Transaction
from django.views.decorators.csrf import csrf_exempt
from bin_bank.forms import RegisterForm
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


def homepage(request):
    total_feedback = Feedback.objects.count()
    data_article = Article.objects.all()
    context = {
        'shared_story':total_feedback,
        'articles': data_article
    }
    return render(request, 'homepage.html', context)

def add_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get("feedback")
        new_feedback = Feedback(feedback=feedback)
        new_feedback.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def article_detail(request, slug):
    return render(request, "article_detail.html")

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
    context = {'form':form}
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
    transactions = Transaction.objects.filter(isFinished=False) # TODO: Add filter user
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


# @login_required(login_url='/login/')
def show_transaction_user_success(request):
    transactions = Transaction.objects.filter(isFinished=True) # TODO: Add filter user
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


# @login_required(login_url='/login/')
def show_transaction_user_range(request):
    if request.method == "POST":
        # transaction = Transaction(
        #     amountKg = 4,
        #     branchName = "New York"
        # )
        # transaction.save()
        transactions = Transaction.objects.filter(amountKg__range=(request.POST["Min"], request.POST["Max"])) # TODO: Add filter user
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)

# @login_required(login_url='/login/')
def show_transaction_user_specific(request):
    print(request)
    form = FindTransactionForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        transactions = Transaction.objects.filter(amountKg = form.amountKg, branchName = form.branchName) # TODO: Add filter user
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")    
    return HttpResponse("Invalid method")

def deposit_sampah(request):
    return render(request, "deposit_sampah.html")


def show_leaderboard(request):
    user_data = MyUser.objects.all().order_by('-points')
    return HttpResponse(serializers.serialize("json", user_data), content_type="application/json")


def leaderboard(request):
    context = {}
    return render(request, "leaderboard.html", context)
