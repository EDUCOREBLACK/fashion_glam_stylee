# Fashion Glam Stylee

## Desarrollo local

Requiere Python 3.12 o superior.

```sh
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

En Windows, activa el entorno con `venv\Scripts\activate`.

## Administrar productos

1. Crea un usuario administrador con `python manage.py createsuperuser`.
2. Inicia el proyecto y abre `http://127.0.0.1:8000/admin/`.
3. En **Categorías**, crea las categorías antes de agregar productos.
4. En **Productos**, completa nombre, categoría, precio, stock, descripción y estado; puedes subir una imagen desde tu computador. El slug se propone desde el nombre y debe ser único.
5. Usa el filtro **Activo** para ocultar productos sin borrarlos. Los pedidos y productos relacionados se administran desde el panel.

En Windows también puedes iniciar el proyecto ejecutando `iniciar_tienda.bat` desde la carpeta descargada. El archivo trabaja desde su propia ubicación, crea el entorno virtual si hace falta y carga productos de muestra sin borrar los datos existentes.

`populate_real_images.py` agrega productos de muestra y sus imágenes locales; no lo ejecutes para actualizar un catálogo real, pues no cambia productos existentes con el mismo slug.

## Despliegue

La aplicación es Django WSGI. En el servicio Linux de alojamiento configura el comando de inicio como:

```sh
gunicorn core.wsgi:application
```

Configura estas variables de entorno en el servicio (no las subas al repositorio):

- `DJANGO_DEBUG=false`
- `DJANGO_SECRET_KEY`: clave aleatoria, privada y distinta para producción.
- `DJANGO_ALLOWED_HOSTS`: dominios permitidos separados por comas, sin `https://`.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: orígenes completos separados por comas, por ejemplo `https://tienda.example.com`.
- `WHATSAPP_PHONE_NUMBER`: número de la tienda en formato internacional, solo dígitos y sin `+`.
- Si se habilitan correos, configura `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
  `EMAIL_HOST_PASSWORD` y `EMAIL_USE_TLS` según el proveedor SMTP.

Antes de abrir el sitio al público, ejecuta `python manage.py migrate` y
`python manage.py collectstatic --noinput`, y crea un administrador con
`python manage.py createsuperuser`. El hosting debe proporcionar HTTPS y
reenviar `X-Forwarded-Proto: https`.

La configuración usa SQLite (`db.sqlite3`) y guarda imágenes subidas en `media/`.
Si el alojamiento usa almacenamiento efímero, configura un disco persistente para
ambos directorios o migra a una base de datos y almacenamiento de medios gestionados;
de lo contrario, los pedidos o imágenes podrían perderse al reiniciar o desplegar.
El workflow de GitHub Actions ejecuta análisis y pruebas, pero no publica el sitio.