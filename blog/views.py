# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views import generic

from blog.forms import RegistrationForm
from blog.models import Post, Comment


def home(request):
    template_name = 'blog/home1.html'
    posts = Post.objects.all()
    for i in posts:
        i.content = i.content[0:100] + "....."
    context = {'object_list': posts}
    return render(request, template_name, context)

def post_detail(request, postno):
    if request.method =="POST":
        comment = request.POST['comment']
        user = User.objects.get(username=request.user.username)
        c = Comment(comment_text=comment, post_id=postno,user=user)
        c.save()
        return redirect("post", postno)
    else:
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
def new_post(request):
    if request.method == "POST":
        title = request.POST['post_title']
        content = request.POST['post_content']
        img = request.FILES['image']
        is_published = "False"
        if 'is_published' in request.POST:
            is_published = request.POST['is_published']
        user = User.objects.get(username=request.user.username)
        newp = Post(user=user,title=title, content=content, img=img, is_published=is_published)
        newp.save()
        return redirect('post',newp.id)
    else:
        template_name = 'blog/newpost.html'
        context ={}
        return render(request, template_name, context)

def edit_post(request, pk):
    post = Post.objects.get(id=int(pk))
    if request.user.username != post.user.username:
        raise PermissionDenied
    if request.method == "GET":
        template_name = 'blog/post_edit.html'
        context = {'post': post}
        return render(request,template_name, context)
    else:
        post.title = request.POST['post_title']
        post.content = request.POST['post_content']
        if 'img' in request.POST:
            post.img = request.FILES['image']
        if 'is_published' in request.POST:
            post.is_published = request.POST['is_published']
        post.save()
        return redirect('post',post.id)


def del_post(request, pk):
    post = Post.objects.get(id=int(pk))
    if request.user.username != post.user.username:
        raise PermissionDenied
    if post != None:
        p = post.id
        post.delete()
        return redirect('home')
    else:
        return HttpResponse("This post does not exist")

def del_com(request, postno, comno):
    post = Post.objects.get(id=int(postno))
    if request.user.username != post.user.username:
        raise PermissionDenied
    com = Comment.objects.get(id=int(comno))
    com.delete()
    return redirect('post',post.id)


def view_drafts(request):
    post = Post.objects.filter(is_published=False)
    context = {"post" : post}
    template = 'blog/draft.html'
    return render(request, template)

def comm_edit(request, postno, comno):
    post = Post.objects.get(id=postno)
    c = Comment.objects.get(id=comno)
    if request.user.username != post.user.username:
        raise PermissionDenied
    if request.method == "GET":
        template = 'blog/editcom.html'
        context = {"comment": c, "post": post}
        return render(request, template, context)
    else:
        comm = request.POST['comment']
        user = User.objects.get(username=request.user.username)
        com = Comment(id=comno, comment_text=comm, user=user,post_id=postno)
        com.save()
        return redirect('post', postno)

def create_acc(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            return HttpResponseRedirect('/accounts/login')
    form = RegistrationForm()
    context = {'form': form}
    print context
    template_name = 'registration/create_Acc.html'
    return render(request, template_name, context)

def base_page(request):
    return redirect('home')