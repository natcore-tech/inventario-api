# store/services/email.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def _send(subject: str, to: str, txt_template: str, html_template: str, context: dict) -> None:
    """
    Helper privado: renderiza ambas versiones del correo (texto plano + HTML)
    y lo envía con EmailMultiAlternatives.

    EmailMultiAlternatives envía texto plano como cuerpo principal y adjunta
    la versión HTML como alternativa. Los clientes que soportan HTML muestran
    la versión HTML; el resto usa texto plano.
    """
    text_body = render_to_string(txt_template, context)
    html_body = render_to_string(html_template, context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to],
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send(fail_silently=False)


def send_welcome_email(user) -> None:
    """Envía correo de bienvenida cuando se registra un nuevo usuario."""
    _send(
        subject='¡Bienvenido a Inventario Api!',
        to=user.email,
        txt_template='emails/welcome.txt',
        html_template='emails/welcome.html',
        context={
            'username': user.username,
            'email':    user.email,
        },
    )


def send_password_reset_email(user, uid: str, token: str) -> None:
    """
    Envía correo con enlace de recuperación de contraseña.
    El enlace apunta al frontend, que luego llamará al endpoint de confirmación de la API.
    """
    reset_url = f"{settings.FRONTEND_URL}/password-reset/confirm/?uid={uid}&token={token}"

    _send(
        subject='Recuperación de contraseña — Inventario Api',
        to=user.email,
        txt_template='emails/password_reset.txt',
        html_template='emails/password_reset.html',
        context={
            'username':  user.username,
            'reset_url': reset_url,
        },
    )

def send_venta_confirmation_email(venta) -> None:
    """
    Envía correo de confirmación cuando se registra una venta.
    Incluye el detalle de ítems y el total.
    """
    items = [
        {
            'product_name': item.producto.nombre,
            'quantity':     item.cantidad,
            'unit_price':   item.precio_unitario_venta,
            'subtotal':     item.subtotal_linea,
        }
        for item in venta.detalles.select_related('producto').all()
    ]

    # Usamos timezone.localtime para mostrar la hora correcta si aplica, o simplemente strftime
    from django.utils.timezone import localtime
    fecha_str = localtime(venta.fecha_emision).strftime('%d/%m/%Y %H:%M') if venta.fecha_emision else ''

    _send(
        subject=f'Confirmación de Venta #{venta.id} — Inventario Api',
        to=venta.cliente.email,
        txt_template='emails/venta_confirmacion.txt',
        html_template='emails/venta_confirmacion.html',
        context={
            'username':   venta.cliente.nombres,
            'venta_id':   venta.id,
            'items':      items,
            'total':      venta.total,
            'estado':     venta.estado,
            'fecha':      fecha_str,
        },
    )

def send_notification_email(user, subject: str, message: str) -> None:
    """
    Envía un correo de notificación personalizada a un usuario.
    Usada tanto para envíos individuales como masivos.
    """
    _send(
        subject=subject,
        to=user.email,
        txt_template='emails/notification.txt',
        html_template='emails/notification.html',
        context={
            'username': user.username,
            'subject':  subject,
            'message':  message,
        },
    )