from django.forms import ModelForm, IntegerField, HiddenInput
from django.forms.widgets import TextInput
from .models import FinanceCategory, Account

class FinanceCategoryForm(ModelForm):
    class Meta:
        model = FinanceCategory
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }

class AccountForm(ModelForm):
    copy_from = IntegerField(required=False, widget=HiddenInput())

    class Meta:
        model = Account
        exclude = ['id', 'user', 'acct_balance']
        help_texts = {
            'title': 'a name to identify this account',
            'init_balance': 'initial balance before data is available (maybe as of earliest data import date)',
            'acct_source': 'the institution that holds the account or other source',
            'acct_type': 'checking, savings, brokerage, 401k, etc.'
        }

