#!/usr/bin/env python3
"""Generator podpisów e-mail M2 TAX.

Uruchom:  python3 tools/podpisy.py
Tworzy:   podpis/index.html          – strona z podglądem i przyciskiem „Kopiuj podpis”
          podpis/<osoba>.htm          – plik podpisu do folderu Signatures w Outlooku (Windows)
Logo leżą w podpis/ i są ładowane z https://www.m2tax.pl/podpis/…
"""
from pathlib import Path
import html

BASE = "https://www.m2tax.pl/podpis/"
SITE = "https://www.m2tax.pl"
BOOKING = "https://m2taxdoradcypodatkowi.zohobookings.eu/m2taxdoradcypodatkowi"

INK = "#1c1d21"
MUTED = "#6b6e76"
ACCENT = "#7A5A37"
LINE = "#D9B98E"
FONT = "Arial, Helvetica, sans-serif"

PEOPLE = [
    dict(slug="marcin-otreba", name="Marcin Otręba", role="Doradca podatkowy", role2="Partner zarządzający",
         wpis="nr wpisu 14609", phone="534 909 534", email="marcin.otreba@m2tax.pl", client="Outlook (Windows)", photo=True),
    dict(slug="michal-ruszniak", name="Michał Ruszniak", role="Doradca podatkowy", role2="Partner zarządzający",
         wpis="nr wpisu 15009", phone="883 643 565", email="michal.ruszniak@m2tax.pl", client="Gmail"),
    dict(slug="filip-ditrejnowski", name="Filip Ditrejnowski", role="Konsultant podatkowy", role2="",
         wpis="", phone="", email="filip.ditrejnowski@m2tax.pl", client="Gmail", photo=True),
]


def row(label, value, href):
    return (
        f'<tr><td style="padding:0 10px 3px 0;font-family:{FONT};font-size:12px;line-height:18px;'
        f'color:{ACCENT};font-weight:bold;width:14px;">{label}</td>'
        f'<td style="padding:0 0 3px 0;font-family:{FONT};font-size:13px;line-height:18px;">'
        f'<a href="{href}" style="color:{INK};text-decoration:none;">{value}</a></td></tr>'
    )


def signature(p, photo=False):
    e = html.escape
    title = e(p["role"]) + (f' <span style="color:{LINE};">|</span> {e(p["role2"])}' if p["role2"] else "")
    wpis = (f'<div style="font-family:{FONT};font-size:11px;line-height:16px;color:{MUTED};'
            f'letter-spacing:.3px;">{e(p["wpis"])}</div>') if p["wpis"] else ""
    contacts = ""
    if p["phone"]:
        contacts += row("T", e(p["phone"]), "tel:+48" + p["phone"].replace(" ", ""))
    contacts += row("E", e(p["email"]), "mailto:" + p["email"])
    contacts += row("W", "www.m2tax.pl", SITE)

    logo_img = f'<a href="{SITE}" style="text-decoration:none;"><img src="{BASE}m2tax-logo.png" width="{{w}}" height="{{h}}" alt="M2 TAX Doradcy Podatkowi" style="display:block;margin:0 auto;width:{{w}}px;height:{{h}}px;border:0;"></a>'
    if photo:
        left = (f'<td valign="middle" align="center" style="padding:0 18px 0 0;width:150px;text-align:center;vertical-align:middle;">'
                f'<img src="{BASE}{p["slug"]}.png" width="96" height="96" alt="{e(p["name"])}" style="display:block;margin:0 auto;width:96px;height:96px;border:0;">'
                f'<div style="height:12px;line-height:12px;font-size:1px;">&nbsp;</div>'
                + logo_img.format(w=120, h=40) + '</td>')
    else:
        left = (f'<td valign="middle" align="center" style="padding:0 18px 0 0;width:150px;text-align:center;vertical-align:middle;">'
                + logo_img.format(w=150, h=50) + '</td>')
    return f"""<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;font-family:{FONT};color:{INK};max-width:560px;">
<tr>
<td colspan="2" style="padding:0 0 14px 0;font-family:Arial, Helvetica, sans-serif;font-size:13px;line-height:18px;color:#222222;font-weight:normal;">Pozdrawiam serdecznie,</td>
</tr>
<tr>
{left}
<td valign="top" style="padding:0 0 0 18px;border-left:2px solid {LINE};">
<div style="font-family:{FONT};font-size:17px;line-height:22px;font-weight:bold;color:{INK};">{e(p['name'])}</div>
<div style="font-family:{FONT};font-size:13px;line-height:19px;font-weight:bold;color:{ACCENT};padding-top:2px;">{title}</div>
{wpis}
<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;margin-top:10px;">
{contacts}
</table>
<div style="padding-top:8px;font-family:{FONT};font-size:12px;line-height:18px;">
<a href="{BOOKING}" style="color:{ACCENT};font-weight:bold;text-decoration:none;">Umów konsultację &rarr;</a>
</div>
</td>
</tr>
<tr>
<td colspan="2" style="padding:16px 0 0 0;">
<div style="border-top:1px solid #e3e2de;padding-top:10px;font-family:{FONT};font-size:10px;line-height:14px;color:#9a9ca2;">
Wiadomość może zawierać informacje objęte tajemnicą doradcy podatkowego. Jeżeli nie jest Pan/Pani jej adresatem, prosimy o poinformowanie nadawcy i usunięcie wiadomości. Informacje o przetwarzaniu danych osobowych: <a href="{SITE}/polityka-prywatnosci.html" style="color:#9a9ca2;text-decoration:underline;">m2tax.pl/polityka-prywatnosci</a>.<br><br>
M2 TAX Doradcy Podatkowi Otręba Ruszniak spółka partnerska, ul. Zwycięska 3, 53-033 Wrocław, KRS 0001238577, NIP 8993058189, REGON 54465563600000.
</div>
</td>
</tr>
</table>"""


GUIDE_GMAIL = """<ol>
<li>Kliknij <b>Kopiuj podpis</b> powyżej.</li>
<li>W Gmailu: koło zębate → <b>Zobacz wszystkie ustawienia</b> → karta <b>Ogólne</b> → sekcja <b>Podpis</b>.</li>
<li><b>Utwórz nowy</b> (np. „M2 TAX”), kliknij w pole i wklej <b>Ctrl+V</b> (Mac: Cmd+V).</li>
<li>Poniżej ustaw ten podpis w <b>Dla nowych e-maili</b> i <b>Przy odpowiadaniu/przekazywaniu</b>.</li>
<li>Przewiń na dół i kliknij <b>Zapisz zmiany</b>.</li>
</ol>
<p class="note">Jeśli konto m2tax.pl jest dodane w Gmailu jako alias „Wyślij jako”, wybierz ten podpis właśnie dla adresu @m2tax.pl.</p>"""

GUIDE_OUTLOOK = """<p><b>Sposób 1 – wklejenie (najprostszy)</b></p>
<ol>
<li>Kliknij <b>Kopiuj podpis</b> powyżej.</li>
<li>W Outlooku: <b>Plik → Opcje → Poczta → Podpisy…</b> (w nowym Outlooku: koło zębate → Konta → Podpisy).</li>
<li><b>Nowy</b>, nazwij „M2 TAX”, kliknij w pole edycji i wklej <b>Ctrl+V</b>.</li>
<li>Po prawej wybierz konto marcin.otreba@m2tax.pl i ustaw podpis dla <b>nowych wiadomości</b> oraz <b>odpowiedzi/przekazywania</b>. <b>OK</b>.</li>
</ol>
<p><b>Sposób 2 – plik (gdyby wklejony podpis się rozjeżdżał, tylko klasyczny Outlook)</b></p>
<ol>
<li>Pobierz plik <a href="marcin-otreba.htm" download>marcin-otreba.htm</a> (wersja ze zdjęciem: <a href="marcin-otreba-zdjecie.htm" download>marcin-otreba-zdjecie.htm</a>).</li>
<li>Naciśnij <b>Win+R</b>, wpisz <code>%APPDATA%\\Microsoft\\Signatures</code> i Enter.</li>
<li>Skopiuj pobrany plik do tego folderu i uruchom Outlooka ponownie.</li>
<li>W <b>Plik → Opcje → Poczta → Podpisy</b> pojawi się podpis „marcin-otreba” – ustaw go jako domyślny.</li>
</ol>"""


def page():
    cards = ""
    for p in PEOPLE:
        guide = GUIDE_OUTLOOK if p["client"].startswith("Outlook") else GUIDE_GMAIL
        alt = ""
        if p.get("photo"):
            alt = f"""
  <h3 class="alt">Wersja ze zdjęciem</h3>
  <div class="sig" id="sig-{p['slug']}-zdjecie">{signature(p, photo=True)}</div>
  <div class="actions">
    <button class="btn" data-target="sig-{p['slug']}-zdjecie">Kopiuj podpis ze zdjęciem</button>
    <span class="ok" aria-live="polite"></span>
  </div>"""
        cards += f"""
<section class="card">
  <header><h2>{html.escape(p['name'])}</h2><span class="chip">{p['client']}</span></header>
  <div class="sig" id="sig-{p['slug']}">{signature(p)}</div>
  <div class="actions">
    <button class="btn" data-target="sig-{p['slug']}">Kopiuj podpis</button>
    <span class="ok" aria-live="polite"></span>
  </div>
{alt}
  <details><summary>Jak wstawić w {p['client']}</summary>{guide}</details>
</section>"""
    return f"""<!doctype html>
<html lang="pl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Podpisy e-mail M2 TAX</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#16171a;--text:#1c1d21;--muted:#5d6068;--line:#e3e2de;--paper-2:#f4f4f2;--accent:#7A5A37;--accent-deep:#5C4228;--gold:#D9B98E}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper-2);color:var(--text);font-family:"Source Sans 3","Segoe UI",Arial,sans-serif;font-size:17px;line-height:1.55}}
.top{{background:var(--ink);color:#f2f1ee;padding:28px 16px}}
.top .wrap,main{{max-width:760px;margin:0 auto}}
.top img{{height:40px;background:#fff;padding:6px 10px;border-radius:6px}}
h1{{font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:28px;margin:18px 0 6px}}
.top p{{margin:0;color:#a6a8ae}}
main{{padding:24px 16px 60px;display:grid;gap:22px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px}}
.card header{{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:18px}}
h2{{font-family:Montserrat,Arial,sans-serif;font-size:19px;margin:0}}
.chip{{font-size:13px;font-weight:700;color:var(--accent);background:#F0E9DE;border-radius:20px;padding:3px 12px;white-space:nowrap}}
.sig{{border:1px dashed var(--line);border-radius:8px;padding:20px;background:#fff;overflow-x:auto}}
.actions{{display:flex;align-items:center;gap:14px;margin-top:16px}}
.btn{{font-family:Montserrat,Arial,sans-serif;font-weight:700;font-size:15px;background:var(--accent);color:#F8F5F0;border:0;border-radius:6px;padding:12px 22px;cursor:pointer}}
.btn:hover{{background:var(--accent-deep)}}
.ok{{color:#2f7a3f;font-weight:600;font-size:15px}}
details{{margin-top:16px;border-top:1px solid var(--line);padding-top:12px}}
summary{{cursor:pointer;font-weight:700;color:var(--accent)}}
details ol{{padding-left:22px;margin:8px 0}}
details li{{margin:4px 0}}
code{{background:var(--paper-2);padding:1px 6px;border-radius:4px;font-size:15px}}
h3.alt{{font-family:Montserrat,Arial,sans-serif;font-size:15px;color:var(--muted);margin:26px 0 10px;text-transform:uppercase;letter-spacing:.08em}}
.note{{font-size:15px;color:var(--muted)}}
</style></head>
<body>
<div class="top"><div class="wrap">
<img src="m2tax-logo.png" alt="M2 TAX">
<h1>Podpisy e-mail</h1>
<p>Strona wewnętrzna. Kliknij „Kopiuj podpis” przy swoim nazwisku i wklej w ustawieniach poczty.</p>
</div></div>
<main>{cards}
</main>
<script>
document.querySelectorAll('.btn[data-target]').forEach(b=>b.addEventListener('click',()=>{{
  const el=document.getElementById(b.dataset.target), ok=b.nextElementSibling;
  const r=document.createRange(); r.selectNodeContents(el);
  const s=window.getSelection(); s.removeAllRanges(); s.addRange(r);
  let done=false; try{{done=document.execCommand('copy')}}catch(e){{}}
  s.removeAllRanges();
  ok.textContent=done?'Skopiowano — teraz wklej (Ctrl+V)':'Zaznacz podpis myszką i skopiuj Ctrl+C';
  setTimeout(()=>ok.textContent='',5000);
}}));
</script>
</body></html>
"""


def outlook_file(p, photo=False):
    return f"""<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>{html.escape(p['name'])}</title></head>
<body style="margin:0;">
{signature(p, photo)}
</body></html>
"""


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "podpis"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page(), encoding="utf-8")
    for p in PEOPLE:
        (out / f"{p['slug']}.htm").write_text(outlook_file(p), encoding="utf-8")
        if p.get("photo"):
            (out / f"{p['slug']}-zdjecie.htm").write_text(outlook_file(p, True), encoding="utf-8")
    print("OK:", out)
