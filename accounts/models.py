from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, default='')
	pp   = models.ImageField(
			'Profile Photo',
			upload_to="profile_pics/",
			null=True, blank=True,
			width_field="width_field",
			height_field="height_field",
		)
	height_field = models.IntegerField(default=0)
	width_field  = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username or self.name

	def get_profile_name(self):
		return self.name or self.user.username
		
	def get_send_message_link(self):
		return reverse('message', kwargs={'username': self.user.username})

	def get_absolute_url(self):
		return reverse('accounts:profile', kwargs={'username': self.user.username})

