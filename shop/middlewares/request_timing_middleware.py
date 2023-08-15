import time

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Request to {request.path} took {execution_time:.2f} seconds")

        return response
