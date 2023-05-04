from django.contrib import admin

from news3.models import News, Category, UsersSubscribed

admin.site.register(News)
admin.site.register(Category)
admin.site.register(UsersSubscribed)
# Register your models here.
