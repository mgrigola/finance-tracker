from django.test import TestCase

import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question_with_date(question_text, day_delta):
    time = timezone.now() + datetime.timedelta(days=day_delta)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    # future question is NOT recent
    def test_was_published_recently__future_question(self):
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_time)
        self.assertIs(future_question.was_published_recently(), False)
    
    # >1 day old question is NOT recent
    def test_was_published_recently__old_question(self):
        past_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=past_time)
        self.assertIs(past_question.was_published_recently(), False)

    # <1 day old question is recent
    def test_was_published_recently__recent_question(self):
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    # no questions exist: indexview response is empty queryset
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    # one past question: indexview response is the question
    def test_past_question(self):
        create_question_with_date(question_text='past question?', day_delta=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list']
            ,['<Question: past question?>']
        )
    
    # one future question: indexview response is empty queryset
    def test_past_question(self):
        create_question_with_date(question_text='future question?', day_delta=2)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])