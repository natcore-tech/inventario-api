# StockMaster

## Sistema de Gestión de Inventario

---

## Integrantes

| Nombre |
|---------|
| Mikaela Zurita |
| Elihu Navarrete |
| Michael Lidioma |

---

# Descripción del Sistema

**StockMaster** es una API REST desarrollada con **Django** y **Django REST Framework**, diseñada para administrar y controlar el inventario de una compañia.

El sistema permite registrar, consultar, actualizar y eliminar información relacionada con el inventario, proporcionando un control eficiente del stock disponible y facilitando la administración de productos.

Su principal objetivo es mantener un registro preciso de las existencias en tiempo real, evitando tanto el desabastecimiento como el exceso de mercancía que pueda generar costos innecesarios.

---

# Instalación del proyecto

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/natcore-tech/inventario-api.git

cd inventario-api

code .
```

---

## Crear entorno virtual

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

> Si el proyecto utiliza **uv**, también puedes ejecutar:

```bash
uv pip install -r requirements.txt
```

---

## Configurar las variables de entorno

Antes de ejecutar el proyecto, asegúrate de tener creada una base de datos PostgreSQL llamada:

```text
inventario_db
```

Posteriormente crea un archivo llamado:

```text
.env
```

Con la siguiente configuración:

```env
# Django
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=inventario_db
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOW_ALL_ORIGINS=True
```

---

## Ejecutar las migraciones

```bash
uv python manage.py migrate
```

---

## Crear un superusuario

```bash
uv python manage.py createsuperuser
```

Sigue las instrucciones que aparecerán en la terminal para registrar el usuario administrador.

---

## Ejecutar el servidor

```bash
uv python manage.py runserver
```

Una vez iniciado el servidor, la API estará disponible en:

```text
http://127.0.0.1:8000/
```

---

# Tecnologías utilizadas

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Postman
- Git
- GitHub

---

# Estado del proyecto

Actualmente el proyecto esta en desarrollo por lo que la API puede ser probada mediante **Postman**, que permite realizar operaciones CRUD.