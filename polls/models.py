from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
# Create your models here.

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published',auto_now_add=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		#return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

