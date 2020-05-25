from rest_framework import status
from rest_framework.generics import (
	CreateAPIView, RetrieveAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import *
from .serializers import *
from account.serializers import UserExistanceSerializer


class FolderCreate(CreateAPIView):

	def post(self, request):
		""" create Folder of an user
			method: POST
		"""

		user_id = UserExistanceSerializer(data=request.data)
		request_data = FolderCreateSerializer(data=request.data)
		check_user_id = user_id.is_valid()
		check_request_data = request_data.is_valid()

		if check_user_id and check_request_data:
			validated_user_id = user_id.validated_data
			validated_request_data = request_data.validated_data

			try:
				instance = FolderHierarchy.objects.create(
					name=validated_request_data.get("name"),
					# parent_id=validated_data.get("parent"),
					user_id=validated_user_id.get("user_id").id
				)

				return Response({
					"id": instance.id,
					"message": "Folder created successfully.",
				}, status=status.HTTP_201_CREATED)
			
			except Exception as err:
				return Response({
					"errors": str(err),
				}, status=status.HTTP_400_BAD_REQUEST)

		else:
			return Response({
				"errors": _prepare_errors(
					user_id.errors, request_data.errors
				),
			}, status=status.HTTP_400_BAD_REQUEST)


class FolderDetails(RetrieveAPIView):

	def get(self, request):
		""" details of a folder of an user
			method: GET
			params: user_id, folder_id
		"""

		response = {}

		user_id = UserExistanceSerializer(data=request.GET)
		folder_id = FolderExistanceSerializer(data=request.GET)
		check_user_id = user_id.is_valid()
		check_folder_id = folder_id.is_valid()

		if check_user_id and check_folder_id:
			validated_user_id = user_id.validated_data
			validated_folder_id = folder_id.validated_data

			folder = {
				"id": validated_folder_id.get("folder_id").id,
				"name": validated_folder_id.get("folder_id").name,
				"parent": validated_folder_id.get("folder_id").parent
			}
			response = {
				"result": folder,
				"status": 200
			}
		else:
			response = {
				"error": folder_id.error,
				"status": 201
			}

		return Response(response)


class FolderList(ListAPIView):

	def get(self, request):
		""" list of folders of an user
			method: GET
			params: user_id
		"""

		user_id = UserExistanceSerializer(data=request.GET)
		check_user_id = user_id.is_valid()

		if check_user_id:
			validated_user_id = user_id.validated_data

			folders = FolderHierarchy.objects.filter(
				user_id=validated_user_id.get("user_id")
			)
			if folders.exists():
				folder_list = [
							{
								"id": folder.id,
								"name": folder.name,
								"parent": folder.parent
							}
							for folder in folders
						]

			return Response({
				"folders": folder_list,
			}, status=status.HTTP_200_OK)

		else:
			return Response({
				"errors": _prepare_errors(
					user_id.errors
				),
			}, status=status.HTTP_400_BAD_REQUEST)
