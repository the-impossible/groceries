from OBMS_basics.models import OrderItem, Order
import uuid

def order(request):
    try:
        if request.user.is_authenticated:
            order = Order.objects.filter(user=request.user, ordered=False).exists()
            ordered = Order.objects.filter(user=request.user, ordered=True).count()
            print(f"CHECKING: {ordered}")
            if order:
                order = Order.objects.get(user=request.user, ordered=False)
                order_quantity = order.product.count()
                return {
                    'order':order,
                    'ordered':ordered,
                    'order_quantity':order_quantity,
                }
            else:
                return {
                    'ordered':ordered,
                    'order_quantity':0,
                }

        return ''
    except Order.DoesNotExist:
        return {
            'order_quantity':0,
        }