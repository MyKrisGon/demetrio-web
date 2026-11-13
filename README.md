# demetrio.mx

Sitio de Demetrio Entertainment: productora, comercialización, operación y desarrollo de espectáculos en Los Cabos y La Paz.

Es un sitio estático, sin build: el HTML, el CSS y el JS van en `index.html` y las imágenes en `assets/`.

## Flujo de trabajo

| Rama      | Se publica en                 |
|-----------|-------------------------------|
| `staging` | sitio de pruebas (subdominio) |
| `main`    | https://demetrio.mx           |

1. Haz los cambios en `staging` y haz push. Se publican solos en el sitio de pruebas.
2. Cuando estén aprobados, haz merge de `staging` a `main` y se publican en demetrio.mx.

El despliegue lo hace `.github/workflows/deploy.yml`, que sube los archivos a HostGator por FTPS.

## Configuración (una sola vez)

En GitHub › Settings › Secrets and variables › Actions, crea estos secrets:

- `FTP_SERVER`: el servidor FTP de HostGator.
- `FTP_USERNAME` y `FTP_PASSWORD`: una cuenta FTP de cPanel limitada a las carpetas del sitio.
- `DEPLOY_DIR_PROD`: la carpeta de demetrio.mx, con `/` al final.
- `DEPLOY_DIR_STAGING`: la carpeta del subdominio de pruebas, con `/` al final.

## Pendientes de contenido

- El número de WhatsApp en `index.html` (la constante `WHATSAPP` y el enlace directo).
- El correo de contacto (hoy dice hola@demetrio.mx).
- El logo en SVG o PNG.
- La página de aviso de privacidad.

## DJs (demetrio.mx/djs)

El roster y los perfiles se generan a partir de `data/djs.json`:

1. Agrega o edita la ficha del DJ en `data/djs.json` y sus fotos en `assets/djs/<slug>/`.
2. Corre `python3 tools/build_djs.py`. Regenera `djs/` y `sitemap.xml`.
3. Haz commit y push.
