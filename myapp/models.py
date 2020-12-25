# License: MIT
# Author: https://github.com/faridmv

from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.db import models


class MyUserManager(UserManager):

	def create_user(self, username, password=None):
		user = self.model(
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email=None, password=None):
		user = self.create_user(
			username,
			password=password,
		)
		user.is_admin = True
		user.is_superuser = True
		user.is_staff = True
		user.email = email.lower()
		user.save(using=self._db)
		return user


class MyUser(AbstractUser):
	username = models.CharField(verbose_name='Username', name='username', max_length=30, unique=True,
								validators=[
									validators.RegexValidator(regex=r'^(?!_)(?!.*\.\.)(?!.*\.$)[a-z0-9][a-z0-9.]{4,29}$',
															  message='Valid Characters: Lowercase Alphanumeric and a Dot(.)',
															  code='Invalid username'),
									validators.MinLengthValidator(limit_value=5)
								],
								error_messages={'unique': 'A user with that username already exists.',
												'invalid': 'Valid Characters: Lowercase Alphanumeric and at most one Underscore(_)'})
	objects = MyUserManager()
