from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class CustomGenericAPIView(GenericAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if isinstance(response.data, (dict, list)):  # Modify response only if it contains dictionary data
            custom_response = Response({
                "status": response.status_code,
                "message": "Success" if response.status_code < 400 else "Error",
                "data": response.data
            }, status=response.status_code)

            custom_response.accepted_renderer = response.accepted_renderer
            custom_response.accepted_media_type = response.accepted_media_type
            custom_response.renderer_context = response.renderer_context

            return custom_response

        return response