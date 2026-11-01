# readytoprod

Web bilingüe de automatización, desarrollo web e integraciones. Sin tienda.

## Desarrollo y comprobaciones

Requiere Python 3.12+, Node 22+ y Chromium de Playwright para pruebas y capturas.

1. npm ci --ignore-scripts --no-audit --no-fund
2. npx playwright install chromium
3. npm run build
4. npm run assets
5. npm run check
6. npm test

Para previsualizar: python3 -m http.server 3000 --directory public.

El generador scripts/build.py es la fuente de las páginas en español e inglés. Textos, rutas equivalentes y metadatos se generan juntos. Se crean páginas por servicio, contacto, equipo y páginas legales. Las páginas legales tienen noindex y no entran en el sitemap.

## Contenido del sitio

El equipo muestra a Frank Seguí y Darío Seguí y conserva sus correos de contacto. El aviso legal no publica datos de una sociedad inventada.

Los datos fiscales y las condiciones legales definitivas siguen pendientes de revisión antes de activar la recepción de consultas en servidor.

## Contacto: modo publicado por defecto

El formulario estructura una consulta y prepara un enlace para abrir un borrador en la aplicación de correo del visitante. La interfaz dice “Preparar correo”, nunca “consulta enviada”. El navegador no guarda los campos y el servidor no los recibe. Los correos siguen disponibles sin JavaScript.

El envío directo está implementado en functions/api/contact.js y desactivado por defecto. Requiere:
- Completar la identidad fiscal y revisar los textos legales con los datos y políticas definitivos.
- LEGAL_REVIEWED=true y CONTACT_LIVE=true durante la compilación.
- TURNSTILE_SITE_KEY durante la compilación y TURNSTILE_SECRET como secreto en Cloudflare Pages.
- RESEND_API_KEY y CONTACT_FROM como secretos/configuración de Cloudflare Pages, con remitente autorizado por el proveedor.
- LEGAL_REVIEWED=true también en el entorno de ejecución.
- Nueva compilación y despliegue.

No insertar claves en HTML, Git ni JavaScript público. El endpoint valida origen, tipos, tamaños y campos, honeypot, Turnstile e identidad idempotente para reintentos. Solo responde éxito cuando el proveedor acepta el correo. Las pruebas usan servicios simulados y nunca envían correos reales.

## Medición

site.js emite eventos locales readytoprod:conversion. No se envían a ningún proveedor por defecto y no existe todavía un cuadro de métricas remoto. Los eventos separan:
- email_copied
- email_draft_prepared: preparación, no consulta enviada
- inquiry_accepted: solo cuando el backend confirma aceptación real

Seleccionar un proveedor y revisar privacidad/consentimiento antes de conectar un receptor. No añadir un banner de cookies vacío ni confundir un clic con una consulta recibida.

## Publicación

bash scripts/deploy.sh

Cloudflare Pages: proyecto readytoprod. Reutiliza proyecto y acceso existentes. Las comprobaciones se ejecutan antes de desplegar; las funciones se compilan desde functions/.

El workflow valida y guarda un artefacto. No publica automáticamente. No se han comprado dominios ni contratado correo profesional: hace falta un dominio controlado por el usuario y un proveedor, no inventar direcciones operativas.

## Pendiente de datos externos

Identidad, roles, retratos y perfiles definitivos; datos legales y revisión final; dominio y proveedor de correo; credenciales y remitente verificado para envío directo; proveedor y condiciones de medición remota.

Estas dependencias no se ocultan con confirmaciones falsas. No se incorporan productos, carrito ni pagos.

## Dirección visual — noviembre 2026

Rediseño claro con acentos azules y verdes, tarjetas de servicios con entregables y uso limitado de iconos. Las cabeceras utilizan las ilustraciones de marca. Todas las rutas comparten el diseño y preservan sus versiones ES/EN.

La fuente Manrope se aloja localmente; su licencia SIL Open Font License se conserva en public/fonts/OFL.txt. No se carga una fuente desde Google en el navegador del visitante.

## Logo original y fondos

La cabecera, el pie, el favicon y las imágenes sociales utilizan una versión del logo original adjunto con contornos más definidos y acabado homogéneo; las variantes alternativas se descartaron. El favicon usa la imagen PNG transparente proporcionada, reducida a 64 x 64 píxeles en public/favicon-transparent-64.png. LOGO_FILE y FAVICON_FILE en scripts/build.py permiten sustituir estos recursos. El icono vectorial anterior se conserva en public/icon.svg para poder recuperarlo.

Los degradados y las ondas azules/verdes son fondos decorativos en CSS, con menor intensidad en móvil, sin añadir iconos ni scripts de animación.

## Imágenes de cabecera

Inicio, servicios y páginas legales utilizan ilustraciones sin texto compartidas entre español e inglés, en `public/images/heroes/`. Se sirven en WebP de 640 y 1280 píxeles con `srcset`. Los prompts originales se conservan en `design/hero-prompts.json`. Contacto no lleva imagen; equipo utiliza los retratos de Frank y Darío.

## Estructura compacta

Inicio prioriza la oferta, los entregables por servicio, las preguntas frecuentes y el contacto. Los servicios terminan con un enlace a contacto sin repetir el formulario completo. La página del equipo reúne título, presentación y dos tarjetas con enlace al correo de cada miembro, siguiendo la referencia visual. La demo se retiró de rutas, navegación, código de interacción y generación de capturas.
