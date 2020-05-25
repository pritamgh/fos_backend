import os
import sys

from django.conf import settings

from rest_framework import status
from rest_framework.generics import (
	CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
)
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import *
from .serializers import *
from account.serializers import UserExistanceSerializer
from folder.serializers import FolderExistanceSerializer
from common.storage import MediaStorage
from common.utils import _prepare_errors, convert_size
from common.S3_config import _bucket_details, _pagination, _prepare_folder_path


class FileUpload(CreateAPIView):

	def post(self, request):
		""" upload file under a folder of an user
			method: POST
		"""

		user_id = UserExistanceSerializer(data=request.data)
		folder_id = FolderExistanceSerializer(data=request.data)
		request_data = FileUploadSerializer(data=request.data)
		check_user_id = user_id.is_valid()
		check_folder_id = folder_id.is_valid()
		check_request_data = request_data.is_valid()

		if check_user_id and check_folder_id and check_request_data:
			validated_user_id = user_id.validated_data
			validated_folder_id = folder_id.validated_data
			validated_request_data = request_data.validated_data

			""" all validated meta properties of requested file """
			file = validated_request_data.get("file")
			name = validated_request_data.get("name")
			size = convert_size(validated_request_data.get("size"))
			extension = validated_request_data.get("extension")

			# organize a path for the file in bucket
			file_directory_within_bucket = "{user_email}/{folder}".format(
				user_email=validated_user_id.get("user_id").email,
				folder=validated_folder_id.get("folder_id").name
			)

			# synthesize a full file path; note that we included the filename
			file_path_within_bucket = os.path.join(
			    file_directory_within_bucket,
			    name
			)

			media_storage = MediaStorage()

			if not media_storage.exists(file_path_within_bucket): # avoid overwriting existing file
				media_storage.save(file_path_within_bucket, file)
				file_url = media_storage.url(file_path_within_bucket)

				"""enter metadata"""
				metadata_instanse = UploadedFile.objects.create(
					user_id=validated_user_id.get("user_id").id,
					folder_id=validated_folder_id.get("folder_id").id,
					name=name,
					size=size,
					extension=extension,
				)

				return Response({
					"file": file_url,
					"message": "File uploaded successfully.",
				}, status=status.HTTP_201_CREATED)

			else:
				return Response({
				    "errors": "Error: file {filename} already exists at {file_directory} in bucket {bucket_name}".format(
				        filename=name,
				        file_directory=file_directory_within_bucket,
				        bucket_name=media_storage.bucket_name
				    ),
				}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				"errors": _prepare_errors(
					user_id.errors, folder_id.errors, request_data.errors
				),
			}, status=status.HTTP_400_BAD_REQUEST)


class FileDetails(RetrieveAPIView):

	def get(self, request):

		user_id = UserExistanceSerializer(data=request.GET)
		check_user_id = user_id.is_valid()

		if check_user_id:
			user_email = user_id.validated_data.get("user_id").email
			session = boto3.Session(
			    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
			    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
			)
			s3 = session.resource('s3')
			bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
			_prefix = "media/{user_email}/documents".format(user_email=user_email)

			for file in bucket.objects.filter(Prefix=_prefix):
				path, filename = os.path.split(file.key)
				print(file.key)
				bucket.download_file(file.key, filename)

			return Response("ok")


class FileList(ListAPIView):

	def get(self, request):
		""" list of files under a folder of an user
			method: GET
			params: user_id, folder_id
		"""

		""" validate user_id, folder_id and check folder is
			blank or not.
		"""
		metadata = MetadataExistanceSerializer(data=request.GET)
		check_metadata = metadata.is_valid()

		if check_metadata:
			user_id = metadata.validated_data.get("user_id").id
			user_email = metadata.validated_data.get("user_id").email
			folder_id = metadata.validated_data.get("folder_id").id
			folder_name = metadata.validated_data.get("folder_id").name

			bucket, bucket_name, bucket_location, message = _bucket_details()
			if bucket and bucket_name and bucket_location:
				_prefix = _prepare_folder_path(user_email, folder_id, folder_name)

				next_token = request.GET.get("pagination_token")
	
				operation_parameters = {
					"Bucket": bucket_name,
				    "Prefix": _prefix,
				    "PaginationConfig": {
				    	"MaxItems": 1,
	            		"StartingToken": next_token,
	            		"PageSize": 1,
					}
				}
				page_iterator = _pagination(operation_parameters)
				next_token = page_iterator.build_full_result().get("NextToken")
				print(next_token)

				file_list = []
				for page in page_iterator:
					for file in page['Contents']:
						file_url = "https://s3-{location}.amazonaws.com/{bucket}/{key}".format(
						    location=bucket_location['LocationConstraint'],
						    bucket=bucket_name,
						    key=file.get("Key")
						)
						file_name = file.get("Key").rsplit("/", 1)[1]
						
						""" get metadata """
						metadata_instanse = UploadedFile.objects.get(
							user_id=user_id,
							folder_id=folder_id,
							name__exact=file_name,
						)
						file_list.append({
							"id":metadata_instanse.uuid,
							"name":file_name,
							"size":metadata_instanse.size,
							"url":file_url,
							"extension":metadata_instanse.extension
						})

				return Response({
					"files": file_list,
					"pagination_token": next_token
				}, status=status.HTTP_200_OK)

			else:
				return Response({
					"errors": "AWS session has not established."
				}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		else:
			return Response({
				"errors": _prepare_errors(
					metadata.errors
				),
			}, status=status.HTTP_400_BAD_REQUEST)
