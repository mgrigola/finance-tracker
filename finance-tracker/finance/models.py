from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime
import csv

# my custom user, in case it needs to change. not easy to migrate later
# class User(AbstractUser):
#     pass

class Account(models.Model):
    title = models.CharField(max_length=64)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acct_balance = models.FloatField(default=0.0)
    acct_source = models.CharField(max_length=64, default=None, blank=True, null=True)  #e.g. Chase (should be INSTITUTION_ID + anotehr table)
    acct_type = models.CharField(max_length=64, default=None, blank=True, null=True)   #savings, checking, investment - later drives how we show transactions maybe?

    def __str__(self):
        return self.title

    # later add different parser for different acct_source
    # Chase export format:
    # 0] Debit/Credit
    # 1] Date(MM/DD/YY)
    # 2] Description
    # 3] Amount (- is withdraw, + is deposit)
    # 4] Type (ACH_DEBIT/CHECK/etc)
    # 5] Balance-after-transaction
    # 6] Check #
    def loadTransactionsFromFile(self, file_name):
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if row[0] == 'Details': continue  # skip header row if present
                tx = Transaction()
                tx.tx_date = datetime.datetime.strptime(row[1], '%m/%d/%Y')
                tx.description = row[2]
                tx.amount = float(row[3])
                tx.tx_type = row[4]
                tx.balance = float(row[5])

                # check for duplicates - import twice gives same transactions as import once
                duplicateTxs = Transaction.objects.filter(account_id=self.id, tx_date=tx.tx_date, description=tx.description, amount=tx.amount)
                if len(duplicateTxs)==0:
                    tx.save()
                # else:
                #     MyModel.objects.filter(pk=some_value).update(field1='some value')


class Transaction(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default=None, blank=True, null=True)
    tx_date = models.DateTimeField('transaction date')
    tx_type = models.CharField(max_length=32, default=None, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0, blank=True, null=True) #balance after the transaction if available

class FinanceCategory(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)

# map each transaction to one or many cateogries
class TransactionCategory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    category = models.ForeignKey(FinanceCategory, on_delete=models.CASCADE)

# # make some default categories somewehere. this holds a custom categories created by/for a user
# class UserCategories(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=64)