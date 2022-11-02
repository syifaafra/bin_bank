import random
from django.core.serializers import json
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

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


# signup and signin kausar


class signup(CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"


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
            new_feedback = Feedback(feedback=feedback, name="ANONYM")
        else:
            new_feedback = Feedback(feedback=feedback, name=name)
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
    transactions = Transaction.objects.all() # TODO: Add filter user
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
        # cities =("New","Los","Chicago","Houston","Phoenix","Philadelphia","San","San","Dallas","San","Austin","Jacksonville","Fort","Columbus","Charlotte","Indianapolis","San","Seattle","Denver","Washington","Nashville","Oklahoma","Boston","El","Portland","Las","Memphis","Detroit","Baltimore","Milwaukee","Albuquerque","Fresno","Tucson","Sacramento","Kansas","Mesa","Atlanta","Omaha","Colorado","Raleigh","Long","Virginia","Miami","Oakland","Minneapolis","Tulsa","Bakersfield","Wichita","Arlington","Aurora","Tampa","New","Cleveland","Honolulu","Anaheim","Louisville","Henderson","Lexington","Irvine","Stockton","Orlando","Corpus","Newark","Riverside","St","Cincinnati","San","Santa","Greensboro","Pittsburgh","Jersey","St","Lincoln","Durham","Anchorage","Plano","Chandler","Chula","Buffalo","Gilbert","Madison","Reno","North","Toledo","Fort","Irving","Lubbock","St","Laredo","Chesapeake","Winston","Glendale","Garland","Scottsdale","Arlington","Enterprise","Boise","Santa","Norfolk","Fremont","Spokane","Richmond","Baton","San","Tacoma","Spring","Hialeah","Huntsville","Modesto","Frisco","Des","Yonkers","Port","Moreno","Worcester","Rochester","Fontana","Columbus","Fayetteville","Sunrise","McKinney","Little","Augusta","Oxnard","Salt","Amarillo","Overland","Cape","Grand","Huntington","Sioux","Grand","Montgomery","Tallahassee","Birmingham","Peoria","Glendale","Vancouver","Providence","Knoxville","Brownsville","Akron","Newport","Fort","Mobile","Shreveport","Paradise","Tempe","Chattanooga","Cary","Eugene","Elk","Santa","Salem","Ontario","Aurora","Lancaster","Rancho","Oceanside","Fort","Pembroke","Clarksville","Palmdale","Garden","Springfield","Hayward","Salinas","Alexandria","Paterson","Murfreesboro","Bayamon","Sunnyvale","Kansas","Lakewood","Killeen","Corona","Bellevue","Springfield","Charleston","Hollywood","Roseville","Pasadena","Escondido","Pomona","Mesquite","Naperville","Joliet","Savannah","Jackson","Bridgeport","Syracuse","Surprise","Rockford","Torrance","Thornton","Kent","Fullerton","Denton","Visalia","McAllen")
        # for x in cities:
        #     transaction = Transaction(
        #         amountKg = random.randint(1, 20),
        #         branchName = x
        #     )
        #     transaction.save()
        transactions = Transaction.objects.filter(
            amountKg__range=(request.POST["Min"], request.POST["Max"]))  # TODO: Add filter user
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)


# @login_required(login_url='/login/')
def show_transaction_user_specific(request):
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
    if request.method == 'POST':
        amountKg = request.POST.get('amountKg')
        branchName = request.POST.get('branchName')
        response_data = {}

        transaction = Transaction(amountKg=amountKg, branchName=branchName, user=request.user)
        transaction.save()

        response_data['result'] = 'Create post successful!'
        response_data['user'] = transaction.user
        response_data['pk'] = transaction.pk
        response_data['amountKg'] = transaction.amountKg
        response_data['branchName'] = transaction.branchName
        response_data['date'] = transaction.date
        response_data['isFinished'] = transaction.isFinished

        return HttpResponse(
            serializers.serialize("json", transaction), content_type="application/json"
        )
    else:
        return HttpResponse(
            serializers.serialize("json", {"nothing to see": "Something happened"}), content_type="application/json"
        )


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
        if username=="":
            return redirect('../cari')
        return redirect('../cari/'+username)
    user_data = MyUser.objects.all().order_by('-points')
    rank = 1
    is_found = False
    context = {'username':request.user.username}

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
        if username=="":
            return redirect('../leaderboard/cari')
        return redirect('cari/'+username)
    context = {'is_found':"", "username":request.user.username}
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
