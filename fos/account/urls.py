from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
	path(
		"sign-up/", 
		csrf_exempt(views.UserSignUp.as_view()), 
		name="sign-up"
	),
]
