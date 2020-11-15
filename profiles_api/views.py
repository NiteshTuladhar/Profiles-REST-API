from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

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

