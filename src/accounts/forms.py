from django import forms
from .utils import *
from .models import User, Account




class PhotoUploadForm(forms.Form):
	image = forms.ImageField(label="Profile Photo", required=True)


class DeleteForm(forms.Form):
	confirm = forms.CharField(
		label='', required=True, 
		widget=forms.TextInput(
			attrs={
				'name': "confirm",
				'type': 'checkbox',
				'value': 'yes',
				'checked': False
			}
		)
	)
	
class ChangePasswordForm(forms.Form):
	c_pass = forms.CharField(
		label='', required=False, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Current Password',
				'class': 'form-control',
				'type': "password",
				'name': "c_pass"
			}
		)
	)
	n_pass = forms.CharField(
		label='', required=False, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'New Password',
				'class': 'form-control',
				'type': "password",
				'name': "n_pass"
			}
		)
	)
	r_pass = forms.CharField(
		label='', required=False, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Confirm Password',
				'class': 'form-control',
				'type': "password",
				'name': "n_pass"
			}
		)
	)


	account = None
	def __init__(self, user, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		self.account = Account.objects.get(user=user)
	def clean(self, *args, **kwargs):
		c_pass = self.cleaned_data.get('c_pass')
		n_pass = self.cleaned_data.get('n_pass')
		r_pass = self.cleaned_data.get('r_pass')

		if c_pass and n_pass and r_pass:
			if not self.account.user.check_password(c_pass):
				raise forms.ValidationError("Incorrect current password")	
			if len(n_pass) < 6:
				raise forms.ValidationError("Password is too short")
			if n_pass != r_pass:
				raise forms.ValidationError("New passwords didn't match")
			if c_pass == n_pass:
				raise forms.ValidationError("This is already your current password")
		else:
			raise forms.ValidationError("All fields are registered")
		return super(ChangePasswordForm, self).clean(*args, **kwargs)



class EditForm(forms.Form):
	name = forms.CharField(
		label='', 
		required=False, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Full Name',
				'class': 'form-control',
				'type': "text",
				'name': "name"
			}
		)
	)
	#pp = forms.ImageField()
	email = forms.CharField(
		label='', 
		required=False, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Email',
				'class': 'form-control',
				'type': "text",
				'name': "enail"
			}
		)
	)
	account = None
	def __init__(self, user, *args, **kwargs):
		super(EditForm, self).__init__(*args, **kwargs)
		self.account = Account.objects.get(user=user)
		VALUES = [self.account.name, user.email]
		index = 0
		for field in self.visible_fields():
			field.field.widget.attrs['value'] = VALUES[index]
			index += 1
            
	def clean(self, *args, **kwargs):
		name = self.cleaned_data.get('name')
		email = self.cleaned_data.get('email')
		if name:	
			if not validName(name):
				raise forms.ValidationError("Please enter a valid name")
		if email:
			if not validEmail(email):
				raise forms.ValidationError('Please enter e valid email')
			qs = User.objects.filter(email=email)
			if qs.exists:
				obj = User.objects.get(email=email)
				if self.account.user != obj:
					raise forms.ValidationError("This email is already registered")
		else:
			raise forms.ValidationError("Email is required field")
		return super(EditForm, self).clean(*args, **kwargs)



class LoginForm(forms.Form):
	username = forms.CharField(
		label='', 
		required=False, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Username or email',
				'class': 'form-control',
				'type': "text",
				'name': "username"
			}
		)
	)
	password = forms.CharField(
		label='',
		required=False,
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Password',
				'class': 'form-control',
				'type': "password",
				'name': "password"
			}
		)
	)
	

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username and password:
			qs = User.objects.filter(username=username)
			if qs.exists():
				user = User.objects.get(username=username)
				if not user.check_password(password):
					raise forms.ValidationError("Password didn't match")
			else:
				qs = User.objects.filter(email=username)
				if qs.exists():
					user = User.objects.get(email=username)
					if not user.check_password(password):
						raise forms.ValidationError("Password didn't match")
				else:	
					raise forms.ValidationError("Username doesn't exist")
		else:
			raise forms.ValidationError("Both fields are required")
		return super(LoginForm, self).clean(*args, **kwargs)
