from rest_framework import serializers
from .models import CustomUser


class UserSignUpSerializer(serializers.Serializer):

	email = serializers.CharField(
		required=True,
		error_messages={
			"blank": "Email field can't be blank."
		}
	)
	mobile = serializers.IntegerField(
		required=False
	)

	def validate(self, request_data):
		errors = {}

		if request_data.get("email"):
			try:
				check_email = CustomUser.objects.get(
					email__exact=request_data.get("email")
				)
				errors["email"] = "Email already exist."
			except CustomUser.DoesNotExist:
				request_data["email"] = request_data.get("email")

		if errors:
			raise serializers.ValidationError(errors)

		return request_data


class UserExistanceSerializer(serializers.Serializer):

	user_id = serializers.IntegerField(
		required=True,
		error_messages={
			"blank": "User can't be blank."
		}
	)

	def validate(self, request_data):
		errors = {}

		if request_data.get("user_id"):
			try:
				check_user_id = CustomUser.objects.get(
					id=request_data.get("user_id")
				)
				request_data["user_id"] = check_user_id				
			except CustomUser.DoesNotExist:
				request_data["user_id"] = None
				errors["user_id"] = "User does not exist."

		if errors:
			raise serializers.ValidationError(errors)

		return request_data
