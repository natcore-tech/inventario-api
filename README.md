PROYECTO GESTIÓN DE INVENTARIO 

TITULO: STOCKMASTER 

INTEGRANTES: 
Mikaela Zurita 
Elihu Navarrete 
Michael Lidioma 

DESCRIPCIÓN DEL SISTEMA: 
El sistema de gestión de inventario "Stockmaster" es un proyecto desarrollado con Django REST Frameworg que permitira rastrear, controlar y optimizar el stock de una empresa en tiempo real. Su objetivo es llevar las cuentas exactas de producto en el momento preciso, evitando la escazes y el exceso de mercancia que genere costos innecesarios.

INSTALACIÓN 
1. Clonarse el repositorio 
git clone https://github.com/natcore-tech/inventario-api.git

2. Creación del entorno virtual
python -m venv venv

WINDOWS 
venv\Scripts\activate
LINUX
source venv\bin\activate

3. Instalar dependencias 

pip install requirements.txt

4. Configuración de variables de entorno.

Asegúrate de tener tu base de datos PostgreSQL creada con el nombre inventario_db.

Crea el archivo .env y agrega esto:
# Django
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=inventario_db
DB_USER= (tu usuario)
DB_PASSWORD= (tu contraseña) 
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOW_ALL_ORIGINS=True

5. Ejecución de migraciones

uv python manage.py migrate

6. Creación de superusuario 

uv python manage.py createsuperuser

7. Ejecución del servidor.

uv python manage.py runserver