from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
	path(
		"folder-create/", 
		csrf_exempt(views.FolderCreate.as_view()), name="folder-create"
	),

	path(
		"folder-details/", 
		csrf_exempt(views.FolderDetails.as_view()), name="folder-details"
	),

	path(
		"folder-list/",
		csrf_exempt(views.FolderList.as_view()), name="folder-list"
	),

 	path(
        "file/", 
        include(("folder.file.urls", "file"), namespace="file")
    ),
]
