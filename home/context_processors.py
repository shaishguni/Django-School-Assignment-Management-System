
from users.models import  Notification, Notification_general

def noti_count(request):
	if request.user.is_authenticated:
	    count1 = Notification.objects.filter(user=request.user, seen=False)
	    count2 = Notification_general.objects.filter(user=request.user, seen=False)
	    return {"count1": count1, 'count2':count2,}
	else:
		return {"?":"?"}