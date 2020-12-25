# License: MIT
# Author: https://github.com/faridmv

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.views import View

from core.models import MyUser


class MyUserCreationForm(UserCreationForm):
	class Meta:
		model = MyUser
		fields = ('username', 'password1', 'password2',)


class SignUp(generic.CreateView):
	form_class = MyUserCreationForm
	success_url = reverse_lazy('home')
	template_name = 'myapp/signup.html'

	def post(self, request):
		if request.user.is_authenticated:
			return redirect('home')

		form = MyUserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect(self.success_url)
		
		ctx = {'form': form}
		return render(request, self.template_name, ctx)

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('home')

		form = MyUserCreationForm()
		ctx = {'form': form}
		return render(request, self.template_name, ctx)
