from OBMS_basics.models import OrderItem
import uuid

def generate_session_id(request):
    if not request.session['nonuser']:
        request.session['nonuser'] = str(uuid.uuid4())

    return {
        'session_id':request.session['nonuser']
    }
    # try:
    #     order_item = OrderItem.objects.get(session_id=request.session['nonuser'], completed=False)
    # except:
    #     request.session['nonuser'] = str(uuid.uuid4())
    #     order_item = OrderItem.objects.create(session_id=request.session['nonuser'], completed=False)

    # return {
    #     'order_item':order_item
    # }
