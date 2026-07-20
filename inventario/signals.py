# store/signals.py  (reemplazar el contenido completo)
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from inventario.models.profile import UserProfile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        _send_welcome(instance)


def _send_welcome(user):
    """Envía correo de bienvenida. Falla en silencio para no bloquear el registro."""
    if not user.email:
        return
    try:
        from inventario.services.email import send_welcome_email
        send_welcome_email(user)
    except Exception:
        logger.exception('Error enviando correo de bienvenida a %s', user.email)