from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.http import HttpResponse
from django.core import serializers
import json
# from django_recaptcha_field import create_form_subclass_with_recaptcha
# from recaptcha import RecaptchaClient
# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post = post).order_by('created_date')

    # MyRecaptchaProtectedForm = create_form_subclass_with_recaptcha(CommentForm, recaptcha_client,)
    # if request.method == "POST":
    #     # form = CommentForm(request.POST, request = request)
    #     form = CommentForm(request.POST)
    #     # form = MyRecaptchaProtectedForm(request, request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.created_date = timezone.now()
    #         comment.post = post
    #         comment.save()
    #         return redirect('post_detail', pk=post.pk)
    # else:
    #     # form = CommentForm(request=request)
    form = CommentForm()
    #     # form = MyRecaptchaProtectedForm(request)
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments' : comments})
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

def like_comment(request):
    likes = 0
    if request.method == 'GET':
        pk = request.GET['comment_id']
        comment = get_object_or_404(Comment, int(pk))

        if comment:
            likes = comment.like + 1
            comment.les
            comment.save()

    return HttpResponse(likes)

def comment(request):
    print("hello")
    if request.method == 'POST':
        pk = request.POST.get('pk')
        author = request.POST.get('author')
        text = request.POST.get('text')
        response_data = {}
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post = post).order_by('created_date')
        comment = Comment(text=text, author=author, post=Post.objects.get(pk = pk))
        comment.save()

        response_data['result'] = 'Create post successful!'
        response_data['commentpk'] = comment.pk
        response_data['text'] = comment.text
        response_data['post'] = pk
        response_data['created'] = comment.created_date.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = comment.author

        # return HttpResponse(
        #     json.dumps(response_data),
        #     content_type="application/json"
        # )

        return render_to_response('blog/comment.html', {'comments' : comments})


    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def load_comment(request):
    comments = Comment.objects.filter(post = post).order_by('created_date')
    # return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments' : comments})
    return render(request, 'blog/comment.html', {
        'comments' : comments
    })
