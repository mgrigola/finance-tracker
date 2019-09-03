from django.urls import path
from . import views

app_name = 'finance'
urlpatterns = [
    path('', views.index, name='index'),
    path('account/<int:account_id>/', views.account_detail, name='detail'),
    path('user/<int:user_id>/', views.create_account, name='create'),
    path('create', views.create_account, name='create')
]


# same idea using generic views
## urlpatterns = [
#     # /polls/
#     path('', views.IndexView.as_view(), name='index'),
#     # /polls/questionNo/detail
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:ok>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote')
# ]