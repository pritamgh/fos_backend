from rest_framework import serializers
from account.models import CustomUser
from ..models import FolderHierarchy
from .models import UploadedFile


class FileUploadSerializer(serializers.Serializer):
	file = serializers.FileField(
		required=True
	)
	name = serializers.CharField(
		required=False
	)
	size = serializers.IntegerField(
		required=False
	)
	extension = serializers.CharField(
		required=False
	)

	def validate(self, request_data):
		errors = {}

		if request_data.get("file"):
			if len(request_data.get("file").name) > 30:
				errors["name"] = "File name should be less than 30."
			else:
				request_data["name"] = request_data.get("file").name
			if request_data.get("file").size > 1000000:
				errors["size"] = "File size should be less than 1 mb."
			else:
				request_data["size"] = request_data.get("file").size
			if request_data.get("file").content_type:
				request_data["extension"] = request_data.get("file").content_type

		if errors:
			raise serializers.ValidationError(errors)

		return request_data


class MetadataExistanceSerializer(serializers.Serializer):

	user_id = serializers.IntegerField(
		required=True,
		error_messages={
			"blank": "User can't be blank."
		}
	)

	folder_id = serializers.CharField(
		required=True,
		error_messages={
			"blank": "Folder can't be blank."
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

		if request_data.get("folder_id"):
			try:
				check_folder_id = FolderHierarchy.objects.get(
					id=request_data.get("folder_id")
				)
				request_data["folder_id"] = check_folder_id
			except FolderHierarchy.DoesNotExist:
				request_data["folder_id"] = None
				errors["folder_id"] = "Folder does not exist."

		if request_data["user_id"] and request_data["folder_id"]:
			check_metadate = UploadedFile.objects.filter(
				user_id=request_data["user_id"].id,
				folder_id=request_data["folder_id"].id
			)
			if not check_metadate:
				errors["blank"] = "Folder contains nothing."

		if errors:
			raise serializers.ValidationError(errors)

		return request_data
