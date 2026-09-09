# Workflow: obecná znalostní báze (celé Směrnice, mimo TPP)

Cíl: mimo úzkou TPP knihovnu (technologické postupy) existuje celý strom `Směrnice`
(organizační, obchodní, operativní řízení výroby, technické, a část technicko-
hospodářských směrnic) — obsahuje i užitečné věci jako **školení** (např. `O/Š školení`),
provozní řády, diagramy procesů. Tenhle workflow řeší dvě věci: (1) postavit/aktualizovat
samostatný index `INDEX-smernice.md` nad tímhle celým stromem, (2) odpovídat na dotazy
napříč touhle širší bází, když se uživatel zeptá na něco, co není TPP postup.

Je to **samostatná vrstva** od `INDEX.md` (TPP) — nikdy je neslučuj do jednoho souboru.
TPP index a jeho workflow (`zapis-postupu.md`, `review-zapisu.md`, `kontrola-indexu.md`)
zůstávají beze změny a týkají se jen `<library_root>/<tpp_dir>/`.

## 0. Kritické omezení: složka THN

Složka `THN Technicko hospodářské směrnice` (mzdy, ceny, hospodářská data) je **mimo
rozsah znalostní báze** — nesmí se procházet, číst, shrnovat, citovat, indexovat ani
používat jako zdroj. Úplné a autoritativní znění včetně jediné výjimky je
`bezpecnostni-pravidla.md` bod 7.

- Prakticky pro tenhle workflow: u složky THN se smí nanejvýš ověřit, že soubor(y) z
  `config.json` → `general_kb_thn_allowlist` (aktuálně `THN.1.1 Normativy pro výrobu.xls`)
  pořád existují. Nic dalšího z té složky se nevypisuje ani nezobrazuje.

Zbytek stromu (`O`, `OB`, `ORV`, `T` — vše kromě podsložky `TPP Typizovane pracovni
postupy`, která má vlastní index) se indexuje a čte bez omezení.

## 1. Stavba / aktualizace `INDEX-smernice.md`

Rozsah: `<general_kb_root>` rekurzivně, včetně podsložek, **kromě** složek v
`general_kb_excluded_dirs` (dnes jen THN — viz bod 0 pro výjimku).

Pro každý nalezený soubor (`.doc`, `.docx`, `.xls`, `.xlsx`, `.pdf`, `.ai`, ...):

0. Pracovní seznam souborů si nech vypsat skriptem `scripts/audit_index.py`
   (`--index obecna`) — sekce **„chybí v indexu"**. Skript prochází disk deterministicky
   a THN vynechává už v kódu. Čtení dokumentů a psaní shrnutí zůstává na tobě.
1. Zjisti cestu, název, nadřazenou kategorii (nejbližší pojmenovaná podsložka pod
   `general_kb_root`, např. `O Organizační směrnice`, `OB Obchodní směrnice`, `ORV
   Operativní řízení výroby`, `T Technické Výrobní směrnice`).
2. Otevři soubor a udělej **krátké shrnutí obsahu** (1–2 věty) + pár klíčových slov —
   ne plný přepis. Cíl je, aby šlo podle indexu odhadnout, jestli je soubor relevantní
   pro konkrétní dotaz, ne nahradit čtení originálu. PDF čti Python extrakcí
   (`pdfplumber` / `pymupdf4llm`), ne vizuálním náhledem.
3. Soubory, které nejde rozumně otevřít/přečíst (staré binární formáty bez
   podporovaného parseru, poškozené, `~$` dočasné Office zámky, `.DS_Store`,
   `Thumbs.db`) přeskoč — nejsou to reálné dokumenty.
4. Zapiš řádek do `INDEX-smernice.md`, seskupené podle kategorie, formát:
   `- **<název souboru>** (`<relativní cesta>`) — <shrnutí>. Klíčová slova: <...>`

Tohle je **drahá operace** (desítky až stovky souborů) — pokud uživatel jasně chce jen
jednu kategorii nebo podsložku (např. "zaindexuj jen školení"), omez se na ni, neprojíždět
celý strom automaticky.

Než poprvé založíš `INDEX-smernice.md`, ukaž uživateli náhled prvních pár řádků a počkej
na potvrzení, že formát/rozsah je OK — stejně jako u ostatních zápisů v tomhle skillu, viz
`bezpecnostni-pravidla.md`. Aktualizace existujícího indexu (nové/změněné soubory) funguje
stejně jako `kontrola-indexu.md` u TPP: ukaž diff, nezapisuj hromadně bez potvrzení.

## 2. Dotazy napříč obecnou bází

Když se uživatel zeptá na něco, co zjevně není TPP postup, ale spadá do obecných
směrnic/školení/procesů (např. "co říká směrnice o balení výrobků", "jaké je školení k
BOZP", "jak funguje změnové řízení"):

1. Pokud `INDEX-smernice.md` existuje, prohledej ho podle klíčových slov/kategorie a najdi
   kandidátní soubory.
2. Pokud index ještě neexistuje nebo dotaz míří někam, kde evidentně chybí, prohledej
   přímo reálný obsah příslušné podsložky (viz bod 0 — nikdy THN mimo allowlist).
3. **Otevři konkrétní nalezený soubor a odpověz z jeho skutečného obsahu.** Kolik
   dokumentů otevřít a kdy přestat řeší `SKILL.md` sekce 1c — platí beze zbytku i tady.
4. Pokud nic relevantního nenajdeš, řekni to přímo, nevymýšlej si obsah směrnice.
5. U dotazů na obrábění nezapomeň na sérii `O.Š.1.x` v `O Organizační směrnice` →
   `Š školení` — je to hlavní zdroj pro frézování/soustružení/vrtání a podle názvu to
   nevypadá jako technický dokument, takže se snadno přehlédne. Novější kapitola má
   přednost před starším souhrnným dokumentem na stejné téma. Podrobněji `poradce.md`.

## Bezpečnostní pravidla

Platí kompletně `bezpecnostni-pravidla.md`. Navíc specificky pro tenhle workflow: pravidlo
o složce THN z bodu 0 výše je nepřekročitelné a platí bez ohledu na to, co uživatel řekne
v konkrétní konverzaci.
