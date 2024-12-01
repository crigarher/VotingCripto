from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
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
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts})

@login_required
def create_post(request, thread_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            thread = get_object_or_404(Thread, id=thread_id)
            post = Post.objects.create(
                thread=thread,
                body=data['body'],
                author=request.user
            )
            return JsonResponse({
                'id': post.id,
                'author': post.author.username,
                'body': post.body,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
