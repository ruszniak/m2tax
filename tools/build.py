#!/usr/bin/env python3
"""Generator strony M2 TAX.

Buduje strony z jednego miejsca, żeby menu, stopka i nagłówek były wszędzie takie same:
  index.html, abonamenty/index.html, doradztwo-podatkowe/index.html, zespol/index.html, kontakt/index.html
Wspólne style: assets/site.css, wspólne skrypty: assets/site.js.

Uruchom z katalogu repozytorium:  python3 tools/build.py
Folder tools/ nie jest publikowany (.vercelignore).
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.m2tax.pl"
TEL1, TEL1_H = "+48883643565", "+48 883 643 565"
TEL2, TEL2_H = "+48534909534", "+48 534 909 534"
MAIL = "kancelaria@m2tax.pl"
# WhatsApp: numer w formacie międzynarodowym bez "+" i gotowa pierwsza wiadomość
WA_NUMBER = "48883643565"
WA_TEXT = "Dzień dobry, mam pytanie podatkowe: "
# Zoho SalesIQ (czat na stronie): wklej tu kod widżetu (parametr wc=... z kodu osadzenia
# w Zoho SalesIQ → Ustawienia → Kanały → Witryna → Instalacja). Pusty = czat wyłączony.
SALESIQ_WC = ""
SALESIQ_HOST = "https://salesiq.zohopublic.eu"
ZOHO_EMBED = "https://m2taxdoradcypodatkowi.zohobookings.eu/portal-embed#/m2taxdoradcypodatkowi"
ZOHO_PUBLIC = "https://m2taxdoradcypodatkowi.zohobookings.eu/#/m2taxdoradcypodatkowi"
TOWNS = [
    ("Wrocław", "kancelarie przy ul. Zwycięskiej 3 i ul. Artemskiej 11"),
    ("Siechnice", "gmina Siechnice"),
    ("Kobierzyce", "gmina Kobierzyce"),
    ("Żórawina", "gmina Żórawina"),
    ("Środa Śląska", "powiat średzki"),
    ("Trzebnica", "powiat trzebnicki"),
    ("Oleśnica", "powiat oleśnicki"),
    ("Oława", "powiat oławski"),
    ("Strzelin", "powiat strzeliński"),
    ("Jelcz-Laskowice", "powiat oławski"),
    ("Długołęka", "gmina Długołęka"),
    ("Kąty Wrocławskie", "gmina Kąty Wrocławskie"),
    ("Oborniki Śląskie", "powiat trzebnicki"),
    ("Brzeg", "powiat brzeski"),
    ("Kępno", "powiat kępiński"),
]
NAV = [("abonamenty/", "Abonamenty"), ("doradztwo-podatkowe/", "Doradztwo podatkowe"), ("dla-biur-rachunkowych/", "Dla biur rachunkowych"), ("zespol/", "Zespół"), ("blog/", "Blog"), ("kontakt/", "Kontakt")]

PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
ENVELOPE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'


# ---------------------------------------------------------------- szkielet
def head(p, title, desc, path, extra_ld=None):
    ld = {
        "@context": "https://schema.org", "@type": "AccountingService",
        "name": "M2 TAX Doradcy Podatkowi Otręba Ruszniak spółka partnerska",
        "url": SITE + "/", "telephone": [TEL1_H, TEL2_H], "email": MAIL,
        "image": SITE + "/img/og-image.jpg", "priceRange": "od 369 zł",
        "address": {"@type": "PostalAddress", "streetAddress": "ul. Zwycięska 3", "postalCode": "53-033",
                    "addressLocality": "Wrocław", "addressCountry": "PL"},
        "areaServed": [{"@type": "City", "name": t} for t, _ in TOWNS],
    }
    lds = [ld] + ([extra_ld] if extra_ld else [])
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="M2 TAX">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{p}img/logo.png">
''' + "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in lds) + f'''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{p}assets/site.css">
</head>
<body>
'''


def header(p, active):
    links = "\n".join(
        f'      <a href="{p}{href}"' + (' aria-current="page"' if href == active else "") + f'>{label}</a>'
        for href, label in NAV)
    return f'''
<header class="topbar">
  <div class="wrap">
    <a class="logo" href="{p or './'}" aria-label="M2 TAX Doradcy Podatkowi — strona główna"><img class="logo-l" src="{p}img/logo.png" alt="M2 TAX Doradcy Podatkowi" width="900" height="302"><img class="logo-d" src="{p}img/logo-light.png" alt="" width="900" height="302"></a>
    <button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Główna nawigacja">
{links}
      <a class="btn btn-primary" href="{p}kontakt/#rezerwacja">Bezpłatne 20 minut</a>
    </nav>
  </div>
</header>

<main id="top">
'''


def wa_link():
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUMBER}?text={quote(WA_TEXT)}"


def wa_button():
    cls = "fab-stack with-chat" if SALESIQ_WC else "fab-stack"
    return f'''<div class="{cls}">
<a class="fab tel-fab" href="tel:{TEL1}" aria-label="Zadzwoń: {TEL1_H}">
  <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path fill="currentColor" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.61 21 3 13.39 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2Z"/></svg>
  <span class="wa-label">Zadzwoń: {TEL1_H}</span>
</a>
<a class="fab wa-fab" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Napisz do nas na WhatsApp">
  <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.36 4 14.97c0 2.11.56 4.17 1.62 5.99L4 29l8.25-2.15a12.1 12.1 0 0 0 5.79 1.47h.01c6.63 0 12.03-5.36 12.03-11.97C28.07 8.36 22.67 3 16.04 3Zm0 21.98h-.01c-1.8 0-3.56-.48-5.1-1.39l-.37-.22-4.9 1.27 1.31-4.75-.24-.39a9.85 9.85 0 0 1-1.52-5.53c0-5.48 4.49-9.94 10.01-9.94 2.67 0 5.18 1.04 7.07 2.91a9.83 9.83 0 0 1 2.93 7.03c0 5.48-4.49 9.94-10 9.94Zm5.49-7.44c-.3-.15-1.78-.87-2.05-.97-.28-.1-.48-.15-.68.15-.2.3-.78.97-.95 1.17-.18.2-.35.22-.65.07-.3-.15-1.27-.46-2.42-1.48-.89-.79-1.5-1.77-1.67-2.07-.18-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.68-1.63-.93-2.23-.24-.58-.49-.5-.68-.51h-.58c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.48.71.31 1.27.49 1.7.63.71.23 1.36.2 1.88.12.57-.09 1.78-.72 2.03-1.42.25-.7.25-1.3.18-1.42-.08-.13-.28-.2-.58-.35Z"/></svg>
  <span class="wa-label">Napisz na WhatsApp</span>
</a>
</div>'''


def salesiq():
    if not SALESIQ_WC:
        return ""
    return f'''
<!-- Zoho SalesIQ: czat na żywo -->
<script>window.$zoho=window.$zoho||{{}};$zoho.salesiq=$zoho.salesiq||{{ready:function(){{}}}};</script>
<script id="zsiqscript" src="{SALESIQ_HOST}/widget?wc={SALESIQ_WC}" defer></script>'''


def footer(p, zoho=False):
    nav = "\n".join(f'        <li><a href="{p}{h}">{l}</a></li>' for h, l in NAV)
    towns = ", ".join(t for t, _ in TOWNS)
    z = ""
    if zoho:
        z = f'''
<!-- Zoho Bookings: kalendarz rezerwacji wbudowany w stronę -->
<script src="https://bookings.nimbuspop.com/assets/embed.js" defer></script>
<script>
window.addEventListener('load', function(){{
  var ZOHO_URL = '{ZOHO_EMBED}';
  var box = document.getElementById('inline-container'); if(!box) return;
  var h = window.innerWidth <= 820 ? '900px' : '760px';
  function done(){{ var l = box.querySelector('.zoho-loading'); if(l) l.remove(); }}
  try {{
    if (window.Bookings && typeof Bookings.inlineEmbed === 'function') {{
      Bookings.inlineEmbed({{ url: ZOHO_URL, parent: '#inline-container', height: h }});
      setTimeout(done, 400); return;
    }}
  }} catch(e) {{}}
  var f = document.createElement('iframe');
  f.title = 'Kalendarz rezerwacji M2 TAX'; f.src = ZOHO_URL; f.style.height = h; f.setAttribute('allowfullscreen','');
  f.addEventListener('load', done); box.appendChild(f);
}});
</script>'''
    return f'''</main>

<footer>
  <div class="wrap">
    <div class="f-brand">
      <a href="{p or './'}" class="f-logo" aria-label="M2 TAX Doradcy Podatkowi — strona główna"><img src="{p}img/logo-light.png" alt="M2 TAX Doradcy Podatkowi" width="900" height="302" loading="lazy"></a>
      <p>Kancelaria doradztwa podatkowego z Wrocławia. Obsługujemy klientów z Wrocławia i {len(TOWNS) - 1} okolicznych miejscowości. <a class="f-map" href="{p}#obszar">Zobacz mapę →</a></p>
      <a class="btn btn-primary" href="{p}kontakt/#rezerwacja">Bezpłatne 20 minut</a>
    </div>
    <div>
      <h4>Strony</h4>
      <ul>
        <li><a href="{p or './'}">Strona główna</a></li>
{nav}
      </ul>
    </div>
    <div>
      <h4>Kontakt</h4>
      <ul>
        <li><a href="tel:{TEL1}">{TEL1_H}</a></li>
        <li><a href="tel:{TEL2}">{TEL2_H}</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><a href="{wa_link()}" target="_blank" rel="noopener">Napisz na WhatsApp</a></li>
        <li>ul. Zwycięska 3, 53-033 Wrocław</li>
        <li>ul. Beaty Artemskiej 11/44, 52-234 Wrocław</li>
      </ul>
    </div>
    <div>
      <h4>Dane rejestrowe</h4>
      <p>M2 TAX DORADCY PODATKOWI<br>OTRĘBA RUSZNIAK<br>spółka partnerska</p>
      <p>ul. Zwycięska 3<br>53-033 Wrocław</p>
      <p>KRS: 0001238577<br>NIP: 8993058189<br>REGON: 54465563600000</p>
    </div>
    <div class="legal"><span>© 2026 M2 TAX. Wszelkie prawa zastrzeżone.</span><span><a href="{p}polityka-prywatnosci.html">Polityka prywatności</a> · <a href="{p}aml.html">Informacja AML</a></span><span>Wykonanie: <a href="https://ruszniak.io" target="_blank" rel="noopener">druslak</a></span></div>
  </div>
</footer>

<div class="toast" id="toast" hidden role="status"></div>
{wa_button()}
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="{p}assets/site.js" defer></script>{z}{salesiq()}
</body>
</html>
'''


def page_hero(p, crumb, eyebrow, h1, lede, fx="network", cta=True):
    c = f'''
      <div class="hero-cta">
        <a class="btn btn-primary" href="{p}kontakt/#rezerwacja">Umów bezpłatne 20 minut</a>
        <a class="btn btn-ghost" href="tel:{TEL1}">Zadzwoń: {TEL1_H}</a>
      </div>''' if cta else ""
    return f'''<section class="page-hero">
  <canvas class="fx3d" data-fx="{fx}" aria-hidden="true"></canvas>
  <div class="wrap">
    <p class="crumbs"><a href="{p}">Strona główna</a> / {crumb}</p>
    <h1 style="margin-top:22px">{h1}</h1>
    <p class="lede">{lede}</p>{c}
  </div>
</section>
'''


def section_head(eyebrow, h2, lede="", hid="", light=False):
    st = ' style="color:#fff"' if light else ""
    l = f'\n      <p class="lede">{lede}</p>' if lede else ""
    return f'''    <div class="section-head">
      <h2{f' id="{hid}"' if hid else ""}{st}>{h2}</h2>{l}
    </div>
'''


def cta_band(p, title, text):
    return f'''    <div class="cta-band">
      <div><h3>{title}</h3><p>{text}</p></div>
      <div class="hero-cta">
        <a class="btn btn-primary" href="{p}kontakt/#rezerwacja">Umów bezpłatne 20 minut</a>
        <a class="btn btn-ghost" href="tel:{TEL1}">{TEL1_H}</a>
      </div>
    </div>
'''


# ---------------------------------------------------------------- treści
SOLUTIONS = [
    ("01", "Stała obsługa podatkowa", "Abonament doradztwa podatkowego z dwoma doradcami pod telefonem. Trzy pakiety: od 2 godzin miesięcznie, także we współpracy z Twoją księgową lub biurem rachunkowym.", "od 369 zł", "netto miesięcznie · 2 h doradztwa", "abonamenty/#stala-obsluga", True),
    ("02", "Konsultacja indywidualna", "Jednorazowa rozmowa o konkretnej sprawie: sprzedaż nieruchomości, wypłata pieniędzy ze spółki, zmiana formy opodatkowania. Pierwsze 20 minut bez opłat.", "od 400 zł", "netto za godzinę", "abonamenty/#konsultacja", False),
    ("03", "Postępowania i kontrole", "Prowadzimy sprawę jako pełnomocnik od pierwszego pisma: czynności sprawdzające, kontrole podatkowe i celno-skarbowe, postępowania podatkowe i odwołania.", "wycena indywidualna", "po zapoznaniu się z pismami", "abonamenty/#postepowania", False),
    ("04", "Sprawy przed WSA i NSA", "Skargi do wojewódzkiego sądu administracyjnego, skargi kasacyjne do NSA i udział w rozprawach. Doradca podatkowy może Cię reprezentować przed sądami administracyjnymi.", "wycena indywidualna", "po analizie decyzji", "abonamenty/#sady", False),
]

BRANCHES = [
    ("PIT · VAT · PCC", "Osoby prywatne i nieruchomości",
     "Obsługa osób, które nie prowadzą działalności gospodarczej: sprzedaż mieszkania lub domu, podział i sprzedaż działek, najem prywatny, spadki i darowizny.",
     ["Sprzedaż nieruchomości przed upływem 5 lat i ulga mieszkaniowa", "Kiedy sprzedaż działek podlega VAT, a kiedy nie", "Najem prywatny, spadki, darowizny i zgłoszenia do urzędu"]),
    ("VAT · MPP · CIT/PIT", "Branża budowlana",
     "Generalni wykonawcy, podwykonawcy i deweloperzy. Dbamy o rozliczenia VAT na każdym etapie inwestycji i o bezpieczeństwo w relacjach z podwykonawcami.",
     ["Stawki VAT 8% i 23% w budownictwie mieszkaniowym", "Podzielona płatność i moment powstania obowiązku VAT", "Kaucje gwarancyjne, umowy z podwykonawcami, kontrole"]),
    ("VAT · ryczałt · spółki", "Branża medyczna",
     "Lekarze, dentyści, fizjoterapeuci, gabinety i podmioty lecznicze. Pomagamy oddzielić usługi zwolnione z VAT od opodatkowanych i dobrać formę działania.",
     ["Zwolnienie z VAT usług medycznych a zabiegi estetyczne", "Kontrakty B2B, ryczałt i spółki lekarskie", "Zmiany wspólników w spółkach i podmiotach leczniczych"]),
    ("VAT · kasa fiskalna · forma opodatkowania", "Branża beauty",
     "Salony kosmetyczne, fryzjerskie i gabinety kosmetologii. Porządkujemy VAT, sprzedaż kosmetyków i współpracę z osobami wynajmującymi stanowiska.",
     ["Limit zwolnienia z VAT i jego przekroczenie", "Sprzedaż usług i kosmetyków, kasa fiskalna online", "Najem stanowisk i współpraca na B2B bez ryzyka"]),
    ("CIT · ulgi · VAT 0%", "Branża produkcyjna",
     "Zakłady produkcyjne i firmy rodzinne z własnym parkiem maszynowym. Pomagamy korzystać z ulg i bezpiecznie rozliczać sprzedaż zagraniczną.",
     ["Ulga B+R, IP Box i ulga na prototyp", "Eksport i wewnątrzwspólnotowe dostawy ze stawką 0%", "Amortyzacja maszyn i inwestycji, ceny transferowe"]),
]

PILLARS = [
    ("art. 14b Ordynacji podatkowej", "Wnioski o interpretację indywidualną",
     "Interpretacja daje ochronę: jeśli zastosujesz się do niej, nie poniesiesz negatywnych skutków, nawet gdy organ później zmieni zdanie. Opis stanu faktycznego decyduje o wszystkim, więc piszemy go tak, żeby Dyrektor KIS odpowiedział na właściwe pytanie.",
     ["opłata 40 zł / zdarzenie", "3 miesiące na wydanie"],
     ["<b>Interpretacje indywidualne</b> w CIT, PIT, VAT, PCC i podatku od spadków i darowizn", "<b>Wiążące informacje stawkowe (WIS)</b> dla VAT", "<b>Opinie zabezpieczające</b> dla transakcji objętych klauzulą przeciwko unikaniu opodatkowania", "<b>Uzupełnienia wniosków</b> po wezwaniu KIS oraz skargi na interpretacje do WSA", "<b>Opinie podatkowe</b> przed transakcją, gdy na interpretację nie ma czasu"]),
    ("Dział IV Ordynacji podatkowej · PPSA", "Postępowania podatkowe i kontrole",
     "Jako pełnomocnik zawodowy prowadzimy sprawę od wszczęcia postępowania albo kontroli aż do wyroku sądu administracyjnego. Budujemy materiał dowodowy od pierwszego dnia, bo w sądzie liczy się to, co jest w aktach.",
     ["odwołanie: 14 dni", "skarga do WSA: 30 dni"],
     ["<b>Kontrole podatkowe</b> w urzędzie skarbowym i kontrole celno-skarbowe KAS", "<b>Postępowania podatkowe</b>: pisma, wnioski dowodowe, udział w przesłuchaniach", "<b>Odwołania</b> od decyzji i <b>zażalenia</b> na postanowienia", "<b>Skargi do WSA</b> i <b>skargi kasacyjne do NSA</b>", "<b>Egzekucja administracyjna</b>: zarzuty, wstrzymanie, raty i odroczenia"]),
    ("art. 272–274c Ordynacji podatkowej", "Czynności sprawdzające",
     "Najczęstszy pierwszy kontakt z urzędem: wezwanie do korekty, wyjaśnień albo dokumentów. Dobra odpowiedź zamyka sprawę. Zła otwiera kontrolę. Przygotowujemy odpowiedź tak, żeby sprawa zakończyła się na tym etapie.",
     ["JPK_VAT", "zwrot VAT", "zeznania roczne"],
     ["<b>Wezwania do wyjaśnień</b> niezgodności w JPK_VAT i zeznaniach", "<b>Weryfikacja zwrotu VAT</b> i przedłużenie terminu zwrotu", "<b>Zapytania o kontrahentów</b> i łańcuchy dostaw", "<b>Decyzja o korekcie</b> albo pozostawieniu deklaracji bez zmian", "<b>Rozmowy telefoniczne z urzędem</b> prowadzone przez pełnomocnika zamiast przez Ciebie"]),
]

SPECS = [
    ("art. 176 KSH · CIT · PIT", "Wypłata pieniędzy ze spółki", "Dobieramy najtańszą legalną drogę: wynagrodzenie zarządu, powołanie, art. 176 KSH, dywidenda, pożyczka albo najem.", ["Porównanie obciążeń CIT, PIT i ZUS dla każdej drogi", "Uchwały i umowy zgodne z praktyką urzędów", "Wynagrodzenie wspólnika w formie świadczeń niepieniężnych"]),
    ("JDG · sp. z o.o. · estoński CIT", "Forma prawna i opodatkowanie", "Liczymy, czy lepsza jest działalność, spółka czy ryczałt od dochodów spółek, zanim zmienisz formę albo zaczniesz nowy biznes.", ["Symulacja podatków i składek na kilka lat", "Skala, liniowy, ryczałt, estoński CIT", "Plan zmiany formy opodatkowania w terminie"]),
    ("przekształcenia · aporty · podziały", "Restrukturyzacje", "Przekształcenie JDG w spółkę, aport przedsiębiorstwa, połączenia i podziały spółek z zachowaniem neutralności podatkowej.", ["Analiza ryzyk i klauzuli przeciw unikaniu opodatkowania", "Wniosek o interpretację przed transakcją", "Harmonogram i dokumenty krok po kroku"]),
    ("ustawa o fundacji rodzinnej", "Fundacje rodzinne", "Pomagamy założyć fundację rodzinną i bezpiecznie przenieść do niej majątek, z myślą o sukcesji w firmie rodzinnej.", ["Statut, akt założycielski i wniesienie mienia", "Opodatkowanie świadczeń dla beneficjentów", "Zakazana działalność gospodarcza fundacji"]),
    ("spadki · darowizny · art. 4a", "Sukcesja i majątek rodzinny", "Przekazanie firmy i majątku dzieciom albo małżonkowi bez zbędnego podatku i z dotrzymaniem terminów zgłoszeń.", ["Zwolnienie dla najbliższej rodziny i zgłoszenie SD-Z2", "Darowizna udziałów i przedsiębiorstwa", "Testament i umowy z myślą o podatkach"]),
    ("VAT · PCC · PIT · podatek od nieruchomości", "Nieruchomości", "Sprzedaż działek, najem, inwestycje deweloperskie i spory z gminą o podatek od nieruchomości.", ["VAT albo PCC przy sprzedaży gruntu i budynku", "Najem prywatny a działalność gospodarcza", "Odwołania od decyzji w podatku od nieruchomości"]),
    ("budynki · budowle · instalacje", "Podatek od nieruchomości", "Audyty i kwalifikacja obiektów dla właścicieli nieruchomości komercyjnych, zakładów produkcyjnych, magazynów i inwestorów.", ["Audyt deklaracji i wykrywanie nieprawidłowości", "Budynek czy budowla: hale, magazyny, instalacje techniczne", "Ryzyka przy inwestycjach, opinie i spory z gminą"]),
    ("UPO · rezydencja · CFC", "Podatki międzynarodowe", "Praca i działalność za granicą, kontrahenci zagraniczni i przeniesienie rezydencji podatkowej.", ["Rezydencja podatkowa i certyfikaty", "Umowy o unikaniu podwójnego opodatkowania", "Podatek u źródła i transakcje z podmiotami zagranicznymi"]),
    ("raty · odroczenia · umorzenia · zarzuty", "Zaległości podatkowe i egzekucja", "Gdy urząd już ściąga podatek albo zajął konto. Negocjujemy z urzędem i bronimy Cię w egzekucji.", ["Rozłożenie na raty, odroczenie i umorzenie zaległości", "Zarzuty w egzekucji administracyjnej", "Wstrzymanie egzekucji i zwolnienie zajętych rachunków"]),
    ("OSS · SME · import usług", "VAT w e-commerce i usługach cyfrowych", "Sprzedaż online do konsumentów z UE, subskrypcje i reklamy kupowane od Meta czy Google.", ["Limit 10 000 euro, procedury OSS i SME", "Import usług przy zwolnieniu z VAT", "Korekty wcześniejszych rozliczeń"]),
    ("B+R · IP Box · robotyzacja", "Ulgi podatkowe dla innowacji", "Sprawdzamy, czy Twoja firma może obniżyć podatek dzięki ulgom na działalność badawczo-rozwojową i własne innowacje.", ["Ulga badawczo-rozwojowa (B+R)", "IP Box: 5% podatku od dochodu z IP", "Ulga na robotyzację i dokumentacja do ulg"]),
    ("opinia · due diligence", "Opinie przed decyzją", "Gdy na interpretację nie ma czasu: pisemna opinia przed podpisaniem umowy, zakupem spółki albo dużą transakcją.", ["Przegląd umów pod kątem podatków", "Due diligence podatkowe przy zakupie firmy", "Opinia, na której możesz oprzeć decyzję"]),
]

PEOPLE = [
    ("michal-ruszniak-garnitur.jpg", 900, 1200, "Michał Ruszniak", "15009",
     ["Założył kilkadziesiąt działalności gospodarczych i spółek prawa handlowego, więc zna podatki z przepisów i z codziennego prowadzenia firmy", "Specjalizuje się w obsłudze małych i średnich przedsiębiorstw oraz firm rodzinnych", "Pełnomocnik zawodowy w kontrolach, postępowaniach podatkowych i przed sądami administracyjnymi", "Prelegent ogólnopolskich konferencji naukowych poświęconych postępowaniom podatkowym", "Juror w finałach krajowych konkursów wiedzy o podatkach"]),
    ("marcin-otreba-garnitur.jpg", 900, 1200, "Marcin Otręba", "14609",
     ["Wieloletni pracownik Izby Skarbowej we Wrocławiu, trener Ministerstwa Finansów i Centrum Edukacji Zawodowej Resortu Finansów", "Doświadczenie na stanowiskach kierowniczych w międzynarodowych firmach z SSE i w renomowanych kancelariach podatkowych", "Od 2010 r. wykładowca prawa podatkowego na Uniwersytecie WSB Merito we Wrocławiu, kierownik merytoryczny studiów podyplomowych „Doradca podatkowy”, wykładowca MBA", "Szkoli Administrację Skarbową i oddziały Stowarzyszenia Księgowych w Polsce; autor publikacji m.in. dla Biuletynu VAT (INFOR)", "Specjalizuje się w VAT, CIT i PIT oraz w kontrolach podatkowych, celno-skarbowych i sporach przed sądami administracyjnymi"]),
]

FAQ_HOME = [
    ("Czym różni się doradca podatkowy od księgowego?", "Księgowy prowadzi księgi. Doradca podatkowy może legalnie doradzać w sprawach podatkowych, wydawać opinie i reprezentować klienta przed urzędami skarbowymi, KAS i sądami administracyjnymi. Odpowiada za swoje porady i ma obowiązkowe ubezpieczenie OC."),
    ("Dlaczego Waszą sprawą zajmuje się dwóch doradców?", "Każda sprawa przechodzi przez ręce dwóch doradców podatkowych. Obaj znają Twoją sytuację, więc zawsze masz z kim porozmawiać, także w czasie urlopu czy rozprawy jednego z nas. Ważne pisma i opinie sprawdza drugi doradca."),
    ("Mam kontrolę z urzędu skarbowego. Co robić?", "Zachować spokój i zadzwonić do doradcy. Doradca podatkowy może reprezentować Cię przed US i KAS, w postępowaniu podatkowym, czynnościach sprawdzających i przed sądami administracyjnymi."),
    ("Ile kosztują usługi doradcy podatkowego?", "Stała obsługa w abonamencie kosztuje od 369 zł netto miesięcznie, a konsultacja indywidualna od 400 zł netto za godzinę. Postępowania, kontrole i sprawy sądowe wyceniamy po zapoznaniu się z pismami. Pierwsze 20 minut rozmowy jest bezpłatne."),
    ("Czy obsługujecie klientów spoza Wrocławia?", "Tak. Na co dzień pracujemy z klientami z Wrocławia, Siechnic, Kobierzyc, Żórawiny, Środy Śląskiej, Trzebnicy, Oleśnicy, Oławy, Strzelina, Jelcza-Laskowic, Długołęki i Kątów Wrocławskich. Spotkania odbywają się w kancelarii przy ul. Zwycięskiej 3 lub ul. Artemskiej 11, u klienta w firmie albo online, a pełnomocnikiem możemy być przed każdym urzędem i sądem w Polsce."),
    ("Ile trwa uzyskanie interpretacji indywidualnej?", "Dyrektor KIS ma 3 miesiące od wpływu kompletnego wniosku. Opłata to 40 zł od każdego stanu faktycznego lub zdarzenia przyszłego. Brak interpretacji w terminie oznacza, że stanowisko wnioskodawcy uznaje się za prawidłowe."),
]

FAQ_ABO = [
    ("Na jak długo zawieramy umowę abonamentową?", "Umowę zawieramy na czas nieokreślony z miesięcznym okresem wypowiedzenia. Zakres i cenę ustalamy po krótkiej rozmowie o Twojej firmie."),
    ("Czym różnią się pakiety?", "Liczbą godzin doradztwa w miesiącu i czasem odpowiedzi. Pakiet „Wsparcie księgowości” jest dla firm, które mają własną księgową lub biuro rachunkowe: Twoja księgowa może dzwonić i pisać do nas bezpośrednio, a przed rozliczeniem rocznym przeglądamy kluczowe pozycje."),
    ("Co się dzieje z niewykorzystanymi godzinami?", "Niewykorzystane godziny przechodzą na następny miesiąc. Jeśli w danym miesiącu potrzebujesz więcej, każdą dodatkową godzinę rozliczamy po preferencyjnej stawce dla abonentów."),
    ("Czy mogę zacząć od jednej konsultacji?", "Tak. Wiele firm zaczyna od konsultacji albo od jednej sprawy, np. odpowiedzi na wezwanie z urzędu, i dopiero potem przechodzi na stałą obsługę."),
    ("Co jeśli w trakcie abonamentu dostanę pismo z urzędu?", "Dzwonisz do nas. Ocenimy pismo i termin, a odpowiedź w czynnościach sprawdzających przygotujemy w ramach stałej obsługi albo wycenimy osobno, jeśli sprawa wymaga prowadzenia postępowania lub kontroli."),
]


def faq_html(items):
    return "\n".join(f'''      <details class="fq"{' open' if i == 0 else ''}>
        <summary><span class="fq-q">{q}</span><span class="fq-ic" aria-hidden="true"></span></summary>
        <div class="fq-a"><p>{a}</p></div>
      </details>''' for i, (q, a) in enumerate(items))


def spec_card(ref, t, d, li, tag="article", h="h4"):
    return f'      <{tag} class="spec"><span class="ref">{ref}</span><{h}>{t}</{h}><p>{d}</p><ul>' + "".join(f"<li>{x}</li>" for x in li) + f"</ul></{tag}>"


def towns_html():
    return "\n".join(f'      <div class="town">{PIN.replace("<svg ", "<svg ")}<b>{t}</b><span>{s}</span></div>' for t, s in TOWNS)


PR_ICO = ['<path d="M4 7h16v12H4zM8 7V5h8v2M4 12h16"/>',
          '<path d="M4 5h16v11H9l-5 4zM8 9h8M8 12h5"/>',
          '<path d="M6 3h9l4 4v14H6zM14 3v5h5M9 13h7M9 17h5"/>',
          '<path d="M12 3v18M5 7h14M5 7l-3 7a4 4 0 0 0 6 0zM19 7l-3 7a4 4 0 0 0 6 0zM8 21h8"/>']


def sol_cards(p):
    out = []
    for i, (n, t, d, price, unit, href, feat) in enumerate(SOLUTIONS):
        m = re.match(r"od (\d+) zł", price)
        pr = f'<span class="pr-from">od</span><b data-count="{m.group(1)}">{m.group(1)}</b><span class="pr-cur">zł</span>' if m else f'<b class="pr-ind">{price}</b>'
        badge = '<span class="pr-badge">Najczęściej wybierany</span>' if feat else ""
        out.append(f'''      <a class="pr{' pr-feat' if feat else ''}" href="{p}{href}" style="--i:{i}">
        {badge}<span class="pr-top"><span class="pr-ico"><svg viewBox="0 0 24 24" aria-hidden="true">{PR_ICO[i]}</svg></span></span>
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="pr-price"><div class="pr-val">{pr}</div><small>{unit}</small></div>
        <span class="pr-go">{'Wybierz pakiet' if feat else 'Szczegóły'} <i aria-hidden="true">→</i></span>
      </a>''')
    return "\n".join(out)


def duo_section(p, show_link=True, portraits=False):
    link = f'<a class="more-link dv-link" href="{p}zespol/">Poznaj doradców →</a>' if show_link else ""
    ico = ['<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
           '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
           '<path d="M12 3v18M5 7h14M5 7l-3 7a4 4 0 0 0 6 0zM19 7l-3 7a4 4 0 0 0 6 0zM8 21h8"/>']
    pts = [("Zawsze ktoś odbierze", "Urlop, rozprawa czy kontrola u innego klienta nie zatrzymują Twojej sprawy."),
           ("Druga para oczu", "Każde ważne pismo, odwołanie i opinię sprawdza drugi doradca przed wysłaniem."),
           ("Dwa doświadczenia", "Praktyka biznesowa i lata pracy w administracji skarbowej przy jednym stole.")]
    cards = "".join(f'''<li class="dv-c" style="--i:{i}"><span class="dv-ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ico[i]}</svg></span><div><b>{t}</b><span>{d}</span></div></li>''' for i, (t, d) in enumerate(pts))
    return f'''<section class="section dv-sec" aria-labelledby="duo-h">
  <div class="dv-grid-bg" aria-hidden="true"></div>
  <div class="wrap dv-lay">
    <div class="dv-copy">
      <h2 id="duo-h" class="split">Każdą sprawą zajmuje się <em>dwóch doradców podatkowych</em></h2>
    </div>
    <div class="dv-vis" aria-hidden="true">
      <svg viewBox="0 0 520 420">
        <defs>
          <radialGradient id="dvA" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#D9B98E" stop-opacity=".16"/><stop offset="1" stop-color="#D9B98E" stop-opacity="0"/></radialGradient>
          <clipPath id="dvClip"><circle cx="195" cy="210" r="150"/></clipPath>
          <linearGradient id="dvG" x1="0" x2="1"><stop offset="0" stop-color="#B8925F"/><stop offset=".5" stop-color="#F3E1BC"/><stop offset="1" stop-color="#B8925F"/></linearGradient>
        </defs>
        <g class="dv-a"><circle cx="195" cy="210" r="150" fill="url(#dvA)"/><circle class="dv-ring" cx="195" cy="210" r="150"/><circle class="dv-ring2" cx="195" cy="210" r="168"/>
          <circle class="dv-dot" r="5"><animateMotion dur="9s" repeatCount="indefinite" path="M45 210a150 150 0 1 0 300 0a150 150 0 1 0-300 0"/></circle>
          <text class="dv-lbl" x="110" y="215" text-anchor="middle">DORADCA</text><text class="dv-lbl2" x="110" y="238" text-anchor="middle">prowadzący</text></g>
        <g class="dv-b"><circle cx="325" cy="210" r="150" fill="url(#dvA)"/><circle class="dv-ring" cx="325" cy="210" r="150"/><circle class="dv-ring2" cx="325" cy="210" r="168"/>
          <circle class="dv-dot" r="5"><animateMotion dur="9s" repeatCount="indefinite" path="M475 210a150 150 0 1 1-300 0a150 150 0 1 1 300 0"/></circle>
          <text class="dv-lbl" x="410" y="215" text-anchor="middle">DORADCA</text><text class="dv-lbl2" x="410" y="238" text-anchor="middle">weryfikujący</text></g>
        <g class="dv-lens"><circle cx="325" cy="210" r="150" clip-path="url(#dvClip)"/></g>
        <g class="dv-core"><text class="dv-k" x="260" y="196" text-anchor="middle">✓✓</text><text class="dv-t" x="260" y="226" text-anchor="middle">Twoja</text><text class="dv-t" x="260" y="250" text-anchor="middle">sprawa</text></g>
      </svg>
    </div>
    <ul class="dv-cards">{cards}</ul>
    {link}
  </div>
</section>
'''


# ---------------------------------------------------------------- strony
def wheel_html():
    items = [(r, t, d, li) for r, t, d, _c, li in PILLARS] + [(r, t, d, li) for r, t, d, li in SPECS]
    data = [{"t": t, "r": r, "d": d, "li": [re.sub(r"<[^>]+>", "", x) for x in li[:3]]} for r, t, d, li in items]
    labels = "".join(f'<li><button type="button" data-i="{n}">{t}</button></li>' for n, (r, t, d, li) in enumerate(items))
    first = data[0]
    lis = "".join(f"<li>{x}</li>" for x in first["li"])
    js = json.dumps(data, ensure_ascii=False).replace("'", "&#39;")
    return f'''<div class="wheel" data-items='{js}'>
      <div class="wheel-dial">
        <div class="wheel-ring" aria-hidden="true"></div>
        <div class="wheel-num" aria-hidden="true"><span>01</span>.</div>
        <ol class="wheel-list">{labels}</ol>
      </div>
      <div class="wheel-card" aria-live="polite">
        <span class="ref wheel-ref">{first["r"]}</span>
        <h3 class="wheel-title">{first["t"]}</h3>
        <p class="wheel-desc">{first["d"]}</p>
        <ul class="wheel-li">{lis}</ul>
        <div class="wheel-nav">
          <button type="button" class="wheel-prev" aria-label="Poprzednia specjalizacja">←</button>
          <button type="button" class="wheel-next" aria-label="Następna specjalizacja">→</button>
          <a class="btn btn-primary" href="kontakt/#rezerwacja">Porozmawiajmy o tym</a>
        </div>
      </div>
    </div>'''


BR_ICONS = [
    '<path d="M3 11.5 12 4l9 7.5M5.5 9.8V20h13V9.8M10 20v-5.5h4V20"/>',
    '<path d="M4 20h16M6 20V9l6-4 6 4v11M9.5 12h1M13.5 12h1M9.5 15.5h1M13.5 15.5h1M2 5h9M11 5V3"/>',
    '<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>',
    '<path d="M12 3l1.8 4.6L18.5 9l-4.7 1.4L12 15l-1.8-4.6L5.5 9l4.7-1.4zM18 15l.9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9z"/>',
    '<path d="M3 21V10l5 3V10l5 3V6h3l1 15M3 21h18M7 17h2M12 17h2"/>',
]


def branch_accordion(p):
    panels = []
    for n, (ref, t, d, li) in enumerate(BRANCHES):
        ico = f'<svg viewBox="0 0 24 24" aria-hidden="true">{BR_ICONS[n % len(BR_ICONS)]}</svg>'
        lis = "".join(f"<li>{x}</li>" for x in li)
        panels.append(f'''      <article class="acc{' on' if n == 0 else ''}" tabindex="0">
        <div class="acc-bg" aria-hidden="true"></div>
        <span class="acc-num" aria-hidden="true">0{n + 1}</span>
        <div class="acc-ico">{ico}</div>
        <span class="acc-title" aria-hidden="true">{t}</span>
        <div class="acc-body">
          <span class="acc-ref">{ref}</span>
          <h3 class="acc-h">{t}</h3>
          <p>{d}</p>
          <ul>{lis}</ul>
        </div>
      </article>''')
    panels.append(f'''      <a class="acc acc-cta" href="{p}kontakt/#rezerwacja">
        <div class="acc-bg" aria-hidden="true"></div>
        <span class="acc-num" aria-hidden="true">?</span>
        <div class="acc-ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></div>
        <span class="acc-title" aria-hidden="true">Twoja branża?</span>
        <div class="acc-body">
          <span class="acc-ref">bezpłatne 20 minut</span>
          <h3 class="acc-h">Nie widzisz swojej branży?</h3>
          <p>Nie widzisz swojej branży? Zadzwoń albo umów rozmowę. Powiemy, czy i jak możemy pomóc.</p>
          <span class="btn btn-primary">Umów rozmowę →</span>
        </div>
      </a>''')
    return '<div class="acc-wrap">\n' + "\n".join(panels) + "\n    </div>"


MQ_ICONS = {
    "li": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="4.5" fill="#0A66C2"/><path fill="#fff" d="M7.1 9.6h2.3V17H7.1zM8.25 6.1a1.33 1.33 0 1 1 0 2.66 1.33 1.33 0 0 1 0-2.66zM10.9 9.6h2.2v1h.03c.31-.58 1.06-1.2 2.18-1.2 2.33 0 2.76 1.53 2.76 3.53V17h-2.3v-3.6c0-.86-.02-1.97-1.2-1.97-1.2 0-1.38.94-1.38 1.9V17h-2.3z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#1877F2"/><path fill="#fff" d="M13.4 22v-7h2.35l.35-2.75h-2.7V10.5c0-.8.22-1.33 1.36-1.33h1.45V6.73a19 19 0 0 0-2.12-.11c-2.1 0-3.53 1.28-3.53 3.63v2h-2.37V15h2.37v7z"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#25D366"/><path fill="#fff" d="M12.04 6.2a5.77 5.77 0 0 0-4.94 8.74L6.3 17.8l2.94-.77a5.77 5.77 0 1 0 2.8-10.83zm3.37 8.18c-.14.4-.83.77-1.15.8-.3.04-.68.06-1.1-.07a10 10 0 0 1-1-.37 7.8 7.8 0 0 1-2.98-2.64c-.37-.5-.89-1.33-.89-2.15 0-.82.43-1.22.58-1.39.15-.17.33-.2.44-.2h.32c.1 0 .24-.04.37.28l.5 1.22c.04.08.07.18.01.29-.05.11-.08.17-.16.27l-.25.28c-.08.08-.17.17-.07.34.1.17.44.72.94 1.17.65.57 1.2.75 1.37.84.17.08.27.07.37-.04l.55-.64c.11-.17.23-.14.38-.08l1.2.57c.17.08.28.12.32.19.04.07.04.4-.1.8z"/></svg>',
    "bl": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#D9B98E"/><text x="12" y="16.6" text-anchor="middle" font-family="Georgia,serif" font-size="13" font-weight="700" fill="#1D1A16">§</text></svg>',
}


def mq_items():
    items = [("li", "LinkedIn", LINKEDIN, "Komentarze do zmian w przepisach"),
             ("fb", "Facebook", "https://www.facebook.com/profile.php?id=61559661710392", "Aktualności kancelarii"),
             ("wa", "WhatsApp", wa_link(), "Napisz do nas teraz"),
             ("bl", "Blog", "blog/", "Podatki w praktyce")]
    out = ""
    for _ in range(2):
        for k, name, href, desc in items:
            ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            out += f'<a class="mq-it" href="{href}"{ext} data-k="{k}" data-d="{desc}">{MQ_ICONS[k]}<span>{name}</span></a>'
    return out


def mq_words(p):
    words = ["interpretacje", "kontrole", "postępowania", "WSA · NSA", "abonament od 369 zł", "bezpłatne 20 minut"]
    return "".join(f'<span class="mq-w">{w}</span>' for w in words * 2)


GL_ICO = {
    "li": '<path d="M6 9v9M6 6v.01M10 18v-5a3 3 0 0 1 6 0v5M10 9v9"/>',
    "fb": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v7h4v-7h3l1-4h-4V8z"/>',
    "bl": '<path d="M4 4h12l4 4v12H4zM8 10h8M8 14h8M8 18h5"/>',
    "wa": '<path d="M4 20l1.4-4A8 8 0 1 1 8 18.6zM9 9c0 3 3 6 6 6l1.5-1.5-2-1-1 1c-1-.5-2-1.5-2.5-2.5l1-1-1-2z"/>',
}


def glass_tiles(p):
    items = [("li", "LinkedIn", LINKEDIN, "Komentarze do przepisów"),
             ("fb", "Facebook", "https://www.facebook.com/profile.php?id=61559661710392", "Aktualności kancelarii"),
             ("bl", "Blog", f"{p}blog/", "Podatki w praktyce"),
             ("wa", "WhatsApp", wa_link(), "Napisz do nas")]
    out = ""
    for k, name, href, desc in items:
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        out += f'<a class="gl-t" href="{href}"{ext}><svg viewBox="0 0 24 24" aria-hidden="true">{GL_ICO[k]}</svg><div><b>{name}</b><span>{desc} <i aria-hidden="true">→</i></span></div></a>'
    return out


# kierunki od Wrocławia (stopnie, 0 = wschód, zgodnie z ruchem wskazówek) i odległość względna
TOWN_GEO = {"Siechnice": (48, .5), "Kobierzyce": (132, .64), "Żórawina": (96, .68), "Środa Śląska": (192, .9), "Trzebnica": (-82, .85), "Oborniki Śląskie": (-122, .82), "Oleśnica": (-40, .88), "Kępno": (-14, 1.0), "Oława": (25, .92), "Brzeg": (46, 1.02), "Strzelin": (72, .95), "Jelcz-Laskowice": (1, .74), "Długołęka": (-64, .62), "Kąty Wrocławskie": (163, .72)}


def towns_orbit(p, head, note=""):
    import math
    nodes = ""
    for t, sub in TOWNS[1:]:
        a, r = TOWN_GEO[t]
        x = 50 + math.cos(math.radians(a)) * r * 44
        y = 50 + math.sin(math.radians(a)) * r * 44
        nodes += f'<div class="to-nd" style="left:{x:.1f}%;top:{y:.1f}%" data-t="{t}"><span class="to-dot"></span><b>{t}</b></div>'
    note_html = f'<p class="to-note">{note}</p>' if note else ""
    return f'''<section class="to-sec to-wide" id="obszar" aria-labelledby="area-h">
  <div class="wrap">
    <div class="to-copy">
{head}    </div>
    <div class="to-orb" role="img" aria-label="Zakres działania: {", ".join(t for t, _ in TOWNS)}">
      <canvas class="to-cv" aria-hidden="true"></canvas>
      <div class="to-core" aria-hidden="true"><img src="{p}img/logo-light.png" alt="" width="900" height="302"><small>Wrocław</small></div>
      {nodes}
    </div>
    {note_html}
  </div>
</section>'''


def bridge_svg():
    hang = ""
    for i in range(1, 12):
        x = 90 + i * 340 / 12
        t = (x - 90) / 340
        y = (1 - t) ** 2 * 60 + 2 * (1 - t) * t * 250 + t * t * 60
        hang += f'<line class="bb-h" style="--d:{1.5 + i * .06:.2f}s" x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="170"/>'
    deck = "".join(f'<rect class="bb-seg" style="--d:{.55 + i * .08:.2f}s" x="{90 + i * 34:.0f}" y="168" width="33" height="9" rx="1.5"/>' for i in range(10))
    win = "".join(f'<rect x="{x}" y="{y}" width="7" height="7" rx="1"/>' for x in (66, 80, 101) for y in (110, 128, 146))
    return f'''<svg class="bb-svg" viewBox="0 0 520 250" aria-hidden="true">
  <defs><linearGradient id="bbg" x1="0" x2="1"><stop offset="0" stop-color="#B8925F"/><stop offset=".5" stop-color="#F3E1BC"/><stop offset="1" stop-color="#B8925F"/></linearGradient></defs>
  <path class="bb-water" d="M0 222 Q 30 214 60 222 T 120 222 T 180 222 T 240 222 T 300 222 T 360 222 T 420 222 T 480 222 T 540 222"/>
  <path class="bb-water bb-w2" d="M0 236 Q 30 228 60 236 T 120 236 T 180 236 T 240 236 T 300 236 T 360 236 T 420 236 T 480 236 T 540 236"/>
  <g class="bb-tw bb-tw1"><rect x="56" y="96" width="62" height="114" rx="5"/><g class="bb-win">{win}</g><rect x="84" y="50" width="12" height="160" rx="3" class="bb-mast"/></g>
  <g class="bb-tw bb-tw2"><rect x="402" y="96" width="62" height="114" rx="5"/><rect x="424" y="50" width="12" height="160" rx="3" class="bb-mast"/><text x="433" y="160" text-anchor="middle">§</text></g>
  {deck}
  <path class="bb-cable" d="M90 60 Q260 250 430 60"/>
  {hang}
  <circle class="bb-spark" r="3.5"><animateMotion dur="3.4s" begin="2.6s" repeatCount="indefinite" path="M90 60 Q260 250 430 60"/></circle>
</svg>'''


def bridge_section(p):
    return f'''<section class="section bb-sec" aria-labelledby="bb-h">
  <div class="wrap">
    <div class="bb-card">
      <div class="bb-glow" aria-hidden="true"></div>
      <div class="bb-copy">
        <h2 id="bb-h" class="split">Prowadzisz biuro rachunkowe? <em>Zbudujmy most.</em></h2>
        <p>Stałe wsparcie doradców podatkowych dla Twojego zespołu, wdrożenie JPK CIT i pomoc przy kontrolach Twoich klientów. Wy prowadzicie księgi, my bierzemy na siebie trudne pytania.</p>
        <ul class="bb-pts">
          <li><b>Odpowiedź na piśmie</b><span>do przekazania klientowi</span></li>
          <li><b>Kontrole i pisma z US</b><span>prowadzimy razem z Wami</span></li>
          <li><b>od <i data-count="419">419</i> zł</b><span>netto miesięcznie</span></li>
        </ul>
        <div class="hero-cta"><a class="btn btn-primary magnet" href="{p}dla-biur-rachunkowych/">Zobacz ofertę dla biur →</a></div>
      </div>
      <div class="bb-vis">
        {bridge_svg()}
        <span class="bb-lb bb-l1">Twoje biuro</span><span class="bb-lb bb-l2">M2 TAX</span>
        <span class="bb-chip bb-q">pytanie o VAT</span>
        <span class="bb-chip bb-a">✓ odpowiedź doradcy</span>
      </div>
    </div>
  </div>
</section>'''


PF_STEPS = [
    ("Sprawdzamy termin", "Ustalamy, co to za pismo, od kiedy biegnie termin i ile czasu realnie zostało. Wystarczy zdjęcie lub skan.", "TERMIN ✓"),
    ("Wstrzymujemy pochopne ruchy", "Nie składasz ustnych wyjaśnień przez telefon i nie wysyłasz dokumentów bez selekcji. To, co raz trafi do akt, zostaje w aktach.", "STOP"),
    ("Przejmujemy kontakt z urzędem", "Zgłaszamy pełnomocnictwo i od tej chwili korespondencja z organem idzie przez doradcę podatkowego.", "PEŁNOMOCNIK"),
    ("Prowadzimy sprawę do końca", "Odpowiedzi na wezwania, zastrzeżenia do protokołu, odwołanie, skarga do WSA i skarga kasacyjna do NSA.", "WSA · NSA"),
]
PF_LETTERS = [
    ("274c", "Wezwanie do złożenia wyjaśnień", "w ramach czynności sprawdzających", "odpowiedz w terminie"),
    ("282b", "Zawiadomienie o zamiarze wszczęcia kontroli", "kontrola rusza nie wcześniej niż po 7 dniach", "7 dni"),
    ("165", "Postanowienie o wszczęciu postępowania", "od tej chwili liczy się każde pismo i dowód", "każde pismo"),
    ("223 § 2", "Decyzja organu I instancji", "odwołanie od doręczenia decyzji", "14 dni"),
]


def pismo_flow():
    steps = "".join(f'''<li class="pf-step" data-stamp="{st}"><span class="pf-node"><i>{i + 1:02d}</i></span><div><h3>{t}</h3><p>{d}</p></div></li>''' for i, (t, d, st) in enumerate(PF_STEPS))
    letters = "".join(f'''<article class="pf-doc" style="--i:{i}"><span class="pf-art">art. <b>{n}</b></span><span class="pf-src">Ordynacja podatkowa</span><h4>{t}</h4><p>{d}</p><span class="pf-due">{due}</span></article>''' for i, (n, t, d, due) in enumerate(PF_LETTERS))
    return f'''    <div class="pf-lay">
      <div class="pf-stage" aria-hidden="true">
        <div class="pf-env">
          <div class="pf-paper"><span class="pf-hd">URZĄD SKARBOWY</span><span class="pf-ln"></span><span class="pf-ln"></span><span class="pf-ln s"></span><span class="pf-ln"></span><span class="pf-ln s"></span><span class="pf-stamp">TERMIN ✓</span></div>
          <div class="pf-back"></div><div class="pf-flap"></div><div class="pf-front"></div>
        </div>
        <div class="pf-ring"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="52"/><circle class="pf-arc" cx="60" cy="60" r="52"/></svg><b><span class="pf-cnt">1</span>/4</b><small>krok</small></div>
      </div>
      <ol class="pf-line" style="--p:0">{steps}</ol>
    </div>
    <div class="pf-docs" aria-label="Najczęstsze pisma">{letters}</div>
'''


def home_blog():
    posts = load_posts()[:2]
    if not posts:
        return ""
    cards = ""
    for x in posts:
        img = f'<div class="pc-img"><img src="img/blog/{x["image"]}" alt="" loading="lazy"></div>' if x["image"] else '<div class="pc-img pc-noimg"><span>§</span></div>'
        cards += f'''      <a class="post-card" href="blog/{x["slug"]}/">
        {img}
        <div class="pc-body">
          <span class="post-cat">{x["category"]}</span>
          <span class="post-meta">{x["date_h"]} · {x["minutes"]} min czytania</span>
          <h3>{x["title"]}</h3>
          <p>{x["lead"]}</p>
          <span class="post-more">Czytaj artykuł <i aria-hidden="true">→</i></span>
        </div>
      </a>
'''
    return f'''<section class="section hb-sec" aria-labelledby="hb-h">
  <div class="wrap">
    <div class="hb-head">
{section_head("Z bloga", "Podatki w praktyce", "Komentujemy wyroki, interpretacje i zmiany w przepisach. Krótko i na przykładach z naszych spraw.", "hb-h")}      <a class="more-link" href="blog/">Wszystkie artykuły →</a>
    </div>
    <div class="post-grid post-grid-2 hb-grid">
{cards}    </div>
  </div>
</section>
'''


SW_GROUPS = [
    ("Kontrole i postępowania", ["Postępowania podatkowe i kontrole", "Czynności sprawdzające", "Zaległości podatkowe i egzekucja"]),
    ("Doradztwo podatkowe", ["Wnioski o interpretację indywidualną", "Opinie przed decyzją", "Podatki międzynarodowe", "VAT w e-commerce i usługach cyfrowych", "Ulgi podatkowe dla innowacji"]),
    ("Firma i majątek", ["Wypłata pieniędzy ze spółki", "Forma prawna i opodatkowanie", "Restrukturyzacje", "Fundacje rodzinne", "Sukcesja i majątek rodzinny"]),
    ("Nieruchomości", ["Nieruchomości", "Podatek od nieruchomości"]),
]
SW_SHORT = {"Postępowania podatkowe i kontrole": "Postępowania i kontrole", "Wnioski o interpretację indywidualną": "Interpretacje indywidualne",
            "Zaległości podatkowe i egzekucja": "Zaległości i egzekucja", "VAT w e-commerce i usługach cyfrowych": "VAT w e-commerce",
            "Ulgi podatkowe dla innowacji": "Ulgi B+R i IP Box", "Sukcesja i majątek rodzinny": "Sukcesja", "Forma prawna i opodatkowanie": "Forma prawna"}


def spec_wheel(p):
    allx = {t: (r, t, d) for r, t, d, _c, li in PILLARS}
    allx.update({t: (r, t, d) for r, t, d, li in SPECS})
    data, lis, k = [], "", 0
    for g, ts in SW_GROUPS:
        lis += f'<li class="sw-g" aria-hidden="true"><span>{g}</span></li>'
        for t in ts:
            r, _, d = allx[t]
            data.append({"t": t, "r": r, "d": d, "g": g, "s": SW_SHORT.get(t, t)})
            lis += f'<li class="sw-i"><button type="button" data-i="{k}">{SW_SHORT.get(t, t)}</button></li>'
            k += 1
    n = len(data)
    rings = ""
    import math
    for band, R in ((0, 560), (1, 520)):
        for j in range(26):
            a = j / 26 * 2 * math.pi
            rings += f'<circle cx="{590 + 7 * math.cos(a):.1f}" cy="{590 + 7 * math.sin(a):.1f}" r="{R - j * 0.55:.1f}"/>'
    js = json.dumps(data, ensure_ascii=False).replace("'", "&#39;")
    f = data[0]
    return f'''<div class="sw" data-items='{js}'>
      <div class="sw-dial">
        <svg class="sw-rings" viewBox="0 0 1180 1180" aria-hidden="true"><g>{rings}</g></svg>
        <span class="sw-pin" aria-hidden="true"><i></i></span>
        <ol class="sw-list">{lis}</ol>
      </div>
      <div class="sw-side">
        <h2 id="spec-h" class="split">W czym możemy pomóc?</h2>
        <div class="sw-mhead" aria-hidden="true">
          <svg viewBox="0 0 400 90" preserveAspectRatio="none"><path class="sw-arc1" d="M-10 0 Q200 110 410 0"/><path class="sw-arc2" d="M-10 22 Q200 128 410 22"/></svg>
          <span class="sw-mg">{f["g"]}</span><b class="sw-mname">{f["t"]}</b>
        </div>
        <div class="sw-cwrap">
        <button type="button" class="sw-mprev" aria-label="Poprzednia specjalizacja"><svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg></button>
        <button type="button" class="sw-mnext" aria-label="Następna specjalizacja"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></button>
        <div class="sw-card" aria-live="polite">
          <span class="sw-cat">{f["g"]}</span>
          <h3 class="sw-title">{f["t"]}</h3>
          <p class="sw-desc">{f["d"]}</p>
          <span class="sw-ref">{f["r"]}</span>
          <a class="btn btn-primary sw-btn" href="{p}kontakt/#rezerwacja">Porozmawiajmy o tym <span aria-hidden="true">→</span></a>
        </div>
        </div>
        <div class="sw-ctl">
          <span class="sw-count"><b>01</b> / {n:02d}</span>
          <span class="sw-bar"><i></i></span>
          <button type="button" class="sw-prev" aria-label="Poprzednia specjalizacja"><svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg></button>
          <button type="button" class="sw-next" aria-label="Następna specjalizacja"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></button>
        </div>
        <a class="more-link" href="{p}doradztwo-podatkowe/">Wszystkie specjalizacje i branże →</a>
      </div>
    </div>'''


def build_home():
    p = ""
    h = head(p, "M2 TAX — Doradcy Podatkowi | Wrocław, Siechnice, Kobierzyce",
             "Kancelaria doradztwa podatkowego M2 TAX we Wrocławiu. Stała obsługa podatkowa od 369 zł netto miesięcznie, konsultacje, kontrole i postępowania podatkowe, sprawy przed WSA i NSA. Dwóch doradców w każdej sprawie. Bezpłatne 20 minut.",
             "")
    body = header(p, "") + f'''<section class="hero hero2">
  <canvas class="fx3d" data-fx="network" aria-hidden="true"></canvas>
  <canvas class="dust" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="hero-copy">
      <div class="brand-anim" role="img" aria-label="M2 TAX">
        <img class="ba-logo" src="img/logo-light.png" alt="" width="900" height="302" fetchpriority="high">
        <i class="gl" style="left:19%;top:14%"></i><i class="gl" style="left:47%;top:4%"></i><i class="gl" style="left:80%;top:44%"></i>
      </div>
      <h1 class="split">Twoje podatki, <em>nasza pasja.</em></h1>
      <div class="hero-cta">
        <a class="btn btn-primary magnet" href="kontakt/#rezerwacja">Umów bezpłatne 20 minut <span aria-hidden="true">→</span></a>
        <a class="btn btn-ghost" href="abonamenty/">Abonamenty od 369 zł</a>
      </div>
    </div>
    <figure class="hero-duo" data-parallax="-0.06">
      <span class="hd-ring" aria-hidden="true"></span><img src="img/doradcy-duo-cut.webp?v=2" alt="Doradcy podatkowi Michał Ruszniak i Marcin Otręba" width="1000" height="1087" fetchpriority="high">
      <figcaption>Michał Ruszniak · Marcin Otręba<span>doradcy podatkowi nr 15009 i 14609</span></figcaption>
    </figure>
  </div>
  <a class="scroll-cue" href="#specjalizacje" aria-label="Przewiń dalej"><span></span></a>
</section>

<section class="sw-sec" id="specjalizacje" aria-labelledby="spec-h">
<div class="sw-pinwrap"><div class="sw-sticky">
{spec_wheel(p)}
</div></div>
</section>

<section class="section br-sec" id="branze" aria-labelledby="br-h">
  <canvas class="fx3d" data-fx="rings" aria-hidden="true"></canvas>
  <div class="wrap">
{section_head("Branże", "Znamy specyfikę Twojej branży", "Doświadczenie z konkretnych sektorów oznacza mniej tłumaczenia i szybsze, trafniejsze odpowiedzi.", "br-h")}    {branch_accordion(p)}
  </div>
</section>



<section class="section bg-paper2 pf-sec" id="pismo" aria-labelledby="pismo-h">
  <div class="wrap">
{section_head("", "Większość sporów z fiskusem da się ustawić na samym początku. Liczy się termin i to, co trafi do akt jako pierwsze.", "", "pismo-h")}{pismo_flow()}
  </div>
</section>

{duo_section(p)}
<section class="section sol-sec" id="rozwiazania" aria-labelledby="sol-h">
  <div class="wrap">
{section_head("Współpraca", "Cztery sposoby współpracy z doradcą podatkowym", "Wybierz to, czego potrzebujesz teraz. Możesz zacząć od jednej konsultacji, a z czasem przejść na stałą obsługę.", "sol-h")}    <div class="pr-grid">
{sol_cards(p)}
    </div>
    <a class="more-link" href="abonamenty/">Zobacz szczegóły abonamentów i cen →</a>
  </div>
</section>

{towns_orbit(p, section_head("Zakres działania", "Doradca podatkowy we Wrocławiu i okolicach", "", "area-h"), "Pełnomocnikiem możemy być przed każdym urzędem skarbowym, KAS i sądem administracyjnym w Polsce, więc z naszych usług korzystają też klienci spoza Dolnego Śląska.")}

{home_blog()}
<section class="section bg-paper2" id="faq" aria-labelledby="faq-h">
  <div class="wrap faq-wrap">
{section_head("FAQ", "Najczęściej zadawane pytania", "Odpowiedzi, które pomogą zrozumieć, jak pracujemy.", "faq-h")}    <div class="faq">
{faq_html(FAQ_HOME)}
    </div>
  </div>
</section>

{bridge_section(p)}

<section class="gl-sec" aria-labelledby="gl-h">
  <div class="gl-blob gl-b1" aria-hidden="true"></div><div class="gl-blob gl-b2" aria-hidden="true"></div>
  <div class="wrap">
    <h2 id="gl-h" class="split">Zostańmy <em>w kontakcie.</em></h2>
    <div class="gl-grid">{glass_tiles(p)}</div>
  </div>
</section>

'''
    return h + body + footer(p)


def build_abonamenty():
    p = "../"
    h = head(p, "Abonamenty i ceny — M2 TAX Doradcy Podatkowi | Wrocław",
             "Abonament doradztwa podatkowego od 369 zł netto miesięcznie (2 godziny), pakiety 3 i 5 godzin, konsultacje od 400 zł netto za godzinę, prowadzenie kontroli i postępowań podatkowych, sprawy przed WSA i NSA. Dwóch doradców w każdej sprawie.",
             "abonamenty/")
    variants = [
        ("Doradztwo podatkowe", "Dla przedsiębiorców i małych firm, które chcą mieć doradcę podatkowego pod telefonem.", "od 369 zł", "netto / mies.", False,
         ["<b>2 godziny</b> doradztwa miesięcznie", "Pytania telefonicznie, mailowo i na wideo", "Odpowiedź w ciągu 2 dni roboczych", "Analiza umów i transakcji przed podpisaniem", "Przegląd pism z urzędu i plan działania", "Dwóch doradców znających Twoją firmę", "Dostęp do bazy wiedzy i wzorów dokumentów"]),
        ("Doradztwo podatkowe + Wsparcie Twojej księgowości", "Dla firm z własną księgową lub biurem rachunkowym. Twoja księgowa ma bezpośredni kontakt z doradcą podatkowym.", "od 590 zł", "netto / mies.", True,
         ["<b>3 godziny</b> doradztwa miesięcznie", "Twoja księgowa pisze i dzwoni do nas bezpośrednio", "Konsultowanie trudnych księgowań i rozliczeń VAT", "Przegląd kluczowych pozycji przed zeznaniem rocznym", "Odpowiedzi na wezwania w czynnościach sprawdzających", "Odpowiedź w ciągu 1 dnia roboczego", "Dostęp do bazy wiedzy i wzorów dokumentów"]),
        ("Doradztwo Biznes", "Dla spółek i firm rodzinnych, które regularnie podejmują decyzje z konsekwencjami podatkowymi.", "od 890 zł", "netto / mies.", False,
         ["<b>5 godzin</b> doradztwa miesięcznie", "Wszystko z pakietu „Doradztwo podatkowe + Wsparcie Twojej księgowości”", "Spotkanie podatkowe raz na kwartał", "Planowanie wypłat ze spółki i inwestycji", "Pierwszeństwo terminów w sprawach pilnych", "Odpowiedź w ciągu 1 dnia roboczego", "Dostęp do bazy wiedzy i wzorów dokumentów"]),
    ]
    vhtml = []
    for t, f, price, unit, feat, li in variants:
        badge = '<span class="badge">Najczęściej wybierany</span>' if feat else ""
        btn = "btn-primary" if feat else "btn-ghost"
        vhtml.append(f'''      <article class="variant{' featured' if feat else ''}">{badge}
        <h3>{t}</h3>
        <p class="for">{f}</p>
        <div class="price"><b>{price}</b><span class="unit">{unit}</span></div>
        <ul>{"".join(f"<li>{x}</li>" for x in li)}</ul>
        <a class="btn {btn}" href="{p}kontakt/#rezerwacja">Wybieram ten pakiet</a>
      </article>''')
    svc = [
        ("konsultacja", "02", "Konsultacja indywidualna", "Jednorazowa rozmowa o konkretnej sprawie, bez umowy na stałe. Dobra na początek współpracy albo dla osób, które nie prowadzą działalności, np. przy sprzedaży mieszkania czy działki.", "od 400 zł", "netto za godzinę · pierwsze 20 minut bezpłatnie",
         ["Spotkanie w kancelarii, u Ciebie w firmie albo online", "Analiza dokumentów przed spotkaniem", "Konkretne wnioski i dalsze kroki na piśmie", "Wycena dalszej pracy, jeśli będzie potrzebna"]),
        ("postepowania", "03", "Prowadzenie postępowań i kontroli", "Działamy jako Twój pełnomocnik od pierwszego pisma. Prowadzimy korespondencję z urzędem, uczestniczymy w czynnościach i budujemy materiał dowodowy na wypadek sporu.", "wycena indywidualna", "po zapoznaniu się z pismami z urzędu",
         ["Czynności sprawdzające i odpowiedzi na wezwania", "Kontrole podatkowe w US i kontrole celno-skarbowe KAS", "Postępowania podatkowe, zastrzeżenia do protokołu", "Odwołania od decyzji i zażalenia na postanowienia", "Egzekucja administracyjna: zarzuty, raty, odroczenia"]),
        ("sady", "04", "Postępowania sądowe przed WSA i NSA", "Gdy decyzja urzędu jest ostateczna, sprawa trafia do sądu administracyjnego. Doradca podatkowy może być Twoim pełnomocnikiem zarówno przed WSA, jak i NSA.", "wycena indywidualna", "po analizie decyzji i akt sprawy",
         ["Skarga do wojewódzkiego sądu administracyjnego", "Wnioski o wstrzymanie wykonania decyzji", "Udział w rozprawach", "Skarga kasacyjna i odpowiedź na skargę kasacyjną do NSA"]),
    ]
    shtml = []
    for sid, n, t, d, price, unit, li in svc:
        shtml.append(f'''    <div class="svc" id="{sid}">
      <div>
        <span class="num">{n}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="price-line">{price}<small>{unit}</small></div>
      </div>
      <div class="pillar" style="padding:28px 28px;grid-template-columns:1fr">
        <ul>{"".join(f"<li>{x}</li>" for x in li)}</ul>
        <a class="btn btn-primary" href="{p}kontakt/#rezerwacja" style="justify-self:start;margin-top:8px">Umów rozmowę</a>
      </div>
    </div>''')
    body = header(p, "abonamenty/") + page_hero(
        p, "Abonamenty", "Abonamenty i ceny",
        "Stała obsługa podatkowa <em>od 369 zł</em> miesięcznie",
        "Cztery sposoby współpracy: abonament doradztwa podatkowego w trzech pakietach, konsultacja indywidualna, prowadzenie postępowań i kontroli oraz sprawy przed sądami administracyjnymi. W każdej sprawie pracuje dwóch doradców podatkowych.",
        fx="wave") + f'''
<section class="section" id="przeglad" aria-labelledby="ov-h">
  <div class="wrap">
{section_head("Przegląd", "Wybierz rozwiązanie", "", "ov-h")}    <div class="pr-grid">
{sol_cards(p).replace('href="../abonamenty/', 'href="')}
    </div>
  </div>
</section>

<section class="section bg-paper2" id="stala-obsluga" aria-labelledby="so-h">
  <div class="wrap">
{section_head("01 · Stała obsługa", "Pakiety doradztwa podatkowego", "Dzwonisz albo piszesz, kiedy masz pytanie, zanim podpiszesz umowę, wystawisz fakturę czy wypłacisz pieniądze ze spółki. Odpowiada doradca podatkowy, nie infolinia.", "so-h")}    <div class="variants">
{chr(10).join(vhtml)}
    </div>
    <div class="pkg-perks">
      <div><b>Bez długich zobowiązań</b><span>Miesięczny okres wypowiedzenia, bez umów na 12 miesięcy.</span></div>
      <div><b>Godziny nie przepadają</b><span>Niewykorzystany czas przechodzi na kolejny miesiąc.</span></div>
      <div><b>Dwóch doradców</b><span>W każdym pakiecie Twoją firmę znają dwaj doradcy podatkowi.</span></div>
      <div><b>Rabat dla abonentów</b><span>Postępowania, kontrole i sprawy sądowe taniej dla stałych klientów.</span></div>
      <div><b>Baza wiedzy i wzory</b><span>W każdym pakiecie opracowania podatkowe i gotowe wzory pism, umów i uchwał.</span></div>
    </div>
    <p class="fine">Ceny netto, do których dolicza się 23% VAT. Czas pracy liczymy w 15-minutowych odcinkach. Ostateczną cenę potwierdzamy po krótkiej rozmowie o skali działalności.</p>
  </div>
</section>

<section class="section" id="pozostale" aria-labelledby="pz-h">
  <div class="wrap">
{chr(10).join(shtml)}
  </div>
</section>

{duo_section(p)}
<section class="section" id="jak-zaczac" aria-labelledby="flow-h">
  <div class="wrap">
    <div class="cta-band" style="display:block">
      <h3 id="flow-h" style="margin-bottom:20px">Jak zacząć współpracę</h3>
      <ol class="flow">
        <li><b>Bezpłatne 20 minut</b><span>Opowiadasz o firmie albo sprawie, telefonicznie lub online.</span></li>
        <li><b>Propozycja</b><span>Wskazujemy rozwiązanie i podajemy cenę przed rozpoczęciem pracy.</span></li>
        <li><b>Umowa</b><span>Podpisujemy umowę i pełnomocnictwo, jeśli jest potrzebne.</span></li>
        <li><b>Dwóch doradców</b><span>Od tej chwili Twoją sprawę prowadzą dwie osoby, które ją znają.</span></li>
      </ol>
      <div class="hero-cta" style="margin-top:24px"><a class="btn btn-primary" href="{p}kontakt/#rezerwacja">Umów bezpłatne 20 minut</a><a class="btn btn-ghost" href="tel:{TEL1}">{TEL1_H}</a></div>
    </div>
  </div>
</section>

<section class="section bg-paper2" id="faq" aria-labelledby="faq-h">
  <div class="wrap faq-wrap">
{section_head("FAQ", "Pytania o abonamenty", "", "faq-h")}    <div class="faq">
{faq_html(FAQ_ABO)}
    </div>
  </div>
</section>
'''
    return h + body + footer(p)


def build_specjalizacje():
    p = "../"
    h = head(p, "Doradztwo podatkowe Wrocław — specjalizacje i branże | M2 TAX Doradcy Podatkowi",
             "Interpretacje indywidualne, kontrole i postępowania podatkowe, czynności sprawdzające, wypłata pieniędzy ze spółki, restrukturyzacje, fundacje rodzinne, nieruchomości. Branże: budowlana, medyczna, beauty, produkcyjna, osoby prywatne.",
             "doradztwo-podatkowe/")
    pill = []
    for ref, t, d, chips, li in PILLARS:
        pill.append(f'''      <article class="pillar">
        <div class="pillar-head">
          <span class="ref">{ref}</span>
          <h3>{t}</h3>
          <p>{d}</p>
          <div class="facts">{"".join(f'<span class="chip">{c}</span>' for c in chips)}</div>
        </div>
        <ul>
{chr(10).join(f"          <li>{x}</li>" for x in li)}
        </ul>
      </article>''')
    body = header(p, "doradztwo-podatkowe/") + page_hero(
        p, "Doradztwo podatkowe", "Doradztwo podatkowe",
        "W czym jesteśmy <em>najlepsi</em>",
        "Trzy obszary, w których spędzamy najwięcej czasu, osiem dodatkowych specjalizacji i pięć branż, które znamy od podszewki.",
        fx="grid") + f'''
<section class="section bg-paper2" aria-labelledby="core-h">
  <div class="wrap">
{section_head("Główne obszary", "Trzy obszary, w których spędzamy najwięcej czasu", "", "core-h")}    <div class="core">
{chr(10).join(pill)}
    </div>
    <h3 class="spec-title">Pozostałe specjalizacje</h3>
    <div class="spec-grid">
{chr(10).join(spec_card(*s) for s in SPECS)}
    </div>
  </div>
</section>

<section class="section br-sec" id="branze" aria-labelledby="br-h">
  <canvas class="fx3d" data-fx="rings" aria-hidden="true"></canvas>
  <div class="wrap">
{section_head("Branże", "Branże, w których mamy doświadczenie", "Każda branża ma swoje pułapki podatkowe. Te znamy z codziennej pracy z klientami.", "br-h")}    {branch_accordion(p)}
  </div>
</section>

{towns_orbit(p, section_head("Zakres działania", "Wrocław i okolice", "", "area-h"), "")}

<section class="section" aria-label="Umów spotkanie">
  <div class="wrap">
{cta_band(p, "Masz sprawę z jednego z tych obszarów?", "Opowiedz nam o niej w ciągu bezpłatnych 20 minut. Powiemy, co da się zrobić i ile to będzie kosztować.")}  </div>
</section>
'''
    return h + body + footer(p)


def build_zespol():
    p = "../"
    h = head(p, "Zespół — Michał Ruszniak i Marcin Otręba | M2 TAX Doradcy Podatkowi",
             "Poznaj doradców podatkowych M2 TAX: Michał Ruszniak (DP nr 15009) i Marcin Otręba (DP nr 14609). Każdą sprawą zajmuje się dwóch doradców podatkowych.",
             "zespol/")
    ppl = []
    for img, w, hh, name, nr, li in PEOPLE:
        ppl.append(f'''      <article class="person">
        <img src="{p}img/{img}" alt="{name}" width="{w}" height="{hh}" loading="lazy">
        <div class="info">
          <span class="ref">Doradca podatkowy nr {nr}</span>
          <h3>{name}</h3>
          <p class="role">Partner zarządzający</p>
          <ul>
{chr(10).join(f"            <li>{x}</li>" for x in li)}
          </ul>
        </div>
      </article>''')
    body = header(p, "zespol/") + page_hero(
        p, "Zespół", "Zespół",
        "Twoją sprawą zajmuje się <em>dwóch</em> doradców",
        "Obaj jesteśmy doradcami podatkowymi wpisanymi na listę prowadzoną przez Krajową Izbę Doradców Podatkowych i obaj znamy każdą sprawę, którą prowadzimy.",
        fx="rings") + f'''
<section class="section dark" aria-labelledby="team-h">
  <canvas class="fx3d" data-fx="network" aria-hidden="true"></canvas>
  <div class="wrap">
{section_head("Partnerzy", "Poznaj naszych doradców", "", "team-h", light=True)}    <div class="team">
{chr(10).join(ppl)}
    </div>
  </div>
</section>

<section class="section bg-paper2" aria-labelledby="why-h">
  <div class="wrap">
{section_head("Dlaczego dwóch doradców", "Co zyskujesz na pracy w parze", "", "why-h")}    <div class="steps">
      <div class="step"><h3>Ciągłość sprawy</h3><p>Obaj znamy Twoją sytuację. Urlop czy rozprawa jednego z nas nie zatrzymują sprawy.</p></div>
      <div class="step"><h3>Kontrola jakości</h3><p>Każde ważne pismo, odwołanie i opinię sprawdza drugi doradca przed wysłaniem.</p></div>
      <div class="step"><h3>Dwie perspektywy</h3><p>Praktyka prowadzenia firm i lata pracy w administracji skarbowej przy jednym stole.</p></div>
      <div class="step"><h3>Odpowiedzialność</h3><p>Doradca podatkowy odpowiada za swoje porady i ma obowiązkowe ubezpieczenie OC.</p></div>
    </div>
  </div>
</section>

<section class="section" aria-label="Umów spotkanie">
  <div class="wrap">
{cta_band(p, "Porozmawiaj z nami osobiście", "W kancelarii przy ul. Zwycięskiej 3 lub ul. Artemskiej 11 we Wrocławiu, u Ciebie w firmie albo online. Pierwsze 20 minut jest bezpłatne.")}  </div>
</section>
'''
    return h + body + footer(p)


def build_kontakt():
    p = "../"
    h = head(p, "Kontakt i rezerwacja — M2 TAX Doradcy Podatkowi | Wrocław",
             "Umów spotkanie z doradcą podatkowym online. M2 TAX, ul. Zwycięska 3, 53-033 Wrocław, tel. 883 643 565, 534 909 534, kancelaria@m2tax.pl. Obsługujemy Wrocław, Siechnice, Kobierzyce, Żórawinę, Środę Śląską, Trzebnicę, Oleśnicę, Oławę, Strzelin, Jelcz-Laskowice, Długołękę, Kąty Wrocławskie, Oborniki Śląskie, Brzeg i Kępno.",
             "kontakt/")
    body = header(p, "kontakt/") + f'''<section class="section bk-section" id="rezerwacja" aria-labelledby="bk-h">
  <canvas class="fx3d" data-fx="wave" aria-hidden="true"></canvas>
  <div class="wrap bk-wrap">
    <div class="bk-intro">
      <p class="crumbs"><a href="{p}">Strona główna</a> / Kontakt</p>
      <h1 id="bk-h" style="font-size:clamp(30px,3.6vw,44px);font-weight:800;color:#fff">Umów spotkanie z doradcą podatkowym</h1>
      <p class="lede">Wybierz rodzaj spotkania i wolny termin. Potwierdzenie i przypomnienie dostaniesz e-mailem.</p>
      <div class="bk-free"><b>20 min</b><span>pierwsza rozmowa<br>bez opłat</span></div>
      <ul class="bk-points">
        <li>Online albo w kancelarii przy ul. Zwycięskiej 3 lub ul. Artemskiej 11</li>
        <li>Możemy też spotkać się u Ciebie w firmie</li>
        <li>Rozmawiasz bezpośrednio z doradcą podatkowym</li>
      </ul>
      <div class="bk-call">
        <span>Wolisz zadzwonić?</span>
        <a href="tel:{TEL1}">{TEL1_H}</a>
        <a href="tel:{TEL2}">{TEL2_H}</a>
      </div>
    </div>
    <div class="bk-card">
      <div class="bk-card-head">
        <span class="bk-dot" aria-hidden="true"></span>
        <b>Kalendarz M2 TAX</b>
        <span class="bk-live">wolne terminy na bieżąco</span>
      </div>
      <div id="inline-container" class="zoho-booking"><div class="zoho-loading"><span class="bk-spin" aria-hidden="true"></span>Ładuję kalendarz…</div></div>
      <p class="bk-card-foot">Kalendarz się nie wyświetla? <a href="{ZOHO_PUBLIC}" target="_blank" rel="noopener">Otwórz go w nowym oknie ↗</a></p>
    </div>
  </div>
</section>

<section class="section bg-paper2" id="kontakt" aria-labelledby="kontakt-h">
  <div class="wrap">
{section_head("Kontakt", "Gdzie nas znaleźć", "", "kontakt-h")}    <div class="contact-row" style="margin-top:0">
      <div class="contact-col">
        <div class="cinfo">
          <div class="cicon">{PIN}</div>
          <div><h4>Adresy kancelarii</h4><p>ul. Zwycięska 3<br>53-033 Wrocław</p><p style="margin-top:10px">ul. Beaty Artemskiej 11/44<br>52-234 Wrocław (Jagodno)</p><p style="margin-top:10px">Na życzenie przyjeżdżamy do klienta.</p></div>
        </div>
        <div class="cinfo">
          <div class="cicon">{PHONE}</div>
          <div><h4>Telefony</h4><p><a href="tel:{TEL1}">{TEL1_H}</a><button class="copy-light" data-copy="{TEL1_H}" type="button">Kopiuj</button><br><a href="tel:{TEL2}">{TEL2_H}</a><button class="copy-light" data-copy="{TEL2_H}" type="button">Kopiuj</button></p></div>
        </div>
        <div class="cinfo">
          <div class="cicon">{ENVELOPE}</div>
          <div><h4>E-mail</h4><p><a href="mailto:{MAIL}">{MAIL}</a><button class="copy-light" data-copy="{MAIL}" type="button">Kopiuj</button></p></div>
        </div>
        <div class="urgent">
          <span class="ref">Pismo z urzędu?</span>
          <h4>Ochłoń i zadzwoń do nas.</h4>
          <p>Wyślij zdjęcie pisma i datę jego doręczenia na {MAIL}. Oddzwonimy i powiemy, ile masz czasu i co robić dalej.</p>
        </div>
      </div>
      <div class="map-col">
        <figure class="office">
          <img src="{p}img/kancelaria-wnetrze.jpg" alt="Wnętrze kancelarii M2 TAX Doradcy Podatkowi we Wrocławiu" width="1400" height="1119" loading="lazy">
          <figcaption><b>Zapraszamy do kancelarii</b><span>Kawa, spokojna rozmowa i konkretny plan działania.</span></figcaption>
        </figure>
        <div class="map">
          <iframe title="Mapa dojazdu do kancelarii M2 TAX" src="https://maps.google.com/maps?q=ul.+Zwyci%C4%99ska+3,+53-033+Wroc%C5%82aw&amp;z=15&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        <a class="maplink" href="https://www.google.com/maps/search/?api=1&amp;query=ul.+Zwyci%C4%99ska+3+Wroc%C5%82aw" target="_blank" rel="noopener">Otwórz w Mapach Google ↗</a>
      </div>
    </div>
  </div>
</section>

{towns_orbit(p, section_head("Zakres działania", "Obsługujemy klientów z Wrocławia i okolic", "", "area-h"), "Spotkania online prowadzimy z klientami z całej Polski.")}
'''
    return h + body + footer(p, zoho=True)




def build_biura():
    p = "../"
    h = head(p, "Doradca podatkowy dla biur rachunkowych — wsparcie i JPK CIT | M2 TAX Wrocław",
             "Stałe wsparcie doradców podatkowych dla biur rachunkowych od 419 zł netto miesięcznie: konsultacje dla księgowych, wdrożenie JPK CIT (JPK_KR_PD, JPK_ST_KR), KSeF, czynności sprawdzające i kontrole klientów biura, interpretacje. W pakiecie baza wiedzy, wzory dokumentów, weryfikacja JPK CIT i sprawozdania do KRS z JPK CIT.",
             "dla-biur-rachunkowych/")
    pains = [
        ("Trudne pytanie od klienta", "Wypłata ze spółki, sprzedaż działki, estoński CIT, ulga B+R. Klient pyta, a odpowiedź musi być pewna i szybka."),
        ("Wezwanie z urzędu u klienta", "Czynności sprawdzające, kontrola albo postępowanie. Księgowa nie może być pełnomocnikiem w sporze z urzędem, doradca podatkowy tak."),
        ("Nowe obowiązki co roku", "JPK CIT, KSeF, zmiany w VAT i PIT. Zespół musi wdrożyć je u wszystkich klientów naraz, bez przestojów."),
        ("Odpowiedzialność biura", "Błąd w kwalifikacji podatkowej to ryzyko dla klienta i dla biura. Opinia doradcy podatkowego daje podkładkę."),
    ]
    helps = [
        ("art. 2 ustawy o doradztwie podatkowym", "Stała obsługa doradcza zespołu", "Twoje księgowe dzwonią i piszą do nas bezpośrednio. Odpowiadamy konkretnie, z podstawą prawną, tak żeby można było od razu zaksięgować albo odpowiedzieć klientowi.", ["Konsultacje telefoniczne, mailowe i na wideo", "Trudne księgowania, VAT, CIT, PIT, ryczałt", "Krótkie notatki z podstawą prawną do akt klienta"]),
        ("JPK_KR_PD · JPK_ST_KR", "Wdrożenie JPK CIT", "Pomagamy przygotować biuro i klientów do przesyłania ksiąg w strukturach JPK CIT. Przechodzimy z zespołem przez plan kont, znaczniki podatkowe i ewidencję środków trwałych.", ["Analiza, których klientów i od kiedy obejmuje obowiązek", "Mapowanie znaczników podatkowych na kontach", "Test pliku i uzgodnienie z CIT-8 przed wysyłką"]),
        ("KSeF · VAT · JPK_VAT", "KSeF i bieżące zmiany", "Tłumaczymy nowe przepisy na praktykę biura: co zmienić w procesach, o co zapytać klientów i jak uniknąć błędów w pierwszych miesiącach.", ["Krótkie szkolenia dla zespołu", "Odpowiedzi na pytania wdrożeniowe", "Wzory komunikatów do klientów biura"]),
        ("art. 272–274c, 282b Ordynacji", "Wezwania i kontrole Twoich klientów", "Gdy klient biura dostaje wezwanie albo kontrolę, przejmujemy kontakt z urzędem jako pełnomocnik, a Ty dalej prowadzisz księgi.", ["Odpowiedzi na wezwania w czynnościach sprawdzających", "Pełnomocnictwo w kontrolach US i KAS", "Odwołania, skargi do WSA i NSA"]),
        ("art. 14b Ordynacji podatkowej", "Interpretacje i opinie", "Przygotowujemy wnioski o interpretacje indywidualne i opinie podatkowe dla klientów biura, gdy sprawa jest niejednoznaczna.", ["Interpretacje indywidualne i WIS", "Opinie przed transakcją", "Przegląd ryzyk przed zamknięciem roku"]),
        ("sukcesja · restrukturyzacja", "Większe projekty klientów", "Przekształcenia, fundacje rodzinne, estoński CIT czy sprzedaż firmy. Prowadzimy projekt podatkowy, a biuro dostaje gotowe wytyczne do ksiąg.", ["Przekształcenie JDG w spółkę", "Fundacja rodzinna i sukcesja", "Wybór formy opodatkowania"]),
    ]
    pkgs = [
        ("Biuro Partner", "Dla małych i średnich biur, które chcą mieć doradcę podatkowego pod telefonem dla całego zespołu.", "od 419 zł", "netto / mies.", True,
         ["<b>2 godziny</b> doradztwa miesięcznie dla całego zespołu", "Bezpośredni kontakt każdej księgowej z doradcą", "Odpowiedź w ciągu 1 dnia roboczego", "Notatki z podstawą prawną do akt klienta", "Niewykorzystane godziny przechodzą na kolejny miesiąc", "Rabat na interpretacje, kontrole i sprawy klientów biura", "<b>W pakiecie:</b> baza wiedzy, wzory dokumentów i aplikacje JPK CIT"]),
        ("Biuro Plus i wdrożenie JPK CIT", "Dla większych biur i na czas wdrożenia JPK CIT albo KSeF u wielu klientów.", "wycena", "indywidualna", False,
         ["Większa pula godzin dopasowana do biura", "Wdrożenie JPK CIT: plan kont, znaczniki, test plików", "Szkolenie zespołu w biurze albo online", "Wsparcie przy pierwszych wysyłkach plików", "Stały kontakt z dwoma doradcami podatkowymi", "<b>W pakiecie:</b> baza wiedzy, wzory dokumentów i aplikacje JPK CIT"]),
    ]
    pk = []
    for t, f, price, unit, feat, li in pkgs:
        badge = '<span class="badge">Dla biur rachunkowych</span>' if feat else ""
        pk.append(f'''      <article class="variant{' featured' if feat else ''}">{badge}
        <h3>{t}</h3>
        <p class="for">{f}</p>
        <div class="price"><b>{price}</b><span class="unit">{unit}</span></div>
        <ul>{"".join(f"<li>{x}</li>" for x in li)}</ul>
        <a class="btn {'btn-primary' if feat else 'btn-ghost'}" href="{p}kontakt/#rezerwacja">Umów rozmowę dla biura</a>
      </article>''')
    body = header(p, "dla-biur-rachunkowych/") + page_hero(
        p, "Dla biur rachunkowych", "Dla biur rachunkowych",
        "Doradca podatkowy <em>dla Twojego biura</em> rachunkowego",
        "Stałe wsparcie dla zespołu księgowych, wdrożenie JPK CIT, KSeF i pomoc przy wezwaniach i kontrolach Twoich klientów. W pakiecie baza wiedzy, wzory dokumentów i aplikacje do JPK CIT. Ty prowadzisz księgi, my bierzemy na siebie trudne tematy podatkowe. Od 419 zł netto miesięcznie.",
        fx="grid") + f'''
<section class="section" aria-labelledby="pain-h">
  <div class="wrap">
{section_head("Znamy to z praktyki", "Z czym biura przychodzą do nas najczęściej", "", "pain-h")}    <div class="steps">
{chr(10).join(f'      <div class="step"><h3>{t}</h3><p>{d}</p></div>' for t, d in pains)}
    </div>
  </div>
</section>

<section class="section bg-paper2" aria-labelledby="help-h">
  <div class="wrap">
{section_head("Jak pomagamy", "Wszystkie tematy podatkowe Twojego biura w jednym miejscu", "Jesteś pierwszą linią kontaktu z klientem. My jesteśmy zapleczem doradczym, które odpowiada na trudne pytania i staje za biurem w sporze z urzędem.", "help-h")}    <div class="spec-grid three">
{chr(10).join(spec_card(*x) for x in helps)}
    </div>
  </div>
</section>

<section class="section dark" aria-labelledby="jpk-h">
  <canvas class="fx3d" data-fx="grid" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="duo">
      <div>
        <h2 id="jpk-h" style="font-size:clamp(28px,3.6vw,42px);font-weight:800;color:#fff;margin-top:14px">Wdrożenie JPK CIT bez nerwów w biurze</h2>
        <p class="lede" style="margin-top:16px">Struktury JPK_KR_PD i JPK_ST_KR pokażą urzędowi całe księgi i znaczniki podatkowe na kontach. Przygotujemy biuro tak, żeby pierwsze pliki przeszły bez korekt i bez pytań z urzędu.</p>
      </div>
      <ol class="flow" style="grid-template-columns:1fr 1fr">
        <li><b>Diagnoza</b><span>Ustalamy, których klientów i od którego roku obejmuje obowiązek.</span></li>
        <li><b>Plan kont i znaczniki</b><span>Przypisujemy znaczniki podatkowe do kont razem z Twoim zespołem.</span></li>
        <li><b>Środki trwałe</b><span>Sprawdzamy ewidencję pod strukturę JPK_ST_KR.</span></li>
        <li><b>Test i uzgodnienie</b><span>Porównujemy plik testowy z CIT-8, zanim zrobi to urząd.</span></li>
      </ol>
    </div>
  </div>
</section>

<section class="section bg-paper2" id="narzedzia" aria-labelledby="tools-h">
  <div class="wrap">
{section_head("W każdym pakiecie", "Narzędzia dla Twojego biura w cenie abonamentu", "Oprócz doradców dostajesz zaplecze, które oszczędza czas zespołu na co dzień. Dostęp mają wszystkie księgowe w biurze.", "tools-h")}    <div class="tools-grid">
      <article class="tool">
        <span class="tool-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/></svg></span>
        <h3>Baza wiedzy</h3>
        <p>Opracowania trudnych tematów podatkowych, odpowiedzi na pytania, które księgowe zadają najczęściej, i omówienia zmian w przepisach. Napisane przez doradców podatkowych, językiem praktyki biura.</p>
        <ul><li>Wyszukiwanie po temacie i podatku</li><li>Aktualizacje po każdej ważnej zmianie przepisów</li></ul>
      </article>
      <article class="tool">
        <span class="tool-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5"/></svg></span>
        <h3>Wzory dokumentów</h3>
        <p>Gotowe wzory pism, które biuro przygotowuje dla klientów: odpowiedzi na wezwania, wnioski, pełnomocnictwa, uchwały i umowy. Uzupełniasz dane klienta i dokument jest gotowy.</p>
        <ul><li>Pisma do urzędu skarbowego i KAS</li><li>Dokumenty korporacyjne spółek</li></ul>
      </article>
      <article class="tool tool-app">
        <span class="tool-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 11l3 3 8-8M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/></svg></span>
        <span class="tool-tag">Aplikacja</span>
        <h3>Weryfikacja JPK CIT</h3>
        <p>Wgrywasz plik JPK_KR_PD przed wysyłką, a aplikacja sprawdza go pod kątem błędów i braków. Zobaczysz konta bez znaczników podatkowych, niespójności i miejsca, o które może zapytać urząd.</p>
        <ul><li>Raport błędów do poprawy w programie księgowym</li><li>Mniej korekt po wysyłce pliku</li></ul>
      </article>
      <article class="tool tool-app">
        <span class="tool-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M3 3v18h18M7 15l4-4 3 3 6-6"/></svg></span>
        <span class="tool-tag">Aplikacja</span>
        <h3>Sprawozdanie do KRS z JPK CIT</h3>
        <p>Na podstawie danych z pliku JPK CIT aplikacja automatycznie przygotowuje projekt sprawozdania finansowego, w tym bilans i rachunek zysków i strat, w formacie do złożenia w KRS. Zespół tylko sprawdza i uzupełnia, zamiast przepisywać liczby.</p>
        <ul><li>Dane prosto z ksiąg, bez ręcznego przepisywania</li><li>Gotowe do weryfikacji i podpisu</li></ul>
      </article>
    </div>
  </div>
</section>

<section class="section bg-paper2" id="pakiet" aria-labelledby="pkg-h">
  <div class="wrap">
{section_head("Pakiet dla biur", "Stałe wsparcie od 419 zł netto miesięcznie", "Jeden abonament dla całego zespołu. Bez umów na rok, z miesięcznym okresem wypowiedzenia.", "pkg-h")}    <div class="variants two">
{chr(10).join(pk)}
    </div>
    <div class="pkg-perks">
      <div><b>Twoi klienci zostają u Ciebie</b><span>Działamy jako zaplecze biura. Nie przejmujemy Twoich klientów.</span></div>
      <div><b>Dwóch doradców</b><span>Twoje biuro znają dwaj doradcy podatkowi, więc zawsze ktoś odbierze.</span></div>
      <div><b>Bez umów na rok</b><span>Miesięczny okres wypowiedzenia.</span></div>
      <div><b>Pełnomocnik dla klienta</b><span>W sporze z urzędem reprezentujemy klienta biura przed US, KAS i sądami.</span></div>
    </div>
    <p class="fine">Ceny netto, do których dolicza się 23% VAT. Czas pracy liczymy w 15-minutowych odcinkach. Sprawy klientów biura, takie jak kontrole czy interpretacje, wyceniamy osobno z rabatem dla biur partnerskich.</p>
  </div>
</section>

<section class="section" aria-label="Umów spotkanie">
  <div class="wrap">
{cta_band(p, "Porozmawiajmy o współpracy z Twoim biurem", "W ciągu bezpłatnych 20 minut opowiesz nam o biurze i klientach, a my zaproponujemy zakres wsparcia i cenę.")}  </div>
</section>
'''
    return h + body + footer(p)

# ---------------------------------------------------------------- blog
LINKEDIN = "https://www.linkedin.com/company/112327069/"
MONTHS = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września", "października", "listopada", "grudnia"]


def load_posts():
    """Wpisy: content/blog/*.md z nagłówkiem (title, date, lead, category, linkedin)."""
    import glob, markdown, datetime
    posts = []
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "blog", "*.md"))):
        if os.path.basename(f).upper() == "README.MD":
            continue
        raw = open(f, encoding="utf-8").read()
        meta, body = {}, raw
        if raw.startswith("---"):
            _, fm, body = raw.split("---", 2)
            for line in fm.strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
        if meta.get("draft") == "true":
            continue
        slug = os.path.splitext(os.path.basename(f))[0]
        d = datetime.date.fromisoformat(meta["date"])
        html = markdown.markdown(body.strip(), extensions=["extra", "sane_lists"])
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        posts.append(dict(slug=slug, title=meta["title"], lead=meta.get("lead", ""), category=meta.get("category", "Podatki"),
                          linkedin=meta.get("linkedin", ""), urn=meta.get("linkedin_urn", ""), urn_h=meta.get("linkedin_height", "560"), image=meta.get("image", ""), date=d, date_h=f"{d.day} {MONTHS[d.month-1]} {d.year}",
                          html=html, minutes=max(1, round(words / 200))))
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


def li_feed():
    f = os.path.join(ROOT, "content", "blog", "linkedin.txt")
    urns = [l.strip() for l in open(f, encoding="utf-8")] if os.path.exists(f) else []
    urns = [u.split() for u in urns if u and not u.startswith("#")]
    if not urns:
        return ""
    frames = "".join(f'<div class="li-item"><iframe src="https://www.linkedin.com/embed/feed/update/{u[0]}?collapsed=1" height="{u[1] if len(u) > 1 else 600}" width="504" frameborder="0" allowfullscreen title="Wpis M2 TAX na LinkedIn" loading="lazy"></iframe></div>' for u in urns)
    return f'''<div class="li-feed">
      <div class="li-head"><h2>Najnowsze wpisy z naszego profilu</h2></div>
      <div class="li-grid">{frames}</div>
    </div>'''


def build_blog_index(posts):
    p = "../"
    h = head(p, "Blog podatkowy — M2 TAX Doradcy Podatkowi | Wrocław",
             "Artykuły doradców podatkowych M2 TAX: interpretacje, kontrole, postępowania, JPK CIT, wypłata pieniędzy ze spółki i bieżące zmiany w przepisach.",
             "blog/")
    if posts:
        def card(x, feat=False):
            img = f'<div class="pc-img"><img src="../img/blog/{x["image"]}" alt="" loading="lazy"></div>' if x["image"] else '<div class="pc-img pc-noimg"><span>§</span></div>'
            return f'''      <a class="post-card{' post-feat' if feat else ''}" href="{x["slug"]}/">
        {img}
        <div class="pc-body">
          {'<span class="pc-new">Najnowszy artykuł</span>' if feat else ''}
          <span class="post-cat">{x["category"]}</span>
          <span class="post-meta">{x["date_h"]} · {x["minutes"]} min czytania</span>
          <h3>{x["title"]}</h3>
          <p>{x["lead"]}</p>
          <span class="post-more">Czytaj artykuł <i aria-hidden="true">→</i></span>
        </div>
      </a>'''
        listing = '<div class="post-grid post-grid-2">\n' + "\n".join(card(x) for x in posts) + "\n    </div>"
    else:
        listing = f'''<div class="post-empty"><b>Pierwsze artykuły już wkrótce</b><span>Do tego czasu nasze komentarze do zmian w przepisach znajdziesz na <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>.</span></div>'''
    body = header(p, "blog/") + page_hero(
        p, "Blog", "Blog podatkowy",
        "Podatki <em>w praktyce</em>",
        "Rozbudowane wersje naszych wpisów z LinkedIn. Piszemy o tym, z czym klienci przychodzą do nas na co dzień: wezwania z urzędu, kontrole, interpretacje, JPK CIT i wypłata pieniędzy ze spółki.",
        fx="grid", cta=False) + f'''
<section class="section" aria-label="Artykuły">
  <div class="wrap">
    {listing}
    {li_feed()}
    <p class="post-follow">Obserwuj nas na <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>, żeby nie przegapić nowych wpisów.</p>
  </div>
</section>
'''
    return h + body + footer(p)


def build_post(x, posts):
    p = "../../"
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": x["title"], "description": x["lead"],
          "datePublished": x["date"].isoformat(), "inLanguage": "pl",
          "author": [{"@type": "Person", "name": "Michał Ruszniak"}, {"@type": "Person", "name": "Marcin Otręba"}],
          "publisher": {"@type": "Organization", "name": "M2 TAX Doradcy Podatkowi", "logo": SITE + "/img/logo.png"},
          "mainEntityOfPage": f"{SITE}/blog/{x['slug']}/"}
    h = head(p, f"{x['title']} | Blog M2 TAX", x["lead"], f"blog/{x['slug']}/", extra_ld=ld)
    li = f'<a class="post-li" href="{x["linkedin"]}" target="_blank" rel="noopener">Dyskusja pod wpisem na LinkedIn →</a>' if x["linkedin"] else ""
    more = [y for y in posts if y["slug"] != x["slug"]][:3]
    more_html = ""
    if more:
        more_html = '<aside class="post-more-list"><h2>Przeczytaj też</h2><div class="post-grid">' + "".join(
            f'<a class="post-card" href="../{y["slug"]}/"><span class="post-meta">{y["date_h"]}</span><h3>{y["title"]}</h3><span class="post-more">Czytaj →</span></a>' for y in more) + "</div></aside>"
    body = header(p, "blog/") + f'''<section class="page-hero post-hero">
  <canvas class="fx3d" data-fx="grid" aria-hidden="true"></canvas>
  <div class="wrap">
    <p class="crumbs"><a href="{p}">Strona główna</a> / <a href="../">Blog</a></p>
    <span class="eyebrow" style="display:block;margin-top:22px">{x["category"]}</span>
    <h1>{x["title"]}</h1>
    <p class="post-meta">{x["date_h"]} · {x["minutes"]} min czytania · Michał Ruszniak, Marcin Otręba</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <article class="prose">
      {f'<figure class="post-img"><img src="{p}img/blog/{x["image"]}" alt="{x["title"]}" loading="eager"></figure>' if x["image"] else ""}
      <p class="prose-lead">{x["lead"]}</p>
{x["html"]}
      {f'<figure class="post-embed"><iframe src="https://www.linkedin.com/embed/feed/update/{x["urn"]}?collapsed=1" height="{x["urn_h"]}" width="504" frameborder="0" allowfullscreen title="Wpis M2 TAX na LinkedIn" loading="lazy"></iframe><figcaption>Oryginalny wpis na LinkedIn</figcaption></figure>' if x["urn"] else ""}
      <div class="post-foot">
        <p><b>Masz podobną sprawę?</b> Pierwsze 20 minut rozmowy z doradcą podatkowym jest bezpłatne.</p>
        <a class="btn btn-primary" href="{p}kontakt/#rezerwacja">Umów bezpłatne 20 minut</a>
        {li}
      </div>
      <p class="fine">Artykuł ma charakter informacyjny i nie stanowi porady podatkowej w konkretnej sprawie. Stan prawny na dzień publikacji.</p>
    </article>
    {more_html}
  </div>
</section>
'''
    return h + body + footer(p)


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if rel.endswith(".html"):
        # strzałki: Montserrat ma bardzo małą strzałkę, więc rysujemy ją krojem tekstu
        html = re.sub(r">([^<]*)", lambda m: ">" + m.group(1).replace("→", '<span class="arw">→</span>').replace("←", '<span class="arw">←</span>'), html)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("zapisano", rel)


def sitemap():
    urls = ["", "abonamenty/", "dla-biur-rachunkowych/", "doradztwo-podatkowe/", "zespol/", "blog/", "kontakt/"] + [f"blog/{x['slug']}/" for x in load_posts()] + [ "polityka-prywatnosci.html", "aml.html"]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", x)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    write("index.html", build_home())
    write("abonamenty/index.html", build_abonamenty())
    write("doradztwo-podatkowe/index.html", build_specjalizacje())
    write("zespol/index.html", build_zespol())
    write("kontakt/index.html", build_kontakt())
    write("dla-biur-rachunkowych/index.html", build_biura())
    posts = load_posts()
    write("blog/index.html", build_blog_index(posts))
    for x in posts:
        write(f"blog/{x['slug']}/index.html", build_post(x, posts))
    sitemap()
