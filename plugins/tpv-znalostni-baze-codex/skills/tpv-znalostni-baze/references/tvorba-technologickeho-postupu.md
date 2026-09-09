# Workflow: poptávka → technologický postup

Cíl: z popisu zakázky (nezkušeným) uživatelem sestavit kompletní technologický postup ve formátu firemního vzoru T.1.3.1, konverzačně, s co nejmenší pracností pro uživatele.

Výstup je čistý Markdown, který se na konci převede na `.docx` přes pandoc — nepiš žádný generovací skript ani JSON, piš rovnou text postupu jako markdown.

Tenhle workflow knihovnu ČTE (TPP odkazy, bod 4) a jedinou věc do ní zapisuje: krátkou stopu do
`poznamky-kontext.md` na konci (bod 9b). Nikdy nevytváří ani nemění T.TPP dokumenty ani
`INDEX.md` — to dělá workflow zapis-postupu.

Kategorie a jejich celé názvy podsložek jsou v `kategorie.json` (vedle tohoto souboru) —
použij tenhle soubor při sestavování cesty k TPP dokumentu (bod 4).

## Workflow

### 1. Zjisti základní údaje o zakázce
Zeptej se konverzačně, pokud uživatel už nenapsal:
- Číslo zakázky (`ZXXXXXX`) a název výrobku
- Obecná poznámka k zakázce: materiál, kontext, cokoliv netypického pro tuhle zakázku — volný text, ne formulářová pole. Toto jde do úvodu dokumentu jako "Poznámka k zakázce".

**Pokud uživatel nahraje fotku/sken výrobního příkazu**, nežádej ho o přepsání údajů — přečti číslo zakázky, název výrobku a základní poznámku přímo z obrázku (Claude vidí obrázky nativně, žádný OCR nástroj není potřeba). Vždy krátce ukaž, co jsi z fotky vyčetl, a nech uživatele potvrdit/opravit, než pojedeš dál — fotky bývají nekvalitní, ruční poznámky špatně čitelné.

### 2. Navrhni aktivní operace
Použij `operations-catalog.md` (vedle tohoto souboru) — číselník ~26 operací s čísly a názvy.
**Čísla a názvy operací** ber přesně z katalogu, neměň je. **Pořadí určuje uživatel** —
pořadí v katalogu není technologická posloupnost, je to jen evidenční řazení
(viz `bezpecnostni-pravidla.md` bod 8). Pokud pořadí navrhuješ ty, vždy ho označ jako
**návrh k potvrzení**, ne jako danost, a po potvrzení už ho sám nepřeskládávej.

Na základě popisu výrobku navrhni, které operace se pro tuhle zakázku použijí. Řekni uživateli návrh a proč, nech ho potvrdit/upravit. Do finálního dokumentu jdou JEN aktivní operace — žádný souhrnný seznam/tabulka všech 26 na konci, ten byl jen pro starý Word makro systém a tady je zbytečný.

### 3. Pro každou aktivní operaci se doptej — nediktuj checklist do dokumentu
`operations-catalog.md` obsahuje orientační kontrolní otázky u některých operací (999027, 999029, 999030, 999035, 999200). Tyto otázky jsou **vodítko pro tebe, kam se zeptat** — ne text, který automaticky skončí v dokumentu.

Postupuj takto:
- Zeptej se přirozeně na to, co otázky pokrývají (klidně víc najednou, ne mechanicky jednu po druhé)
- Uživatel odpoví, přeskočí, nebo řekne "standardní" / "jako obvykle"
- Do dokumentu zapiš výsledek jako krátký volný text (2-4 věty), ne odrážkový výpis původních otázek
- Pokud uživatel nechce nic doplňovat u dané operace, nech sekci stručnou (jen čas/ks a případně TPP odkaz) — nevymýšlej obsah za něj

### 4. TPP odkazy
Pokud pro operaci existuje relevantní `T.TPP.*` dokument v knihovně:
- **Neopisuj jeho obsah.** Vlož jako **skutečný markdown odkaz**: `[T.TPP.OBR.1 Obrábění na soustruhu od 35cm](file:///cesta/k/souboru)` — musí se to v dokumentu zobrazit jako klikatelný odkaz, ne jako obyčejný text.
- Cestu k souboru sestav z `config.json` (`library_root` + `tpp_dir`) + celý název kategorijní podsložky z `kategorie.json` a ověř skutečný obsah té podsložky na disku (ne jen paměť/odhad) — stejný princip jako u ostatních workflow, index/knihovna se může lišit od toho, co si pamatuješ z dřívějška. URL-encoduj mezery a diakritiku v cestě (`%20` atd.), jinak odkaz v docx nefunguje.
- Pokud žádný TPP přesně nesedí, napiš krátké kroky přímo jako volný text.

### 4b. Doporučení z obecné znalostní báze (volitelné, měkké)

Po vyřešení TPP odkazu pro danou operaci (bod 4) nech doběhnout **poradce** —
pravidla jsou v `poradce.md` (vedle tohoto souboru): kdy se ozvat, kde hledat, jak
citovat. Nejde o náhradu TPP odkazu, jen o doplňkové upozornění na relevantní obecnou
směrnici nebo školení, pokud existuje.

Specifika pro tenhle workflow navíc k tomu, co říká `poradce.md`:

- Pokud `INDEX-smernice.md` neexistuje (cesta z `config.json` → `general_kb_root` +
  `general_kb_index_file`), tenhle krok přeskoč beze zmínky — workflow pokračuje přesně
  jako dnes, jen s TPP odkazem.
- Nikdy nevkládej do dokumentu automaticky/tiše — jen po potvrzení uživatelem.
- Po potvrzení vlož do dokumentu jako viditelně odlišený blok (kurzíva/citace + odkaz na
  zdrojový soubor jako `file:///...`), jasně oddělený od TPP odkazu — aby bylo i v
  hotovém dokumentu zřejmé, že jde o doplňkovou citaci z obecné směrnice, ne o TPP
  postup.
- Pokud nic relevantního nenajdeš, žádná nová povinná otázka — jen tiše pokračuj dál.

### 5. Čas/ks — placeholder i párování z volného textu

**Výchozí chování:** vlož `Čas/ks: _____ min/ks` jako placeholder. Nevyplňuj, neodhaduj z normativů — vědomé rozhodnutí uživatele nechat prázdné.

**Pokud uživatel v podkladech (poptávka, popis, diktát) sám zmíní konkrétní čas u nějaké činnosti** (např. "soustružení cca 8 min/ks", "lakování trvá přes noc", "seřízení stroje 2 hodiny"), napáruj ho na odpovídající operaci pomocí `cas-klicova-slova.json` (vedle tohoto souboru) — hotová vyhledávací tabulka klíčové slovo → kód operace, nemusíš to odvozovat z názvu operace za běhu:

1. Vyhledej klíčové slovo ze zmínky v `cas-klicova-slova.json`. Pokud zmínka jasně odpovídá jedné konkrétní aktivní operaci, použij nalezený kód rovnou.
2. Pokud je nejednoznačné, ke které operaci čas patří (víc shod, žádná shoda, nebo obecná zmínka typu "celkem to zabere den" bez rozpadu na kroky), **nehádej — zeptej se**, ke které operaci ho přiřadit, nebo jestli má zůstat jen jako obecná poznámka k zakázce.
3. Napárovaný čas dosaď do pole `Čas/ks:` té operace místo prázdného placeholderu, ve stejném formátu (`min/ks`, případně přepočti jednotky jako hodiny→minuty a řekni, že jsi přepočítal).
4. Časy u operací, které uživatel nezmínil, zůstávají prázdný placeholder jako doteď — nedopočítávej, nedomýšlej.
5. Krátce potvrď uživateli, co jsi napároval a kam ("Čas 8 min/ks jsem přiřadil k 999048 Soustružení"), ať má šanci to opravit před finálním náhledem.

### 6. Formát dokumentu
```markdown
# ZXXXXXX — Název výrobku

**Poznámka k zakázce:** volný text...

---

## 999027 GRAFICKÁ PŘÍPRAVA
Čas/ks: _____ min/ks

Volný text / kroky / TPP odkaz.

---

## <další aktivní operace v pořadí určeném uživatelem>
...
```
Vodorovná čára (`---`) mezi každou operací — vizuálně je to odděluje po převodu do Wordu.

**Název operace piš verzálkami** (`999027 GRAFICKÁ PŘÍPRAVA`, ne `999027 Grafická
příprava`) — takhle to mají reálné vyplněné postupy ve výrobě a na dílenském papíře se
hlavička operace hledá očima, ne čtením. Číslo operace zůstává před názvem, diakritika i
ve verzálkách (`ŘEZÁNÍ`, ne `REZANI`). V `operations-catalog.md` jsou názvy psané normálně
— verzálky dělej až tady při sestavování dokumentu, katalog kvůli tomu neupravuj.

### 7. Převod na .docx a kontrola
```
bash scripts/md_to_docx.sh postup.md postup.docx
```
(cesta je relativní ke **kořeni skillu** — skript leží v `scripts/`; uprav ji podle aktuálního working directory). U prvního použití v konverzaci zkontroluj vizuálně (převod na PDF + náhled, viz `docx` skill), dál pandoc pipeline je deterministický a další kontrola není nutná.

Skript si pandoc najde sám i mimo PATH (na Windows ho winget instaluje do
`%LOCALAPPDATA%\Pandoc`) a automaticky použije `assets/reference.docx` — firemní styly
odvozené ze vzoru T.1.3.1 (písmo Aptos, 12 pt, cs-CZ, A4, okraje 2,5 cm). **Volej ho
tedy vždy přes skript, ne holým `pandoc` příkazem** — jinak přijdeš o šablonu a výstup
bude vypadat jako převedený markdown, ne jako firemní dokument. Když pandoc chybí,
skript vypíše instalační příkaz; nainstaluj až po odsouhlasení uživatelem.

`assets/reference.docx` je vygenerovaný, ne ručně kreslený — když se firemní šablona
`T.1.3.1B ... .dotm` změní, přegeneruj ho pomocí `scripts/build_reference_docx.py`
(bere styly, motiv a rozměry ze šablony, makra do výstupu záměrně nepřenáší).

### 8. Tisk
Výstup je `.docx` — tisk řeší uživatel nativně. TPP odkazy vedou přímo na soubor v knihovně, uživatel si je otevře/vytiskne zvlášť, pokud potřebuje.

### 9. Uložení
Po vygenerování vždy nabídni ke stažení (present_files). Neukládej automaticky do síťové knihovny bez potvrzení umístění.

### 9b. Stopa do poznámek ke kontextu (automaticky, bez ptaní)

Po dokončení postupu vždy připoj krátký zápis do souboru z `config.json` →
`context_notes_file` (v `library_root` + `tpp_dir`). Tenhle jediný zápis je pro
`tvorba-technologickeho-postupu` povolený — viz `bezpecnostni-pravidla.md` bod 6.

Proč automaticky a bez ptaní: kdyby se to nabízelo, nikdo to neodklikne a soubor
zůstane prázdný. Smysl je, že se za pár měsíců dá `poznamky-kontext.md` přečíst a
vidět, která témata se vracejí — to je podklad pro rozhodnutí, co má cenu sepsat jako
skutečný standardizovaný TPP. Bez té stopy to rozhodnutí nemá o co opřít.

**Nejdřív ověř duplicitu — necti celý soubor.** Cíleně vyhledej (Grep) v souboru kód
zakázky a 1–2 klíčová slova z názvu výrobku:
- Stejná zakázka už zapsaná → **nepřipojuj znovu a nic neupravuj** (soubor je append-only);
  jen to řekni uživateli jednou větou.
- Tematicky podobná, ale **jiná** zakázka → zápis přidej normálně, to není duplicita.

Formát — připoj na konec souboru, nikdy nepřepisuj starší zápisy:

```markdown
---

## RRRR-MM-DD — ZXXXXXX Název výrobku — NEOVĚŘENO (zdroj: hovor, workflow tvorba… 9b)

Krátce (3-5 řádků): materiál, zákazník, řetězec operací se šipkami, zmíněné TPP odkazy.

Automaticky doplněno workflow tvorba-technologickeho-postupu (krok 9b) — jde jen o
soft-note, žádný formální T.TPP dokument tím nevznikl.
```

Značka `NEOVĚŘENO` je podstatná: obsah je zápis z hovoru, ne schválený postup. Takový zápis
se nesmí později recyklovat jako firemní znalost ani jako podklad pro další postup — viz
**zákaz recyklace** v `bezpecnostni-pravidla.md` bodu 6. Uživateli o zápisu řekni jednou
větou na konci, ať ví, že vznikl — ne jako otázku.

## Interaktivní widget (kdekoli je dostupný `visualize:show_widget`)

`visualize:show_widget` bývá dostupný nejen v Claude.ai chatu, ale i v Cowork session
(jako deferred tool přes `ToolSearch`) — než rozhodneš, že widget "tady není", zkus ho
vyhledat/použít, ne to jen předpokládat podle typu rozhraní.

Pokud je `visualize:show_widget` dostupný, místo čistě konverzačního postupu kroků 1-4
nabídni uživateli interaktivního průvodce:

1. Zjisti konverzačně základní údaje o zakázce (krok 1) a připrav si předem odhad, které operace a jaký draft textu budou pravděpodobně sedět (na základě popisu zakázky) — widget nemá živé spojení k AI, takže návrhy (`drafts`, `preselect`) musíš vygenerovat ty předem a vložit do kódu widgetu.
2. Over aktuální `T.TPP.*` knihovnu (přes `config.json`) a naplň `tppByOp` reálnými dostupnými dokumenty pro operace, kde to dává smysl (frézování, soustružení, lakování...).
3. Widget má oddělený **STATICKÝ** blok (katalog operací, nápovědy, veškerá logika — nikdy needit) a **DYNAMICKÝ** blok `=== DYNAMICKÁ DATA ZAKÁZKY ===` (jasně ohraničený komentáři, obsahuje **jeden JSON objekt** s klíči `orderDesc`, `drafts`, `preselect`, `tppByOp`).
   Uprav pro aktuální zakázku **jen tenhle blok** přes `str_replace` na
   `assets/wizard_widget.html` (cesta od kořene skillu) — data vlož jako validní JSON, ne
   jako JS literály; uvozovky, apostrofy i diakritiku v názvu zakázky pak nic nerozbije.
   Jediné, co se v JSON stringu musí escapovat navíc, je sekvence `</` (piš `<\/`).
   Nepřepisuj/negeneruj zbytek souboru z paměti, jen ho pak celý načti (`view`) a vlož jako
   `widget_code` do `visualize:show_widget`. **Ověř, že `str_replace` skutečně proběhl**
   (blok obsahuje data zakázky, ne prázdný sentinel) — pokud ne, widget nezobrazuj a jeď
   konverzačně, jinak bys uživateli ukázal cizí nebo prázdná data.
4. Widget uživateli ukáže: vyhledávání/přidávání operací s **šipkami pro přeuspořádání pořadí** (↑/↓ u chipu, i v pásku pořadí během kroku 5) → krok po kroku textové pole s předvyplněným návrhem + volitelný TPP odkaz z knihovny (vyhledávací pole) → na konci tlačítko, které přes `sendPrompt()` pošle zpět do chatu surové poznámky **ve finálním, uživatelem nastaveném pořadí**.
5. **Po přijetí zprávy z widgetu VŽDY projdi obsah, strukturuj, oprav formulace a ukaž náhled** (viz krok 3 výše — cleanup pass). Nikdy negeneruj finální dokument rovnou z widgetu bez tohoto kroku — **výjimka:** pokud zpráva výslovně říká "přeskoč kontrolní náhled a rovnou vygeneruj" (tlačítko "Generovat rovnou" ve widgetu), jde o vědomou volbu uživatele — přeskoč zobrazení náhledu a jdi rovnou na formát/převod (kroky 6-9), text ale i tak tiše proveď přes drobný jazykový cleanup (bez zobrazení), ne 1:1 kopii syrových poznámek.
6. **Po zobrazení náhledu nepokládej otázku textem** — místo toho vlož `assets/confirm_widget.html` (cesta od kořene skillu) do `visualize:show_widget` (dvě tlačítka: "Vypadá dobře, generovat" / "Ještě upravit operace"). Tlačítko "upravit" pošle přes `sendPrompt` požadavek na opětovné otevření průvodce se stejnými daty — tehdy widget znovu naplň (krok 3 výše) tak, aby `preselect`/`drafts`/pořadí odpovídalo poslednímu stavu z náhledu, ne původním výchozím návrhům.
7. Teprve po potvrzení (tlačítko "Vypadá dobře") pokračuj kroky 6-9 (formát, převod, tisk, uložení).

Widget je pomocná vrstva navíc pro chat — základní konverzační workflow (kroky 1-9) musí fungovat i bez něj (Claude Code apod.).

## Co tento workflow NEDĚLÁ (zatím)
- Neřeší kalkulaci ceny.
- Nezapisuje nové T.TPP dokumenty do knihovny (dělá workflow zapis-postupu).
- Neodhaduje čas/ks z normativů THN — dosazuje jen časy, které uživatel sám výslovně zmínil (bod 5).

## Bezpečnostní pravidla

Platí kompletně `bezpecnostni-pravidla.md` (vedle tohoto souboru, sdílené napříč celým
skillem). Specifikum tohoto workflow navíc: z knihovny jen čte a jediný zápis, který
smí udělat, je připojení odstavce do `poznamky-kontext.md` (bod 9b). Žádné T.TPP
dokumenty, žádný `INDEX.md`, nikdy nic nemaže ani nepřepisuje.
