from logging import exception
from operator import attrgetter
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CutomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from .models import*
from django.conf import settings
import requests
from django.core.mail import send_mail
import instaloader
from getpass import getpass

import time
import math
from bs4 import BeautifulSoup
import csv
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Create your views here.
@login_required(login_url='login')
def channel_selector(request):
	print('channelview')
	loginuser= request.user.username
	loggedUser= User.objects.filter(username=loginuser)
	print('LoginUSerchannel:', loginuser)
	print('In home view', request.POST, request.GET)
	channel_selected= request.POST.get('channel')
	print('channelselected:', channel_selected)
	channelobj= ChannelSelector.objects.create(user=loggedUser[0], channel=channel_selected)
	channelobj.save()
	return redirect('home')

def home(request):
	TopperFollowers = 0
	newlist = None
	
	# if request.method == 'POST':
	list_of_followers= []	
	print('In home view')
	followers=None
	username=""
	loginuser= request.user.username
	loggedUser= User.objects.filter(username=loginuser)
	print('LoginUSer:', loginuser)
	client_checked= None
	if request.method == 'POST':
		options = Options()
		options.headless = False
		main_url = "https://www.instagram.com"
		chrome_options = webdriver.ChromeOptions()
		driver = webdriver.Chrome(options=chrome_options)
		driver.get(main_url)
		time.sleep(4)
		user_name = "mikismines@gmail.com"
		password = "L00000000l#"
		driver.find_element_by_name("username").send_keys(user_name)
		driver.find_element_by_name("password").send_keys(password)   
		driver.find_elements_by_tag_name("button")[1].click()
		driver.get('https://www.instagram.com/' + str(user_name))
		new_user_name = "russellbrunson"
		driver.get('https://www.instagram.com/' + str(new_user_name))
		source = driver.page_source
		s= BeautifulSoup(source, "html.parser")
		tag= s.find("meta",  {"name" : "description"})
		try:
			text= tag.attrs["content"]
		except:
				pass
		status= text.split("-")[0]
		details = status.split(",")
		print(details)
		followers = details[0]
		following = details[1]
		posts = details[2]
		print(status,"\nfollowers", followers,"\nfollowing:",following)

		client_checked= request.POST.get('is_client')
		print('client_checked:' , client_checked)
		if followers != None and client_checked == 'is_client' :
			instaAccountObj = instaAccounts.objects.create(user=loggedUser[0], username=username,is_client=True)
			instaAccountObj.save()
		else:
			instaAccountObj = instaAccounts.objects.create(user=loggedUser[0], username=username,is_client=False)
			instaAccountObj.save()
	
		
	# comparisonObj = instaAccounts.objects.filter(user = loggedUser[0] )

	# # chrome_options = webdriver.ChromeOptions()
	# options = Options()
	# driver = webdriver.Firefox(options=options)
	# options.headless = False
	# main_url = "https://www.instagram.com"
	# driver.get(main_url)
	# time.sleep(10)
	# user_name = "mikismines@gmail.com"
	# password = "L00000000l#"
	# driver.find_element_by_name("username").send_keys(user_name)
	# driver.find_element_by_name("password").send_keys(password)   
	# driver.find_elements_by_tag_name("button")[1].click()
		
	# for compair in comparisonObj:
	# 	username = compair.username	
	# 	client=compair.is_client
	# 	driver.get('https://www.instagram.com/' + str(user_name))
	# 	new_user_name = "russellbrunson"
	# 	driver.get('https://www.instagram.com/' + str(new_user_name))
	# 	source = driver.page_source
	# 	s= BeautifulSoup(source, "html.parser")
	# 	tag= s.find("meta",  {"name" : "description"})
	# 	try:
	# 		text= tag.attrs["content"]
	# 	except:
	# 			pass
	# 	status= text.split("-")[0]
	# 	details = status.split(",")
	# 	print(details)
	# 	followers = details[0]
	# 	following = details[1]
	# 	posts = details[2]
	# 	print(status,"\nfollowers", followers,"\nfollowing:",following)
		
	# 	temp = {'username':username,'followers':followers, 'is_client': client }
	# 	list_of_followers.append(temp)
	# 	newlist = sorted(list_of_followers, key=lambda d: d['followers'], reverse=True) 
		
	# 	Topperelement= newlist[0]
	# 	TopperFollowers=Topperelement.get('followers')
	# 	print('Followers1',TopperFollowers)
	# print('New list', newlist)

	temp = {'username':'tayyabimran8','followers':100, 'is_client': True }
	list_of_followers.append(temp)

	temp = {'username':'chk','followers':40, 'is_client': False }
	list_of_followers.append(temp)

	temp = {'username':'no Client2','followers':80, 'is_client': False }
	list_of_followers.append(temp)

	temp = {'username':'chk2','followers':20, 'is_client': False }
	list_of_followers.append(temp)

	temp = {'username':'no Client','followers':30, 'is_client': False }
	list_of_followers.append(temp)

	newlist = sorted(list_of_followers, key=lambda d: d['followers'], reverse=True) 

	Topperelement= newlist[0]
	TopperFollowers=Topperelement.get('followers')

	finalList = []
	for l in range(len(newlist)):
		if l != len(newlist) and l !=0:
			temp = {
				'username':newlist[l]['username'],
				'followers':newlist[l]['followers'], 
				'is_client': newlist[l]['is_client'], 
				'to_step_up': newlist[l-1]['followers'] - newlist[l]['followers'],
				'to_top': newlist[0]['followers'] - newlist[l]['followers'],
			}
			finalList.append(temp)
		elif l == 0:
			temp = {
				'username':newlist[0]['username'],
				'followers':newlist[0]['followers'], 
				'is_client': newlist[0]['is_client'], 
				'to_step_up': 0,
				'to_top': 0,
			}
			finalList.append(temp)

	channelindb= ChannelSelector.objects.filter(user=loggedUser[0]) 
	if channelindb.exists():
		channelindb = channelindb[0]
	
	context = {
		'topper_followers': TopperFollowers,
		'channel': channelindb,
		'comparisonObj':finalList,
	}
	return render(request,'User/home.html',context)



def loginUser(request):

	if request.user.is_authenticated:
		return redirect('home')
	msg = None
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			user = User.objects.get(username=username)
			user = authenticate(request, username=username, password=password) # check password

			if user is not None and accountsCheck.objects.get(user=user).is_verified:
				login(request, user)
				return redirect('home')
			else:
				msg = 'User/Something is wrong'
		except:
			msg = 'User not recognized.'
	context = {
		'msg':msg
	}
	return render(request,'User/login.html',context)

def register(request):
	msg = None
	form = CutomUserCreationForm
	if request.method == 'POST':
		form = CutomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			# user.username = user.username.lower()
			user.save()

			auth_token = str(uuid.uuid4())
			accountsCheck_obj = accountsCheck.objects.create(user=user, auth_token = auth_token)
			accountsCheck_obj.save()

			verificationMain(user.email,auth_token)

			msg = 'Verifecation Link has been send to your mail. Kindly verify it.'
			context = {'form':form, 'msg':msg}
			return render(request,'User/register.html', context)
		else:
			msg = 'Error.'
	context = {'form':form, 'msg':msg}
	return render(request,'User/register.html', context)

def verify(request, auth_token):
    accountsCheck_obj = accountsCheck.objects.get(auth_token = auth_token)
    if accountsCheck:
        accountsCheck_obj.is_verified = True
        accountsCheck_obj.save()
        return redirect('login')

def verificationMain(email, auth_token):
    subject = 'Please verify your account'
    message = f'Hi please click on the link to verify your account http://localhost:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from, recipient_list)

def logoutUser(request):
	logout(request)
	return redirect('login')

# def InstagramLoginUser(request):
	
# 	L = instaloader.Instaloader()

	
# 	return redirect('home')