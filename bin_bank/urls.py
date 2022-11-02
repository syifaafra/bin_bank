from django.urls import path
from bin_bank.views import login_user, register, logout_user, show_transaction_user, show_transaction_user_ongoing, \
    show_transaction_user_success, update_transaction, show_history, show_transaction_user_range, leaderboard, \
    show_leaderboard, show_support_message, add_support_message, add_transaction
from bin_bank.views import homepage, deposit_sampah, show_feedback_json, add_feedback, show_transaction_user_specific

app_name = 'bin_bank'

urlpatterns = [
    path('', homepage, name='homepage'),  # TODO : homepage
    path('login/', login_user, name='login'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('leaderboard/add-support-message', add_support_message, name='add_support_message'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('history/', show_history, name='show_history'),
    path('feedback-json/', show_feedback_json, name='show_feedback_json'),
    path('add-feedback/', add_feedback, name='add_feedback'),
    path('json/', show_transaction_user, name='show_transaction_user'),
    path('json/ongoing', show_transaction_user_ongoing, name='show_transaction_user_ongoing'),
    path('json/success', show_transaction_user_success, name='show_transaction_user_success'),
    path('json/range/', show_transaction_user_range, name='show_transaction_user_range'),
    path('json/search/', show_transaction_user_specific, name='show_transaction_user_specific'),
    path('json/leaderboard', show_leaderboard, name='show_leaderboard'),
    path('json/support-message', show_support_message, name='show_support_message'),
    path('update-transaction/<int:id>', update_transaction, name='update_transaction'),
    path('deposit_sampah/', deposit_sampah, name='deposit_sampah'),
    path('deposit_sampah/add_transaction/', add_transaction, name='add_transaction'),

]
