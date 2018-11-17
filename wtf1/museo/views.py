# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
	#print(username)
	#print(userid)
	pidx=0
	pids=request.POST.get('upvote')
	puds=request.POST.get('downvote')

	if pids!=None:
		pidx=int(pids)
	#print(pidx)
	

	if pidx!=0:
		cursor.execute('''select * from user_upvote where user_id=%s and post_upvoted=%s;''',[userid,pidx])
		row2=cursor.fetchall()
		if len(row2)>0:
			messages.warning(request,"This post is already upvoted by you")
			print(1)
			
		else:
			cursor.execute('''insert into user_upvote set user_id=%s,post_upvoted=%s;''',[userid,pidx])
	if puds!=None:
		cursor.execute('''select * from user_downvote where user_id=%s and post_downvoted=%s;''',[userid,puds])
		row2=cursor.fetchall()
		if len(row2)>0:
			messages.warning(request,"This post is already downvoted by you")
			print(2)
		else:
			cursor.execute('''insert into user_downvote set user_id=%s,post_downvoted=%s''',[userid,puds])
	
	cursor.execute('''select * from post_list''')
	row=cursor.fetchall()
	args['row']=row
	cursor.execute('''select post_upvoted from user_upvote where user_id=%s;''',[userid])
	upvoted_posts=cursor.fetchall()
	args['upvoted_posts']=upvoted_posts
	#print(upvoted_posts)
	return render(request,'museo/feed.html',args)

def createpost(request):
	cursor=connection.cursor()
	args={}
	content=str(request.POST.get('content'))
	print(content)
	if content!="None":
		print(1)
		cursor.execute('''insert into post_list(uid,upvotes,downvotes,content) values(%s,0,0,%s);''',[request.user.id,content])
	#cursor.execute('''delete from post_list where content=%s;''',["None"])
	else:
		print(2)

	return render(request,'museo/createpost.html',args)

def topusers(request):
	cursor=connection.cursor()
	args={}
	cursor.execute('''select uid,sum(upvotes),sum(downvotes) from post_list group by uid order by sum(upvotes)-sum(downvotes) desc''')
	row=cursor.fetchall()
	print('ROW:',row)
	args['row']=row
	return render(request,'museo/topusers.html',args)

def profile(request):
	pass
