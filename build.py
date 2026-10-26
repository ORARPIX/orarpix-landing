"""Genera las páginas del sitio de Orarpix (español e inglés) con la cabecera y el pie comunes.

Los textos de cada página están en src/. Para regenerar: python3 build.py
"""
import pathlib

SITE = pathlib.Path(__file__).parent
SRC = SITE / "src"

UI = {
    "es": dict(skip="Saltar al contenido", home_label="Orarpix, inicio", nav_main="Principal",
               story="Historia", games="Juegos", contact="Contacto", privacy="Privacidad", support="Soporte",
               f_privacy="Política de privacidad", f_terms="Términos", f_support="Soporte",
               legal="Legal", made="Hecho en Colombia.", other="English", other_lang="en"),
    "en": dict(skip="Skip to content", home_label="Orarpix, home", nav_main="Main",
               story="Story", games="Games", contact="Contact", privacy="Privacy", support="Support",
               f_privacy="Privacy policy", f_terms="Terms", f_support="Support",
               legal="Legal", made="Made in Colombia.", other="Español", other_lang="es"),
}

# (sección, idioma, título, descripción, cuerpo); sección "" es la portada.
PAGES = [
    ("", "es", "Orarpix · Estudio independiente de juegos",
     "Estudio independiente de juegos en Colombia. Primero Android, pronto iOS y después Steam.",
     "home.es.html"),
    ("", "en", "Orarpix · Independent game studio",
     "Independent game studio in Colombia. Android first, iOS soon and Steam after that.",
     "home.en.html"),
    ("privacy", "es", "Política de privacidad · Orarpix",
     "Política de privacidad de Orarpix y de Transit Chaos: Bus Jam 3D.", "privacy.es.html"),
    ("privacy", "en", "Privacy policy · Orarpix",
     "Privacy policy for Orarpix and Transit Chaos: Bus Jam 3D.", "privacy.en.html"),
    ("terms", "es", "Términos y condiciones · Orarpix",
     "Términos y condiciones de uso de los juegos de Orarpix.", "terms.es.html"),
    ("terms", "en", "Terms of service · Orarpix",
     "Terms of service for Orarpix games.", "terms.en.html"),
    ("support", "es", "Soporte · Orarpix",
     "Ayuda y soporte para los juegos de Orarpix.", "support.es.html"),
    ("support", "en", "Support · Orarpix",
     "Help and support for Orarpix games.", "support.en.html"),
]

# Elige idioma: el que el visitante eligió con el selector; si no, el primero entre español e
# inglés que prefiera su navegador; si no prefiere ninguno de los dos, inglés. Las anclas que
# cambian de nombre entre idiomas se traducen al redirigir.
LANG_SCRIPT = """  <script>(function(){var p="{lang}",o="{other_href}",w;try{w=localStorage.getItem("orarpix-lang")}catch(e){}if(w!=="es"&&w!=="en"){w="en";var l=navigator.languages||[navigator.language||""];for(var i=0;i<l.length;i++){var c=String(l[i]).toLowerCase().slice(0,2);if(c==="es"||c==="en"){w=c;break}}}if(w===p)return;var h=location.hash,m={"#borrado":"#deletion","#deletion":"#borrado","#consentimiento":"#consent","#consent":"#consentimiento"};location.replace(o+(m[h]||h))})();</script>
"""

TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{lang_script}  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#FFF4E0">
  <link rel="alternate" hreflang="es" href="https://orarpix.com/{es_url}">
  <link rel="alternate" hreflang="en" href="https://orarpix.com/{en_url}">
  <link rel="alternate" hreflang="x-default" href="https://orarpix.com/{en_url}">
{og}  <link rel="icon" type="image/svg+xml" href="{r}assets/img/orarpix-icono.svg">
  <link rel="apple-touch-icon" href="{r}assets/img/orarpix-icono-512.png">
  <link rel="stylesheet" href="{r}assets/css/styles.css">
</head>
<body>
  <a class="skip" href="#contenido">{skip}</a>
  <header class="top">
    <div class="wrap">
      <a class="marca" href="{home}" aria-label="{home_label}">
        <img src="{r}assets/img/orarpix-icono.svg" alt="" width="44" height="44">
        <span>Orarpix</span>
      </a>
      <nav aria-label="{nav_main}">
{nav}
        <a class="lang" href="{other_href}" hreflang="{other_lang}" lang="{other_lang}" onclick="try{{localStorage.setItem('orarpix-lang','{other_lang}')}}catch(e){{}}">{other}</a>
      </nav>
    </div>
  </header>

{main}

  <footer>
    <div class="wrap">
      <small>© <span id="anio">2026</span> Orarpix. {made}</small>
      <nav aria-label="{legal}">
        <a href="{r}privacy/{sub}">{f_privacy}</a>
        <a href="{r}terms/{sub}">{f_terms}</a>
        <a href="{r}support/{sub}">{f_support}</a>
      </nav>
    </div>
  </footer>
  <script>document.getElementById('anio').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

DOC_MAIN = """  <main id="contenido" class="doc">
    <div class="wrap">
      <div class="card">
        <article>
{body}
        </article>
      </div>
    </div>
  </main>"""

OG = """  <meta property="og:title" content="Orarpix">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://orarpix.com/assets/img/orarpix-icono-512.png">
  <meta property="og:url" content="https://orarpix.com/{url}">
"""

for section, lang, title, desc, body in PAGES:
    base = f"{section}/" if section else ""
    out = base + ("en/index.html" if lang == "en" else "index.html")
    r = "../" * out.count("/")
    ui = UI[lang]
    sub = "en/index.html" if lang == "en" else "index.html"
    home = r + sub
    other_href = "../index.html" if lang == "en" else "en/index.html"
    if section:
        nav = (f'        <a href="{home}#juegos">{ui["games"]}</a>\n'
               f'        <a href="{r}privacy/{sub}">{ui["privacy"]}</a>\n'
               f'        <a href="{r}support/{sub}">{ui["support"]}</a>')
        main = DOC_MAIN.format(body=(SRC / body).read_text().rstrip("\n"))
    else:
        nav = (f'        <a href="#historia">{ui["story"]}</a>\n'
               f'        <a href="#juegos">{ui["games"]}</a>\n'
               f'        <a href="#contacto">{ui["contact"]}</a>')
        main = (SRC / body).read_text().rstrip("\n").replace("{r}", r)
    url = base + ("en/" if lang == "en" else "")
    html = TEMPLATE.format(
        lang=lang, title=title, desc=desc, r=r, home=home, nav=nav, main=main, sub=sub,
        es_url=base, en_url=base + "en/", other_href=other_href,
        lang_script=LANG_SCRIPT.replace("{lang}", lang).replace("{other_href}", other_href),
        og=OG.format(desc=desc, url=url) if not section else "",
        **ui)
    dest = SITE / out
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print("escrito", out)
