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
		driver = webdriver.Firefox(options=options)
		main_url = "https://www.instagram.com/accounts/login/"
		driver.get(main_url)

		time.sleep(4)
		user_name = "testingdjango009@gmail.com"
		password = "ShAn123456"
		driver.find_element_by_name("username").send_keys(user_name)
		driver.find_element_by_name("password").send_keys(password)   
		driver.find_elements_by_tag_name("button")[1].click()

		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[4]/a')))
		driver.get('https://www.instagram.com/' + str(user_name))
		time.sleep(7)
		username = request.POST.get('username')
		driver.get('https://www.instagram.com/' + str(username))
		# page source
		source = driver.page_source
		# scrapper
		s= BeautifulSoup(source, "html.parser")
		tag= s.find("meta",  {"name" : "description"})
		try:
			text= tag.attrs["content"]
		except:
				pass

		status= text.split("-")[0]
		details = status.split(",")
		print(details)
		followers_temp = details[0]

		client_checked= request.POST.get('is_client')
		print('client_checked:' , client_checked)
		if followers_temp != None and client_checked:
			instaAccountObj = instaAccounts.objects.create(user=loggedUser[0], username=username,is_client=True)
			instaAccountObj.save()
		else:
			instaAccountObj = instaAccounts.objects.create(user=loggedUser[0], username=username,is_client=False)
			instaAccountObj.save()

	comparisonObj = instaAccounts.objects.filter(user = request.user)

	if comparisonObj:
		options = Options()
		options.headless = False
		driver = webdriver.Firefox(options=options)
		main_url = "https://www.instagram.com/accounts/login/"
		driver.get(main_url)

		time.sleep(4)
		user_name = "testingdjango009@gmail.com"
		password = "ShAn123456"
		driver.find_element_by_name("username").send_keys(user_name)
		driver.find_element_by_name("password").send_keys(password)   
		driver.find_elements_by_tag_name("button")[1].click()

		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[4]/a')))
		driver.get('https://www.instagram.com/' + str(user_name))
		time.sleep(7)

		for compair in comparisonObj:
			username = compair.username	
			client=compair.is_client
			driver.get('https://www.instagram.com/' + str(username))
			# page source
			source = driver.page_source
			# scrapper
			s= BeautifulSoup(source, "html.parser")
			tag= s.find("meta",  {"name" : "description"})
			try:
				text= tag.attrs["content"]
			except:
					pass

			status= text.split("-")[0]
			details = status.split(",")
			print(details)
			followers_temp = details[0]

			followers = 0
			if 'm' in followers_temp:
				temp = followers_temp.split('m')
				num = float(temp[0])
				followers = num*1000000
			elif 'k' in followers_temp:
				temp = followers_temp.split('m')
				num = float(temp[0])
				followers = num*1000
			else:
				print(followers_temp,"***********")
				temp = followers_temp.split(' ')
				print(temp[0],"***********")
				num = float(temp[0])
				followers = num
			
			temp = {'username':username,'followers':followers, 'is_client': client }
			list_of_followers.append(temp)
			newlist = sorted(list_of_followers, key=lambda d: d['followers'], reverse=True) 
			
			Topperelement= newlist[0]
			TopperFollowers=Topperelement.get('followers')
			print('Followers1',TopperFollowers)
		print('New list', newlist)

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
					'to_step_up': int(newlist[l-1]['followers'])-int(newlist[l]['followers']),
					'to_top': newlist[0]['followers']-int(newlist[l]['followers']),
					'position':l,
				}
				finalList.append(temp)
			elif l == 0:
				temp = {
					'username':newlist[0]['username'],
					'followers':newlist[0]['followers'], 
					'is_client': newlist[0]['is_client'], 
					'to_step_up': 0,
					'to_top': 0,
					'position':0,
				}
				finalList.append(temp)

		channelindb= ChannelSelector.objects.filter(user=request.user) 
		if channelindb.exists():
			channelindb = channelindb[0]
		
		context = {
			'topper_followers': TopperFollowers,
			'channel': channelindb,
			'comparisonObj':finalList,
		}
		return render(request,'User/home.html',context)
	channelindb= ChannelSelector.objects.filter(user=request.user) 
	if channelindb.exists():
		channelindb = channelindb[0]
	context = {
			'channel': channelindb,
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

			verificationMain(request,user.email,auth_token)

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

def verificationMain(request,email, auth_token):
    subject = 'Please verify your account'
    message = f'Hi please click on the link to verify your account {request.build_absolute_uri()}verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from, recipient_list)

def logoutUser(request):
	logout(request)
	return redirect('login')

# def InstagramLoginUser(request):
	
# 	L = instaloader.Instaloader()

	
# 	return redirect('home')