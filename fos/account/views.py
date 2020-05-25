from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import *
from .serializers import *


class UserSignUp(CreateAPIView):
	serializer_class = UserSignUpSerializer
	# authentication_classes = [authentication.TokenAuthentication]
	# permission_classes = [permissions.IsAdminUser]

	def post(self, request):
		response = {}

		request_data = UserSignUpSerializer(
			data=request.data
		)
		check_request_data = request_data.is_valid()
		
		if check_request_data:
			validated_data = request_data.validated_data
			try:
				instance = CustomUser.objects.create(
					first_name=request.data.get("first_name"),
					last_name=request.data.get("last_name"),
					email=validated_data.get("email"),
					username=request.data.get("username"),
					mobile=validated_data.get("mobile"),
					is_staff=True
				)
				instance.set_password(request.data.get("password"))
				instance.save()
				response = {
					"id": instance.id,
					"message": "Signup successful.",
					"status": 200
				}
			except Exception as err:
				response = {
					"message": str(err),
					"status": 201
				}
		else:
			response = {
				"errors": request_data.errors,
				"status": 201
			}

		return Response(response)
