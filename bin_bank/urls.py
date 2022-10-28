from django.urls import path
from bin_bank.views import login_user,reshow_transaction_user, show_transaction_user_ongoing, show_transaction_user_success, show_transaction_user_failed


app_name = 'bin_bank'

urlpatterns = [
    path('', main, name='main'),  #TODO : homepage 
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('json/', show_transaction_user, name='show_transaction_user'), 
    path('json/ongoing', show_transaction_user_ongoing, name='show_transaction_user_ongoing'),
    path('json/success', show_transaction_user_success, name='show_transaction_user_success'), 
    path('json/failed', show_transaction_user_failed, name='show_transaction_user_failed'), 
    
]