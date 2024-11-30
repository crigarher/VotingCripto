from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Question, Choice
from .forms import QuestionForm, ChoiceFormSet

# Get questions and display them


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choices


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

# Get question and display results


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Vote for a question choice


def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))



def create_poll(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        
        choice_formset = ChoiceFormSet(request.POST)
        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save()
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print(choice_formset)

            for form in choice_formset:
                choice = form.save(commit=False)  
                if choice.choice_text:
                    choice.question = question
                    choice.save()

            return redirect('index')
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none())

    return render(request, 'polls/create.html', {
        'question_form': question_form,
        'choice_formset': choice_formset,
    })