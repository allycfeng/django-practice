from django import forms
from .models import Question, Choice
from django.forms.models import inlineformset_factory, BaseInlineFormSet


MAX_CHOICES = 2

class MandatoryInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
        	raise forms.ValidationError('You must have at least one order', code='missing data')

	def __init__(self, *args, **kwargs):
		super(BaseInlineFormSet, self).__init__(*args, **kwargs)
		no_of_forms = len(self)
		for i in range(0, no_of_forms):
			#self[i].fields['choice_text'].label += "haha-%d" % (i+1)
			self.fields['choice_text'].label += "haha-%d" % (i+1)

ChoiceFormSet = inlineformset_factory(Question,
    Choice,
    can_delete=False,
    fields=['choice_text'],
    extra=MAX_CHOICES,
    formset=MandatoryInlineFormSet)

class UserSubmittedQuestionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.fields['question_text'].label = "Poll Question"

	class Meta:
		model = Question
		fields=['question_text']
        #exclude = ('pub_date', )