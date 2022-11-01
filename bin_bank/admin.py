from django.contrib import admin
from .models import Article, Feedback, MyUser

admin.site.register(Article)
admin.site.register(Feedback)
admin.site.register(MyUser)
