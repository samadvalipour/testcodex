from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_serializer

from . import services


class OtpAuthAPI(APIView):
    """
    This API endpoint implements a two-step OTP authentication flow:

    1. First, the user sends their phone number (`phone`) to request an OTP code.
       - The API responds with "OTP sent".

    2. Then, the user sends the phone number and the received OTP code (`code`) to verify.
       - If verification is successful, the API returns access and refresh JWT tokens.
       - If verification fails, the API returns an error message.

    Note: Registration and login are combined in this flow. If the phone number does not exist,
    a new user is automatically created during verification.
    """

    @extend_schema_serializer(component_name='OtpAuthInput')
    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(max_length=15)
        code = serializers.CharField(max_length=6, required=False)

    @extend_schema_serializer(component_name='OtpAuthOutput')
    class OutputSerializer(serializers.Serializer):
        access = serializers.CharField()
        refresh = serializers.CharField()

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data.get('code')

        if code:
            if services.verify_otp_code(phone=phone, code=code):
                user = services.login_or_register(phone=phone)
                tokens = services.generate_tokens_for_user(user=user)
                output = self.OutputSerializer(tokens)
                return Response(output.data)
            return Response({'detail': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            services.send_otp_code(phone=phone)
            return Response({'detail': 'OTP sent'}, status=status.HTTP_200_OK)
