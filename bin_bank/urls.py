from django.urls import path
from bin_bank.views import login_user, register, logout_user, article_detail, get_articles_json, get_feedback_json, \
    show_transaction_user, show_transaction_user_ongoing, show_transaction_user_success, update_transaction, show_history, \
    show_transaction_user_range, show_leaderboard, leaderboard

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
    path('json/range/', show_transaction_user_range, name='show_transaction_user_range'),
    path('update-transaction/<int:id>', update_transaction, name='update_transaction'),
    path('deposit_sampah/', deposit_sampah, name='deposit_sampah'),
    path('json/leaderboard', show_leaderboard, name='show_leaderboard'),
    path('leaderboard', leaderboard, name='leaderboard'),
]
