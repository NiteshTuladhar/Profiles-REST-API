from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

"""For searching objects"""
from rest_framework import filters

"""For login authentication"""
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.settings import api_settings

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions



"""from rest_framework import status : This is the list of handy http status codes that can be used when returning response from the API"""

class HelloApiView(APIView):
	"""Test API View"""
	serializer_class = serializers.HelloSerializer

	def get(self, request, format=None):
		"""Returns a list of APiview features"""

		an_apiview = [

			'Uses HTTP methods as function (get,post,patch,put,delete)',
			'Is similar to a traditional Django View',
			'Gives you the most control over your application logic',
			'Is mapped manuallly to URLS',

		]


		return Response({'message':'Hello','an_apiview':an_apiview})


	def post(self,request):
		"""Create a hello message with our name"""

		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			name = serializer.validated_data.get('name')
			message  = f'Hello {name}'

			return Response({'message': message})

		else:
			return Response(

				serializer.errors,
				status = status.HTTP_400_BAD_REQUEST


			)


	def put(self,request,pk=None):
		"""Handles updating an object"""

		return Response({'method': 'PUT'})


	def patch(self,request,pk=None):
		"""Handles the partial update of an object eg: if there is first name and last name and we patch the last name it does not delete the first name and create an new obj all together like the put method"""

		return Response({'method':'PATCH'})


	def delete(self,request,pk=None):
		""" Delete an object"""

		return Response({'method':'Delete'})



class HelloViewSet(viewsets.ViewSet):
	"""Test API ViewSet"""
	serializer_class = serializers.HelloSerializer

	def list(self, request):
		"""Returns hello message"""

		a_viewset = [

			'Uses actions (list, create, retrieve, update, partial_update)',
			'Automatically maps to urls using Routers',
			'Provides more funtionality with less code'

		]

		return Response({'message':'Hello!','a_viewset':a_viewset})


	def create(self,request):
		"""Create a new hello message"""
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid:
			name = serializer.validated_data.get('name')
			message = f'Hello {name}!'

			return Response({'message':message})

		else:
			return Response(
				serializer.errors,
				status = status.HTTP_400_BAD_REQUEST
			)


	def retrieve(self,request,pk=None):
		"""Handle getting an object by its id"""

		return Response({'http_method': 'GET'})


	def update(self,request,pk=None):
		"""Handle updating an object"""
		return Response({'http_method': 'PUT'})

	def partial_update(self,request,pk=None):
		"""Handle updating part of an object"""
		return Response({'http_method':'PATCH'})

	def destroy(self, request, pk=None):
		"""Handle removing an object"""
		return Response({'http_method':'dELETE'})




class UserProfileViewSet(viewsets.ModelViewSet):
	"""Handle creating and updating profiles"""

	serializer_class = serializers.UserProfileSerializer
	queryset = models.UserProfile.objects.all()

	authentication_classes = (TokenAuthentication,)
	""",after TokenAuthentication so that the token gets created as a tuple and not a single obj"""

	permission_classes = (permissions.UpdateOwnProfile,)

	filter_backends = (filters.SearchFilter,)
	search_fields = ('name','email',) 
	"""This search_field will allow us to search based on name and email"""


class UserLoginApiView(ObtainAuthToken):
	"""Handles creating user authentication tokens"""

	"""renderer_classes is used so that class is visible in the browsable django admin site or browsable api"""
	"""Since other classes like UserProfileViewset that has viewsets.ModelViewSet has this by default but the ObtainAuthToken does not have it as default"""
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class UserProfileFeedViewSet(viewsets.ModelViewSet):
	"""Handles creating, reading and updating profile feed items"""
	authentication_classes = {TokenAuthentication,}
	serializer_class = serializers.ProfileFeedItemSerializer
	queryset = models.ProfileFeedItem.objects.all()

	permission_classes = {

		permissions.UpdateOwnStatus,

		IsAuthenticated


	}

	"""IsAuthenticatedOrReadOnly"""
	"""The IsAuthenticatedorReadOnly allows unauthenticated user to view the feed but the IsAuthenticated does not allow the unauthenticated user to even view the feed"""

	"""The permission_classes is taken from permission.py whose funtion is to not allow the unauthenticated user to create any feeds"""

	def perform_create(self, serializer):
		"""Sets the user profile to the logged in user while creating the feed which was set as readonly in serializer.py"""
		serializer.save(user_profile = self.request.user)

