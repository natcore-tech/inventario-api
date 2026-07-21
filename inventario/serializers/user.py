# inventario/serializers/user.py
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username  = serializers.CharField(max_length=150)
    email     = serializers.EmailField()
    password  = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already registered.')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_active', 'date_joined', 'avatar_url',
        ]
        read_only_fields = ['id', 'date_joined']

    def get_avatar_url(self, obj):                     # ← nuevo
        request = self.context.get('request')
        try:
            avatar = obj.profile.avatar
            if avatar:
                return request.build_absolute_uri(avatar.url) if request else avatar.url
        except Exception:
            pass
        return None    


class UserProfileSerializer(serializers.ModelSerializer):

    avatar_url = serializers.SerializerMethodField()

    avatar = serializers.ImageField(source='profile.avatar', required=False)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar','avatar_url', 'is_staff']
        read_only_fields = ['id', 'is_staff']

    def validate_email(self, value):
        request = self.context.get('request')
        if User.objects.filter(email=value).exclude(pk=request.user.pk).exists():
            raise serializers.ValidationError('This email is already in use.')
        return value

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        try:
            avatar = obj.profile.avatar
            if avatar:
                return request.build_absolute_uri(avatar.url) if request else avatar.url
        except Exception:
            pass
        return None

    def validate_avatar(self, value):
        max_size    = 2 * 1024 * 1024  # 2 MB
        valid_types = ['image/jpeg', 'image/png', 'image/webp']
        if value and value.size > max_size:
            raise serializers.ValidationError('Image size must not exceed 2 MB.')
        if value and value.content_type not in valid_types:
            raise serializers.ValidationError('Only JPEG, PNG, and WebP images are allowed.')
        return value

    def update(self, instance, validated_data):
        from inventario.models.profile import UserProfile
        profile_data = validated_data.pop('profile', {})
        instance     = super().update(instance, validated_data)
        if profile_data:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return instance            


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password     = serializers.CharField(min_length=8, write_only=True)
    new_password2    = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': 'Passwords do not match.'})
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    """Paso 1: el usuario envía su email para solicitar el reset."""
    email = serializers.EmailField()

    # No validamos si el email existe en esta capa:
    # la vista lo maneja en silencio para evitar enumeración de usuarios.


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Paso 2: el usuario envía uid + token + nueva contraseña."""
    uid           = serializers.CharField()
    token         = serializers.CharField()
    new_password  = serializers.CharField(min_length=8, write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        # Decodificar el uid para obtener el usuario
        try:
            pk   = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'uid': 'Enlace inválido o expirado.'})

        # Verificar el token con el generador nativo de Django
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError({'token': 'Token inválido o expirado.'})

        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': 'Las contraseñas no coinciden.'})

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user        

class SendNotificationSerializer(serializers.Serializer):
    """
    Cuerpo del request para enviar una notificación manual.

    - Si se provee `user_id`, el correo va solo a ese usuario.
    - Si `user_id` es null u omitido, el correo se envía a todos los
      usuarios activos que no son staff (envío masivo).
    """
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()
    user_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_user_id(self, value):
        if value is not None:
            if not User.objects.filter(pk=value, is_active=True, is_staff=False).exists():
                raise serializers.ValidationError(
                    'Usuario no encontrado, inactivo o es staff.'
                )
        return value