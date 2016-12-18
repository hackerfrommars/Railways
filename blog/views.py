#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import mechanize
import sys
from bs4 import BeautifulSoup


from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
from django.template import RequestContext

# from django_recaptcha_field import create_form_subclass_with_recaptcha
# from recaptcha import RecaptchaClient
# Create your views here.

def post_list(request):
	if request.method == "POST": 
		from_station = request.POST.get("from_station", "")
		to_station = request.POST.get("to_station", "")
		date = request.POST.get("date", "")
	elif request.method == "GET" and request.GET.get("from_station"): 
		from_station = request.GET["from_station"]
		to_station = request.GET["to_station"]
		date = request.GET["date"]		
	else:
		from_station = "АСТАНА" 
		to_station = "АЛМА АТА 1"
		date = "31.12.2016"

	res = ""	

	reload(sys)
	sys.setdefaultencoding('utf-8')

	cj = mechanize.CookieJar()

	br = mechanize.Browser()
	br.set_cookiejar(cj)

	br.set_handle_robots(False)
	br.set_handle_referer(True)
	br.set_handle_refresh(True)
	br.set_handle_equiv(True)
	br.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
	url = 'http://railways.kz/'
	br.open(url)
	br.select_form(nr=1)
	br.form['FROM_STATION'] = from_station
	br.form['TO_STATION'] = to_station
	br.form['DATE'] = date
	f = br.submit()
	soup = BeautifulSoup(f.read())

	res = res + from_station + " => " + to_station + " :: " + date + " :: "
	res = "{ 'res': [{'from_station': '" + from_station + "', 'to_station': '" + to_station + "', 'date': '" + date + "'}" 

	path = soup.find_all("a", {"class" : "link link-location jsTooltip"})
	time_from = soup.find_all("span", {"class" : "time-from"})
	time_to = soup.find_all("span", {"class" : "time-to"})
	second_class = soup.find_all("td", {"data-wagon-type" : "second-class"})
	compartment = soup.find_all("td", {"data-wagon-type" : "compartment"})
	luxury = soup.find_all("td", {"data-wagon-type" : "luxury"})	

	for i in range(len(path)):
		res += ", {'path': '" + path[i].text[1:] + "', "
		res += "'time_from': '" + time_from[i].text + "', "
		res += "'time_to': '" + time_to[i].text + "', "
		res += "'price_luxury': '" + luxury[i].text + "', " 		
		res += "'price_compartment': '" + compartment[i].text + "', "
		res += "'price_second': '" + second_class[i].text + "'}"
	
	res += "]}"	


	return HttpResponse(res)

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
