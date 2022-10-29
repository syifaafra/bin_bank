from django.urls import path
from bin_bank.views import article_detail, get_articles_json, get_feedback_json, login_user, register, logout_user, show_transaction_user, show_transaction_user_ongoing, \
    show_transaction_user_success,update_transaction,show_history
from bin_bank.views import homepage, deposit_sampah

app_name = 'bin_bank'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('<str:slug>/', article_detail, name='article_detail'),
    path('get-feedback-json/', get_feedback_json, name='get_feedback_json'),
    path('get-articles-json/', get_articles_json, name='get_articles_json'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('history/', show_history, name='show_history'),
    path('json/', show_transaction_user, name='show_transaction_user'),
    path('json/ongoing', show_transaction_user_ongoing, name='show_transaction_user_ongoing'),
    path('json/success', show_transaction_user_success, name='show_transaction_user_success'),
    path('update-transaction/<int:id>', update_transaction, name='update_transaction'),
    path('deposit_sampah/', deposit_sampah, name='deposit_sampah'),
]