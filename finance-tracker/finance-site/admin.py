from django.contrib import admin
from .models import Account, FinanceCategory

# class ChoiceInline(admin.StackedInline):
class FinanceCategoryInline(admin.TabularInline):
    model = FinanceCategory
    extra = 1


class AccountAdmin(admin.ModelAdmin):
    list_display = ('title', 'balance')
    search_fields = ['title']

# class UserAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Account, AccountAdmin)
# admin.site.register(Choice)