---
name: tpv-znalostni-baze
description: Znalostní báze interních dokumentů firmy Mašek – umělecká výroba (dřevěné hračky, loutky, marionety) - technologické postupy (TPP), firemní směrnice a školení. Použij, když uživatel chce sestavit technologický postup pro konkrétní zakázku (i z fotky výrobního příkazu), najít existující TPP nebo se zeptat na jeho obsah, zeptat se na interní směrnici či školení, zapsat nový TPP do knihovny, schválit/zrevidovat draft TPP, nebo zkontrolovat/zauditovat indexy knihovny (INDEX.md, INDEX-smernice.md). NEPOUŽÍVEJ na obecné technologické a řemeslné otázky bez vazby na firemní dokumenty (např. "jak se frézuje buk").
---

# TPV znalostní báze — Mašek, umělecká výroba

Verze skillu: **1b** (evidováno v `config.json` → `skill_version`).
## Kompatibilita s Codex/ChatGPT

Tato verze běží jako lokální Codex plugin bez MCP serveru. Následující pravidla mají přednost před případnými Claude-specifickými pokyny v referenčních souborech:

- Nepoužívej `visualize:show_widget`, `sendPrompt()` ani HTML widgety z `assets/`. Stejný postup proveď konverzačně a před zápisem či generováním vždy vyžádej stejné potvrzení, jaké požaduje příslušný workflow.
- Obrázky a skeny čti pomocí dostupného obrazového vstupu Codex/ChatGPT; nejisté údaje vždy ukaž uživateli ke kontrole.
- Pro výstup `.docx` použij dostupný dokumentový nástroj/skill a firemní šablonu `assets/reference.docx`. Shellový `scripts/md_to_docx.sh` použij jen v prostředí, kde je Bash skutečně dostupný.
- Výrazy „Claude“ v evaluačních očekáváních znamenají obecně asistenta Codex/ChatGPT.

Tenhle skill pokrývá 6 workflow kolem znalostní báze malé dřevozpracující firmy: 5 kolem
technologických postupů (TPP) a 1 kolem širší firemní báze (obecné směrnice, školení).
Místo samostatných skillů je to jeden skill s referenčními soubory — načti vždy jen
ten, který aktuální požadavek potřebuje, ne všechny najednou.

## 0. Načti config

Vždy jako první krok přečti `config.json` (leží v kořeni tohoto skillu) — obsahuje
`library_root`, `tpp_dir`, `index_file`, `context_notes_file`. **Nikdy cesty
nehardcoduj**, vždy vycházej z tohoto souboru. `index_file` i `context_notes_file`
leží v `<library_root>/<tpp_dir>/`, ne v kořeni knihovny.

## 1. Rozpoznej záměr a načti odpovídající workflow

Podle toho, co uživatel chce, přečti PŘESNĚ JEDEN z těchto souborů a řiď se jím —
nenačítej **žádný z ostatních**, dokud ho fakticky nepotřebuješ (šetří to kontext):

| Uživatel chce... | Načti |
|---|---|
| Sestavit technologický postup pro konkrétní zakázku (ZXXXXXX), z popisu nebo fotky výrobního příkazu | `references/tvorba-technologickeho-postupu.md` |
| Najít existující TPP nebo se zeptat na jeho obsah ("máme TPP na osmovosk?", "co říká T.TPP.OBR.1?") | `references/poradce.md` |
| Zapsat nový standardizovaný TPP dokument do knihovny, nebo zapsat neformální postřeh z výroby | `references/zapis-postupu.md` |
| Schválit/zamítnout draft TPP záznamu, projít čekající review | `references/review-zapisu.md` |
| Zkontrolovat, jestli indexy odpovídají realitě na disku (audit `INDEX.md` i `INDEX-smernice.md`) | `references/kontrola-indexu.md` |
| Zaindexovat/aktualizovat obecnou znalostní bázi (mimo TPP), nebo se zeptat na obsah směrnic/školení mimo TPP | `references/obecna-znalostni-baze.md` |

Pokud záměr není jasný z první zprávy (např. jen "mám novou zakázku Z123456" — může to
být tvorba postupu i jen poznámka), krátce se zeptej, o co jde, než začneš číst
referenční soubor — ušetří to zbytečné čtení a doptávání uvnitř špatného workflow.

Pokud uživatel v jedné zprávě chce víc věcí najednou (např. "zapiš tenhle postup a rovnou
ho schval"), zpracuj je jako samostatné kroky v pořadí, v jakém dávají smysl (zápis →
review), ne najednou — každý workflow má vlastní pravidla pro potvrzení.

## 1b. Poradce — běží uvnitř workflow

Napříč workflow platí ještě jedno chování navrch: když v hovoru padne konkrétní
operace, materiál nebo produktová řada, sám upozorni, že na to v knihovně něco je.
Pravidla (kdy se ozvat, kde hledat, jak citovat, kde poradce naopak nemá běžet) jsou v
`references/poradce.md` — načti ho, jakmile v hovoru padne něco konkrétního z výroby.

Neběží v `kontrola-indexu.md` ani v `review-zapisu.md` — tam by to byl jen šum.

## 1c. Jak číst knihovnu (platí ve všech workflow)

Tohle rozhoduje o tom, kolik se toho načte, ještě než načteš cokoli dalšího:

1. Začni indexem (`INDEX.md` pro TPP, `INDEX-smernice.md` pro zbytek).
2. Vyber **max. 2–3 kandidátní dokumenty**, ne všechno, co má podobné klíčové slovo.
3. Otevři jen ty, které opravdu potřebuješ. **Když první odpoví dostatečně, další
   neotvírej.** Výjimka: dotaz míří na víc oblastí, dokumenty si odporují, nebo uživatel
   výslovně chce porovnání.
4. Nikdy nečti preventivně "pro jistotu" ani celou kategorijní podsložku.
5. **Index je navigace, ne zdroj pravdy.** Shrnutí a klíčová slova v indexu slouží
   k výběru souboru a k odpovědi na otázku "co v knihovně existuje". Jakmile ale tvrdíš
   "směrnice stanovuje…" nebo cituješ, musí to být ověřené v originálním dokumentu.
   Vyjmenovat dokumenty z indexu je levné a povolené; drahé je otevřít je všechny.

## 2. Sdílené soubory

| Soubor | K čemu | Kdo ho čte |
|---|---|---|
| `config.json` | cesty ke knihovně, názvy indexů, vyloučené složky/allowlist, verze skillu | všechna workflow (krok 0) |
| `references/bezpecnostni-pravidla.md` | hierarchie zápisu A/B/C, potvrzování, THN, pořadí operací | všechna workflow |
| `references/kategorie.json` | zkratka kategorie (PM, OBR, PU, M, MO, O, L, T) → přesný název podsložky na disku; hodnota se používá 1:1 | `tvorba…`, `zapis-postupu`, `review-zapisu`, `kontrola-indexu` |
| `references/poradce.md` | průběžné doporučování z knihovny i cílené hledání existujících TPP | `tvorba…`, `zapis-postupu`, `obecna-znalostni-baze` |
| `references/operations-catalog.md` | číselník ~26 operací (kód, název, kontrolní otázky) | `tvorba…` |
| `references/cas-klicova-slova.json` | klíčové slovo → kód operace (párování zmíněných časů) | `tvorba…` krok 5 |
| `assets/wizard_widget.html`, `assets/confirm_widget.html` | interaktivní widgety | `tvorba…` |
| `scripts/md_to_docx.sh` | převod Markdown → .docx s firemní šablonou | `tvorba…` krok 7 |
| `assets/reference.docx` | styly odvozené z firemního vzoru T.1.3.1 (generovaný soubor, needituj ručně) | `md_to_docx.sh` |
| `scripts/build_reference_docx.py` | přegeneruje `reference.docx` ze šablony `.dotm` | ručně při změně šablony |
| `scripts/audit_index.py` | deterministický diff disk ↔ index, nic nezapisuje | `kontrola-indexu`, `obecna-znalostni-baze` |

## Co tenhle skill nikdy nedělá

- **Nemění schválenou knihovnu bez výslovného textového potvrzení uživatele u KAŽDÉ
  jednotlivé změny** (T.TPP dokumenty, `INDEX.md`, `INDEX-smernice.md`) — nikdy hromadně,
  nikdy na základě mlčení nebo emoji. Jediná výjimka v celém skillu je append-only stopa
  označená `NEOVĚŘENO` do `context_notes_file` (krok 9b workflow tvorby). Žádné jiné
  automatické zápisy neexistují — viz hierarchie A/B/C v `bezpecnostni-pravidla.md`.
- Neodesílá obsah knihovny (může jít o interní know-how firmy) mimo tuto konverzaci /
  knihovnu samotnou.
- **Nepracuje se složkou `THN Technicko hospodářské směrnice`** (mzdy, ceny, hospodářská
  data) — mimo jediný soubor uvedený v `config.json` → `general_kb_thn_allowlist`. Úplné
  znění je `references/bezpecnostni-pravidla.md` bod 7.
- **Nemění pořadí operací.** Pořadí určuje uživatel, katalog je jen číselník — viz
  `bezpecnostni-pravidla.md` bod 8.

Detaily viz `references/bezpecnostni-pravidla.md`.

