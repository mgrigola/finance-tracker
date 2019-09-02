from django.urls import path
from . import views

app_name = 'finance'
urlpatterns = [
    # /finance/
    path('', views.index, name='index'),
    # /finance/questionNo/detail
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
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