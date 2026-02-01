import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        print(f"Request: {request.method} {request.path} | Time: {duration:.4f}s")
        
        return response

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if hasattr(request, 'session'):
            cart = request.session.get('cart', [])
            request.cart_count = len(cart)
            request.cart_ids = cart
        else:
            request.cart_count = 0
            request.cart_ids = []

        response = self.get_response(request)

        return response