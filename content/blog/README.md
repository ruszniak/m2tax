# Wpisy na blog M2 TAX

Każdy wpis to jeden plik `.md` w tym folderze. Nazwa pliku = adres wpisu,
np. `czynnosci-sprawdzajace.md` → m2tax.pl/blog/czynnosci-sprawdzajace/

Na początku pliku nagłówek:

    ---
    title: Tytuł artykułu
    date: 2026-10-29
    lead: Jedno-dwa zdania zachęty, widoczne na liście i w Google.
    category: Kontrole i postępowania
    linkedin: https://www.linkedin.com/feed/update/...   (opcjonalnie)
    linkedin_urn: urn:li:share:7516860846338150400       (opcjonalnie: osadzi oryginalny post)
    draft: false                                         (true = nie publikuj)
    ---

Pod spodem treść w Markdown: `## Śródtytuł`, listy `- punkt`, **pogrubienie**,
> cytat. Potem: `python3 tools/build.py`.
