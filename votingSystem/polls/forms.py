from django import forms
from django.forms import modelformset_factory
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pollEndDate']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

ChoiceFormSet = modelformset_factory(
    Choice,
    form=ChoiceForm,
    extra=2,
)
