"""THIS FILE IS CREATED SO THAT THE USER IS ONLY ALLOWED TO EDIT THEIR OWN PROFILE AND NOT OTHERS"""

from rest_framework import permissions



class UpdateOwnProfile(permissions.BasePermission):
	"""Allows user to edit only their own profile"""


	"""This funtions below passes the authenticated user and and checks the permission"""
	def has_object_permission(self, request, view, obj):
		"""Check user is trying to edit their own profile or not"""

		"""SAFE_METHODS are the methods like CREATE,GET,LIST that does not perform any destructive changes to the existing objects"""
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.id == request.user.id



class UpdateOwnStatus(permissions.BasePermission):
	"""Allows users to update their own status"""


	def has_object_permission(self, request, view, obj):
		"""Check if the user is trying to update their own status in the feed"""

		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.user_profile.id == request.user.id