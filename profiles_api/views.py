from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
	
from profiles_api import serializers

"""from rest_framework import status : This is the list of handy http status codes that can be used when returning response from the API"""

class HelloApiView(APIView):
	"""Test API View"""
	serializer_class = serializers.HelloSerializer

	def get(self, request, format=None):
		"""Retruns a list of APiview features"""

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