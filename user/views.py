from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

import requests

from user.forms import RegistrationForm, AccountAuthenticationForm, PreferenceSelectionForm

from user.models import NewsPreference, NewsDomain

# Create your views here.

def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			# return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'user/register.html', context)


def logout_view(request):
	logout(request)
	return redirect("login_view")



def login_view(request, *args, **kwargs):
	context = {}

	user = request.user

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				is_exist_preference = NewsPreference.objects.filter(user_id=user.id, is_active=1)
				if is_exist_preference:
					return redirect('/user_home/'+str(user.id)) 
				else:
					return preference_set_view(request)
				# return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "user/login.html", context)


def preference_set_view(request):
	all_available_preference = {}

	user = request.user

	preferences = NewsDomain.objects.filter(is_active=1)

	all_available_preference['preferences'] = preferences
	all_available_preference['user'] = user

	return render(request, "user/choose_preference.html", all_available_preference)


def preference_submit(request, *args, **kwargs):
	context = {}
	if request.POST:
		form = PreferenceSelectionForm(request.POST)
		if form.is_valid():
			user_id = request.POST['user_id']
			news_preference = request.POST['news_preference']
			old_preferences = NewsPreference.objects.filter(user_id=user_id, is_active=1)
			if old_preferences:
				for obj in old_preferences:
					obj.is_active = False
					obj.save()

			new_preference_entry = NewsPreference(user_id=user_id, news_preference=news_preference)
			new_preference_entry.save()

	return HttpResponse("Updated!")






