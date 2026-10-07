#!/usr/bin/env python3
"""Builds the static site from products.json.

    python3 build.py

Writes index.html, software/index.html, software/<slug>/index.html, litwell/index.html
(redirect for the first link that was shared), and 404.html. Commit the output; GitHub
Pages serves the files as they are. To add a program, add an entry to products.json
(copy the Litwell one) and run this again.
"""
import datetime
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))
SITE = DATA["site"]
PRODUCTS = DATA["products"]
YEAR = datetime.date.today().year
e = html.escape


def page(title, body, *, path, desc="", current="", extra_head=""):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == current else ""}>{label}</a>'
        for key, href, label in (("home", "/", "Home"), ("software", "/software/", "Software"))
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc or SITE['lede'])}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<script>try{{var t=localStorage.getItem("theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/style.css">
{extra_head}</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/">{e(SITE['name'])}</a>
  <div class="right">
    <nav aria-label="Main">{nav}</nav>
    <button class="theme" type="button" hidden>Dark</button>
  </div>
</div></header>
{body}
<footer><div class="wrap">
  <span>&copy; {YEAR} {e(SITE['name'])}</span>
  <span>Software is provided as-is, without warranty.</span>
</div></footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def card(p):
    return f"""<article class="card">
  <img src="{p['icon']}" alt="" width="72" height="72">
  <div>
    <h3><a href="/software/{p['slug']}/">{e(p['name'])}</a></h3>
    <p>{e(p['tagline'])}</p>
    <div class="meta"><span data-version-repo="{p['repo']}">Latest version</span> &middot; {e(p['platforms'])}</div>
  </div>
  <a class="btn ghost go" href="/software/{p['slug']}/">Details</a>
</article>"""


def home():
    cards = "\n".join(card(p) for p in PRODUCTS)
    body = f"""<main>
<section class="hero"><div class="wrap">
  <p class="eyebrow">{e(SITE['title'])}</p>
  <h1>{e(SITE['headline'])}</h1>
  <p class="lede">{e(SITE['lede'])}</p>
  <a class="btn" href="/software/">Browse software</a>
</div></section>

<section class="wrap block">
  <h2 class="sec">Available now <a href="/software/">All software</a></h2>
  <div class="cards">
{cards}
  </div>
</section>

<section class="wrap block" style="padding-bottom:64px">
  <h2 class="sec">How downloads work</h2>
  <ol class="steps">
    <li><strong>Choose a program</strong><p>Each program has a page that explains what it does and what it needs before you download.</p></li>
    <li><strong>Download for your computer</strong><p>One file for Windows, one for Mac. The page shows the current version number.</p></li>
    <li><strong>Open it</strong><p>The programs are not signed with a paid certificate, so your computer asks you to confirm once. Each page shows exactly where to click.</p></li>
  </ol>
</section>
</main>"""
    return page(f"{SITE['name']} — {SITE['title']}", body, path="index.html", current="home")


def catalog():
    cards = "\n".join(card(p) for p in PRODUCTS)
    body = f"""<main>
<section class="pagehead"><div class="wrap">
  <p class="crumb"><a href="/">Home</a> / Software</p>
  <h1>Software</h1>
  <p class="lede">Programs available to download. More will be added here as they are ready.</p>
</div></section>
<section class="wrap block" style="padding-top:40px;padding-bottom:64px">
  <div class="cards">
{cards}
  </div>
</section>
</main>"""
    return page(f"Software — {SITE['name']}", body, path="software/index.html", current="software")


def product(p):
    feats = "".join(f"<li>{e(x)}</li>" for x in p["features"])
    paras = "".join(f"<p>{e(x)}</p>" for x in p["summary"])
    rows = "".join(
        f"<tr><td><strong>{e(a)}</strong></td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in p["sources"]
    )
    setup = ""
    if p.get("patent_setup"):
        u = "".join(f"<li>{x}</li>" for x in p["patent_setup"]["uspto"])
        o = "".join(f"<li>{x}</li>" for x in p["patent_setup"]["epo"])
        setup = f"""<h2 class="sub" id="patents">Setting up patent search</h2>
<p>The two patent sources are free, but each patent office asks you to identify yourself with a key. It is a one-time step of a few minutes. The other six sources need nothing.</p>
<div class="two">
  <div><h3>USPTO (US patents)</h3><ol class="num">{u}</ol></div>
  <div><h3>EPO (worldwide patents)</h3><ol class="num">{o}</ol></div>
</div>"""
    base = f"https://github.com/{p['repo']}/releases/latest/download"
    body = f"""<main>
<section class="pagehead product"><div class="wrap">
  <img src="{p['icon']}" alt="{e(p['name'])} icon" width="96" height="96">
  <div>
    <p class="crumb"><a href="/">Home</a> / <a href="/software/">Software</a> / {e(p['name'])}</p>
    <h1>{e(p['name'])}</h1>
    <p class="lede" style="margin-top:12px">{e(p['tagline'])}</p>
  </div>
</div></section>

<div class="wrap cols">
<article>
  <h2 class="sub" style="margin-top:0;border-top:0;padding-top:0">What it does</h2>
  {paras}
  <ul class="plain">{feats}</ul>

  <h2 class="sub">Where it searches</h2>
  <table>
    <thead><tr><th>Source</th><th>Covers</th><th>Key needed</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>

  {setup}

  <h2 class="sub" id="first-run">The first time you open it</h2>
  <p>The program is not signed with a paid developer certificate, so your computer asks you to confirm once. After that it opens normally.</p>
  <div class="two">
    <div><h3>Windows</h3><ol class="num">
      <li>Download the file and open it.</li>
      <li>If you see <em>Windows protected your PC</em>, click <strong>More info</strong>, then <strong>Run anyway</strong>.</li>
    </ol></div>
    <div><h3>Mac</h3><ol class="num">
      <li>Download the zip and double-click it to unpack it.</li>
      <li>Drag the app to Applications and open it.</li>
      <li>If macOS says it cannot check the app, open <strong>System Settings → Privacy &amp; Security</strong>, scroll down and click <strong>Open Anyway</strong>. On older versions of macOS, right-click the app and choose <strong>Open</strong>.</li>
    </ol></div>
  </div>

  <h2 class="sub">Privacy</h2>
  <p>{e(p['privacy'])}</p>
</article>

<aside class="dl" data-has-os aria-labelledby="dlh">
  <h2 id="dlh">Download</h2>
  <div class="meta"><span data-version-repo="{p['repo']}">Latest version</span></div>
  <div class="meta yours" aria-live="polite"></div>
  <a class="btn full" data-os="win" href="{base}/{p['windows_asset']}">Windows</a>
  <a class="btn full ghost" data-os="mac" href="{base}/{p['mac_asset']}">Mac</a>
  <ul>
    <li><b>Windows</b> 10 or 11, 64-bit. One file, no installer.</li>
    <li><b>Mac</b> Apple silicon or Intel. Zip containing the app.</li>
    <li><b>Cost</b> Free.</li>
    <li><a href="https://github.com/{p['repo']}/releases">All versions</a></li>
  </ul>
</aside>
</div>
</main>"""
    return page(f"{p['name']} — {SITE['name']}", body, path=f"software/{p['slug']}/index.html",
                desc=p["tagline"], current="software")


def redirect(to):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Moved</title>
<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{to}">
</head><body><p>This page has moved to <a href="{to}">{to}</a>.</p></body></html>
"""


def not_found():
    body = """<main><section class="pagehead"><div class="wrap">
  <p class="crumb">Error 404</p><h1>Page not found</h1>
  <p class="lede">That page does not exist. Try the <a href="/software/">software list</a> or the <a href="/">home page</a>.</p>
</div></section></main>"""
    return page(f"Not found — {SITE['name']}", body, path="404.html")


def write(rel, text):
    f = ROOT / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")
    print("wrote", rel)


write("index.html", home())
write("software/index.html", catalog())
for p in PRODUCTS:
    write(f"software/{p['slug']}/index.html", product(p))
    write(f"{p['slug']}/index.html", redirect(f"/software/{p['slug']}/"))  # keeps old /<slug>/ links alive
write("404.html", not_found())
