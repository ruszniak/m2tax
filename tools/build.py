#!/usr/bin/env python3
"""Generator strony M2 TAX.

Buduje strony z jednego miejsca, żeby menu, stopka i nagłówek były wszędzie takie same:
  index.html, abonamenty/index.html, specjalizacje/index.html, zespol/index.html, kontakt/index.html
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
ZOHO_EMBED = "https://m2taxdoradcypodatkowi.zohobookings.eu/portal-embed#/m2taxdoradcypodatkowi"
ZOHO_PUBLIC = "https://m2taxdoradcypodatkowi.zohobookings.eu/#/m2taxdoradcypodatkowi"
TOWNS = [
    ("Wrocław", "kancelaria przy ul. Zwycięskiej 3"),
    ("Siechnice", "gmina Siechnice"),
    ("Kobierzyce", "gmina Kobierzyce"),
    ("Żórawina", "gmina Żórawina"),
    ("Środa Śląska", "powiat średzki"),
    ("Trzebnica", "powiat trzebnicki"),
]
NAV = [("abonamenty/", "Abonamenty"), ("specjalizacje/", "Specjalizacje"), ("zespol/", "Zespół"), ("kontakt/", "Kontakt")]

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
        <li>ul. Zwycięska 3<br>53-033 Wrocław</li>
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
<script src="{p}assets/site.js"></script>{z}
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
    ("01", "Stała obsługa podatkowa", "Abonament z dwoma doradcami podatkowymi pod telefonem. Do wyboru trzy warianty: samo doradztwo, doradztwo z księgowością naszych partnerów albo doradztwo wspólnie z Twoją księgowością.", "od 369 zł", "netto miesięcznie", "abonamenty/#stala-obsluga", True),
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
    ("michal-ruszniak.jpg", 1000, 857, "Michał Ruszniak", "15009",
     ["Założył kilkadziesiąt działalności gospodarczych i spółek prawa handlowego, więc zna podatki z przepisów i z codziennego prowadzenia firmy", "Specjalizuje się w obsłudze małych i średnich przedsiębiorstw oraz firm rodzinnych", "Pełnomocnik zawodowy w kontrolach, postępowaniach podatkowych i przed sądami administracyjnymi", "Prelegent ogólnopolskich konferencji naukowych poświęconych postępowaniom podatkowym", "Juror w finałach krajowych konkursów wiedzy o podatkach"]),
    ("marcin-otreba.jpg", 753, 1024, "Marcin Otręba", "14609",
     ["Wieloletni pracownik Izby Skarbowej we Wrocławiu, trener Ministerstwa Finansów i Centrum Edukacji Zawodowej Resortu Finansów", "Doświadczenie na stanowiskach kierowniczych w międzynarodowych firmach z SSE i w renomowanych kancelariach podatkowych", "Od 2010 r. wykładowca prawa podatkowego na Uniwersytecie WSB Merito we Wrocławiu, kierownik merytoryczny studiów podyplomowych „Doradca podatkowy”, wykładowca MBA", "Szkoli Administrację Skarbową i oddziały Stowarzyszenia Księgowych w Polsce; autor publikacji m.in. dla Biuletynu VAT (INFOR)", "Specjalizuje się w VAT, CIT i PIT oraz w kontrolach podatkowych, celno-skarbowych i sporach przed sądami administracyjnymi"]),
]

FAQ_HOME = [
    ("Czym różni się doradca podatkowy od księgowego?", "Księgowy prowadzi księgi. Doradca podatkowy może legalnie doradzać w sprawach podatkowych, wydawać opinie i reprezentować klienta przed urzędami skarbowymi, KAS i sądami administracyjnymi. Odpowiada za swoje porady i ma obowiązkowe ubezpieczenie OC."),
    ("Dlaczego Waszą sprawą zajmuje się dwóch doradców?", "Każda sprawa przechodzi przez ręce dwóch doradców podatkowych. Obaj znają Twoją sytuację, więc zawsze masz z kim porozmawiać, także w czasie urlopu czy rozprawy jednego z nas. Ważne pisma i opinie sprawdza drugi doradca."),
    ("Mam kontrolę z urzędu skarbowego. Co robić?", "Zachować spokój i zadzwonić do doradcy. Doradca podatkowy może reprezentować Cię przed US i KAS, w postępowaniu podatkowym, czynnościach sprawdzających i przed sądami administracyjnymi."),
    ("Ile kosztują usługi doradcy podatkowego?", "Stała obsługa w abonamencie kosztuje od 369 zł netto miesięcznie, a konsultacja indywidualna od 400 zł netto za godzinę. Postępowania, kontrole i sprawy sądowe wyceniamy po zapoznaniu się z pismami. Pierwsze 20 minut rozmowy jest bezpłatne."),
    ("Czy obsługujecie klientów spoza Wrocławia?", "Tak. Na co dzień pracujemy z klientami z Wrocławia, Siechnic, Kobierzyc, Żórawiny, Środy Śląskiej i Trzebnicy. Spotkania odbywają się w kancelarii przy ul. Zwycięskiej 3 albo online, a pełnomocnikiem możemy być przed każdym urzędem i sądem w Polsce."),
    ("Ile trwa uzyskanie interpretacji indywidualnej?", "Dyrektor KIS ma 3 miesiące od wpływu kompletnego wniosku. Opłata to 40 zł od każdego stanu faktycznego lub zdarzenia przyszłego. Brak interpretacji w terminie oznacza, że stanowisko wnioskodawcy uznaje się za prawidłowe."),
]

FAQ_ABO = [
    ("Na jak długo zawieramy umowę abonamentową?", "Umowę zawieramy na czas nieokreślony z miesięcznym okresem wypowiedzenia. Zakres i cenę ustalamy po krótkiej rozmowie o Twojej firmie."),
    ("Czym różnią się warianty stałej obsługi?", "W pierwszym wariancie dostajesz samo doradztwo podatkowe. W drugim księgi prowadzi nasze partnerskie biuro rachunkowe, a my weryfikujemy rozliczenia. W trzecim pracujemy z Twoją obecną księgowością, więc nie musisz niczego zmieniać."),
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
        visual = f'''      <div class="duo-visual">
        <img src="{p}img/michal-ruszniak.jpg" alt="Michał Ruszniak, doradca podatkowy" loading="lazy">
        <img src="{p}img/marcin-otreba.jpg" alt="Marcin Otręba, doradca podatkowy" loading="lazy">
      </div>'''
    else:
        visual = f'''      <figure class="duo-photo">
        <img src="{p}img/doradcy-togi.jpg" alt="Doradcy podatkowi Michał Ruszniak i Marcin Otręba w togach" width="1200" height="896" loading="lazy">
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
    <figure class="hero-photo" aria-label="Partnerzy kancelarii">
      <img src="img/doradcy-togi.jpg" alt="Doradcy podatkowi Michał Ruszniak i Marcin Otręba w togach" width="1200" height="896" fetchpriority="high">
      <figcaption><b>Michał Ruszniak</b><span>DP nr 15009</span></figcaption>
      <figcaption class="r"><b>Marcin Otręba</b><span>DP nr 14609</span></figcaption>
    </figure>
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
<section class="section bg-paper2" id="specjalizacje" aria-labelledby="spec-h">
  <div class="wrap">
{section_head("Specjalizacje", "W czym pomagamy najczęściej", "Interpretacje, kontrole i czynności sprawdzające to nasza codzienność. Do tego wypłata pieniędzy ze spółki, restrukturyzacje, fundacje rodzinne i nieruchomości.", "spec-h")}    <div class="spec-grid">
{chr(10).join(spec_card(*s) for s in [(PILLARS[0][0], PILLARS[0][1], "Ochrona przed zmianą zdania urzędu, zanim podejmiesz decyzję.", ["Interpretacje w CIT, PIT, VAT i PCC", "Wiążące informacje stawkowe", "Opinie zabezpieczające"]), (PILLARS[1][0], PILLARS[1][1], "Pełnomocnik od pierwszego pisma aż do wyroku sądu.", ["Kontrole US i KAS", "Odwołania i zażalenia", "Skargi do WSA i NSA"]), (PILLARS[2][0], PILLARS[2][1], "Odpowiedź, która zamyka sprawę, zanim zrobi się z niej kontrola.", ["Wezwania do wyjaśnień", "Weryfikacja zwrotu VAT", "Rozmowy z urzędem za Ciebie"])] + SPECS[:5])}
    </div>
    <a class="more-link" href="specjalizacje/">Wszystkie specjalizacje i branże →</a>
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
{section_head("Zakres działania", "Doradca podatkowy we Wrocławiu i okolicach", "Spotykamy się w kancelarii przy ul. Zwycięskiej 3 we Wrocławiu albo online.", "area-h")}    <div class="towns">
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
             "Stała obsługa podatkowa od 369 zł netto miesięcznie w trzech wariantach, konsultacje od 400 zł netto za godzinę, prowadzenie kontroli i postępowań podatkowych, sprawy przed WSA i NSA. Dwóch doradców w każdej sprawie.",
             "abonamenty/")
    variants = [
        ("Doradztwo podatkowe", "Dla firm, które mają uporządkowaną księgowość i potrzebują doradcy pod telefonem.", "od 369 zł", "netto / mies.", False,
         ["Pytania telefonicznie, mailowo i na wideo", "Analiza umów i transakcji przed podpisaniem", "Odpowiedzi na wezwania w czynnościach sprawdzających", "Przegląd pism z urzędu i plan działania", "Dwóch doradców znających Twoją firmę"]),
        ("Doradztwo z księgowością partnera", "Księgi prowadzi nasze sprawdzone biuro partnerskie, a my jako doradcy weryfikujemy rozliczenia.", "od 790 zł", "netto / mies.", True,
         ["Wszystko z wariantu „Doradztwo podatkowe”", "Księgowość prowadzona przez biuro partnerskie", "Weryfikacja rozliczeń przez doradcę podatkowego", "Jeden punkt kontaktu w sprawach podatkowych", "Przegląd przed zamknięciem roku"]),
        ("Doradztwo z Twoją księgowością", "Zostajesz przy obecnym biurze lub księgowej, a my stale z nimi współpracujemy.", "wycena", "indywidualna", False,
         ["Wszystko z wariantu „Doradztwo podatkowe”", "Stały kontakt z Twoją księgową lub biurem", "Konsultowanie trudnych księgowań i rozliczeń", "Regularne przeglądy podatkowe", "Nic nie musisz zmieniać w obecnej obsłudze"]),
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
        <a class="btn {btn}" href="{p}kontakt/#rezerwacja">Zapytaj o ten wariant</a>
      </article>''')
    svc = [
        ("konsultacja", "02", "Konsultacja indywidualna", "Jednorazowa rozmowa o konkretnej sprawie, bez umowy na stałe. Dobra na początek współpracy albo dla osób, które nie prowadzą działalności, np. przy sprzedaży mieszkania czy działki.", "od 400 zł", "netto za godzinę · pierwsze 20 minut bezpłatnie",
         ["Spotkanie w kancelarii przy ul. Zwycięskiej 3 albo online", "Analiza dokumentów przed spotkaniem", "Konkretne wnioski i dalsze kroki na piśmie", "Wycena dalszej pracy, jeśli będzie potrzebna"]),
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
        "Cztery sposoby współpracy: stały abonament w trzech wariantach, konsultacja indywidualna, prowadzenie postępowań i kontroli oraz sprawy przed sądami administracyjnymi. W każdej sprawie pracuje dwóch doradców podatkowych.",
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
{section_head("01 · Stała obsługa", "Stała obsługa podatkowa w trzech wariantach", "Dzwonisz albo piszesz, kiedy masz pytanie, zanim podpiszesz umowę, wystawisz fakturę czy wypłacisz pieniądze ze spółki. Odpowiada doradca podatkowy, nie infolinia.", "so-h")}    <div class="variants">
{chr(10).join(vhtml)}
    </div>
    <p class="fine">Ceny netto, do których dolicza się 23% VAT. Umowa na czas nieokreślony z miesięcznym okresem wypowiedzenia. Ostateczną cenę ustalamy po rozmowie o skali działalności i zakresie obsługi.</p>
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
    h = head(p, "Specjalizacje i branże — M2 TAX Doradcy Podatkowi | Wrocław",
             "Interpretacje indywidualne, kontrole i postępowania podatkowe, czynności sprawdzające, wypłata pieniędzy ze spółki, restrukturyzacje, fundacje rodzinne, nieruchomości. Branże: budowlana, medyczna, beauty, produkcyjna, osoby prywatne.",
             "specjalizacje/")
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
    body = header(p, "specjalizacje/") + page_hero(
        p, "Specjalizacje", "Specjalizacje",
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
{section_head("Zakres działania", "Wrocław i okolice", "Spotykamy się w kancelarii przy ul. Zwycięskiej 3 we Wrocławiu albo online.", "area-h")}    <div class="towns">
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
{cta_band(p, "Porozmawiaj z nami osobiście", "W kancelarii przy ul. Zwycięskiej 3 we Wrocławiu albo online. Pierwsze 20 minut jest bezpłatne.")}  </div>
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
        <li>Online albo w kancelarii przy ul. Zwycięskiej 3</li>
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
          <div><h4>Adres</h4><p>ul. Zwycięska 3<br>53-033 Wrocław</p></div>
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


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("zapisano", rel)


def sitemap():
    urls = ["", "abonamenty/", "specjalizacje/", "zespol/", "kontakt/", "polityka-prywatnosci.html", "aml.html"]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", x)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    write("index.html", build_home())
    write("abonamenty/index.html", build_abonamenty())
    write("specjalizacje/index.html", build_specjalizacje())
    write("zespol/index.html", build_zespol())
    write("kontakt/index.html", build_kontakt())
    sitemap()
