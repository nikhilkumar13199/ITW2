# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
# Create your views here.

def index(request):
	cursor=connection.cursor()
	args={}
	cursor.execute('''select * from movies_list''')
	row=cursor.fetchall()
	print('ROW:',row)
	args['row']=row
	return render(request,'museo/index.html',args)

def register(request):
	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data['username']
			password=form.cleaned_data['password2']
			user=authenticate(username=username ,password=password)
			login(request,user)
			return redirect('/museo/index')
	else:
		form=UserCreationForm()
	context={'form':form}
	return render(request,'museo/sign_up.html',context)

def feed(request):
	cursor=connection.cursor()
	args={}
	username=""
	userid=-1
	if request.user.is_authenticated:
		username=request.user.username
		userid=request.user.id
	print(username)
	print(userid)
	pidx=0
	pids=request.POST.get('upvote')
	if pids!=None:
		pidx=int(pids)
	print(pidx)
	if pidx!=0:
		cursor.execute('''insert into user_upvote set user_id=%s,post_upvoted=%s''',[userid,pidx])
	
	
	cursor.execute('''select * from post_list''')
	row=cursor.fetchall()
	args['row']=row
	cursor.execute('''select post_upvoted from user_upvote where user_id=%s''',[userid])
	upvoted_posts=cursor.fetchall()
	args['upvoted_posts']=upvoted_posts
	print(upvoted_posts)
	return render(request,'museo/feed.html',args)