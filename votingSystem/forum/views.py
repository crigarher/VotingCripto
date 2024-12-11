from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from polls.views import generate_alias_hash
from .models import Thread, Post

@login_required
def thread_list(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'forum/thread_list.html', {'threads': threads})

@login_required
def create_thread(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            thread = Thread.objects.create(
                title=data['title'],
                body=data['body'],
                author=request.user 
            )
            return JsonResponse({
                'id': thread.id,
                'title': thread.title,
                'body': thread.body,
                'created_at': thread.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    # Si el método es GET, renderiza el formulario para crear un hilo
    return render(request, 'forum/create_thread.html')

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all().order_by('created_at')
    questions = thread.questions.all()  # Acceso gracias a related_name='questions'
    
    if 'alias_hash' not in request.session:
        alias_hash = generate_alias_hash()
        request.session['alias_hash'] = alias_hash
        request.session.modified = True
    alias_hash = request.session['alias_hash']
    print(alias_hash)
    user_is_admin = (
        request.user.is_authenticated and 
        request.user.groups.filter(name="admin").exists()
    )    
    return render(request, 'forum/thread_detail.html', 
            {'thread': thread, 'posts': posts, 'questions': questions, 'user_is_admin': user_is_admin, 'alias_hash': alias_hash})


@login_required
def create_post(request, thread_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            thread = get_object_or_404(Thread, id=thread_id)
            alias_hash = request.session.get('alias_hash')
            if not alias_hash:
                # Generar un hash en caso de que no exista y guardarlo en la sesión
                alias_hash = generate_alias_hash()
                request.session['alias_hash'] = alias_hash
                request.session.modified = True
            post = Post.objects.create(
                thread=thread,
                body=data['body'],
                anonymous_author=alias_hash,
               
            )
            print(post)

            return JsonResponse({
                'id': post.id,
                'author_hash': post.anonymous_author,
                'body': post.body,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

@login_required
def obtener_posts(request, thread_id):
    try:
        thread = get_object_or_404(Thread, id=thread_id)
        posts = thread.posts.all().order_by('created_at')
      
        posts_json = [
            {
                'id': post.id,
                'anonymous_author': post.anonymous_author,
                'body': post.body,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            } for post in posts
        ]

        return JsonResponse({'posts': posts_json})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
