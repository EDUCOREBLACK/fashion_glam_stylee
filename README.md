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