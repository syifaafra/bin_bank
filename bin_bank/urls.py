from django.urls import path
from bin_bank.views import *
app_name = 'bin_bank'

urlpatterns = [
    path('', homepage, name='homepage'),  # TODO : homepage
    path('json/user_login', user_login_data, name='user_login_data'),
    path('login/', login_user, name='login'),
    path('login/ajax', ajax_login_user, name='ajax_login_user'),
    path('register/', register, name='register'),
    path('register/ajax', ajax_register, name='ajax_register'),
    path('logout/', logout_user, name='logout'),
    path('logout/ajax', ajax_logout_user, name='ajax_logout_user'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('leaderboard/add-support-message', add_support_message, name='add_support_message'),
    path('leaderboard/cari', find_username_menu, name='find_username_menu' ),
    path('leaderboard/cari/<str:username>', find_username, name='find_username' ),  # type: ignore
    path('history/', show_history, name='show_history'),
    path('feedback-json/', show_feedback_json, name='show_feedback_json'),
    path('article-json/', show_article_json, name='show_article_json'),
    path('add-feedback/', add_feedback, name='add_feedback'),
    path('json/', show_transaction_user, name='show_transaction_user'),
    path('json/ongoing/', show_transaction_user_ongoing, name='show_transaction_user_ongoing'),
    path('json/success/', show_transaction_user_success, name='show_transaction_user_success'),
    path('json/range/', show_transaction_user_range, name='show_transaction_user_range'),
    path('json/search/', show_transaction_user_specific, name='show_transaction_user_specific'),
    path('json/leaderboard', show_leaderboard, name='show_leaderboard'),
    path('json/support-message', show_support_message, name='show_support_message'),
    path('update-transaction/<int:id>', update_transaction, name='update_transaction'),
    path('deposit_sampah/', deposit_sampah, name='deposit_sampah'),
    path('deposit_sampah/add_transaction/', add_transaction, name='add_transaction'),
    path('deposit_sampah/show_transaction/', show_transaction, name='show_transaction'),
    path('deposit_sampah/delete_transaction/', delete_transaction, name='delete_transaction'),
    path('json/post/', show_transaction_user_post, name='show_transaction_user_post'),
    path('json/post/ongoing', show_transaction_user_ongoing_post, name='show_transaction_user_ongoing_post'),
    path('json/post/success', show_transaction_user_success_post, name='show_transaction_user_success_post'),
    path('json/post/range', show_transaction_user_range_post, name='show_transaction_user_range_post'),
    path('json/post/branch', show_transaction_user_branch_post, name='show_transaction_user_branch_post'),
    path('update-transaction-post/', update_transaction_post, name='update_transaction_post'),

]
