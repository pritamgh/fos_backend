from django.db import models
import uuid
from account.models import CustomUser
from folder.models import FolderHierarchy
from common.storage import MediaStorage


class UploadedFile(models.Model):

	uuid = models.UUIDField(
	    primary_key=True, default=uuid.uuid4, editable=False,
	)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
		related_name="uploaded_file_owner"
	)
	folder = models.ForeignKey(FolderHierarchy, on_delete=models.CASCADE, 
		related_name="uploaded_file_folder"
	)
	name = models.CharField(
		max_length=20,
		blank=False
	)
	size = models.CharField(
		max_length=10,
		null=True,
		blank=True
	)
	extension = models.CharField(
		max_length=10,
		null=True,
		blank=True
	)
	thumb = models.CharField(
		max_length=300,
		null=True,
		blank=True
	)
	download_url = models.TextField(
		null=True,
		blank=True
	)
	description = models.TextField(
		null=True,
		blank=False
	)

	created = models.DateTimeField(auto_now_add=True)

