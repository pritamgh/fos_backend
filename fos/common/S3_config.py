
from django.conf import settings

import boto3
from botocore.exceptions import ClientError

from folder.models import FolderHierarchy


def _create_session():

	session = boto3.Session(
	    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
	    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
	)

	return {"session": session, "message": "Session started."} 


def _bucket_details():
	"""
		initialize session (proxy) and return bucket(object), 
		bucket name, owner location
	"""

	status = _create_session()
	if status.get("session"):
		s3 = status.get("session").resource("s3")
		bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
		bucket_name = settings.AWS_STORAGE_BUCKET_NAME
		bucket_location = status.get("session").client("s3").get_bucket_location(Bucket=bucket_name)
	else:
		bucket, bucket_name, bucket_location = None

	return bucket, bucket_name, bucket_location, status.get("message")


def _pagination(operation_parameters):
	
	status = _create_session()
	if status.get("session"):
		paginator = status.get("session").client("s3").get_paginator('list_objects_v2')
		page_iterator = paginator.paginate(**operation_parameters)

	return page_iterator


def _prepare_folder_path(user_email, folder_id, folder_name):

	# FolderHierarchy.objects.get()

	_prefix = "media/{user_email}/{folder_name}".format(
		user_email=user_email,
		folder_name=folder_name
	)

	return _prefix
