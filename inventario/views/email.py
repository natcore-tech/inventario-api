import logging
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from inventario.serializers.user import SendNotificationSerializer
from inventario.services.email import send_notification_email

logger = logging.getLogger(__name__)


class SendNotificationView(APIView):
    """
    POST /api/emails/send/
    Solo accesible para usuarios staff (is_staff=True).

    Envío individual:
        { "subject": "...", "message": "...", "user_id": 5 }

    Envío masivo (sin user_id o user_id: null):
        { "subject": "...", "message": "..." }
        → Envía a todos los usuarios activos que no son staff y tienen email.

    Responde con el número de correos enviados y fallidos.
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']
        user_id = serializer.validated_data.get('user_id')

        if user_id:
            recipients = User.objects.filter(pk=user_id)
        else:
            # Masivo: todos los usuarios activos no-staff que tienen email
            recipients = User.objects.filter(
                is_staff=False,
                is_active=True,
            ).exclude(email='')

        sent   = 0
        failed = 0

        for user in recipients:
            try:
                send_notification_email(user, subject, message)
                sent += 1
            except Exception:
                failed += 1
                logger.exception('Error enviando notificación a %s', user.email)

        return Response(
            {
                'detail': f'Correo enviado a {sent} usuario(s).',
                'sent':   sent,
                'failed': failed,
            },
            status=status.HTTP_200_OK,
        )
