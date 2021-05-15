from users.models import Account
from location.models import Object

def get_homes(request):
    obj = {"homes":None, "current":None}
    if request.user.role == "moderator":
        current_object = request.session.get('current_object')
        homes = request.user.object.all()
        if homes.count()>0:
            current=None
            if current_object:
                current = request.user.object.get(id=current_object)
            else:
                current = request.user.object.first()
                request.session['current_object'] = current.id
            obj['homes'] = homes.exclude(id=current.id)
            obj['current'] = current
    elif request.user.role == "client":
        try:
            object_id = Account.objects.get(custom_user=request.user).object_id
            obj['current'] =  Object.objects.filter(id=object_id).first()
            request.session['current_object'] = obj['current'].id
        except:
            pass
    return obj