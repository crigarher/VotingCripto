import hashlib
import os
import uuid
from xhtml2pdf import pisa
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from forum.models import Thread
from .models import Question, Choice, Vote
from .forms import QuestionForm, ChoiceFormSet
from account.decorator import group_required
from django.template.loader import render_to_string


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
    has_voted = Vote.objects.filter(user=request.session['alias_hash'], question=question).exists()
    return render(request, 'polls/detail.html', {'question': question, 'has_voted': has_voted})

# Get question and display results

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    votes = Vote.objects.filter(question=question).select_related('user', 'choice')
    return render(request, 'polls/results.html', {'question': question, 'votes': votes})

# Vote for a question choice


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if  not question.is_active:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "The poll is closed.",
        })
    
    # Verificar si el usuario ya votó en esta pregunta
    if Vote.objects.filter(user=request.session['alias_hash'], question=question).exists():
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
        Vote.objects.create(user=request.session['alias_hash'], question=question, choice=selected_choice)

        # Redirigir al usuario a la página de resultados
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))


@group_required('admin')
def create_poll(request, thread_id):
    # Obtén el hilo asociado al thread_id
    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and choice_formset.is_valid():
            # Crear la pregunta asociada al hilo
            question = question_form.save(commit=False)
            question.thread = thread
            question.save()

            # Guardar las opciones
            for form in choice_formset:
                choice = form.save(commit=False)
                if choice.choice_text:
                    choice.question = question
                    choice.save()

            # Redirigir de vuelta al detalle del hilo
            return redirect('thread_detail', thread_id=thread_id)
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none())

    return render(request, 'polls/create.html', {
        'question_form': question_form,
        'choice_formset': choice_formset,
        'thread': thread,
    })

def generate_alias_hash():
    alias = str(uuid.uuid4())
    return hashlib.sha256(alias.encode()).hexdigest()

def generate_pdf(request, question_id):
    # Obtener la pregunta y sus opciones
    question = get_object_or_404(Question, id=question_id)
    votes = Vote.objects.filter(question=question)
    print(question.question_text)
    # Renderizar el contexto en una plantilla HTML
    context = {
        'question': question,
        'votes': votes,
    }
    template_path = 'polls/question_result_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="results_{question.id}.pdf"'

    # Convertir HTML a PDF usando xhtml2pdf
    html = render_to_string(template_path, context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar si hubo errores en la conversión
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response
