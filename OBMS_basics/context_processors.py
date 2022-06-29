from OBMS_basics.models import OrderItem, Order
import uuid

def generate_session_id(request):
    try:
        request.session['nonuser']
    except KeyError:
        request.session['nonuser'] = str(uuid.uuid4())

    try:
        order = Order.objects.get(session_id=request.session['nonuser'], ordered=False)
        order_quantity = order.product.count()
        order = Order.objects.get(session_id=request.session['nonuser'], ordered=False)
    except Order.DoesNotExist:
        order_quantity = 0
        return {
            'session_id':request.session['nonuser'],
            'order_quantity':order_quantity,
        }
    else:
        return {
            'session_id':request.session['nonuser'],
            'order':order,
            'order_quantity':order_quantity,
        }