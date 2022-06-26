from OBMS_basics.models import OrderItem, Order
import uuid

def generate_session_id(request):
    if not request.session['nonuser']:
        request.session['nonuser'] = str(uuid.uuid4())
    try:
        order = Order.objects.get(session_id=request.session['nonuser'], ordered=False)
        order_quantity = order.product.count()
    except OrderItem.DoesNotExist:
        order_quantity = 0
    return {
        'session_id':request.session['nonuser'],
        'order_quantity':order_quantity
    }
    # try:
    #     order_item = OrderItem.objects.get(session_id=request.session['nonuser'], completed=False)
    # except:
    #     request.session['nonuser'] = str(uuid.uuid4())
    #     order_item = OrderItem.objects.create(session_id=request.session['nonuser'], completed=False)

    # return {
    #     'order_item':order_item
    # }
