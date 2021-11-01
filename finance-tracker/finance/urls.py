from django.conf.urls import url
from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'finance'
urlpatterns = [
    path('', views.all_account_summary, name='all_account_summary'),
    path('<uuid:account_id>/', views.account_detail, name='account_detail'),
    # path('user/<int:user_id>/', views.create_account, name='create'),
    path('create', views.create_account, name='create_account'),
    path('<uuid:account_id>/export-empty', views.account_export_empty, name='account_export_empty')
]
