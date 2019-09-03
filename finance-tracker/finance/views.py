from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.utils import timezone

from .models import Account, Transaction, TransactionCategory#, User

def index(request):
    # show the most recently published questions. exclude future-dated questions 
    current_user = request.user
    account_list = Account.objects.filter(user_id=current_user.id)
    template = loader.get_template('finance/index.html')
    context = {
        'current_user': current_user
        ,'account_list': account_list
    }
    return HttpResponse(template.render(context, request))


def account_detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, 'finance/detail.html', {'account':account})

def create_account(request):
    current_user = request.user
    return render(request, 'finance/create.html', {'current_user':current_user})