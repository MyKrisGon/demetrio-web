#!/usr/bin/env python3
"""Genera el roster de DJs (djs/index.html) y un perfil por DJ (djs/<slug>/index.html)
a partir de data/djs.json.

Uso:  python3 tools/build_djs.py
Para agregar un DJ: agrega su ficha a data/djs.json y sus fotos en assets/djs/<slug>/,
corre este script y haz commit de los archivos generados.
"""
import html
import json
import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHATSAPP = "526242454573"
SITE = "https://demetrio.mx"
CSS_V = "2"

e = lambda s: html.escape(str(s), quote=True)

ARROW = ('<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def head(title, desc, url, image):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="Demetrio Entertainment">
<meta property="og:image" content="{e(image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E0D10">
<link rel="canonical" href="{e(url)}">
<link rel="icon" href="/favicon.ico?v=2" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=2">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
</head>
<body>
"""


def header(cta_href, cta_text):
    return f"""<header class="nav">
  <div class="wrap nav-in">
    <a class="logo" href="/"><img src="/assets/brand/logo-demetrio.png" alt="Demetrio Entertainment" width="184" height="38"></a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="navLinks">Menú</button>
    <nav class="links" id="navLinks" aria-label="Principal">
      <a href="/#que-producimos">Qué producimos</a>
      <a href="/#servicios">Servicios</a>
      <a href="/#eventos">Eventos</a>
      <a href="/djs/" aria-current="page">DJs</a>
      <a href="https://linktr.ee/demetrio.mx">Boletos</a>
      <a class="btn btn-primary" href="{cta_href}">{e(cta_text)}</a>
    </nav>
  </div>
</header>
"""


FOOTER = """<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="logo" href="/"><img src="/assets/brand/logo-demetrio-full.png" alt="Demetrio Entertainment, Los Cabos, B.C.S., México" width="260" height="73" loading="lazy"></a>
        <p>Productora, comercialización, operación y desarrollo de espectáculos. Los Cabos y La Paz, Baja California Sur.</p>
      </div>
      <div><h3>Productora</h3><ul><li><a href="/#que-producimos">Qué producimos</a></li><li><a href="/#servicios">Servicios</a></li><li><a href="/#eventos">Eventos</a></li><li><a href="/djs/">DJs</a></li></ul></div>
      <div><h3>Público</h3><ul><li><a href="https://linktr.ee/demetrio.mx">Boletos y próximos shows</a></li><li><a href="/#formatos">Formatos propios</a></li><li><a href="/#cotiza">Cotiza tu evento</a></li></ul></div>
      <div><h3>Síguenos</h3><ul><li><a href="https://www.instagram.com/demetrio_cabo">Instagram</a></li><li><a href="https://www.facebook.com/share/19ekVby3qt/">Facebook</a></li><li><a href="https://www.youtube.com/@demetriocabo8282">YouTube</a></li></ul></div>
    </div>
    <div class="legal"><span>© <span id="yr">2026</span> Demetrio Entertainment · demetrio.mx</span><span class="legal-links"><a href="/#aviso">Aviso de privacidad</a><span aria-hidden="true">·</span>Sitio hecho por <a href="https://desarrollo.siemex.xyz" rel="noopener">Desarrollo SIEMEX</a></span></div>
  </div>
</footer>
"""

BASE_JS = """<script>
(function(){
  document.getElementById('yr').textContent = new Date().getFullYear();
  var mb = document.getElementById('menuBtn'), nl = document.getElementById('navLinks');
  mb.addEventListener('click', function(){ var o = nl.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });
  nl.addEventListener('click', function(e){ if(e.target.closest('a')){ nl.classList.remove('open'); mb.setAttribute('aria-expanded','false'); } });
})();
</script>
"""


def embed(s):
    if s["tipo"] == "youtube":
        return (f'<div class="set set-video"><div class="set-frame"><iframe src="https://www.youtube-nocookie.com/embed/{e(s["id"])}" '
                f'title="{e(s["titulo"])}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" '
                f'allowfullscreen></iframe></div></div>')
    src = ("https://w.soundcloud.com/player/?url=" + quote(s["url"], safe="") +
           "&color=%23e60048&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false&visual=false")
    return (f'<div class="set set-audio"><p class="set-title">{e(s["titulo"])}</p>'
            f'<iframe src="{e(src)}" title="{e(s["titulo"])} en SoundCloud" loading="lazy" allow="autoplay" height="166"></iframe></div>')


def profile(dj):
    slug = dj["slug"]
    base = f"/assets/djs/{slug}/"
    url = f"{SITE}/djs/{slug}/"
    og = f"{SITE}{base}og.jpg" if os.path.exists(os.path.join(ROOT, f"assets/djs/{slug}/og.jpg")) else f"{SITE}/og-image.jpg?v=2"
    title = f"{dj['nombre']} · DJ en {dj['ciudad'].split(',')[0]} | Demetrio Entertainment"
    desc = f"{dj['nombre']}: {', '.join(dj['generos'][:3])}. {dj['tagline']} Contrátalo para tu evento con Demetrio Entertainment."
    chips = "".join(f"<span>{e(g)}</span>" for g in dj["generos"])
    datos = "".join(f'<div><dt>{e(d["texto"])}</dt><dd>{e(d["valor"])}</dd></div>' for d in dj["datos"])
    bio = "".join(f"<p>{e(p)}</p>" for p in dj["bio"])
    bio_en = "".join(f"<p>{e(p)}</p>" for p in dj["bio_en"])
    stage = "".join(f"<li>{e(a)}</li>" for a in dj["escenario"])
    sets = "".join(embed(s) for s in dj["sets"])
    gal = "".join(f'<a href="{base}{e(g)}" class="gal-item"><img src="{base}{e(g)}" alt="{e(dj["nombre"])} en cabina, foto {i+1}" loading="lazy"></a>'
                  for i, g in enumerate(dj["galeria"]))
    eventos = "".join(f"<span>{e(x)}</span>" for x in dj["eventos"])
    ciudades = "".join(f"<span>{e(x)}</span>" for x in dj["ciudades"])
    rider = "".join(f'<div><h3>{e(r["titulo"])}</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in r["items"])}</ul></div>' for r in dj["rider"])
    redes = "".join(f'<a class="btn btn-ghost btn-sm" href="{e(r["url"])}">{e(r["nombre"])}</a>' for r in dj["redes"])
    opts_ev = "".join(f"<option>{e(x)}</option>" for x in dj["eventos"])

    return head(title, desc, url, og) + header("#contratar", f"Contratar a {dj['nombre']}") + f"""
<main>
<section class="dj-hero">
  <div class="wrap dj-hero-grid">
    <div>
      <nav class="crumbs" aria-label="Ruta"><a href="/djs/">DJs</a><span aria-hidden="true">/</span><span>{e(dj['nombre'])}</span></nav>
      <p class="cue"><b>DJ</b> {e(dj['ciudad'])}</p>
      <h1 class="dj-name">{e(dj['nombre'])}</h1>
      <p class="lead">{e(dj['tagline'])}</p>
      <div class="tags dj-genres">{chips}</div>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="#contratar">Contratar a {e(dj['nombre'])} {ARROW}</a>
        <a class="btn btn-ghost" href="#escuchar">Escuchar sets</a>
      </div>
    </div>
    <div class="dj-portrait"><img src="{base}{e(dj['imagen_retrato'])}" alt="{e(dj['nombre'])} tocando en cabina" width="960" height="1280"></div>
  </div>
  <div class="wrap"><dl class="dj-facts">{datos}</dl></div>
</section>

<section id="escuchar" class="dj-sec">
  <div class="wrap">
    <p class="cue"><b>Escúchalo</b> Sets</p>
    <h2 class="h2" style="margin-top:20px">Dale play antes de contratar</h2>
    <div class="sets">{sets}</div>
  </div>
</section>

<section class="dj-sec dj-band">
  <div class="wrap dj-two">
    <div>
      <p class="cue"><b>Bio</b> Trayectoria</p>
      <div class="dj-bio">{bio}</div>
      <details class="dj-en"><summary>Read in English</summary>{bio_en}</details>
    </div>
    <div>
      <p class="cue"><b>Escenario</b> Ha compartido cabina con</p>
      <ul class="stage">{stage}</ul>
    </div>
  </div>
</section>

<section class="dj-sec">
  <div class="wrap">
    <p class="cue"><b>Galería</b> En cabina</p>
    <div class="gallery">{gal}</div>
  </div>
</section>

<section class="dj-sec dj-band">
  <div class="wrap dj-three">
    <div><p class="cue"><b>Eventos</b> Para qué contratarlo</p><div class="tags">{eventos}</div></div>
    <div><p class="cue"><b>Plazas</b> Se ha presentado en</p><div class="tags">{ciudades}</div></div>
    <div><p class="cue"><b>Rider</b> Técnico</p><div class="rider">{rider}</div></div>
  </div>
  <div class="wrap"><div class="dj-social">{redes}</div></div>
</section>

<section class="quote" id="contratar">
  <div class="wrap quote-grid">
    <div>
      <p class="cue"><b>Booking</b> Vía Demetrio Entertainment</p>
      <h2 class="h2" style="margin-top:20px">Contrata a {e(dj['nombre'])} para tu evento</h2>
      <p class="lead" style="margin-top:20px">Cuéntanos la fecha y el tipo de evento. Revisamos disponibilidad y te mandamos propuesta con equipo, horario y costo.</p>
      <div class="direct">
        <span>¿Prefieres escribir directo?</span>
        <div>WhatsApp: <a href="https://wa.me/{WHATSAPP}">624 245 4573</a></div>
      </div>
    </div>
    <form class="wizard" id="booking" novalidate>
      <div class="fields">
        <div class="field"><label for="b-fecha">Fecha del evento</label><input id="b-fecha" name="fecha" type="text" placeholder="Ej. 14 de febrero 2027"></div>
        <div class="field"><label for="b-ciudad">Ciudad</label><select id="b-ciudad" name="ciudad"><option>Los Cabos</option><option>La Paz</option><option>Otra ciudad</option></select></div>
        <div class="field"><label for="b-tipo">Tipo de evento</label><select id="b-tipo" name="tipo">{opts_ev}</select></div>
        <div class="field"><label for="b-horas">Horas de set</label><select id="b-horas" name="horas"><option>2 horas</option><option>3 horas</option><option>4 horas</option><option>5 horas o más</option></select></div>
        <div class="field"><label for="b-nombre">Tu nombre</label><input id="b-nombre" name="nombre" type="text" autocomplete="name"></div>
        <div class="field"><label for="b-tel">Tu WhatsApp</label><input id="b-tel" name="tel" type="tel" autocomplete="tel" placeholder="624 000 0000"></div>
        <div class="field full"><label for="b-det">Detalles</label><textarea id="b-det" name="det" placeholder="Venue, número de invitados, si ya hay equipo de audio…"></textarea></div>
      </div>
      <p class="err" id="bErr" role="alert"></p>
      <div class="nav-steps"><button type="submit" class="btn btn-primary" style="margin-left:auto">Preparar mensaje</button></div>
      <div id="bDone" hidden>
        <div class="summary" id="bSum"></div>
        <div class="done-actions"><a class="btn btn-primary" id="bWa" href="#">Enviar por WhatsApp</a></div>
      </div>
    </form>
  </div>
</section>
</main>
""" + FOOTER + BASE_JS + f"""<script>
(function(){{
  var f = document.getElementById('booking'), err = document.getElementById('bErr');
  function v(n){{ return (f.elements[n].value || '').trim(); }}
  f.addEventListener('submit', function(ev){{
    ev.preventDefault();
    if(!v('nombre') || !v('tel')){{ err.textContent = 'Escribe tu nombre y tu WhatsApp para que podamos responderte.'; return; }}
    err.textContent = '';
    var m = ['Hola Demetrio, quiero contratar a {e(dj["nombre"])}.', '',
      'Fecha: ' + (v('fecha') || 'por definir'), 'Ciudad: ' + v('ciudad'), 'Tipo de evento: ' + v('tipo'),
      'Horas de set: ' + v('horas'), 'Detalles: ' + (v('det') || '—'), '', 'Nombre: ' + v('nombre'), 'WhatsApp: ' + v('tel')].join('\\n');
    document.getElementById('bSum').textContent = m;
    document.getElementById('bWa').href = 'https://wa.me/{WHATSAPP}?text=' + encodeURIComponent(m);
    document.getElementById('bDone').hidden = false;
  }});
}})();
</script>
</body>
</html>
"""


def roster(djs):
    url = f"{SITE}/djs/"
    cards = "".join(f"""
      <a class="dj-card" href="/djs/{e(d['slug'])}/">
        <div class="dj-card-img"><img src="/assets/djs/{e(d['slug'])}/{e(d['imagen_card'])}" alt="{e(d['nombre'])}" loading="lazy"></div>
        <div class="dj-card-body">
          <h3>{e(d['nombre'])}</h3>
          <p>{e(' · '.join(d['generos'][:3]))}</p>
          <span class="type-cta">Ver perfil {ARROW}</span>
        </div>
      </a>""" for d in djs)
    return head("DJs para tu evento en Los Cabos y La Paz | Demetrio Entertainment",
                "Roster de DJs de Demetrio Entertainment para bodas, beach clubs, eventos privados, corporativos y festivales en Los Cabos, La Paz y todo México.",
                url, f"{SITE}/og-image.jpg?v=2") + header("/#cotiza", "Cotiza tu evento") + f"""
<main>
<section class="dj-hero">
  <div class="wrap">
    <p class="cue"><b>Roster</b> DJs</p>
    <h1 class="dj-name" style="margin-top:24px">DJs para tu evento</h1>
    <p class="lead" style="margin-top:24px">Una selección de DJs con los que trabajamos. Escucha sus sets, revisa su trayectoria y contrátalos para bodas, beach clubs, eventos privados, corporativos y festivales. Nosotros coordinamos la fecha, el equipo y la logística.</p>
  </div>
</section>
<section class="dj-sec" style="padding-top:0">
  <div class="wrap">
    <div class="dj-grid">{cards}
      <div class="dj-card dj-card-empty">
        <h3>¿Eres DJ?</h3>
        <p>Buscamos DJs con trayectoria para nuestro roster. Mándanos tus sets y tu media kit.</p>
        <a class="btn btn-ghost btn-sm" href="https://wa.me/{WHATSAPP}?text={quote('Hola Demetrio, soy DJ y me gustaría estar en su roster.')}">Escríbenos</a>
      </div>
    </div>
  </div>
</section>
</main>
""" + FOOTER + BASE_JS + "</body>\n</html>\n"


def main():
    djs = json.load(open(os.path.join(ROOT, "data/djs.json"), encoding="utf-8"))
    os.makedirs(os.path.join(ROOT, "djs"), exist_ok=True)
    open(os.path.join(ROOT, "djs/index.html"), "w", encoding="utf-8").write(roster(djs))
    for dj in djs:
        d = os.path.join(ROOT, "djs", dj["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(profile(dj))
    urls = [f"{SITE}/", f"{SITE}/djs/"] + [f"{SITE}/djs/{d['slug']}/" for d in djs]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"{len(djs)} DJ(s) generados")


if __name__ == "__main__":
    main()
