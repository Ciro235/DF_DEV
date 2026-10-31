#!/usr/bin/env python3
"""Build bilingual static pages. No production dependencies."""
import json
import os
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public"
ORIGIN = "https://readytoprod.pages.dev"
ROUTES = {
    "home": {"es": "/", "en": "/en/"},
    "automation": {"es": "/servicios/automatizacion/", "en": "/en/services/automation/"},
    "web": {"es": "/servicios/desarrollo-web/", "en": "/en/services/web-development/"},
    "integrations": {"es": "/servicios/integraciones/", "en": "/en/services/integrations/"},
    "demo": {"es": "/demo/", "en": "/en/demo/"},
    "contact": {"es": "/contacto/", "en": "/en/contact/"},
    "team": {"es": "/equipo/", "en": "/en/team/"},
    "privacy": {"es": "/privacidad/", "en": "/en/privacy/"},
    "legal": {"es": "/aviso-legal/", "en": "/en/legal/"},
}
EMAILS = ["dariosc235@gmail.com", "fsegui16@gmail.com"]
ARROW = '<svg class="arrow" aria-hidden="true" viewBox="0 0 24 24"><path d="M5 19 19 5M5 5h14v14"/></svg>'
def t(es, en, lang):
    return es if lang == "es" else en
def path(key, lang):
    return ROUTES[key][lang]
def link(key, label, lang, cls="text-link"):
    return '<a class="' + cls + '" href="' + path(key, lang) + '">' + esc(label) + ARROW + '</a>'
def mail(lang):
    subject = "Proyecto%20para%20readytoprod" if lang == "es" else "Project%20for%20readytoprod"
    return "mailto:" + EMAILS[0] + "?cc=fsegui16%40gmail.com&amp;subject=" + subject
def icon(kind):
    shapes = {"form":"M6 3h9l4 4v14H6zM14 3v5h5M9 12h7M9 16h7","sort":"M4 7h16M7 12h10M10 17h4M8 4v6M16 9v6","send":"m3 11 18-8-6 18-4-7zM11 14l10-11"}
    return '<span class="flow-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="' + shapes[kind] + '"/></svg></span>'

SERVICES = {
"automation": {
"es": {"title":"Automatización con IA", "lead":"Para solicitudes, documentos y tareas que vuelven a repetirse.",
"desc":"Conectamos los pasos que hoy haces a mano para que la información llegue organizada a la persona adecuada.",
"problems":["Copias los mismos datos entre formularios, documentos y correo.","Los avisos y el seguimiento dependen de que alguien se acuerde.","Preparar un reporte implica reunir información de varias herramientas."],
"deliverables":["Mapa del proceso y sus puntos de revisión.","Flujo configurado con los conectores acordados.","Pruebas de los recorridos, errores y excepciones definidos.","Documentación de uso y accesos incluidos en la propuesta."],
"inputs":["Qué haces hoy y qué quieres mejorar.","Herramientas que utilizas y permisos disponibles.","Un ejemplo de los datos, sin información sensible."],
"scope":"Utilizamos IA cuando aporta valor al proceso. Si basta con reglas claras, no añadimos complejidad. Los envíos y decisiones sensibles pueden incluir revisión humana."},
"en": {"title":"AI automation", "lead":"For requests, documents and tasks that keep coming back.",
"desc":"We connect the steps you handle manually so information reaches the right person in an organized way.",
"problems":["You copy the same data between forms, documents and email.","Reminders and follow-up depend on someone remembering.","Preparing a report means gathering information from several tools."],
"deliverables":["A process map with agreed review points.","A configured workflow with the agreed connectors.","Tests for the defined workflows, errors and exceptions.","Usage documentation and the access details included in the proposal."],
"inputs":["What you do today and what you want to improve.","The tools you use and available permissions.","A sample of the data without sensitive information."],
"scope":"We use AI where it adds value. If clear rules are enough, we keep the process simple. Sensitive messages and decisions can include human review."}},
"web": {
"es": {"title":"Desarrollo web", "lead":"Una web que explica lo que haces y facilita el siguiente paso.",
"desc":"Creamos sitios y aplicaciones adaptados a tu negocio, con contenido comprensible, navegación clara y atención al móvil.",
"problems":["Tu oferta no se entiende rápidamente.","Contactar exige demasiados pasos o depende de enlaces poco claros.","Necesitas gestionar solicitudes o información desde una web propia."],
"deliverables":["Estructura de páginas y contenido acordados.","Diseño adaptable a móvil, tableta y escritorio.","Formularios e integraciones incluidos en el alcance.","Metadatos, comprobaciones de accesibilidad y documentación de entrega."],
"inputs":["Tu oferta, tu público y el objetivo de la web.","Marca, textos y materiales disponibles.","Qué debe ocurrir cuando una persona visita o contacta."],
"scope":"Acordamos contenido, funcionalidades y alojamiento antes de empezar. Los dominios, licencias y servicios externos se identifican por separado. No prometemos posiciones en buscadores."},
"en": {"title":"Web development", "lead":"A website that explains what you do and makes the next step easy.",
"desc":"We build websites and applications around your business, with clear content, straightforward navigation and attention to mobile users.",
"problems":["Visitors do not quickly understand your offer.","Getting in touch takes too many steps or relies on unclear links.","You need to manage requests or information through your own website."],
"deliverables":["An agreed page structure and content.","A layout for mobile, tablet and desktop.","The forms and integrations included in the scope.","Metadata, accessibility checks and handover documentation."],
"inputs":["Your offer, your audience and the website's purpose.","Your brand, copy and available materials.","What should happen when someone visits or contacts you."],
"scope":"We agree on content, functionality and hosting before starting. Domains, licenses and external services are identified separately. We do not promise search rankings."}},
"integrations": {
"es": {"title":"Integraciones a medida", "lead":"Para que tus herramientas compartan la información que necesitas.",
"desc":"Conectamos formularios, correo, CRM y APIs para reducir el trabajo de trasladar datos de un sistema a otro.",
"problems":["La misma información cambia en una herramienta y queda desactualizada en otra.","Tu equipo comprueba manualmente si una solicitud ha llegado.","Necesitas conectar una API con tu proceso interno."],
"deliverables":["Diseño del intercambio de información y campos.","Conexiones con los sistemas acordados.","Validación, manejo de errores y pruebas del recorrido.","Documentación de credenciales, límites y mantenimiento previsto."],
"inputs":["Qué herramientas hay que conectar.","Qué datos se intercambian y cuál es su origen.","Documentación de APIs y accesos autorizados."],
"scope":"La viabilidad depende de las APIs, permisos y límites del proveedor. Comprobamos esos requisitos antes de cerrar el alcance y mantenemos las credenciales fuera del código."},
"en": {"title":"Custom integrations", "lead":"So your tools share the information you need.",
"desc":"We connect forms, email, CRMs and APIs to reduce the work of moving data between systems.",
"problems":["Information changes in one tool but stays out of date in another.","Your team manually checks whether a request has arrived.","You need to connect an API to your internal workflow."],
"deliverables":["A design for the data exchange and fields.","Connections to the agreed systems.","Validation, error handling and workflow tests.","Documentation of credentials, limits and planned maintenance."],
"inputs":["Which tools need to connect.","What data is exchanged and where it comes from.","API documentation and authorized access."],
"scope":"Feasibility depends on the provider's APIs, permissions and limits. We check these before agreeing on scope and keep credentials out of the code."}}
}

def workflow(lang):
    rows = [
        ("form", t("Recibe una solicitud","Receive a request",lang), t("Un cliente completa tu formulario.","A customer fills out your form.",lang)),
        ("sort", t("Organiza la información","Organize the information",lang), t("El flujo clasifica y guarda los datos.","The workflow sorts and saves the data.",lang)),
        ("send", t("Define el siguiente paso","Define the next step",lang), t("Tu equipo revisa lo que necesita atención.","Your team reviews what needs attention.",lang)),
    ]
    return '<aside class="terminal" aria-label="' + t("Flujo de automatización","Automation workflow",lang) + '"><div class="terminal-top">' + t("De una solicitud a una acción","From a request to an action",lang) + '</div><ol class="workflow">' + ''.join('<li>'+icon(k)+'<span><strong>'+a+'</strong><small>'+b+'</small></span></li>' for k,a,b in rows) + '</ol><div class="terminal-bottom">' + link("demo",t("Probar con datos de muestra","Try it with sample data",lang),lang) + '</div></aside>'

def team_section(lang, full=False):
    text = t("Somos dos hermanos detrás de readytoprod. Trabajamos online y acordamos contigo los avances y la comunicación del proyecto.","We are the two brothers behind readytoprod. We work online and agree on progress updates and communication with you.",lang)
    cards = []
    for letter, name, role in [("A","Alex Ejemplo",t("Desarrollo web","Web development",lang)),("B","Sam Ejemplo",t("Automatización e integraciones","Automation and integrations",lang))]:
        cards.append('<article class="person"><span class="initial" aria-hidden="true">'+letter+'</span><div><h3>'+name+'</h3><p>'+role+'</p><span class="mock-label">'+t("Nombre y rol de muestra","Sample name and role",lang)+'</span></div></article>')
    return '<section id="equipo" class="shell team"><div><h2>'+t("Equipo pequeño.<br><em>Trato directo.</em>","Small team.<br><em>Direct contact.</em>",lang)+'</h2><p>'+text+'</p><p class="notice">'+t("Presentación provisional: los nombres y roles de estas tarjetas son ficticios. Se sustituirán por los datos verificados del equipo.","Provisional presentation: the names and roles in these cards are fictional. They will be replaced with verified team details.",lang)+'</p></div><div class="people">'+''.join(cards)+'</div></section>'

def faq(lang):
    pairs = [
        (t("¿Cuánto cuesta y cuánto tarda?","How much does it cost, and how long does it take?",lang),t("Depende del alcance, las integraciones y el contenido. Te proponemos un presupuesto y un calendario para acordarlos antes de empezar.","It depends on scope, integrations and content. We propose a budget and timeline to agree on before starting.",lang)),
        (t("¿Qué necesitáis para empezar?","What do you need to get started?",lang),t("Cuéntanos qué haces, qué tarea te consume tiempo y qué herramientas utilizas. Con eso podemos definir el problema y los siguientes pasos.","Tell us what you do, which tasks take up your time and what tools you use. That gives us a starting point to define the problem and next steps.",lang)),
        (t("¿Necesito saber de tecnología?","Do I need technical knowledge?",lang),t("No. Tú conoces tu negocio; nosotros te ayudamos a convertir lo que necesitas en una solución que puedas entender, probar y utilizar.","No. You know your business; we help turn your needs into a solution you can understand, test and use.",lang)),
        (t("¿De quién es el código y qué recibo?","Who owns the code, and what do I receive?",lang),t("La propuesta recoge las condiciones de propiedad, los accesos, la documentación y los materiales que se entregan. También identificamos las licencias y servicios de terceros.","The proposal sets out ownership terms, access details, documentation and deliverables. We also identify third-party licenses and services.",lang)),
        (t("¿Qué pasa después de la entrega?","What happens after delivery?",lang),t("Acordamos las opciones de mantenimiento y soporte en la propuesta, para que sepas qué incluye el proyecto y cómo continuar.","We agree on maintenance and support options in the proposal so you know what is included and how to move forward.",lang)),
    ]
    return '<section id="preguntas" class="shell faq"><div><h2>'+t("Antes de empezar.","Before we start.",lang)+'</h2><p>'+t("Las dudas que conviene resolver antes de construir.","The questions worth answering before building anything.",lang)+'</p>'+link("contact",t("¿Tienes otra pregunta?","Have another question?",lang),lang)+'</div><div>'+''.join('<details><summary>'+q+'</summary><p>'+a+'</p></details>' for q,a in pairs)+'</div></section>'

def contact_section(lang):
    live = os.environ.get("CONTACT_LIVE") == "true"
    title = t("Cuéntanos qué quieres<br>dejar de hacer a mano.","Tell us what you want<br>to stop doing by hand.",lang)
    mode = t("Enviar consulta","Send inquiry",lang) if live else t("Preparar correo","Prepare email",lang)
    notice = t("El formulario enviará tu consulta al equipo. Revisa la información de privacidad antes de continuar.","The form will send your inquiry to the team. Review the privacy information before continuing.",lang) if live else t("Preparamos un enlace con tu consulta. Ábrelo para enviarla desde tu correo. La web no envía ni guarda estos datos.","We prepare a link with your inquiry. Open it to send the message from your email app. This website does not send or store these details.",lang)
    options = '<option value="">'+t("Elige un servicio","Choose a service",lang)+'</option>'
    options += ''.join('<option value="'+key+'">'+esc(SERVICES[key][lang]["title"])+'</option>' for key in SERVICES)
    sender_fields = ''
    if live:
        sender_fields = '<label for="contact-name">'+t("Tu nombre (opcional)","Your name (optional)",lang)+'</label><input id="contact-name" name="name" maxlength="120" autocomplete="name"><label for="contact-email">'+t("Correo para responderte","Your reply email",lang)+'</label><input id="contact-email" name="email" type="email" maxlength="254" autocomplete="email" required>'
    challenge = ''
    if live:
        challenge = '<div class="cf-turnstile" data-sitekey="'+esc(os.environ.get("TURNSTILE_SITE_KEY",""),quote=True)+'"></div><script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>'
    return '<section id="contacto" class="shell contact"><div><h2>'+title+'</h2><p>'+t("Cuéntanos tu proceso, las herramientas que utilizas y qué necesitas mejorar.","Tell us about your process, the tools you use and what you want to improve.",lang)+'</p><div class="contact-options"><h3>'+t("También puedes escribirnos directamente.","You can also email us directly.",lang)+'</h3>'+''.join('<div class="email-row"><a href="mailto:'+e+'">'+e+'</a><button class="copy" type="button" data-copy="'+e+'" aria-label="'+t("Copiar correo ","Copy email ",lang)+e+'">'+t("Copiar","Copy",lang)+'</button></div>' for e in EMAILS)+'<p id="copy-status" role="status" aria-live="polite"></p></div></div><form id="contact-form" data-mode="'+("live" if live else "email")+'" action="'+mail(lang)+'" method="get">'+sender_fields+'<label for="contact-service">'+t("¿Qué necesitas?","What do you need?",lang)+'</label><select id="contact-service" name="service" required>'+options+'</select><label for="contact-message">'+t("Tu consulta","Your inquiry",lang)+'</label><textarea id="contact-message" name="message" rows="5" minlength="15" maxlength="4000" placeholder="'+t("Describe la tarea o el proyecto…","Describe the task or project…",lang)+'" required></textarea><p class="form-help">'+t("No incluyas contraseñas ni información sensible.","Do not include passwords or sensitive information.",lang)+'</p><div class="trap" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div><p>'+notice+'</p><p class="form-help">'+link("privacy",t("Consultar privacidad — borrador de muestra","Privacy information — sample draft",lang),lang)+'</p>'+challenge+'<button type="submit" class="button">'+mode+ARROW+'</button><p id="contact-status" role="status" aria-live="polite"></p><noscript><p>'+t("Para preparar el borrador, utiliza uno de los enlaces de correo.","To prepare your message, use one of the email links.",lang)+'</p></noscript></form></section>'

def home(lang):
    cards = '<div class="service-layout"><article class="service-main"><p class="service-label">'+t("Para las tareas que se repiten","For tasks you do over and over",lang)+'</p><h3>'+SERVICES["automation"][lang]["title"]+'</h3><p>'+SERVICES["automation"][lang]["desc"]+'</p>'+link("automation",t("Ver alcance y entregables","Explore scope and deliverables",lang),lang)+'</article><div class="service-secondary">'
    for key in ["web","integrations"]:
        d=SERVICES[key][lang]
        cards += '<article><h3>'+d["title"]+'</h3><p>'+d["desc"]+'</p>'+link(key,t("Ver el servicio","Explore this service",lang),lang)+'</article>'
    cards += '</div></div>'
    steps = [(t("Diagnóstico","Discovery",lang),t("Entendemos el proceso y acordamos prioridades, alcance y presupuesto.","We understand the process and agree on priorities, scope and budget.",lang)),(t("Prototipo","Prototype",lang),t("Pruebas una primera versión y revisamos los avances contigo.","You test a first version and we review progress together.",lang)),(t("Entrega y mejora","Delivery and improvement",lang),t("Preparamos las pruebas, la documentación y los accesos acordados.","We prepare the agreed tests, documentation and access details.",lang))]
    return '<section class="hero shell"><div class="hero-copy"><p class="intro-label">'+t("Automatización y desarrollo web para pymes","Automation and web development for small businesses",lang)+'</p><h1>'+t("Menos tareas.<br><em>Más negocio.</em>","Fewer tasks.<br><em>More business.</em>",lang)+'</h1><p class="intro">'+t("Ayudamos a equipos que gestionan solicitudes, clientes y reportes. Automatizamos lo repetitivo, creamos tu web y conectamos tus herramientas.","We help teams that manage inquiries, customers and reports. We automate repetitive tasks, build your website and connect your tools.",lang)+'</p><div class="actions">'+link("contact",t("Cuéntanos tu idea","Tell us your idea",lang),lang,"button")+link("demo",t("Probar una demo","Try a demo",lang),lang)+'</div><p class="hero-note">'+t("Dos hermanos. Un equipo. Trabajo 100 % online.","Two brothers. One team. Working entirely online.",lang)+'</p></div>'+workflow(lang)+'<div class="hero-foot"><span>'+t("Webs a medida","Custom websites",lang)+'</span><span>'+t("Procesos automatizados","Automated processes",lang)+'</span><span>'+t("Herramientas conectadas","Connected tools",lang)+'</span></div></section><section id="servicios" class="shell services"><div class="section-head"><h2>'+t("Tecnología para<br>quitarte trabajo.","Technology that<br>lightens your workload.",lang)+'</h2><p>'+t("Empezamos por el problema. Elegimos las herramientas después.","We start with the problem. Then we choose the tools.",lang)+'</p></div>'+cards+'</section><section id="proceso" class="shell"><div class="section-head"><h2>'+t("Del problema<br>a una solución usable.","From a problem<br>to a working solution.",lang)+'</h2><p>'+t("Alcance claro y avances que puedes revisar.","A clear scope and progress you can review.",lang)+'</p></div><ol class="steps">'+''.join('<li><h3>'+a+'</h3><p>'+b+'</p></li>' for a,b in steps)+'</ol></section><section id="demo" class="shell example-intro"><div><h2>'+t("Pruébalo.<br>No te quedes con la promesa.","Try it.<br>See what it does.",lang)+'</h2><p>'+t("Hemos construido una demo que organiza una solicitud con reglas y genera un resumen descargable. Puedes probarla sin introducir datos personales.","We built a demo that organizes a request using rules and generates a downloadable summary. Try it without entering personal details.",lang)+'</p>'+link("demo",t("Abrir demo interactiva","Open the interactive demo",lang),lang,"button")+'</div><div class="demo-preview"><img class="demo-image" src="/demo-preview-'+lang+'.png" width="1120" height="683" loading="lazy" alt="'+t("Captura real de la demo de organización de solicitudes","Actual screenshot of the request organization demo",lang)+'"><p class="service-label">'+t("Demo propia · procesamiento local","Our own demo · local processing",lang)+'</p><h3>'+t("Solicitud → clasificación → siguiente paso","Request → classification → next step",lang)+'</h3><p>'+t("El resultado cambia con tus elecciones. Puedes revisar y descargar los datos que produce.","The result changes with your choices. Review and download the data it produces.",lang)+'</p></div></section>'+team_section(lang)+faq(lang)+contact_section(lang)

def service_page(key, lang):
    d=SERVICES[key][lang]
    section = lambda title,items: '<article><h2>'+title+'</h2><ul>'+''.join('<li>'+esc(i)+'</li>' for i in items)+'</ul></article>'
    return '<section class="shell page-intro"><a class="text-link" href="'+path("home",lang)+'#servicios">'+t("Volver a servicios","Back to services",lang)+'</a><h1>'+d["title"]+'</h1><p class="lead">'+d["lead"]+'</p><p>'+d["desc"]+'</p>'+link("contact",t("Hablar de este proyecto","Discuss this project",lang),lang,"button")+'</section><section class="shell content-grid">'+section(t("Cuándo tiene sentido","When it makes sense",lang),d["problems"])+section(t("Qué podemos entregar","What we can deliver",lang),d["deliverables"])+section(t("Qué necesitamos de ti","What we need from you",lang),d["inputs"])+'<article><h2>'+t("Un alcance acordado","An agreed scope",lang)+'</h2><p>'+d["scope"]+'</p><p>'+t("Precio y calendario se acuerdan tras el diagnóstico; no hay una promesa de coste o plazo genérica.","Pricing and timeline are agreed after discovery; there is no one-size-fits-all cost or deadline.",lang)+'</p></article></section>'+contact_section(lang)

def demo_page(lang):
    return '<section class="shell page-intro"><h1>'+t("De una solicitud<br>al siguiente paso.","From a request<br>to the next step.",lang)+'</h1><p class="lead">'+t("Prueba una demo que clasifica una solicitud y prepara un resumen.","Try a demo that classifies a request and prepares a summary.",lang)+'</p><p>'+t("Funciona con reglas en tu navegador. No usa IA ni conecta con un CRM real. No envía ni guarda datos en un servidor.","It uses rules in your browser. It does not use AI or connect to a real CRM. No data is sent to or stored on a server.",lang)+'</p></section><section class="shell demo-layout"><form id="demo-form"><label for="demo-service">'+t("Tipo de solicitud","Request type",lang)+'</label><select id="demo-service" name="service">'+''.join('<option value="'+k+'">'+SERVICES[k][lang]["title"]+'</option>' for k in SERVICES)+'</select><label for="demo-volume">'+t("Solicitudes al día","Requests per day",lang)+'</label><input id="demo-volume" name="volume" type="number" min="1" max="10000" value="12" required><label for="demo-urgency">'+t("Prioridad declarada","Requested priority",lang)+'</label><select id="demo-urgency" name="urgency"><option value="normal">'+t("Normal","Normal",lang)+'</option><option value="urgent">'+t("Urgente","Urgent",lang)+'</option></select><button class="button" type="submit">'+t("Organizar solicitud","Organize request",lang)+'</button><button class="text-button" id="demo-reset" type="button">'+t("Restablecer muestra","Reset sample",lang)+'</button></form><div class="demo-output"><h2>'+t("Resultado de la demo","Demo result",lang)+'</h2><p id="demo-status" role="status" aria-live="polite">'+t("Elige los datos y organiza la solicitud para ver el resultado.","Choose the data and organize the request to see the result.",lang)+'</p><dl id="demo-result"></dl><button type="button" class="button" id="demo-download" hidden>'+t("Descargar resumen CSV","Download CSV summary",lang)+'</button></div><noscript><p>'+t("Esta demo necesita JavaScript. Puedes explorar los servicios o escribirnos por correo.","This demo needs JavaScript. You can still explore our services or email us.",lang)+'</p></noscript></section>'+contact_section(lang)

def legal_page(key, lang):
    title=t("Privacidad: borrador de muestra","Privacy: sample draft",lang) if key=="privacy" else t("Aviso legal: borrador de muestra","Legal notice: sample draft",lang)
    notice=t("Este documento utiliza datos ficticios por petición del titular del proyecto. No es una política definitiva ni acredita cumplimiento legal. Debe revisarse y sustituirse antes de activar la recogida de consultas en servidor.","This document uses fictional information requested by the project owner. It is not a final policy or evidence of legal compliance. It must be reviewed and replaced before enabling server-side inquiry collection.",lang)
    if key=="privacy":
        body='<h2>'+t("Cómo funciona esta versión","How this version works",lang)+'</h2><p>'+t("La demo procesa las opciones en el navegador. El formulario de contacto prepara un correo en tu aplicación; no envía ni guarda su contenido en un servidor de readytoprod. El alojamiento puede tratar registros técnicos según sus propias condiciones.","The demo processes choices in your browser. The contact form prepares a message in your email app; it does not send or store its contents on a readytoprod server. Hosting may process technical logs under its own terms.",lang)+'</p><h2>'+t("Información pendiente de completar","Information still to be completed",lang)+'</h2><ul>'+''.join('<li>'+x+'</li>' for x in [t("Identidad, NIF y dirección reales del responsable.","The controller's real identity, tax identification and address.",lang),t("Bases jurídicas, plazos de conservación y canal de derechos.","Lawful bases, retention periods and a channel for exercising rights.",lang),t("Proveedores y condiciones de tratamiento del correo y alojamiento.","Email and hosting providers and their processing terms.",lang)])+'</ul><h2>'+t("Cookies y medición","Cookies and measurement",lang)+'</h2><p>'+t("Esta versión no incorpora analítica de marketing ni cookies no necesarias desde su código. No se cuentan las visitas como conversiones. Cualquier servicio de medición futuro deberá revisarse antes de activarlo.","This version does not add marketing analytics or non-essential cookies through its code. Visits are not counted as conversions. Any future measurement service must be reviewed before activation.",lang)+'</p>'
    else:
        body='<dl class="legal-data"><dt>'+t("Titular — ficticio","Owner — fictional",lang)+'</dt><dd>Ready to Prod Demo, S.L. ('+t("nombre de muestra","sample name",lang)+')</dd><dt>NIF</dt><dd>'+t("NO VÁLIDO — dato pendiente","NOT VALID — details pending",lang)+'</dd><dt>'+t("Dirección profesional","Business address",lang)+'</dt><dd>'+t("Pendiente de sustituir por una dirección real.","To be replaced with a real address.",lang)+'</dd></dl><p>'+t("Los servicios, precios, alcance, propiedad del código y soporte se concretan en una propuesta individual. Esta web no permite comprar productos ni contratar un servicio mediante pago online.","Services, pricing, scope, code ownership and support are defined in an individual proposal. This website does not sell products or allow online payment for services.",lang)+'</p>'
    return '<section class="shell page-intro"><h1>'+title+'</h1><p class="notice">'+notice+'</p></section><section class="shell legal-copy">'+body+'</section>'

def page(key, lang, content):
    other="en" if lang=="es" else "es"
    title = SERVICES[key][lang]["title"] if key in SERVICES else {
        "home":t("Automatización y desarrollo web para pymes","Automation and web development for small businesses",lang),
        "demo":t("Demo de organización de solicitudes","Request organization demo",lang),
        "contact":t("Cuéntanos tu proyecto","Tell us about your project",lang),
        "team":t("Equipo y forma de trabajar","Team and how we work",lang),
        "privacy":t("Privacidad — muestra","Privacy — sample",lang),
        "legal":t("Aviso legal — muestra","Legal notice — sample",lang),
    }[key]
    description = SERVICES[key][lang]["desc"] if key in SERVICES else t("Automatización, desarrollo web e integraciones para equipos que gestionan solicitudes, clientes y reportes.","Automation, web development and integrations for teams handling inquiries, customers and reports.",lang)
    languages=''.join('<a data-language="'+l+'" lang="'+l+'" hreflang="'+l+'" href="'+path(key,l)+'"'+(' aria-current="page"' if l==lang else '')+' aria-label="'+("Español" if l=="es" else "English")+'">'+l.upper()+'</a>' for l in ["es","en"])
    nav=''.join('<a href="'+path("home",lang)+'#'+anchor+'">'+label+'</a>' for anchor,label in [("servicios",t("Servicios","Services",lang)),("proceso",t("Proceso","Process",lang)),("equipo",t("Equipo","Team",lang)),("preguntas",t("Preguntas","FAQs",lang))])
    data={"@context":"https://schema.org","@type":"Organization","name":"readytoprod","url":ORIGIN,"email":EMAILS[0]}
    return '<!doctype html>\n<html lang="'+lang+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' · readytoprod</title><meta name="description" content="'+esc(description,quote=True)+'"><meta name="theme-color" content="#09172d"><link rel="canonical" href="'+ORIGIN+path(key,lang)+'">'+''.join('<link rel="alternate" hreflang="'+l+'" href="'+ORIGIN+path(key,l)+'">' for l in ["es","en"])+'<link rel="alternate" hreflang="x-default" href="'+ORIGIN+path(key,"es")+'"><link rel="icon" href="/icon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css"><meta property="og:title" content="'+esc(title,quote=True)+' · readytoprod"><meta property="og:description" content="'+esc(description,quote=True)+'"><meta property="og:type" content="website"><meta property="og:locale" content="'+("es_ES" if lang=="es" else "en_US")+'"><meta property="og:url" content="'+ORIGIN+path(key,lang)+'"><meta property="og:image" content="'+ORIGIN+'/social'+("-en" if lang=="en" else "")+'.png"><meta name="twitter:card" content="summary_large_image">'+('<meta name="robots" content="noindex,follow">' if key in ["team","privacy","legal"] else '')+'<script type="application/ld+json">'+json.dumps(data)+'</script><script defer src="/site.js"></script></head><body id="inicio"><a class="skip" href="#contenido">'+t("Saltar al contenido","Skip to content",lang)+'</a><header class="nav shell"><a class="brand" href="'+path("home",lang)+'" aria-label="'+t("readytoprod, inicio","readytoprod, home",lang)+'" translate="no"><img src="/icon.svg" alt="" width="36" height="40"><span>readytoprod</span></a><nav id="main-nav" aria-label="'+t("Principal","Main",lang)+'">'+nav+'</nav><div class="header-actions"><div class="language-switch" role="group" aria-label="'+t("Idioma","Language",lang)+'">'+languages+'</div><a class="button small" href="'+path("contact",lang)+'">'+t("Hablemos","Let’s talk",lang)+ARROW+'</a><button id="menu-toggle" class="menu-toggle" aria-controls="main-nav" aria-expanded="true" type="button" hidden>'+t("Menú","Menu",lang)+'</button></div></header><main id="contenido">'+content+'</main><footer class="shell"><a class="brand" href="'+path("home",lang)+'" translate="no"><img src="/icon.svg" alt="" width="36" height="40"><span>readytoprod</span></a><div class="footer-links">'+link("contact",t("Contacto","Contact",lang),lang)+link("privacy",t("Privacidad · muestra","Privacy · sample",lang),lang)+link("legal",t("Aviso legal · muestra","Legal notice · sample",lang),lang)+'</div><span>© 2026 readytoprod</span></footer></body></html>'

def build():
    OUT.mkdir(exist_ok=True)
    for lang in ["es","en"]:
        for key in ROUTES:
            if key=="home": content=home(lang)
            elif key in SERVICES: content=service_page(key,lang)
            elif key=="demo": content=demo_page(lang)
            elif key=="contact": content=contact_section(lang).replace("<h2>","<h1>",1).replace("</h2>","</h1>",1)
            elif key=="team": content='<section class="shell page-intro"><h1>'+t("El equipo detrás del proyecto","The team behind the project",lang)+'</h1></section>'+team_section(lang,True)
            else: content=legal_page(key,lang)
            dest=OUT / path(key,lang).strip("/") / "index.html"
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(page(key,lang,content),encoding="utf-8")
    # A real 404 prevents unknown paths from returning the homepage with HTTP 200.
    (OUT/"404.html").write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada · readytoprod</title><link rel="stylesheet" href="/style.css"><main class="shell page-intro"><h1>Esta página no está aquí.<br>This page is not here.</h1><p>Revisa la dirección o vuelve al inicio. / Check the address or return home.</p><a class="button" href="/">Español</a> <a class="button" href="/en/">English</a></main></html>',encoding="utf-8")
    entries=[]
    for key in ROUTES:
        if key in ["team","privacy","legal"]: continue
        alternates=''.join('<xhtml:link rel="alternate" hreflang="'+l+'" href="'+ORIGIN+path(key,l)+'"/>' for l in ["es","en"])
        entries.extend('<url><loc>'+ORIGIN+path(key,l)+'</loc>'+alternates+'</url>' for l in ["es","en"])
    (OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+''.join(entries)+'</urlset>')
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+ORIGIN+"/sitemap.xml\n")
    (OUT/"contact-config.json").write_text(json.dumps({"mode":"live" if os.environ.get("CONTACT_LIVE")=="true" else "email"}))
    print("Built",len(ROUTES)*2,"localized pages and a real 404.")

if __name__=="__main__":
    if os.environ.get("CONTACT_LIVE")=="true" and (os.environ.get("LEGAL_REVIEWED")!="true" or not os.environ.get("TURNSTILE_SITE_KEY")):
        raise SystemExit("Live collection requires reviewed, real legal data. Do not activate it with mock documents.")
    build()
