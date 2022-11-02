from django.contrib import admin
from .models import Article, Feedback, MyUser, SupportMessage

admin.site.register(Feedback)
admin.site.register(Article)
admin.site.register(MyUser)
admin.site.register(SupportMessage)