# inventario/views/auth.py
from inventario.services.email import send_password_reset_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from inventario.serializers.user import PasswordResetRequestSerializer
from inventario.serializers.user import PasswordResetConfirmSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from inventario.serializers.user import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user    = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access':   str(refresh.access_token),
            'refresh':  str(refresh),
            'user_id':  user.id,
            'username': user.username,
            'email':    user.email,
            'is_staff': user.is_staff,
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return Response(
                {'error': 'Token is invalid or expired.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'message': 'Session closed successfully.'})

class PasswordResetRequestView(APIView):
    """
    POST /api/auth/password-reset/
    Body: { "email": "user@example.com" }

    Genera un token y envía el correo. Siempre responde 200
    independientemente de si el email existe (anti-enumeración de usuarios).
    """
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user  = User.objects.get(email=email, is_active=True)
            uid   = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            send_password_reset_email(user, uid, token)
        except User.DoesNotExist:
            pass  # No revelar si el email está registrado

        return Response(
            {'detail': 'Si el correo está registrado, recibirás un enlace de recuperación.'},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """
    POST /api/auth/password-reset/confirm/
    Body: { "uid": "...", "token": "...", "new_password": "...", "new_password2": "..." }

    Valida el token y actualiza la contraseña. Una vez usado, el token queda inválido.
    """
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Contraseña actualizada correctamente.'},
            status=status.HTTP_200_OK,
        )        