from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.conf import settings

class UserProfileManager(BaseUserManager):
	"""Manager for user profiles"""

	def create_user(self,email,name,password=None):
		"""Create a new user profile"""
		if not email:
			raise ValueError('User must have an email address')

		email = self.normalize_email(email)
		user = self.model(email=email, name=name)
		

		user.set_password(password)
		user.save(using=self._db) 
		"""using=self._db allows us to use multiple db incase we change it in future"""

		return user


	def create_superuser(self,email,name,password):
		"""Create and save a new superuser with given details"""

		user = self.create_user(email,name,password)

		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db) 

		return user

	

class UserProfile(AbstractBaseUser, PermissionsMixin):
	"""Database model for users in the system"""

	email 		= models.EmailField(max_length=255, unique=True)
	name 		= models.CharField(max_length=255)
	is_active 	= models.BooleanField(default=True)
	is_staff	= models.BooleanField(default=False)


	objects = UserProfileManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']


	def get_full_nema(self):
		"""Retreive full name of the user"""

		return self.name


	def get_short_name(self):
		"""Retreive short name of user"""

		return self.name


	def __str__(self):
		"""Return string representation of our user"""

		return self.email



class ProfileFeedItem(models.Model):
	"""Profile status update"""

	user_profile = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	"""Here we used the settings.Auth_user_model because the auth_user_model specified in the settings so later if we want to change the user model and use"""
	"""the default django user models then there is no problems in the future """

	status_text = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		"""return the model as a string"""

		return self.status_text