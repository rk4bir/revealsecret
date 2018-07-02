from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Message


@login_required
def favourite_view(request, pk):
	if request.method == "POST":
		msg = get_object_or_404(Message, pk=pk)
		msg.is_fav = True
		msg.save()
	return HttpResponseRedirect('/accounts/' + str(request.user.username) + "/")

def delete_view(request, pk):
	if request.method == "POST":
		msg = get_object_or_404(Message, pk=pk)
		msg.delete()
	return HttpResponseRedirect('/accounts/' + str(request.user.username) + "/")