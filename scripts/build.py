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
    "automation": {"es": "/services/automation/", "en": "/en/services/automation/"},
    "web": {"es": "/services/web-development/", "en": "/en/services/web-development/"},
    "integrations": {"es": "/services/integrations/", "en": "/en/services/integrations/"},
    "contact": {"es": "/contact/", "en": "/en/contact/"},
    "team": {"es": "/team/", "en": "/en/team/"},
    "privacy": {"es": "/privacy/", "en": "/en/privacy/"},
    "legal": {"es": "/legal/", "en": "/en/legal/"},
}
LOGO_FILE = "/logo-original.webp"
FAVICON_FILE = "/favicon-transparent-64.png"
EMAILS = ["dariosc235@gmail.com", "fsegui16@gmail.com"]
ARROW = '<svg class="arrow" aria-hidden="true" viewBox="0 0 24 24"><path d="M5 19 19 5M5 5h14v14"/></svg>'
def t(es, en, lang):
    return es if lang == "es" else en
def path(key, lang):
    return ROUTES[key][lang]
def link(key, label, lang, cls="text-link"):
    return '<a class="' + cls + '" href="' + path(key, lang) + '">' + esc(label) + (ARROW if cls == 'button' else '') + '</a>'
def mail(lang):
    subject = "Proyecto%20para%20readytoprod" if lang == "es" else "Project%20for%20readytoprod"
    return "mailto:" + EMAILS[0] + "?cc=fsegui16%40gmail.com&amp;subject=" + subject

SERVICES = {
"automation": {
"es": {"title":"Automatización con IA", "lead":"Para solicitudes, documentos y tareas que vuelven a repetirse.",
"desc":"Conectamos los pasos que hoy haces a mano para que la información llegue organizada a la persona adecuada.",
"problems":["Copias los mismos datos entre formularios, documentos y correo.","Los avisos y el seguimiento dependen de que alguien se acuerde.","Preparar un reporte implica reunir información de varias herramientas."],
"deliverables":["Mapa del proceso y sus puntos de revisión.","Flujo configurado con los conectores acordados.","Pruebas de los recorridos, errores y excepciones definidos.","Documentación de uso y accesos incluidos en la propuesta."],
"inputs":["Qué haces hoy y qué quieres mejorar.","Herramientas que utilizas y permisos disponibles.","Los datos del proceso, sin información sensible."],
"scope":"Utilizamos IA cuando aporta valor al proceso. Si basta con reglas claras, no añadimos complejidad. Los envíos y decisiones sensibles pueden incluir revisión humana."},
"en": {"title":"AI automation", "lead":"For requests, documents and tasks that keep coming back.",
"desc":"We connect the steps you handle manually so information reaches the right person in an organized way.",
"problems":["You copy the same data between forms, documents and email.","Reminders and follow-up depend on someone remembering.","Preparing a report means gathering information from several tools."],
"deliverables":["A process map with agreed review points.","A configured workflow with the agreed connectors.","Tests for the defined workflows, errors and exceptions.","Usage documentation and the access details included in the proposal."],
"inputs":["What you do today and what you want to improve.","The tools you use and available permissions.","Process data without sensitive information."],
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

def hero_art(key):
    base = "/images/heroes/" + key
    return '<figure class="hero-art"><img src="'+base+'-1280.webp" srcset="'+base+'-640.webp 640w, '+base+'-1280.webp 1280w" sizes="(max-width: 800px) 110px, 360px" width="1280" height="853" alt="" fetchpriority="high" decoding="async"></figure>'


def team_section(lang):
    text = t("Somos dos hermanos detrás de readytoprod. Trabajamos online y acordamos contigo los avances y la comunicación del proyecto.","We are the two brothers behind readytoprod. We work online and agree on progress updates and communication with you.",lang)
    cards = []
    arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16m-6-6 6 6-6 6"/></svg>'
    for slug, name, role, email in [("frank-segui", "Frank Seguí", "Backend Specialist &amp; Web Developer", EMAILS[1]), ("dario-segui", "Darío Seguí", "Automation &amp; Solutions Architect", EMAILS[0])]:
        cards.append('<a class="team-card" href="mailto:'+email+'" aria-label="'+t("Escribir a ","Email ",lang)+name+'"><span class="team-portrait"><img src="/team/'+slug+'.webp" alt="'+t("Retrato de ","Portrait of ",lang)+name+'" width="640" height="640" decoding="async"></span><span class="team-card-copy"><h2>'+name+'</h2><span class="team-role" translate="no">'+role+'</span><span class="team-card-rule" aria-hidden="true"></span></span><span class="team-card-arrow">'+arrow+'</span></a>')
    title = t("Nuestro <span>equipo</span>", "Our <span>team</span>", lang)
    return '<section id="team" class="shell team-profile"><h1>'+title+'</h1><p class="team-intro">'+text+'</p><div class="team-cards">'+''.join(cards)+'</div></section>'


def faq(lang):
    pairs = [
        (t("¿Cuánto cuesta y cuánto tarda?","How much does it cost, and how long does it take?",lang),t("Depende del alcance, las integraciones y el contenido. Te proponemos un presupuesto y un calendario para acordarlos antes de empezar.","It depends on scope, integrations and content. We propose a budget and timeline to agree on before starting.",lang)),
        (t("¿Qué necesitáis para empezar?","What do you need to get started?",lang),t("Cuéntanos qué haces, qué tarea te consume tiempo y qué herramientas utilizas. Con eso podemos definir el problema y los siguientes pasos.","Tell us what you do, which tasks take up your time and what tools you use. That gives us a starting point to define the problem and next steps.",lang)),
        (t("¿Necesito saber de tecnología?","Do I need technical knowledge?",lang),t("No. Tú conoces tu negocio; nosotros te ayudamos a convertir lo que necesitas en una solución que puedas entender, probar y utilizar.","No. You know your business; we help turn your needs into a solution you can understand, test and use.",lang)),
        (t("¿De quién es el código y qué recibo?","Who owns the code, and what do I receive?",lang),t("La propuesta recoge las condiciones de propiedad, los accesos, la documentación y los materiales que se entregan. También identificamos las licencias y servicios de terceros.","The proposal sets out ownership terms, access details, documentation and deliverables. We also identify third-party licenses and services.",lang)),
        (t("¿Qué pasa después de la entrega?","What happens after delivery?",lang),t("Acordamos las opciones de mantenimiento y soporte en la propuesta, para que sepas qué incluye el proyecto y cómo continuar.","We agree on maintenance and support options in the proposal so you know what is included and how to move forward.",lang)),
    ]
    return '<section id="faq" class="shell faq"><div><h2>'+t("Preguntas frecuentes","Frequently asked questions",lang)+'</h2>'+link("contact",t("¿Tienes otra pregunta?","Have another question?",lang),lang)+'</div><div>'+''.join('<details><summary>'+q+'</summary><p>'+a+'</p></details>' for q,a in pairs)+'</div></section>'

def contact_section(lang):
    live = os.environ.get("CONTACT_LIVE") == "true"
    title = t("Hablemos de tu proyecto","Tell us about your project",lang)
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
    return '<section id="contact" class="shell contact"><div><h2>'+title+'</h2><p>'+t("Cuéntanos tu proceso, las herramientas que utilizas y qué necesitas mejorar.","Tell us about your process, the tools you use and what you want to improve.",lang)+'</p><div class="contact-options"><h3>'+t("Correo directo","Direct email",lang)+'</h3>'+''.join('<div class="email-row"><a href="mailto:'+e+'">'+e+'</a><button class="copy" type="button" data-copy="'+e+'" aria-label="'+t("Copiar correo ","Copy email ",lang)+e+'">'+t("Copiar","Copy",lang)+'</button></div>' for e in EMAILS)+'<p id="copy-status" role="status" aria-live="polite"></p></div></div><form id="contact-form" data-mode="'+("live" if live else "email")+'" action="'+mail(lang)+'" method="get">'+sender_fields+'<label for="contact-service">'+t("¿Qué necesitas?","What do you need?",lang)+'</label><select id="contact-service" name="service" required>'+options+'</select><label for="contact-message">'+t("Tu consulta","Your inquiry",lang)+'</label><textarea id="contact-message" name="message" rows="5" minlength="15" maxlength="4000" placeholder="'+t("Describe la tarea o el proyecto…","Describe the task or project…",lang)+'" required></textarea><p class="form-help">'+t("No incluyas contraseñas ni información sensible.","Do not include passwords or sensitive information.",lang)+'</p><div class="trap" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div><p>'+notice+'</p><p class="form-help">'+link("privacy",t("Consultar privacidad","Privacy information",lang),lang)+'</p>'+challenge+'<button type="submit" class="button">'+mode+ARROW+'</button><p id="contact-status" role="status" aria-live="polite"></p><noscript><p>'+t("Para preparar el borrador, utiliza uno de los enlaces de correo.","To prepare your message, use one of the email links.",lang)+'</p></noscript></form></section>'

def home(lang):
    cards = []
    for key in SERVICES:
        d = SERVICES[key][lang]
        cards.append('<article class="service-card"><h3>'+d["title"]+'</h3><p>'+d["desc"]+'</p><ul>'+''.join('<li>'+esc(item)+'</li>' for item in d["deliverables"][:2])+'</ul>'+link(key,t("Ver entregables y requisitos","View deliverables and requirements",lang),lang)+'</article>')
    hero = '<section class="hero shell"><div class="hero-copy"><h1>'+t("Desarrollo web y <em>automatización.</em>","Web development <em>and automation.</em>",lang)+'</h1><p class="intro">'+t("Creamos webs y conectamos formularios, correo, CRM y APIs para reducir las tareas manuales de tu equipo.","We build websites and connect forms, email, CRMs and APIs to reduce your team’s manual work.",lang)+'</p><div class="actions">'+link("contact",t("Cuéntanos qué necesitas","Tell us what you need",lang),lang,"button")+'</div></div>'+hero_art('home')+'</section>'
    services = '<section id="services" class="shell services"><h2>'+t("Qué hacemos y qué recibes","What we build and deliver",lang)+'</h2><div class="service-layout">'+''.join(cards)+'</div></section>'
    return hero + services + faq(lang) + contact_section(lang)


def contact_cta(lang):
    return '<section class="shell contact-cta"><p>'+t("Para definir alcance, precio y calendario, indícanos tu objetivo y las herramientas que utilizas.","To define scope, price and timeline, tell us your goal and the tools you use.",lang)+'</p>'+link("contact",t("Consultar este servicio","Discuss this service",lang),lang,"button")+'</section>'


def service_page(key, lang):
    d=SERVICES[key][lang]
    section = lambda title,items: '<article><h2>'+title+'</h2><ul>'+''.join('<li>'+esc(i)+'</li>' for i in items)+'</ul></article>'
    return '<section class="shell page-intro"><a class="text-link" href="'+path("home",lang)+'#services">'+t("Volver a servicios","Back to services",lang)+'</a><h1>'+d["title"]+'</h1><p class="lead">'+d["lead"]+'</p><p>'+d["desc"]+'</p>'+link("contact",t("Hablar de este proyecto","Discuss this project",lang),lang,"button")+'</section><section class="shell content-grid">'+section(t("Qué recibes","What you receive",lang),d["deliverables"])+section(t("Cuándo tiene sentido","When it makes sense",lang),d["problems"])+section(t("Qué necesitamos de ti","What we need from you",lang),d["inputs"])+'<article><h2>'+t("Un alcance acordado","An agreed scope",lang)+'</h2><p>'+d["scope"]+'</p></article></section>'+contact_cta(lang)

def legal_page(key, lang):
    title = t("Privacidad", "Privacy", lang) if key == "privacy" else t("Aviso legal", "Legal notice", lang)
    if key == "privacy":
        body = '<h2>'+t("Uso de la información", "Use of information", lang)+'</h2><p>'+t("El formulario de contacto prepara un correo en tu aplicación; la web no envía ni guarda su contenido en un servidor de readytoprod. El alojamiento puede tratar registros técnicos según sus propias condiciones.", "The contact form prepares a message in your email app; the website does not send or store its contents on a readytoprod server. Hosting may process technical logs under its own terms.", lang)+'</p><h2>'+t("Cookies y medición", "Cookies and measurement", lang)+'</h2><p>'+t("La web no incorpora analítica de marketing ni cookies no necesarias desde su código.", "The website does not add marketing analytics or non-essential cookies through its code.", lang)+'</p><h2>'+t("Contacto", "Contact", lang)+'</h2><p>'+t("Para cualquier consulta sobre privacidad, escríbenos a los correos de contacto.", "For privacy questions, email our contact addresses.", lang)+'</p>'
    else:
        body = '<h2>readytoprod</h2><p>'+t("Desarrollo web, automatización e integraciones. Frank Seguí y Darío Seguí forman el equipo de readytoprod.", "Web development, automation and integrations. Frank Seguí and Darío Seguí are the team behind readytoprod.", lang)+'</p><h2>'+t("Servicios y contratación", "Services and agreements", lang)+'</h2><p>'+t("Los servicios, precios, alcance, propiedad del código y soporte se concretan en una propuesta individual. Esta web no permite comprar productos ni contratar un servicio mediante pago online.", "Services, pricing, scope, code ownership and support are defined in an individual proposal. This website does not sell products or allow online payment for services.", lang)+'</p>'
    contacts = '<h2>'+t("Correos de contacto", "Contact emails", lang)+'</h2><ul>'+''.join('<li><a href="mailto:'+email+'">'+email+'</a></li>' for email in EMAILS)+'</ul>'
    return '<section class="shell page-intro"><h1>'+title+'</h1></section><section class="shell legal-copy">'+body+contacts+'</section>'


def page(key, lang, content):
    if key not in ("home", "contact", "team"):
        intro, closing, rest = content.partition('</section>')
        intro = intro.replace('class="shell page-intro"', 'class="shell page-intro illustrated-intro"', 1)
        intro = intro.replace('>', '><div class="page-intro-copy">', 1)
        content = intro+'</div>'+hero_art(key)+closing+rest
    title = SERVICES[key][lang]["title"] if key in SERVICES else {
        "home":t("Automatización y desarrollo web para pymes","Automation and web development for small businesses",lang),
        "contact":t("Cuéntanos tu proyecto","Tell us about your project",lang),
        "team":t("Equipo y forma de trabajar","Team and how we work",lang),
        "privacy":t("Privacidad","Privacy",lang),
        "legal":t("Aviso legal","Legal notice",lang),
    }[key]
    description = SERVICES[key][lang]["desc"] if key in SERVICES else t("Automatización, desarrollo web e integraciones para equipos que gestionan solicitudes, clientes y reportes.","Automation, web development and integrations for teams handling inquiries, customers and reports.",lang)
    languages=''.join('<a data-language="'+l+'" lang="'+l+'" hreflang="'+l+'" href="'+path(key,l)+'"'+(' aria-current="page"' if l==lang else '')+' aria-label="'+("Español" if l=="es" else "English")+'">'+l.upper()+'</a>' for l in ["es","en"])
    nav_items = [("home",t("Inicio","Home",lang)),("services",t("Servicios","Services",lang)),("team",t("Equipo","Team",lang)),("contact",t("Contacto","Contact",lang))]
    nav = ''.join('<a href="'+(path("home",lang)+"#services" if k=="services" else path(k,lang))+'"'+(' class="is-current"' if (k==key or (k=="services" and key in SERVICES)) else '')+'>'+label+'</a>' for k,label in nav_items)
    data={"@context":"https://schema.org","@type":"Organization","name":"readytoprod","url":ORIGIN,"email":EMAILS[0],"logo":ORIGIN+LOGO_FILE}
    return '<!doctype html>\n<html lang="'+lang+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' · readytoprod</title><meta name="description" content="'+esc(description,quote=True)+'"><meta name="theme-color" content="#ffffff"><link rel="canonical" href="'+ORIGIN+path(key,lang)+'">'+''.join('<link rel="alternate" hreflang="'+l+'" href="'+ORIGIN+path(key,l)+'">' for l in ["es","en"])+'<link rel="alternate" hreflang="x-default" href="'+ORIGIN+path(key,"es")+'"><link rel="icon" href="'+FAVICON_FILE+'" type="image/png"><link rel="preload" href="/fonts/manrope.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="/style.css"><meta property="og:title" content="'+esc(title,quote=True)+' · readytoprod"><meta property="og:description" content="'+esc(description,quote=True)+'"><meta property="og:type" content="website"><meta property="og:locale" content="'+("es_ES" if lang=="es" else "en_US")+'"><meta property="og:url" content="'+ORIGIN+path(key,lang)+'"><meta property="og:image" content="'+ORIGIN+'/social'+("-en" if lang=="en" else "")+'.png"><meta name="twitter:card" content="summary_large_image">'+('<meta name="robots" content="noindex,follow">' if key in ["privacy","legal"] else '')+'<script type="application/ld+json">'+json.dumps(data)+'</script><script defer src="/site.js"></script></head><body id="home" class="page-'+key+'"><a class="skip" href="#content">'+t("Saltar al contenido","Skip to content",lang)+'</a><header class="nav shell"><a class="brand" href="'+path("home",lang)+'" aria-label="'+t("readytoprod, inicio","readytoprod, home",lang)+'" translate="no"><img src="'+LOGO_FILE+'" alt="" width="36" height="40"><span>readytoprod</span></a><nav id="main-nav" aria-label="'+t("Principal","Main",lang)+'">'+nav+'</nav><div class="header-actions"><div class="language-switch" role="group" aria-label="'+t("Idioma","Language",lang)+'">'+languages+'</div><a class="button small" href="'+path("contact",lang)+'">'+t("Hablemos","Let’s talk",lang)+ARROW+'</a><button id="menu-toggle" class="menu-toggle" aria-controls="main-nav" aria-expanded="true" type="button" hidden>'+t("Menú","Menu",lang)+'</button></div></header><main id="content">'+content+'</main><footer class="shell"><a class="brand" href="'+path("home",lang)+'" translate="no"><img src="'+LOGO_FILE+'" alt="" width="36" height="40"><span>readytoprod</span></a><div class="footer-links">'+link("contact",t("Contacto","Contact",lang),lang)+link("privacy",t("Privacidad","Privacy",lang),lang)+link("legal",t("Aviso legal","Legal notice",lang),lang)+'</div><span>© 2026 readytoprod</span></footer></body></html>'

def build():
    OUT.mkdir(exist_ok=True)
    for legacy in ['/demo/', '/en/demo/', '/servicios/automatizacion/', '/servicios/desarrollo-web/', '/servicios/integraciones/', '/contacto/', '/equipo/', '/privacidad/', '/aviso-legal/']:
        (OUT / legacy.strip("/") / "index.html").unlink(missing_ok=True)
    for retired in (OUT / "demo", OUT / "en/demo"):
        if retired.is_dir() and not any(retired.iterdir()):
            retired.rmdir()
    for lang in ["es","en"]:
        for key in ROUTES:
            if key=="home": content=home(lang)
            elif key in SERVICES: content=service_page(key,lang)
            elif key=="contact": content=contact_section(lang).replace("<h2>","<h1>",1).replace("</h2>","</h1>",1)
            elif key=="team": content=team_section(lang)
            else: content=legal_page(key,lang)
            dest=OUT / path(key,lang).strip("/") / "index.html"
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(page(key,lang,content),encoding="utf-8")
    # A real 404 prevents unknown paths from returning the homepage with HTTP 200.
    (OUT/"404.html").write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada · readytoprod</title><link rel="preload" href="/fonts/manrope.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="/style.css"><main class="shell page-intro"><h1>Esta página no está aquí.<br> This page is not here.</h1><p>Revisa la dirección o vuelve al inicio. / Check the address or return home.</p><a class="button" href="/">Español</a> <a class="button" href="/en/">English</a></main></html>',encoding="utf-8")
    entries=[]
    for key in ROUTES:
        if key in ["privacy","legal"]: continue
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
