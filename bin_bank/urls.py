from django.urls import path
from bin_bank.views import login_user, register, logout_user, show_transaction_user, show_transaction_user_ongoing, \
    show_transaction_user_success, show_transaction_user_failed
from bin_bank.views import homepage, deposit_sampah

app_name = 'bin_bank'

urlpatterns = [
    path('', homepage, name='homepage'),  # TODO : homepage
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('json/', show_transaction_user, name='show_transaction_user'),
    path('json/ongoing', show_transaction_user_ongoing, name='show_transaction_user_ongoing'),
    path('json/success', show_transaction_user_success, name='show_transaction_user_success'),
    path('json/failed', show_transaction_user_failed, name='show_transaction_user_failed'),
    path('deposit_sampah/', deposit_sampah, name='deposit_sampah'),
]
