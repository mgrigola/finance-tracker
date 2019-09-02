from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
##from django.views import generic

from .models import Account, Transation, User, TransactionCategory

def index(request):
    # show the most recently published questions. exclude future-dated questions 
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))


def detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, 'finance/detail.html', {'account':account})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "invalid choice."
        })
    else:
        selected_choice.votes = F('votes')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) #need the empty comma here...
