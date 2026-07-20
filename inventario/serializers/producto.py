# inventario/serializers/product.py
from rest_framework import serializers
from inventario.models import Producto
from inventario.serializers.categoria import CategoriaSerializer


class SerializerResumenProducto(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'es_activo', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class SerializerProducto(serializers.ModelSerializer):
    categoria       = CategoriaSerializer(read_only=True)
    categoria_id    = serializers.PrimaryKeyRelatedField(
        source='categoria',
        write_only=True,
        queryset=Producto.objects.none(),
    )
    precio_con_impuesto = serializers.SerializerMethodField()
    en_stock       = serializers.SerializerMethodField()
    image_url      = serializers.SerializerMethodField()

    class Meta:
        model  = Producto
        # 🛠️ CORRECCIÓN: Quitamos 'creado_en' y 'actualizado_en' de la lista
        fields = [
            'id', 'nombre', 'descripcion',
            'precio', 'precio_con_impuesto',
            'stock', 'en_stock', 'es_activo',
            'categoria', 'categoria_id',
            'image', 'image_url'
        ]
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from inventario.models import Categoria
        self.fields['categoria_id'].queryset = Categoria.objects.filter(activa=True)

    def get_precio_con_impuesto(self, obj) -> float:
        # Manejo seguro por si la propiedad o método tampoco existe en tu modelo
        try:
            return obj.precio_con_impuesto
        except AttributeError:
            return float(obj.precio) * 1.15  # Cálculo rápido de IVA estándar local

    def get_en_stock(self, obj) -> bool:
        try:
            return obj.en_stock
        except AttributeError:
            return obj.stock > 0

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor que 0.')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value

    def validate_image(self, value):
        max_size    = 2 * 1024 * 1024  # 2 MB
        valid_types = ['image/jpeg', 'image/png', 'image/webp']
        if value and value.size > max_size:
            raise serializers.ValidationError('Image size must not exceed 2 MB.')
        if value and value.content_type not in valid_types:
            raise serializers.ValidationError('Only JPEG, PNG, and WebP images are allowed.')
        return value    