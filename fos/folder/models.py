from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from account.models import CustomUser


class FolderHierarchy(MPTTModel):

	name = models.CharField(max_length=50, unique=True)
	parent = TreeForeignKey("self", on_delete=models.CASCADE, 
		null=True, blank=True, related_name="children"
	)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
		related_name="folder_owner"
	)
	is_default = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class MPTTMeta:
	    order_insertion_by = ['name']

	def __str__(self):
		return self.name
