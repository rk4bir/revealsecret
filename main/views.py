from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from accounts.models import User, Account
from django.contrib.auth.decorators import login_required
from secretmessages.models import Message
from django.contrib import messages


def about_view(request):
	return render(request, 'about.html', {})

def send_message_view(request, username):
	template_name = 'send_message.html'
	error = ""
	user = get_object_or_404(User, username=username)
	account = Account.objects.get(user=user)
	if request.method == "POST":
		message = request.POST.get('message')
		if len(message) == 0:
			error = "Write something to send"
		elif len(message) > 260:
			error = "Message exceeded 260 characters"
		else:
			msg_obj = Message()
			msg_obj.user = user
			if not request.user.is_anonymous:
				msg_obj.sender = request.user.username
			msg_obj.content = message
			msg_obj.save()
			messages.success(request, 'Your message has been sent.')
			return HttpResponseRedirect('/' + str(username) + '/')
	contex = {
		'account': account,
		'error': error
	}
	return render(request, template_name, contex)








def index_view(request):
	template_name = 'base.html'
	contex = {}

	return render(request, template_name, contex)



def not_authorized_view(request):
	template_name = 'not_authorized.html'
	contex = {}

	return render(request, template_name, contex)