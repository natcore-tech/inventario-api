# Inventario API

Sistema backend robusto para la gestión de inventario académico, desarrollado con Django REST Framework y PostgreSQL.

## 🚀 Instalación y Ejecución

1. Clonar el repositorio:
   `git clone https://github.com/Michaelslj/lidioma_inventario_api.git`
2. Instalar dependencias:
   `pip install -r requirements.txt`
3. Configurar variables de entorno (Base de datos):
   *Asegúrate de tener tu base de datos PostgreSQL creada.*
4. Ejecutar migraciones:
   `python manage.py migrate`
5. Iniciar servidor:
   `python manage.py runserver`

## 🔐 Autenticación
El sistema utiliza JWT. Para acceder a los endpoints protegidos:
1. Haz POST a `/api/token/` con tus credenciales.
2. Usa el `access` token recibido en el Header: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNTQ5NzY5LCJpYXQiOjE3ODA1NDYxNjksImp0aSI6IjMzZTg4NWVmYTRlMzRiMmNiNjExODMxNmQ0N2NlNjBjIiwidXNlcl9pZCI6IjMiLCJ1c2VybmFtZSI6Im1pY2hhZWxzbGoiLCJlbWFpbCI6Im1pY2hhZWxzbGpAZ21haWwuY29tIiwiaXNfc3RhZmYiOnRydWV9.2OjJBjOZGaZUxEH5dsLiT0fuMXfV57bwJXFrm9hLrXA`

## 📌 Endpoints Principales
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| POST | `/api/token/` | Obtener token de acceso |
| GET | `/api/productos/` | Listar productos |
| POST | `/api/movimientos/` | Registrar entrada/salida de stock |
| ... | ... | ... |

