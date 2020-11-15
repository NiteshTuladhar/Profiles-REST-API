from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
	"""Serializes a name field for testing our APIView"""

	name 	= serializers.CharField(max_length=10)



class UserProfileSerializer(serializers.ModelSerializer):
	"""Serializes a user profile object"""

	class Meta:
		model = models.UserProfile
		fields = ('id','email','name','password')
		extra_kwargs = {

			'password' : {
				'write_only' : True,
				'style' : {'input_type' : 'password'}
			}
		}
		"""This extra_kwargs is used to specify that the password field is only write_only meaning it cannot be retreived like other fields."""



	"""We use this funtion which is actually built in already in rest framework beacuse to overwrite the existing funtion and call our create.user funtion from the models"""

	def create(self, validated_data):
		"""Creats and returns a new user"""
		user = models.UserProfile.objects.create_user(

			email = validated_data['email'],
			name = validated_data['name'],
			password = validated_data['password'],
		)

		return user