from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')

class CustomUser(AbstractUser):

	first_name = models.CharField(_('first name'),
	    max_length=30, blank=True, null=True
	)
	last_name = models.CharField(_('last name'),
	    max_length=30, blank=True, null=True
	)
	email = models.EmailField(_('email address'),
	    unique=True, 
	    error_messages={
	        'unique': _("A user with this email already exists."),
	    },
	    help_text=_('Email is used as internal username'),
	)
	mobile = models.CharField(_('mobile no'), max_length=10, 
		blank=True, null=True, validators=[numeric])

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['email']

	class Meta:
	    verbose_name_plural = 'CustomUsers'

	def __str__(self):
	    if self.first_name:
	        return '{self.first_name} {self.last_name}'.format(
	            self=self).strip()
	    return self.email
