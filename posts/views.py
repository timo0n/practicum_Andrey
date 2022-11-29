from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Group, Post

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.POST_COUNT_DEFAULT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post_list': post_list,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, settings.POST_COUNT_DEFAULT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'post_list': post_list,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    posts_cnt = author.posts.count()
    paginator = Paginator(post_list, settings.POST_COUNT_DEFAULT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
        'post_cnt': posts_cnt,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_cnt = post.author.posts.count()
    # form = CommentForm()
    context = {
        'post': post,
        'post_cnt': posts_cnt,
       # 'form': form,
       # 'comments':post.comments.select_related('author')
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    title = 'Создание нового поста'
    template = 'posts/post_create.html'
    form = PostForm(request.POST or None)
    form.author = request.user
    error = 'Заполните форму!'
    context = {
        'form': form,
        'title': title,
        'error': error,
    }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    else:
        return render(request, template, context,)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post.id)
    context = {'form': form, 'is_edit': True}
    return render(request, 'posts/post_create.html', context)

