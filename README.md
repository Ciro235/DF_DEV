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

El generador scripts/build.py es la fuente de las páginas en español e inglés. Textos, rutas equivalentes y metadatos se generan juntos. Se crean páginas por servicio, demo, contacto, equipo y borradores legales. Los borradores legales y la página del equipo tienen noindex y no entran en el sitemap.

## Datos de muestra

El usuario pidió datos de mockup. Alex Ejemplo, Sam Ejemplo y Ready to Prod Demo, S.L. son ficticios y están identificados como tales. El NIF es expresamente NO VÁLIDO. No hay perfiles falsos ni fotos de personas presentadas como miembros reales. Los correos reales de contacto se conservan.

Antes de declarar el sitio legalmente completo, sustituir los datos de muestra por identidad, NIF y dirección verificados y revisar privacidad, proveedores, plazos y derechos. No se presenta el borrador como una política aprobada.

## Contacto: modo publicado por defecto

El formulario estructura una consulta y prepara un enlace para abrir un borrador en la aplicación de correo del visitante. La interfaz dice “Preparar correo”, nunca “consulta enviada”. El navegador no guarda los campos y el servidor no los recibe. Los correos siguen disponibles sin JavaScript.

El envío directo está implementado en functions/api/contact.js y desactivado por defecto. Requiere:
- Sustituir identidad y textos legales de muestra por los datos y políticas reales revisados.
- LEGAL_REVIEWED=true y CONTACT_LIVE=true durante la compilación.
- TURNSTILE_SITE_KEY durante la compilación y TURNSTILE_SECRET como secreto en Cloudflare Pages.
- RESEND_API_KEY y CONTACT_FROM como secretos/configuración de Cloudflare Pages, con remitente autorizado por el proveedor.
- LEGAL_REVIEWED=true también en el entorno de ejecución.
- Nueva compilación y despliegue.

No insertar claves en HTML, Git ni JavaScript público. El endpoint valida origen, tipos, tamaños y campos, honeypot, Turnstile e identidad idempotente para reintentos. Solo responde éxito cuando el proveedor acepta el correo. Las pruebas usan servicios simulados y nunca envían correos reales.

## Demo propia

/demo/ y /en/demo/ organizan solicitudes con reglas locales y generan CSV según las opciones seleccionadas. La demo no usa IA, no envía datos ni conecta un CRM. Las capturas se generan desde la demo funcional.

## Medición

site.js emite eventos locales readytoprod:conversion. No se envían a ningún proveedor por defecto y no existe todavía un cuadro de métricas remoto. Los eventos separan:
- demo_completed y demo_downloaded
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
