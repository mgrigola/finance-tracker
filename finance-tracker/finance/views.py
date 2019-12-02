from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
import json
import datetime

from .models import Account, Transaction, FinanceCategory

@login_required
def index(request):
    # show the most recently published questions. exclude future-dated questions 
    current_user = request.user
    account_list = Account.objects.filter(user_id=current_user.id)
    template = loader.get_template('finance/index.html')
    context = {
        'current_user': current_user
        ,'account_list': account_list
        ,'title': ''
    }
    return HttpResponse(template.render(context, request))

@login_required
def account_detail(request, account_id): # , dateRange) ?
    account = get_object_or_404(Account, pk=account_id)
    userCats = FinanceCategory.objects.filter(user=request.user)
    dateRangeStart = datetime.datetime.now() + datetime.timedelta(days=-180)
    dateRangeEnd = datetime.datetime.now()
    catSums = account.aggregate_transactions_by_category(dateRangeStart, dateRangeEnd)
    jsData = 'abcd'
    context = {
        'account': account,
        'title': "Transactions",
        'userCats': userCats,
        'catSums': catSums
        'jsData': jsData
    }
    return render(request, 'finance/account.html', context)

@login_required
def create_account(request):
    current_user = request.user
    context = {
        'user':current_user
        ,'title':"create account"
    }
    return render(request, 'finance/create.html', context)