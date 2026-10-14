# m2tax.pl – strona M2 TAX Doradcy Podatkowi

Strona statyczna publikowana na Vercelu (bez kroku budowania).

| Ścieżka | Opis |
|---|---|
| `index.html` | Strona główna (generowana) |
| `abonamenty/`, `specjalizacje/`, `zespol/`, `kontakt/` | Podstrony (generowane) |
| `assets/site.css`, `assets/site.js` | Wspólne style i skrypty (efekty 3D, menu) |
| `polityka-prywatnosci.html`, `aml.html` | RODO i informacja AML |
| `tools/build.py` | Generator i treści wszystkich stron (nie jest publikowany) |

Edycja treści: zmień teksty w `tools/build.py` i uruchom `python3 tools/build.py`.
