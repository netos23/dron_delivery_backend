from orders.models import OrderModel


def get_count_photos(order: OrderModel):
    delta = order.date_end - order.date_begin
    return delta.total_seconds() // 3600 * order.satellites.count()

def get_total_price(order: OrderModel):
    cnt = get_count_photos(order)
    coeff = sum(order.plugins.values_list('per_photo', flat=True))
    price = order.tarif.base_price + (order.tarif.per_photo + coeff) * cnt
    return price