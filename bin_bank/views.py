import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from bin_bank.models import Article, Feedback, MyUser, SupportMessage, Transaction
from bin_bank.forms import RegisterForm, SupportMessageForm,FeedbackForm, RegisterForm, FindTransactionForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Fungsi Autentikasi
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            return redirect('bin_bank:homepage')
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('bin_bank:homepage') #response

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

# Asynchronous JavaScript (AJAX) login, register, and logout view 
@csrf_exempt
def ajax_login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # Redirect to a success page.
                return JsonResponse({
                "status": True,
                "username":username,
                "message": "Successfully Logged In!"
                # Insert any extra data if you want to pass data to Flutter
                }, status=200)
            else:
                return JsonResponse({
                "status": False,
                "message": "Failed to Login, Account Disabled."
                }, status=401)

        else:
            return JsonResponse({
            "status": False,
            "message": "Failed to Login, check your email/password."
            }, status=401)
    
@login_required(login_url='/login/')
def user_login_data(request):
  login_user_data = User.objects.filter(id=request.user.id)
  return HttpResponse(serializers.serialize('json', login_user_data), content_type="application/json")

def ajax_logout_user(request):
    logout(request)
    if request.method == "POST":
        return JsonResponse({
        "status": True,
        "message": "Successfully Logout"
        # Insert any extra data if you want to pass data to Flutter
        }, status=200)
    else:
        return JsonResponse({
        "status": False,
        "message": "Failed to Logout"
        }, status=401)

@csrf_exempt
def ajax_register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return JsonResponse({
            "status": True,
            "message": "Successfully Register"
            # Insert any extra data if you want to pass data to Flutter
            }, status=200)
        else :
            error_register_form = form.errors

            return JsonResponse({
            "status": False,
            "message": error_register_form.as_json()
            }, status=401)
    
    return JsonResponse({
            "status": False,
            "message": "Register Fail"
            }, status=401)

# Fungsi untuk menampilkan homepage
def homepage(request):
    username = request.user.username
    total_feedback = Feedback.objects.count()
    data_transaction = Transaction.objects.all()
    data_article = Article.objects.all()
    if total_feedback > 4:
        data_feedback = Feedback.objects.all()[:4]
    else:
        data_feedback = Feedback.objects.all()

    total_waste = 0
    for transaction in data_transaction:
        total_waste += transaction.amountKg

    context = {
        'username': username,
        'shared_story': total_feedback,
        'waste_collected': total_waste,
        'articles': data_article,
        'feedbacks': data_feedback
    }

    return render(request, 'homepage.html', context)

@login_required(login_url='/login/')
def add_feedback(request):
    username = request.user.username
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid(): # Kondisi data pada field valid
            new_feedback = Feedback(
                user = request.user,
                subject = form.cleaned_data['subject'], 
                feedback = form.cleaned_data['feedback'],
            )
            new_feedback.save() # Menyimpan task ke database
            return HttpResponse(b"CREATED", status=201)
    else:
        form = FeedbackForm()
    
    context = {'form':form, 'username':username}
    return render(request, "feedback.html", context)

@login_required(login_url='/login/')
@csrf_exempt
def post_feedback_json(request):
    username = request.user.username
    if request.method == "POST":
        store = json.loads(request.body.decode('utf-8'))
        subject = store['subject']
        feedback = store['feedback']
        user = request.user,
        new_feedback = Feedback(
                user = user,
                subject = subject,
                feedback = feedback,
        )
        new_feedback.save()
        context = {'message': 'SUCCESS'}
    else:
        context = {'message': 'FAILED'}

    return JsonResponse(context)

# Fungsi untuk mengembalikan seluruh data task dalam bentuk JSON
def show_feedback_json(request):
    data_feedback = Feedback.objects.all()
    return HttpResponse(serializers.serialize('json', data_feedback), content_type='application/json')

def show_article_json(request):
    data = Article.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login/')
def show_history(request):
    # TODO: Sessions
    form = FindTransactionForm()
    context = {
        'username': request.user.username,
        'form': form
    }
    return render(request, "history.html", context)


@login_required(login_url='/login/')
def update_transaction(request, id):
    transaction_list = Transaction.objects.filter(id=id)
    transaction = transaction_list[0]
    transaction.isFinished = True
    transaction.save()
    request.user.points += transaction.amountKg
    request.user.save()
    return redirect('bin_bank:show_history')


@login_required(login_url='/login/')
def show_transaction_user(request):
    transactions = Transaction.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


@login_required(login_url='/login/')
def show_transaction_user_ongoing(request):
    transactions = Transaction.objects.filter(user=request.user, isFinished=False)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


@login_required(login_url='/login/')
def show_transaction_user_success(request):
    transactions = Transaction.objects.filter(user=request.user, isFinished=True)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


@login_required(login_url='/login/')
def show_transaction_user_range(request):
    if request.method == "POST":
        transactions = Transaction.objects.filter(
            user=request.user,
            amountKg__range=(request.POST["Min"],
                             request.POST["Max"]))
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)


@login_required(login_url='/login/')
def show_transaction_user_specific(request):
    form = FindTransactionForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        transactions = Transaction.objects.filter(user=request.user, branchName=form.branchName)
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method")


@login_required(login_url='/login/')
def deposit_sampah(request):
    username = request.user.username
    return render(request, "deposit_sampah.html", {'username':username})


@login_required(login_url='/login/')
def add_transaction(request):
    if request.method == 'POST':
        amountKg = request.POST.get('amountKg')
        branchName = request.POST.get('branchName')
        response_data = {}

        transaction = Transaction(amountKg=amountKg, branchName=branchName, user=request.user)
        transaction.save()


        response_data['result'] = 'Create post successful!'
        response_data['username'] = transaction.user.username
        response_data['pk'] = transaction.pk
        response_data['date'] = transaction.date.strftime('%B %d, %Y %I:%M %p')
        response_data['amountKg'] = transaction.amountKg
        response_data['branchName'] = transaction.branchName
        response_data['isFinished'] = transaction.isFinished

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/login/')
def show_transaction(request):
    transactions = Transaction.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


@login_required(login_url='/login/')
def delete_transaction(request):
    transactions = Transaction.objects.all().delete()
    redirect('bin_bank:deposit_sampah')

def show_leaderboard(request):
    user_data = MyUser.objects.all().order_by('-points')
    return HttpResponse(serializers.serialize("json", user_data), content_type="application/json")


def leaderboard(request):
    form = SupportMessageForm
    context = {
        'username': request.user.username,
        'form': form,
    }
    if request.user.username != "":
        context['point'] = request.user.points
    return render(request, "leaderboard.html", context)


@csrf_exempt
def find_username(request, username):
    if request.method == 'POST':
        username = request.POST.get("textinput")
        if username == "":
            return redirect('../cari')
        return redirect('../cari/' + username)
    user_data = MyUser.objects.all().order_by('-points')
    rank = 1
    is_found = False
    context = {'username': request.user.username}

    for user in user_data:
        if user.is_admin:
            continue
        if user.username == username:
            is_found = True
            break
        rank += 1

    context["searched_user"] = username
    context["is_found"] = False

    if is_found:
        context["rank"] = rank
        context["is_found"] = True

    return render(request, "leaderboard_search.html", context)


@csrf_exempt
def find_username_menu(request):
    if request.method == 'POST':
        username = request.POST.get("textinput")
        if username == "":
            return redirect('../leaderboard/cari')
        return redirect('cari/' + username)
    context = {'is_found': "", "username": request.user.username}
    return render(request, "leaderboard_search.html", context)


def show_support_message(request):
    message_data = SupportMessage.objects.all().order_by('?')[:12]
    data = []
    for item in message_data:
        data.append({
            'username': item.user.username,
            'date': item.date,
            'message': item.message
        })
    data = {'data': data}
    return JsonResponse(data)


def add_support_message(request):
    if request.method == 'POST':
        user = request.user
        message = request.POST.get("message")

        new_message = SupportMessage(user=user, message=message)
        new_message.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

# For flutter
@csrf_exempt
def add_support_message_post(request):
    print("\n\n\nlol\n\n\n")
    print(request.POST)
    print(request.POST['user'])
    if request.method == 'POST':
        user = MyUser.objects.filter(username=request.POST["user"])[0]
        message = request.POST.get("message")

        new_message = SupportMessage(user=user, message=message)
        new_message.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

# Method untuk flutter
@csrf_exempt
def show_transaction_user_post(request):
    if request.method == "POST":
        user = MyUser.objects.filter(username=request.POST["user"])
        transactions = Transaction.objects.filter(
            user=user[0])
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)

@csrf_exempt
def show_transaction_user_ongoing_post(request):
    if request.method == "POST":
        user = MyUser.objects.filter(username=request.POST["user"])
        transactions = Transaction.objects.filter(
            user=user[0], isFinished=False)
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)

@csrf_exempt
def show_transaction_user_success_post(request):
    if request.method == "POST":
        user = MyUser.objects.filter(username=request.POST["user"])
        transactions = Transaction.objects.filter(
            user=user[0], isFinished=True)
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)

@csrf_exempt
def show_transaction_user_range_post(request):
    if request.method == "POST":
        user = MyUser.objects.filter(username=request.POST["user"])
        transactions = Transaction.objects.filter(
            user=user[0],
            amountKg__range=(request.POST["Min"],
                             request.POST["Max"]))
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)

@csrf_exempt
def show_transaction_user_branch_post(request):
    if request.method == "POST":
        user = MyUser.objects.filter(username=request.POST["user"])
        transactions = Transaction.objects.filter(
            user=user[0],
            branchName=request.POST["branchName"])
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)

@csrf_exempt
def update_transaction_post(request):
    user = MyUser.objects.filter(username=request.POST["user"])
    user = user[0]
    pk = int(request.POST['pk'])
    transaction_list = Transaction.objects.filter(id=pk)
    transaction = transaction_list[0]
    transaction.isFinished = True
    transaction.save()
    user.points += transaction.amountKg
    user.save()
    return JsonResponse({
    "status": True,
    "message": "Successfully update!"
    }, status=200)
