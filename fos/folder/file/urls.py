from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
	path(
		"file-upload/", 
		csrf_exempt(views.FileUpload.as_view()), name="file-upload"
	),

	path(
		"file-details/", 
		csrf_exempt(views.FileDetails.as_view()), name="file-details"
	),

	path(
		"file-list/", 
		csrf_exempt(views.FileList.as_view()), name="file-list"
	),
]