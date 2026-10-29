#!/usr/bin/env python3
"""Generator strony M2 TAX.

Buduje strony z jednego miejsca, żeby menu, stopka i nagłówek były wszędzie takie same:
  index.html, abonamenty/index.html, doradztwo-podatkowe/index.html, zespol/index.html, kontakt/index.html
Wspólne style: assets/site.css, wspólne skrypty: assets/site.js.

Uruchom z katalogu repozytorium:  python3 tools/build.py
Folder tools/ nie jest publikowany (.vercelignore).
"""
import json, os

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
]
NAV = [("abonamenty/", "Abonamenty"), ("doradztwo-podatkowe/", "Doradztwo podatkowe"), ("dla-biur-rachunkowych/", "Dla biur rachunkowych"), ("zespol/", "Zespół"), ("kontakt/", "Kontakt")]

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
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
    <a class="logo" href="{p or './'}" aria-label="M2 TAX Doradcy Podatkowi — strona główna"><img src="{p}img/logo.png" alt="M2 TAX Doradcy Podatkowi" width="900" height="302"></a>
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
      <p>Kancelaria doradztwa podatkowego z Wrocławia. Obsługujemy klientów z miejscowości: {towns}.</p>
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
<script src="{p}assets/site.js"></script>{z}{salesiq()}
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
    <span class="eyebrow" style="display:block;margin-top:22px">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>{c}
  </div>
</section>
'''


def section_head(eyebrow, h2, lede="", hid="", light=False):
    st = ' style="color:#fff"' if light else ""
    l = f'\n      <p class="lede">{lede}</p>' if lede else ""
    return f'''    <div class="section-head">
      <span class="eyebrow">{eyebrow}</span>
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
    ("UPO · rezydencja · CFC", "Podatki międzynarodowe", "Praca i działalność za granicą, kontrahenci zagraniczni i przeniesienie rezydencji podatkowej.", ["Rezydencja podatkowa i certyfikaty", "Umowy o unikaniu podwójnego opodatkowania", "Podatek u źródła i transakcje z podmiotami zagranicznymi"]),
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
    ("Czy obsługujecie klientów spoza Wrocławia?", "Tak. Na co dzień pracujemy z klientami z Wrocławia, Siechnic, Kobierzyc, Żórawiny, Środy Śląskiej i Trzebnicy. Spotkania odbywają się w kancelarii przy ul. Zwycięskiej 3 lub ul. Artemskiej 11, u klienta w firmie albo online, a pełnomocnikiem możemy być przed każdym urzędem i sądem w Polsce."),
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
    return "\n".join(f'''      <details open>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''' for q, a in items)


def spec_card(ref, t, d, li, tag="article", h="h4"):
    return f'      <{tag} class="spec"><span class="ref">{ref}</span><{h}>{t}</{h}><p>{d}</p><ul>' + "".join(f"<li>{x}</li>" for x in li) + f"</ul></{tag}>"


def towns_html():
    return "\n".join(f'      <div class="town">{PIN.replace("<svg ", "<svg ")}<b>{t}</b><span>{s}</span></div>' for t, s in TOWNS)


def sol_cards(p):
    out = []
    for n, t, d, price, unit, href, feat in SOLUTIONS:
        out.append(f'''      <a class="sol{' featured' if feat else ''}" href="{p}{href}">
        <span class="num">{n}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="price-tag">{price}<small>{unit}</small></div>
      </a>''')
    return "\n".join(out)


def duo_section(p, show_link=True, portraits=False):
    link = f'\n        <a class="more-link" href="{p}zespol/" style="color:var(--accent)">Poznaj doradców →</a>' if show_link else ""
    if portraits:
        visual = f'''      <figure class="duo-blend">
        <img src="{p}img/doradcy-duo.jpg" alt="Doradcy podatkowi Michał Ruszniak i Marcin Otręba" width="1000" height="1200" loading="lazy">
        <figcaption>Michał Ruszniak · Marcin Otręba<span>doradcy podatkowi nr 15009 i 14609</span></figcaption>
      </figure>'''
    else:
        visual = f'''      <figure class="duo-blend">
        <img src="{p}img/doradcy-togi-3.jpg" alt="Doradcy podatkowi Michał Ruszniak i Marcin Otręba w togach" width="1000" height="1200" loading="lazy">
        <figcaption>Michał Ruszniak · Marcin Otręba<span>doradcy podatkowi nr 15009 i 14609</span></figcaption>
      </figure>'''
    return f'''<section class="section dark" aria-labelledby="duo-h">
  <canvas class="fx3d" data-fx="rings" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="duo">
{visual}
      <div>
        <span class="eyebrow">Nasza zasada</span>
        <h2 id="duo-h" style="font-size:clamp(28px,3.6vw,42px);font-weight:800;color:#fff;margin-top:14px">Każdą sprawą zajmuje się dwóch doradców podatkowych</h2>
        <p class="lede" style="margin-top:16px">Obaj znamy Twoją sprawę i wiemy, co się w niej dzieje. Nie tłumaczysz wszystkiego od nowa nowej osobie.</p>
        <div class="duo-points">
          <div class="duo-card"><b>Zawsze ktoś odbierze</b><span>Urlop, rozprawa czy kontrola u innego klienta nie zatrzymują Twojej sprawy.</span></div>
          <div class="duo-card"><b>Druga para oczu</b><span>Każde ważne pismo, odwołanie i opinię sprawdza drugi doradca przed wysłaniem.</span></div>
          <div class="duo-card"><b>Dwa doświadczenia</b><span>Praktyka biznesowa i lata pracy w administracji skarbowej przy jednym stole.</span></div>
        </div>{link}
      </div>
    </div>
  </div>
</section>
'''


# ---------------------------------------------------------------- strony
def build_home():
    p = ""
    h = head(p, "M2 TAX — Doradcy Podatkowi | Wrocław, Siechnice, Kobierzyce",
             "Kancelaria doradztwa podatkowego M2 TAX we Wrocławiu. Stała obsługa podatkowa od 369 zł netto miesięcznie, konsultacje, kontrole i postępowania podatkowe, sprawy przed WSA i NSA. Dwóch doradców w każdej sprawie. Bezpłatne 20 minut.",
             "")
    body = header(p, "") + f'''<section class="hero">
  <canvas class="fx3d" data-fx="network" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">Kancelaria doradztwa podatkowego · Wrocław</span>
      <h1>Twoje podatki, <em>nasza pasja.</em></h1>
      <p class="lede">Znajdziemy legalne sposoby, by firma nie płaciła więcej, niż musi. Stała obsługa podatkowa firm, konsultacje dla osób prywatnych, kontrole, postępowania i sprawy przed sądami administracyjnymi. Każdą sprawą zajmuje się dwóch doradców podatkowych.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="kontakt/#rezerwacja">Umów bezpłatne 20 minut</a>
        <a class="btn btn-ghost" href="abonamenty/">Abonamenty od 369 zł</a>
      </div>
      <div class="hero-facts">
        <div><b>2</b><span>doradców podatkowych w każdej sprawie</span></div>
        <div><b>20 min</b><span>pierwszej konsultacji bez opłat</span></div>
        <div><b>369 zł</b><span>netto miesięcznie za stałą obsługę</span></div>
      </div>
    </div>
    <div class="seal" aria-hidden="true">
      <div class="seal-glow"></div><div class="seal-ring"></div><div class="seal-ring seal-ring2"></div>
      <svg class="seal-txt" viewBox="0 0 400 400"><defs><path id="sealp" d="M200,200 m-171,0 a171,171 0 1,1 342,0 a171,171 0 1,1 -342,0"/></defs>
        <text font-size="12.5" fill="currentColor"><textPath href="#sealp" textLength="1068" lengthAdjust="spacing">DORADCY PODATKOWI · NR 15009 · NR 14609 · WROCŁAW · KANCELARIA DORADZTWA PODATKOWEGO · </textPath></text></svg>
      <span class="seal-tick"></span>
      <div class="seal-core"><img src="img/logo-light.png" alt="" width="900" height="302"><div class="seal-ln"></div><small>Wrocław</small></div>
    </div>
  </div>
</section>

<section class="alarm" aria-labelledby="alarm-h">
  <div class="wrap">
    <div>
      <h2 id="alarm-h">Dostałeś pismo bądź telefon z urzędu? Ochłoń i zadzwoń do nas.</h2>
      <p>Zanim odpowiesz urzędnikowi, złożysz wyjaśnienia albo wyślesz dokumenty, porozmawiaj z doradcą. Pierwsze 20 minut rozmowy nic nie kosztuje.</p>
    </div>
    <div class="callcard">
      <span class="ref">Telefony kancelarii</span>
      <a class="phone" href="tel:{TEL1}">{TEL1_H}</a>
      <a class="phone" href="tel:{TEL2}">{TEL2_H}</a>
      <div class="callrow">
        <button class="copy" data-copy="{TEL1_H}" type="button">Kopiuj numer 1</button>
        <button class="copy" data-copy="{TEL2_H}" type="button">Kopiuj numer 2</button>
        <button class="copy" data-copy="{MAIL}" type="button">Kopiuj e-mail: {MAIL}</button>
      </div>
    </div>
  </div>
</section>

<section class="section" id="rozwiazania" aria-labelledby="sol-h">
  <div class="wrap">
{section_head("Jak możemy pomóc", "Cztery sposoby współpracy z doradcą podatkowym", "Wybierz to, czego potrzebujesz teraz. Możesz zacząć od jednej konsultacji, a z czasem przejść na stałą obsługę.", "sol-h")}    <div class="sol-grid">
{sol_cards(p)}
    </div>
    <a class="more-link" href="abonamenty/">Zobacz szczegóły abonamentów i cen →</a>
  </div>
</section>

{duo_section(p, portraits=True)}
<section class="section" aria-label="Dla biur rachunkowych" style="padding-bottom:0">
  <div class="wrap">
    <div class="cta-band">
      <div><span class="eyebrow">Dla biur rachunkowych</span><h3 style="margin-top:8px">Prowadzisz biuro rachunkowe? Zostań naszym partnerem</h3><p>Stałe wsparcie doradców podatkowych dla Twojego zespołu, wdrożenie JPK CIT i pomoc przy kontrolach Twoich klientów. Od 419 zł netto miesięcznie.</p></div>
      <div class="hero-cta"><a class="btn btn-primary" href="dla-biur-rachunkowych/">Zobacz ofertę dla biur</a></div>
    </div>
  </div>
</section>
<section class="section bg-paper2" id="specjalizacje" aria-labelledby="spec-h">
  <div class="wrap">
{section_head("Specjalizacje", "W czym pomagamy najczęściej", "Interpretacje, kontrole i czynności sprawdzające to nasza codzienność. Do tego wypłata pieniędzy ze spółki, restrukturyzacje, fundacje rodzinne i nieruchomości.", "spec-h")}    <div class="spec-grid">
{chr(10).join(spec_card(*s) for s in [(PILLARS[0][0], PILLARS[0][1], "Ochrona przed zmianą zdania urzędu, zanim podejmiesz decyzję.", ["Interpretacje w CIT, PIT, VAT i PCC", "Wiążące informacje stawkowe", "Opinie zabezpieczające"]), (PILLARS[1][0], PILLARS[1][1], "Pełnomocnik od pierwszego pisma aż do wyroku sądu.", ["Kontrole US i KAS", "Odwołania i zażalenia", "Skargi do WSA i NSA"]), (PILLARS[2][0], PILLARS[2][1], "Odpowiedź, która zamyka sprawę, zanim zrobi się z niej kontrola.", ["Wezwania do wyjaśnień", "Weryfikacja zwrotu VAT", "Rozmowy z urzędem za Ciebie"])] + SPECS[:5])}
    </div>
    <a class="more-link" href="doradztwo-podatkowe/">Wszystkie specjalizacje i branże →</a>
  </div>
</section>

<section class="section" id="branze" aria-labelledby="br-h">
  <div class="wrap">
{section_head("Branże", "Znamy specyfikę Twojej branży", "Doświadczenie z konkretnych sektorów oznacza mniej tłumaczenia i szybsze, trafniejsze odpowiedzi.", "br-h")}    <div class="branch-grid">
{chr(10).join(spec_card(*b) for b in BRANCHES)}
      <a class="sol" href="kontakt/#rezerwacja" style="justify-content:center"><span class="num">Twoja branża?</span><h3>Nie widzisz swojej branży?</h3><p>Zadzwoń albo umów bezpłatne 20 minut. Powiemy, czy i jak możemy pomóc.</p><div class="price-tag">Umów rozmowę →</div></a>
    </div>
  </div>
</section>

<section class="section bg-paper2" id="pismo" aria-labelledby="pismo-h">
  <div class="wrap">
{section_head("Pismo z urzędu", "Co robimy, kiedy przyniesiesz nam pismo z urzędu", "Większość sporów z fiskusem da się ustawić na samym początku. Liczy się termin i to, co trafi do akt jako pierwsze.", "pismo-h")}    <div class="steps">
      <div class="step"><h3>Sprawdzamy termin</h3><p>Ustalamy, co to za pismo, od kiedy biegnie termin i ile czasu realnie zostało. Wystarczy zdjęcie lub skan.</p></div>
      <div class="step"><h3>Wstrzymujemy pochopne ruchy</h3><p>Nie składasz ustnych wyjaśnień przez telefon i nie wysyłasz dokumentów bez selekcji. To, co raz trafi do akt, zostaje w aktach.</p></div>
      <div class="step"><h3>Przejmujemy kontakt z urzędem</h3><p>Zgłaszamy pełnomocnictwo i od tej chwili korespondencja z organem idzie przez doradcę podatkowego.</p></div>
      <div class="step"><h3>Prowadzimy sprawę do końca</h3><p>Odpowiedzi na wezwania, zastrzeżenia do protokołu, odwołanie, skarga do WSA i skarga kasacyjna do NSA.</p></div>
    </div>
    <div class="letters" aria-label="Najczęstsze pisma">
      <div class="letter"><span class="ref">art. 274c Ordynacji podatkowej</span><b>Wezwanie do złożenia wyjaśnień</b><span>w ramach czynności sprawdzających</span></div>
      <div class="letter"><span class="ref">art. 282b Ordynacji podatkowej</span><b>Zawiadomienie o zamiarze wszczęcia kontroli</b><span>kontrola rusza nie wcześniej niż po 7 dniach</span></div>
      <div class="letter"><span class="ref">art. 165 Ordynacji podatkowej</span><b>Postanowienie o wszczęciu postępowania</b><span>od tej chwili liczy się każde pismo i dowód</span></div>
      <div class="letter"><span class="ref">art. 223 § 2 Ordynacji podatkowej</span><b>Decyzja organu I instancji</b><span>14 dni na odwołanie od doręczenia</span></div>
    </div>
  </div>
</section>

<section class="section" id="obszar" aria-labelledby="area-h">
  <div class="wrap">
{section_head("Zakres działania", "Doradca podatkowy we Wrocławiu i okolicach", "Spotykamy się w kancelarii przy ul. Zwycięskiej 3 lub ul. Artemskiej 11 we Wrocławiu, u Ciebie w firmie albo online.", "area-h")}    <div class="towns">
{towns_html()}
    </div>
    <p class="area-note">Pełnomocnikiem możemy być przed każdym urzędem skarbowym, KAS i sądem administracyjnym w Polsce, więc z naszych usług korzystają też klienci spoza Dolnego Śląska.</p>
  </div>
</section>

<section class="section bg-paper2" id="faq" aria-labelledby="faq-h">
  <div class="wrap faq-wrap">
{section_head("FAQ", "Najczęściej zadawane pytania", "Odpowiedzi, które pomogą zrozumieć, jak pracujemy.", "faq-h")}    <div class="faq">
{faq_html(FAQ_HOME)}
    </div>
  </div>
</section>

<section class="section" aria-label="Umów spotkanie">
  <div class="wrap">
{cta_band(p, "Porozmawiajmy o Twojej sprawie", "Pierwsze 20 minut jest bezpłatne. Powiemy, jakie rozwiązanie pasuje do Twojej sytuacji i ile będzie kosztować.")}  </div>
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
         ["<b>2 godziny</b> doradztwa miesięcznie", "Pytania telefonicznie, mailowo i na wideo", "Odpowiedź w ciągu 2 dni roboczych", "Analiza umów i transakcji przed podpisaniem", "Przegląd pism z urzędu i plan działania", "Dwóch doradców znających Twoją firmę"]),
        ("Doradztwo podatkowe + Wsparcie Twojej księgowości", "Dla firm z własną księgową lub biurem rachunkowym. Twoja księgowa ma bezpośredni kontakt z doradcą podatkowym.", "od 590 zł", "netto / mies.", True,
         ["<b>3 godziny</b> doradztwa miesięcznie", "Twoja księgowa pisze i dzwoni do nas bezpośrednio", "Konsultowanie trudnych księgowań i rozliczeń VAT", "Przegląd kluczowych pozycji przed zeznaniem rocznym", "Odpowiedzi na wezwania w czynnościach sprawdzających", "Odpowiedź w ciągu 1 dnia roboczego"]),
        ("Doradztwo Biznes", "Dla spółek i firm rodzinnych, które regularnie podejmują decyzje z konsekwencjami podatkowymi.", "od 890 zł", "netto / mies.", False,
         ["<b>5 godzin</b> doradztwa miesięcznie", "Wszystko z pakietu „Doradztwo podatkowe + Wsparcie Twojej księgowości”", "Spotkanie podatkowe raz na kwartał", "Planowanie wypłat ze spółki i inwestycji", "Pierwszeństwo terminów w sprawach pilnych", "Odpowiedź w ciągu 1 dnia roboczego"]),
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
{section_head("Przegląd", "Wybierz rozwiązanie", "", "ov-h")}    <div class="sol-grid">
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

<section class="section" id="branze" aria-labelledby="br-h">
  <div class="wrap">
{section_head("Branże", "Branże, w których mamy doświadczenie", "Każda branża ma swoje pułapki podatkowe. Te znamy z codziennej pracy z klientami.", "br-h")}    <div class="branch-grid">
{chr(10).join(spec_card(*b) for b in BRANCHES)}
      <a class="sol" href="{p}kontakt/#rezerwacja" style="justify-content:center"><span class="num">Twoja branża?</span><h3>Nie widzisz swojej branży?</h3><p>Zadzwoń albo umów bezpłatne 20 minut. Powiemy, czy i jak możemy pomóc.</p><div class="price-tag">Umów rozmowę →</div></a>
    </div>
  </div>
</section>

<section class="section bg-paper2" id="obszar" aria-labelledby="area-h">
  <div class="wrap">
{section_head("Zakres działania", "Wrocław i okolice", "Spotykamy się w kancelarii przy ul. Zwycięskiej 3 lub ul. Artemskiej 11 we Wrocławiu, u Ciebie w firmie albo online.", "area-h")}    <div class="towns">
{towns_html()}
    </div>
  </div>
</section>

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
             "Umów spotkanie z doradcą podatkowym online. M2 TAX, ul. Zwycięska 3, 53-033 Wrocław, tel. 883 643 565, 534 909 534, kancelaria@m2tax.pl. Obsługujemy Wrocław, Siechnice, Kobierzyce, Żórawinę, Środę Śląską i Trzebnicę.",
             "kontakt/")
    body = header(p, "kontakt/") + f'''<section class="section bk-section" id="rezerwacja" aria-labelledby="bk-h">
  <canvas class="fx3d" data-fx="wave" aria-hidden="true"></canvas>
  <div class="wrap bk-wrap">
    <div class="bk-intro">
      <p class="crumbs"><a href="{p}">Strona główna</a> / Kontakt</p>
      <span class="eyebrow">Rezerwacja online</span>
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
        <div class="map">
          <iframe title="Mapa dojazdu do kancelarii M2 TAX" src="https://maps.google.com/maps?q=ul.+Zwyci%C4%99ska+3,+53-033+Wroc%C5%82aw&amp;z=15&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        <a class="maplink" href="https://www.google.com/maps/search/?api=1&amp;query=ul.+Zwyci%C4%99ska+3+Wroc%C5%82aw" target="_blank" rel="noopener">Otwórz w Mapach Google ↗</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="obszar" aria-labelledby="area-h">
  <div class="wrap">
{section_head("Zakres działania", "Obsługujemy klientów z Wrocławia i okolic", "", "area-h")}    <div class="towns">
{towns_html()}
    </div>
    <p class="area-note">Spotkania online prowadzimy z klientami z całej Polski.</p>
  </div>
</section>
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
        <span class="eyebrow">JPK CIT</span>
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

def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("zapisano", rel)


def sitemap():
    urls = ["", "abonamenty/", "dla-biur-rachunkowych/", "doradztwo-podatkowe/", "zespol/", "kontakt/", "polityka-prywatnosci.html", "aml.html"]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", x)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    write("index.html", build_home())
    write("abonamenty/index.html", build_abonamenty())
    write("doradztwo-podatkowe/index.html", build_specjalizacje())
    write("zespol/index.html", build_zespol())
    write("kontakt/index.html", build_kontakt())
    write("dla-biur-rachunkowych/index.html", build_biura())
    sitemap()
