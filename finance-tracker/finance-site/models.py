from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime


# my custom user, in case it needs to change. not easy to migrate later
class User(AbstractUser):
    pass

class Account(models.Model):
    title = models.CharField(max_length=64)
    balance = models.FloatField(default=0.0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return (now - datetime.timedelta(days=1)) <= self.pub_date <= now

    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True
    # was_published_recently.short_description = 'Recent?'

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    tx_date = models.DateTimeField('transaction date')
    amount = models.FloatField(default=0.0)

class FinanceCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)

# map each transaction to one or many cateogries
class TransactionCategory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    category = models.ForeignKey(FinanceCategory, on_delete=models.CASCADE)

# # make some default categories somewehere. this holds a custom categories created by/for a user
# class UserCategories(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=64)