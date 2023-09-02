from shop.models import Cart


class CartContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        else:
            cart = None

        # add info about cart in request
        request.cart = cart

        response = self.get_response(request)

        return response
