from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.utils import timezone

import json, csv, datetime, itertools, operator

import bokeh.plotting as bkplotting
import bokeh.embed as bkembed

from .models import Account, Transaction, FinanceCategory
from .forms import AccountForm, FinanceCategoryForm, UploadTransactionFileForm


@login_required
def all_account_summary(request):
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
    
    template = loader.get_template('finance/account_summary.html')
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
    catSums = acct.aggregate_transactions_by_category(dateRangeStart, dateRangeEnd)
    for cat in userCats:
        if not cat in catSums: catSums[cat]=0
    
    txs = acct.transaction_set.filter(tx_date__range=(dateRangeStart, dateRangeEnd))
    txData = [(tx.tx_date, tx.balance, tx.amount) for tx in txs.order_by('tx_date', '-id')]
    plotDates = [row[0] for row in txData]
    plotBalances = [row[1] for row in txData]

    debitDates = [x[0] for x in filter(lambda x: x[2] < 0, txData)]
    debitVals = [-x[2] for x in filter(lambda x: x[2] < 0, txData)]
    debitVals = list(itertools.accumulate(debitVals, operator.add))

    crebitDates = [x[0] for x in filter(lambda x: x[2] > 0, txData)]
    crebitVals = [x[2] for x in filter(lambda x: x[2] > 0, txData)]
    crebitVals = list(itertools.accumulate(crebitVals, operator.add))

    # testPlot = figure(title='Test Plot', x_axis_label='Test X', y_axis_label='Test Y', plot_width=400, plot_height=400)
    bPlot = bkplotting.figure(title='Balance', x_axis_type='datetime', y_axis_label='$', plot_width=60, plot_height=30)
    bPlot.title.text_font_size = '12pt'
    bPlot.title.align = 'center'
    bPlot.sizing_mode = 'scale_width'
    bPlot.line(plotDates, plotBalances, line_width=3, line_color='blue', legend_label='balance')
    bPlot.line(debitDates, debitVals, line_width=2, line_color='red', alpha=0.8, legend_label='total debits')
    bPlot.line(crebitDates, crebitVals, line_width=2, line_color='green', alpha=0.8, legend_label='total credits')
    bPlot.toolbar.logo = None
    bPlot.toolbar_location = None
    bPlot.legend.location = 'top_left'

    bScript, bPlot = bkembed.components(bPlot)

    jsData = 'abcd'
    context = {
        'account': acct,
        'title': "Transactions",
        'catSums': catSums,
        'jsData': jsData,
        'bokehScript': bScript,
        'bokehPlot': bPlot
    }
    return render(request, 'finance/account_detail.html', context)


@login_required
def account_export(request, account_id):
    #todo: provide different headers for different types of accounts? E.g. different banks and whatnot to match how they export data, maybe
    #todo: actually move to Account class
    acctSrc = get_object_or_404(Account, pk=account_id).acct_source
    
    if acctSrc == 'Chase Bank':
        tsvHeaders = ['Details', 'Posting Date','Description','Amount','Type','Balance','Check or Slip #']
    elif acctSrc == 'Schwab':
        tsvHeaders = ['Description', 'Date','Type','Amount','Balance']
    else:
        tsvHeaders = ['Description', 'Date','Type','Amount','Balance']

    response = HttpResponse(
        content_type='text/tsv',
        headers={'Content-Disposition': 'attachment; filename="transaction-import-template.tsv"'},
    )

    writer = csv.writer(response, delimiter='\t')
    writer.writerow(tsvHeaders)

    return response


@login_required
def account_export_empty(request, account_id):
    #todo: provide different headers for different types of accounts? E.g. different banks and whatnot to match how they export data, maybe
    #todo: actually move to Account class
    acctSrc = get_object_or_404(Account, pk=account_id).acct_source
    
    if acctSrc == 'Chase Bank':
        tsvHeaders = ['Details', 'Posting Date','Description','Amount','Type','Balance','Check or Slip #']
    elif acctSrc == 'Schwab':
        tsvHeaders = ['Description', 'Date','Type','Amount','Balance']
    else:
        tsvHeaders = ['Description', 'Date','Type','Amount','Balance']

    response = HttpResponse(
        content_type='text/tsv',
        headers={'Content-Disposition': 'attachment; filename="transaction-import-template.tsv"'},
    )

    writer = csv.writer(response, delimiter='\t')
    writer.writerow(tsvHeaders)

    return response


''' FORM INPUTS '''

@login_required
def account_create(request):
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
            return HttpResponseRedirect(reverse('finance:all_account_summary'))
    else:
        form = AccountForm()
    context['form'] = form
    return render(request, 'finance/account_create.html', context)


@login_required
def upload_transactions_file(request, account_id):
    acct = get_object_or_404(Account, pk=account_id)
    if request.method == 'POST':
        acct = get_object_or_404(Account, pk=account_id)
        form = UploadTransactionFileForm(request.POST, request.FILES)
        if form.is_valid():
            acct.load_transactions_from_file(request.FILES['txFile'])
            return HttpResponseRedirect(reverse('finance:account_detail', args=(account_id))
    else:
        form = UploadTransactionFileForm()
    return render(request, 'finance/account_import.html', {'form': form})
        
