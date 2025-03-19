from django.utils.deprecation import MiddlewareMixin

class ReverseProxyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
        if forwarded_for:
            real_ip = forwarded_for.split(",")[0].strip()
            request.META["REMOTE_ADDR"] = real_ip
