from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, Vote
from .forms import QuestionForm, ChoiceFormSet
from account.decorator import group_required



# Get questions and display them

@login_required
def index(request):
    # Obtener las últimas 5 preguntas publicadas
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    if request.user.is_authenticated:
        # Obtener IDs de preguntas en las que el usuario ya ha votado
        voted_question_ids = Vote.objects.filter(
            user=request.user,
            question__in=latest_question_list
        ).values_list('question_id', flat=True)
    else:
        # Si el usuario no está autenticado, no ha votado en ninguna pregunta
        voted_question_ids = []
    
    context = {
        'latest_question_list': latest_question_list,
        'voted_question_ids': voted_question_ids
    }
    
    return render(request, 'polls/index.html', context)

# Show specific question and choices

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Verificar si el usuario ya votó
    has_voted = Vote.objects.filter(user=request.user, question=question).exists()
    return render(request, 'polls/detail.html', {'question': question, 'has_voted': has_voted})

# Get question and display results

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Vote for a question choice


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Verificar si el usuario ya votó en esta pregunta
    if Vote.objects.filter(user=request.user, question=question).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You have already voted on this question.",
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Mostrar el formulario de votación nuevamente si no se seleccionó una opción
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Incrementar el voto en la opción seleccionada
        selected_choice.votes += 1
        selected_choice.save()

        # Registrar el voto en el modelo Vote
        Vote.objects.create(user=request.user, question=question)

        # Redirigir al usuario a la página de resultados
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))


@group_required('admin')
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

            return redirect('polls:index')
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none())

    return render(request, 'polls/create.html', {
        'question_form': question_form,
        'choice_formset': choice_formset,
    })