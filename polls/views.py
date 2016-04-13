from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import Context
from .models import Question, Choice


# Create your views here.

# function-based view
# def index(request):
# 	latest_question_list = Question.objects.order_by('pub_date')[:5]
# 	output = ', '.join([q.question_text for q in latest_question_list])
# 	#return HttpResponse(output)

# 	context = {
# 		'latest_question_list': latest_question_list
# 	}
# 	#template = loader.get_template('polls/index.html')
# 	#return HttpResponse(template.render(context, request))

# 	#the same thing. as shortcut
# 	return render(request, 'polls/index.html', context)


# def detail(request, question_id):

# 	# try:
# 	# 	question = Question.objects.get(pk=question_id)
# 	# except Question.DoesNotExist:
# 	# 	raise Http404("Question does not exist")

# 	question = get_object_or_404(Question, pk=question_id)

# 	return render(request, 'polls/detail.html', {'question':question})

# def results(request, question_id):
# 	#response = "You're looking at result %s"
# 	#return HttpResponse( response % question_id)
# 	question = get_object_or_404(Question,pk=question_id)
# 	return render(request, 'polls/results.html',{'question':question})

def about(request):	
	return render(request, 'polls/about.html', {} )

#try class-based generic view
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.order_by('pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'	

def vote(request, question_id):
	#return HttpResponse("You're voting on question %s" % question_id)

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


