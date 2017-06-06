# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic

from blog.models import Post, Comment


def home(request):
    template_name = 'blog/home1.html'
    posts = Post.objects.all()
    for i in posts:
        i.content = i.content[0:100] + "....."
    context = {'object_list': posts}
    return render(request, template_name, context)

def post_detail(request, postno):
    p = Post.objects.get(id=postno)
    c = Comment.objects.filter(post=p)
    template_name = "blog/post1.html"
    context = {"post": p, "comm": c}
    return render(request, template_name, context)


def login_page(request):
    if request.method == 'GET':
        template = "blog/login.html"
        return render(request, template)

    elif request.method =="POST":
        user_name = str(request.POST['username'])
        passwd = str(request.POST['password'])
        return HttpResponse()
