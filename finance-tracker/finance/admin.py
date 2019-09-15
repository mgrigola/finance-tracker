from django.contrib import admin
from .models import Account, FinanceCategory
from .forms import FinanceCategoryForm

# or StackedInline
# class FinanceCategoryInline(admin.TabularInline):
#     model = FinanceCategory
#     extra = 1



class AccountAdmin(admin.ModelAdmin):
    list_display = ('title', 'acct_type', 'acct_source', 'acct_balance')
    search_fields = ['title', 'acct_type', 'acct_source']


class FinanceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'color')
    list_filter = ['user']        # allow filter on Question.pub_date
    search_fields = ['title' 'user']
    form = FinanceCategoryForm
    fieldsets = [
        (None, {'fields': ['title', 'color', 'user'] }),
    ]



admin.site.register(Account, AccountAdmin)
admin.site.register(FinanceCategory, FinanceCategoryAdmin)


# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserChangeForm
# from .models import User
# class MyUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = User

# class MyUserAdmin(UserAdmin):
#     form = MyUserChangeForm

#     # fieldsets = UserAdmin.fieldsets + (
#     #         (None, {'fields': ('some_extra_data',)}),
#     # )

# admin.site.register(User, MyUserAdmin)

