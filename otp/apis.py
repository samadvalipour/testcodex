from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from . import services


class OtpAuthAPI(APIView):
    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(max_length=15)
        code = serializers.CharField(max_length=6, required=False)

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

