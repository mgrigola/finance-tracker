from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
import json
import datetime
import bokeh.plotting as bkplotting
import bokeh.embed as bkembed

from .models import Account, Transaction, FinanceCategory
from .forms import AccountForm, FinanceCategoryForm

@login_required
def index(request):
    # show the most recently published questions. exclude future-dated questions 
    current_user = request.user
    account_list = Account.objects.filter(user_id=current_user.id)
    
    # TODO: aggregate all accounts, remove acct0
    dateRangeStart = datetime.datetime.now() + datetime.timedelta(days=-365)
    dateRangeEnd = datetime.datetime.now()
    acct0 = account_list[0]
    txs0 = acct0.transaction_set.filter(tx_date__range=(dateRangeStart, dateRangeEnd))
    if txs0.count()!=0:
        plotData = [(tx.tx_date, tx.balance) for tx in txs0.order_by('tx_date')]
        plotDates = [row[0] for row in plotData]
        plotBalances = [row[1] for row in plotData]
        # testPlot = figure(title='Test Plot', x_axis_label='Test X', y_axis_label='Test Y', plot_width=400, plot_height=400)
        bPlot = bkplotting.figure(title='Balance', x_axis_type='datetime', y_axis_label='$', plot_width=60, plot_height=30)
        bPlot.sizing_mode = 'scale_width'
        bPlot.line(plotDates, plotBalances, line_width=3)
        bScript, bPlot = bkembed.components(bPlot)
    else:
        bScript = ""
        bPlot = ""
    
    template = loader.get_template('finance/index.html')
    context = {
        'current_user': current_user,
        'account_list': account_list,
        'title': '',
        'bokehScript': bScript,
        'bokehPlot': bPlot,
    }
    return HttpResponse(template.render(context, request))

@login_required
def account_detail(request, account_id): # , dateRange) ?
    acct = get_object_or_404(Account, pk=account_id)
    userCats = FinanceCategory.objects.filter(user=request.user)
    dateRangeStart = datetime.datetime.now() + datetime.timedelta(days=-365)
    dateRangeEnd = datetime.datetime.now()
    catSums = account.aggregate_transactions_by_category(dateRangeStart, dateRangeEnd)
    for cat in userCats:
        if not cat in catSums: catSums[cat]=0
    
    txs = acct.transaction_set.filter(tx_date__range=(dateRangeStart, dateRangeEnd))
    plotData = [(tx.tx_date, tx.balance) for tx in txs.order_by('tx_date')]
    plotDates = [row[0] for row in plotData]
    plotBalances = [row[1] for row in plotData]
    # testPlot = figure(title='Test Plot', x_axis_label='Test X', y_axis_label='Test Y', plot_width=400, plot_height=400)
    bPlot = bkplotting.figure(title='Balance', x_axis_type='datetime', y_axis_label='$', plot_width=60, plot_height=30)
    bPlot.sizing_mode = 'scale_width'
    bPlot.line(plotDates, plotBalances, line_width=3)
    bScript, bPlot = bkembed.components(bPlot)

    jsData = 'abcd'
    context = {
        'account': account,
        'title': "Transactions",
        'catSums': catSums,
        'jsData': jsData,
        'bokehScript': bScript,
        'bokehPlot': bPlot
    }
    return render(request, 'finance/account_detail.html', context)

# @login_required
# def create_account(request):
#     current_user = request.user
#     context = {
#         'user':current_user
#         ,'title':"create account"
#     }
#     return render(request, 'finance/create.html', context)
@login_required
def create_account(request):
    context = {}
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            acct = form.save(commit=False)
            acct.user = request.user
            acct.save()

            initTx = Transaction(account=acct, decription='initial balance', amount=acct.init_balance, balance=acct.init_balance)
            initTx.save()
            #return render(request, 'finance/create_account.html', args)
            return HttpResponseRedirect(reverse('finance:index'))
    else:
        form = AccountForm()
        # if 'account_id' in request.GET:
        #     try:
        #         Account.objects.get(pk=request.GET.get('account_id'))
        #     except:
        #         form = AccountForm()
        #     else:
        #         acct = Account.objects.get(pk=request.GET.get('account_id'))
        #         form = AccountForm()
        # else:
        #    form = AccountForm()
    context['form'] = form
    return render(request, 'finance/create_account.html', context)
    