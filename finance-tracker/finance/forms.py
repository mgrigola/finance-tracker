from django import forms
from .models import FinanceCategory, Account

class FinanceCategoryForm(forms.ModelForm):
    class Meta:
        model = FinanceCategory
        fields = '__all__'
        widgets = {
            'color': forms.widgets.TextInput(attrs={'type': 'color'}),
        }

class AccountForm(forms.ModelForm):
    copy_from = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Account
        exclude = ['id', 'user', 'acct_balance']
        help_texts = {
            'title': 'a name to identify this account',
            'init_balance': 'initial balance before data is available (maybe as of earliest data import date)',
            'acct_source': 'the institution that holds the account or other source',
            'acct_type': 'checking, savings, brokerage, 401k, etc.'
        }

class UploadTransactionFileForm(forms.Form):
    title = forms.CharField
    txFile = forms.FileField(label='Transaction data file', help_text='csv / tsv file in same format as the export')