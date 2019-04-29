from secretmessages.models import Message


def mesgNo_processor(request):
 	try:
 		msgNo = Message.objects.all().filter(user=request.user) 
 	except:
 		return {'msgNo': 0}
 	if msgNo.count:
 		msgNo = msgNo.count
 	else:
 		msgNo = 0      
 	return {'msgNo': msgNo}


def fav_msgNo_processor(request):
	try:
 		fav_msgNo = Message.objects.all().filter(user=request.user).filter(is_fav=True)
	except:
 		return {'fav_msgNo': 0}

	if fav_msgNo.count:
		fav_msgNo = fav_msgNo.count
	else:
		fav_msgNo = 0

	return {'fav_msgNo': fav_msgNo}

def sent_msgNo_processor(request):
	try:
		sent_msgNo = Message.objects.all().filter(sender=request.user.username)
	except:
		return {'sent_msgNo': 0}
	if sent_msgNo.count:
		sent_msgNo = sent_msgNo.count
	else:
		sent_msgNo = 0
	return {'sent_msgNo': sent_msgNo}