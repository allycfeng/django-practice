from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import Context
from .models import Question, Choice
from .forms import UserSubmittedQuestionForm, ChoiceFormSet


class MyPollView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(owner=self.request.user.id)


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		#return Question.objects.order_by('pub_date')[:10]
		return Question.objects.order_by('pub_date')


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'	


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	
	try:
		print 'choice POST:',request.POST['choice']
		selected_choice = question.choice_set.get(pk=request.POST['choice'])

	except(KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html',{
			'question':question,
			'error_message':"You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return HttpResponseDirect after successfully dealing with POST data.
		# This prevents data from being posted twice if a user hit the back button

		#use reverse() to avoid hard-coded url
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

@login_required
def create(request):
	if request.POST:
		form = UserSubmittedQuestionForm(request.POST)
		if form.is_valid():
			question = form.save(commit=False)
			question.owner = User.objects.get(id=request.user.id)
			choice_formset = ChoiceFormSet(request.POST, instance=question)			
			if choice_formset.is_valid():
				question.save()
				choice_formset.save()
				return HttpResponseRedirect(reverse('polls:index'))
			else:
				print "errors", choice_formset.errors
				choice_formset.errormsg = "Please enter 2 choices"
				
		else:
			choice_formset = ChoiceFormSet(instance=Choice())
	else:
		form = UserSubmittedQuestionForm()
		choice_formset = ChoiceFormSet(instance=Choice())

	context = {
		"form": form,
		"choice_formset": choice_formset,
	}
	return render(request,'polls/create.html', context)

