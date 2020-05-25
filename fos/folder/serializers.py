from rest_framework import serializers
from .models import FolderHierarchy


class FolderCreateSerializer(serializers.Serializer):

	name = serializers.CharField(
		required=True,
		error_messages={
			"blank": "Name field can't be blank."
		}
	)
	# parent = serializers.CharField(
	# 	required=True,
	# 	error_messages={
	# 		"blank": "Parent field can't be blank."
	# 	}
	# )

	def validate(self, request_data):
		errors = {}

		# if request_data.get("parent"):
		# 	print(request_data.get("parent"))
		# 	if request_data.get("parent") is "self":
		# 		request_data["parent"] = None
		# 	else:
		# 		try:
		# 			check_parent = FolderHierarchy.objects.get(
		# 				parent_id=request_data.get("parent")
		# 			)
		# 			request_data["parent"] = check_parent
		# 		except FolderHierarchy.DoesNotExist:
		# 			error["parent"] = "Parent does not exist."

		if errors:
			raise serializers.ValidationError(errors)

		return request_data


class FolderExistanceSerializer(serializers.Serializer):

	folder_id = serializers.CharField(
		required=True,
		error_messages={
			"blank": "Folder can't be blank."
		}
	)

	def validate(self, request_data):
		errors = {}

		if request_data.get("folder_id"):
			try:
				check_folder_id = FolderHierarchy.objects.get(
					id=request_data.get("folder_id")
				)
				request_data["folder_id"] = check_folder_id
			except FolderHierarchy.DoesNotExist:
				request_data["folder_id"] = None
				errors["folder_id"] = "Folder does not exist."

		if errors:
			raise serializers.ValidationError(errors)

		return request_data
