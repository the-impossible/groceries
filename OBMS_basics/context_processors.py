# from OBMS_basics.models import OrderItem
# import uuid

# def cart_creator(request):
#     try:
#         order_item = OrderItem.objects.get(session_id=['nonuser'], completed=False)
#     except OrderItem.DoesNotExist:
#         key = str(uuid.uuid4())
#         request.session['nonuser'] = key
#         order_item = OrderItem.objects.create(session_id=key, completed=False)

#         return {
#             'cart':order_item
#         }

def cart_creator(request):

    print('Hello world')
    return {}