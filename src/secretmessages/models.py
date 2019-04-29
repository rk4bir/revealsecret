from django.db import models
from accounts.models import User

class Message(models.Model):
	user      = models.ForeignKey(User, on_delete=models.CASCADE)
	sender    = models.CharField(max_length=100, default='Anonymous')
	content   = models.TextField()
	is_fav    = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return str(self.user.username) + ' - ' + self.sender + ': ' + self.content
	class Meta:
		ordering = ['-timestamp']