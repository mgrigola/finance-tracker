from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import uuid
import datetime
import csv

WITHDRAWL_CATEGORY_ID = 11
DEPOSIT_CATEGORY_ID = 10

# my custom user, in case it needs to change. not easy to migrate later
# class User(AbstractUser):
#     pass

# category definitions unique to a user
class FinanceCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=64)
    color = models.CharField(max_length=7, null=True) #represents rgb color
    

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acct_balance = models.FloatField(default=0.0)
    acct_source = models.CharField(max_length=64, default=None, blank=True, null=True)  #e.g. Chase (should be INSTITUTION_ID + anotehr table)
    acct_type = models.CharField(max_length=64, default=None, blank=True, null=True)   #savings, checking, investment - later drives how we show transactions maybe?

    def __str__(self):
        return self.title

    def latest_date(self):
        return self.transaction_set.order_by('-tx_date')[0].tx_date
    
    # later add different parser for different acct_source
    # Chase export format:
    # 0] Debit/Credit
    # 1] Date(MM/DD/YY)
    # 2] Description
    # 3] Amount (- is withdraw, + is deposit)
    # 4] Type (ACH_DEBIT/CHECK/etc)
    # 5] Balance-after-transaction
    # 6] Check #
    def load_transactions_from_file(self, file_name):
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if row[0] == 'Details': continue  # skip header row if present
                tx = Transaction()
                tx.account = self
                tx.tx_date = datetime.datetime.strptime(row[1], '%m/%d/%Y')
                tx.description = row[2]
                tx.amount = float(row[3])
                tx.tx_type = row[4]
                if row[5]=='' or row[5]==' ': tx.balance = None
                else: tx.balance = float(row[5])

                # check for duplicates - import twice gives same transactions as import once, hopefully
                duplicateTxs = Transaction.objects.filter(account=self, tx_date=tx.tx_date, description=tx.description, amount=tx.amount)
                if len(duplicateTxs)==0:
                    tx.save()
                # else:
                #     MyModel.objects.filter(pk=some_value).update(field1='some value')
        
        # get current balance. don't rely on what's loaded. may be recent-er tx already in db
        recentTxs = self.transaction_set.order_by('-tx_date')
        for recentTx in recentTxs:
            bal = recentTx.balance
            if bal is not None: break
        
        self.acct_balance = bal
        self.save()
    
    # aggregate transaction amounts by category - not very efficiently...
    def aggregate_transactions_by_category(self, dateStart, dateEnd=datetime.datetime.now()):
        withdrawlCat = FinanceCategory.objects.get(pk=WITHDRAWL_CATEGORY_ID)
        depositCat = FinanceCategory.objects.get(pk=DEPOSIT_CATEGORY_ID)
        tots = {withdrawlCat: 0, depositCat:0}
        
        for tx in self.transaction_set.filter(tx_date__range=(dateStart, dateEnd)): # TODO: check timezone - maybe at caller
            qset = tx.get_categories()
            if len(qset) == 0:
                if tx.amount > 0:
                    tots[depositCat] += tx.amount
                # withdrawl total is negative
                else:
                    tots[withdrawCat] += tx.amount
                        
            else:
                for cat in qset:
                    if tx.amount > 0:
                        tots[depositCat] += tx.amount
                    else:
                        tots[withdrawCat] += tx.amount
                    
                    if not cat in tots:
                        tots[cat] = tx.amount
                    else:
                        tots[cat] += tx.amount
        
        return(tots)
    
    # return a dictionary with dates  - Python 3.6: dicts are ordered sets!
    def aggregate_balance_by_date(self, dateStart, dateEnd=datetime.datetime.now()):
        pass


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default=None, blank=True, null=True)
    tx_date = models.DateTimeField('transaction date')
    tx_type = models.CharField(max_length=32, default=None, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0, blank=True, null=True) #balance after the transaction if available
    categories = models.ManyToManyField(FinanceCategory)

    def is_positive(self):
        return (self.amount > 0)

    # specifically for Chase descriptions, they have a bunch of spaces after the real description, then some sort of unique identifier info
    def short_desc(self):
        idx = self.description.find('  ')
        return self.description[:idx]
    
    def get_categories(self):
        return self.categories.all()
        # return TransactionCategory.objects.filter(transaction=self)

    class Meta:
        ordering = ['-tx_date']
