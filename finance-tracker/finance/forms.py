from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import FinanceCategory

class FinanceCategoryForm(ModelForm):
    class Meta:
        model = FinanceCategory
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }