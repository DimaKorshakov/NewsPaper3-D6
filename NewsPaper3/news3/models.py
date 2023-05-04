from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    date = models.DateField(auto_now_add=True)
    header = models.CharField(max_length=50, unique=True)
    description = models.TextField(unique=True)
    email = models.EmailField()
    cat = models.ManyToManyField('Category')

    def __str__(self):
        return f'{self.date} {self.header} {self.description[:20]} {self.email} {self.cat}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # названия категорий тоже не должны повторяться
    user = models.ManyToManyField(User, 'UsersSubscribed')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/news/category/{self.id}'


class UsersSubscribed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} is subscribed to category {self.category}'

