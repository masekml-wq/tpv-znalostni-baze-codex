# Workflow: kontrola indexu vs. realita na disku

Audituje **oba indexy** — `INDEX.md` (TPP postupy) i `INDEX-smernice.md` (obecná báze:
organizační, obchodní, ORV, technické směrnice a školení). Jsou to samostatné vrstvy nad
jinými částmi disku a nikdy se neslučují, ale drift se u obou hlídá stejně a stejným
způsobem. Postup níže popisuje nejdřív TPP (body 2–5) a pak obecnou bázi (bod 6), která
má jiný klíč porovnání.

Proč to u obecné báze vůbec řešit: `INDEX-smernice.md` používá **poradce**
(`poradce.md`) k tomu, aby v hovoru nabídl existující směrnici nebo školení. Když index
zastará, poradce prostě mlčí — nic nespadne, jen se tiše přestane ozývat a nikdo si toho
nevšimne. Tenhle audit je jediné místo, kde takový drift vyjde najevo.

Cíl u TPP: porovnat záznamy v `INDEX.md` se skutečnými soubory v knihovně a ukázat rozdíly —
chybějící záznamy v indexu, záznamy v indexu bez souboru na disku, případné kolize
(víc souborů pod stejným kódem). **Nikdy nic sám neopravuje** — to je vždy rozhodnutí
uživatele, provedené přes workflow zapis-postupu/review-zapisu, ne tímto workflow.

Doplňuje workflow zapis-postupu a review-zapisu, které
kontrolují jen levně (jedna kategorie při zápisu/review) — tenhle workflow dělá **drahý
plný audit**, proto výhradně na vyžádání, nikdy automaticky/na pozadí.

Kategorie a jejich celé názvy podsložek jsou v `kategorie.json` (vedle tohoto souboru).

Cesty ber vždy z `config.json`. Pokud cesta v configu neexistuje nebo je nedostupná (u
síťového disku `U:` se to stane běžně — odpojená nebo nepřipojená složka) → **zastav se a
řekni to uživateli přímo**, nehádej ani nekontroluj proti staré/jiné kopii bez upozornění.
Prázdný výpis nedostupného disku vypadá úplně stejně jako smazaná knihovna a vedl by
k hlášení desítek falešných "chybí na disku".

## 1. Zjisti rozsah kontroly

Zeptej se (pokud uživatel už neřekl):
- **Který index** — TPP (`INDEX.md`), obecná báze (`INDEX-smernice.md`), nebo oba?
  Když uživatel řekne jen "zkontroluj index" bez upřesnění, ber to jako **oba** — drift
  v obecné bázi je hůř vidět než v TPP, takže vynechat ji potichu je horší chyba než
  udělat práci navíc.
- Celá knihovna (všechny kategorie), nebo jen jedna kategorie (např. jen OBR)?
- Celá kontrola je drahá operace (výpis celého stromu `TPP/`, u obecné báze celého
  `general_kb_root`) — pokud uživatel jasně chtěl jen rychlý dotaz na jednu kategorii,
  omez se na ni.

## 2. Sesbírej data

Sběr dat dělá skript `scripts/audit_index.py` (cesta je relativní ke kořeni skillu) —
deterministicky projde disk, načte `INDEX.md` a vypíše diff. Sám nic nezapisuje.

```
python scripts/audit_index.py --index tpp
```

1. Pouštěj ho s **velkorysým timeoutem** — síťový disk `U:`, průchod stromem trvá jednotky
   minut. Rozsah podle bodu 1 omez přepínačem `--kategorie OBR`.
2. **Nenulový návratový kód = zastav se a řekni to uživateli** (typicky nedostupný kořen).
   Nepokračuj s prázdným ani částečným výpisem — vypadal by jako smazaná knihovna.
3. Nepřepisuj a needituj nic v tomto kroku — čistě čtení.

## 3. Porovnej a vytvoř diff

Pro každou kategorii zvlášť (přehlednější než jeden velký seznam):

- **Chybí v indexu** — soubor existuje na disku, ale žádný řádek v `INDEX.md` ho nezmiňuje
  (podle kódu v názvu souboru, např. `T.TPP.PU.5...`).
- **Chybí na disku** — řádek v `INDEX.md` odkazuje na kód, pro který neexistuje žádný
  soubor v příslušné podsložce (možná smazáno mimo systém, přejmenováno, nebo chyba
  v indexu).
- **Kolize kódu** — víc než jeden soubor ve stejné kategorii se stejným kódem (např.
  `T.TPP.OBR.3` — známá existující kolize, viz varovný blok v hlavičce `INDEX.md` — nahlas
  ji znovu, pokud pořád trvá, ale neopravuj).
- **Mimo rozsah** — soubory ležící přímo v kořeni `<tpp_dir>` (mimo kategorijní podsložky)
  a položky sekce "Mimo rozsah" v `INDEX.md` vykazuj **zvlášť, jako informaci**, ne jako
  drift. Nejsou to chybějící záznamy a nenabízej je k doplnění.

Stav `existující` (i varianty `existující — KOLIZE`, `existující — referenční pomůcka`) je
**finální stav** dokumentů z doby před tímhle skillem — není to nedokončený záznam, nehlas
ho jako chybu a nenabízej ho k review. Stav se eviduje výhradně v `INDEX.md`, ne v hlavičce
dokumentu, takže se stavy neporovnávají.

## 4. Ukaž výsledek, nic neoprav

Výstup vždy jako **přehledný diff/tabulka**, ne jen prozaický popis:

```
Kategorie OBR:
  Chybí v indexu: T.TPP.OBR.4, T.TPP.OBR.6.1
  Chybí na disku: (žádné)
  Kolize kódu: T.TPP.OBR.3 (2 soubory: "...hranaté tvary.docx" a "...XPS.md")

Kategorie PU:
  Chybí v indexu: T.TPP.PU.6, T.TPP.PU.7
  ...
```

Na konci shrň počty (kolik chybí v indexu, kolik na disku, kolik kolizí) napříč
zkontrolovaným rozsahem.

## 5. Nabídni další krok, ale nedělej ho sám

- Pro chybějící záznamy v indexu: nabídni "chceš, abych je doplnil do INDEX.md po jednom
  s tvým potvrzením u každého?" — pokud ano, doplňuj **po jednom**, ukaž řádek před
  zápisem, počkej na potvrzení (stejný princip jako workflow zapis-postupu/review-zapisu,
  žádné hromadné tiché doplnění).
- Pro kolize: nasměruj na ruční rozhodnutí uživatele (přečíslovat/sloučit) — tenhle
  workflow kolize sám neřeší, jen hlásí.
- Pro záznamy chybějící na disku: jen nahlas, nech uživatele rozhodnout, jestli jde o
  chybu v indexu (smazat řádek) nebo o soubor smazaný mimo systém — smazání řádku v
  `INDEX.md` je stejně citlivá operace jako jinde, vyžaduje výslovné potvrzení, ne
  automatiku.

## 6. Audit obecné báze (`INDEX-smernice.md`)

Běží jen tehdy, když je v rozsahu podle bodu 1. Logika je stejná jako u TPP, liší se
klíč porovnání: TPP se páruje podle **kódu** (`T.TPP.PU.5`), obecná báze podle
**relativní cesty k souboru** — směrnice nemají jednotné kódování v názvu a stejný název
se může legitimně objevit ve dvou složkách.

### 6.1 Rozsah a nepřekročitelné omezení

Rozsah je `<general_kb_root>` rekurzivně, **kromě** složek v `general_kb_excluded_dirs`.
Prakticky to dnes znamená: **složku `THN Technicko hospodářské směrnice` neotvírej a
neprocházej** — obsahuje mzdové a finanční podklady. Jediná výjimka je soubor z
`general_kb_thn_allowlist`, u kterého smíš ověřit pouze to, že pořád existuje. Do diffu
nikdy nevypisuj názvy ostatních souborů z THN, ani jako "nalezeno navíc" — to je pořád
únik obsahu té složky, jen oklikou přes audit. Viz `obecna-znalostni-baze.md` bod 0 a
`bezpecnostni-pravidla.md` bod 7.

Zároveň vynech podsložku `<tpp_dir>` — tu pokrývá audit `INDEX.md`, jinak by se soubory
hlásily jako chybějící v obou indexech.

### 6.2 Co porovnat

1. Sběr i porovnání udělá `python scripts/audit_index.py --index obecna` — načte
   `INDEX-smernice.md`, vylistuje reálné dokumenty v rozsahu podle 6.1 a vypíše diff.
   Vyloučení THN i `<tpp_dir>` má natvrdo v kódu, stejně jako přeskakování `~$` zámků
   Office, `.DS_Store` a `Thumbs.db` — ty nejsou dokumenty a jen by zaplevelily diff.
2. Platí totéž co v bodě 2: velkorysý timeout, **nenulový návratový kód = zastav se a řekni
   to uživateli**, nikdy nepracuj s částečným výpisem.
3. Rozdíly pojmenuj takhle:
   - **Chybí v indexu** — soubor je na disku, index ho nezná. Nejčastější případ a ten,
     kvůli kterému poradce mlčí.
   - **Chybí na disku** — index na něj odkazuje, soubor tam není (přejmenovaný, přesunutý,
     smazaný mimo systém).
   - **Přejmenováno/přesunuto** (pravděpodobné) — když jedna položka chybí na disku a jiná
     se stejným nebo velmi podobným názvem chybí v indexu, nabídni to jako jednu změnu
     cesty místo dvou nesouvisejících řádků. Je to jen odhad, tak to i formuluj.
4. Pokud `INDEX-smernice.md` vůbec neexistuje, neber to jako chybu — řekni, že obecná báze
   ještě nebyla zaindexovaná, a nasměruj na `obecna-znalostni-baze.md` bod 1.

### 6.3 Výstup a zápis

Výstup stejně jako v bodě 4 — tabulka/diff seskupený podle kategorie (`O`, `OB`, `ORV`,
`T`), na konci součty. **Sám nic nezapisuj.**

Doplnění chybějícího řádku do `INDEX-smernice.md` má oproti TPP jednu komplikaci: řádek
obsahuje shrnutí obsahu, takže se soubor musí nejdřív otevřít a přečíst (PDF přes
pdfplumber/pymupdf4llm, ne prohlížením stránek). Proto:

- Nabídni doplnění a udělej ho **po jednom souboru**: otevři, přečti, ukaž navržený řádek
  včetně shrnutí a klíčových slov, počkej na potvrzení, teprve pak zapiš.
- Když je souborů hodně, řekni rovnou kolik jich je a nabídni omezení na jednu kategorii —
  ať uživatel neodklikává třicet položek v jednom sezení.
- Soubory, které nejde přečíst (starý binární formát bez parseru, poškozené), do indexu
  nedávej s vymyšleným shrnutím. Buď je vynech, nebo je zapiš s poznámkou "obsah nepřečten"
  — hádat obsah podle názvu souboru je horší než ho tam nemít, protože poradce by pak
  citoval něco, co v dokumentu není.
- Mazání řádků (chybí na disku) je citlivá operace stejně jako u TPP — jen po jednom, s
  výslovným potvrzením, nikdy hromadně.

## Bezpečnostní pravidla

Platí kompletně `bezpecnostni-pravidla.md` (vedle tohoto souboru, sdílené napříč celým
skillem). Specifikum tohoto workflow navíc: nikdy nic sám nepřepisuje ani nemaže, ani
hromadně — i doplnění chybějícího řádku do INDEX.md (bod 5) jde jen po jednom, s
výslovným potvrzením u každého záznamu.

## Měsíční automatické spuštění

Tenhle workflow běží i sám, jednou měsíčně o víkendu (scheduled task). Automatický běh se
od ručního liší jen jednou věcí, zato zásadní: **skončí u reportu**. Projde oba indexy,
sepíše diff a tím to pro ten běh končí — nezapisuje, i kdyby šlo o triviální doplnění
jednoho řádku. Zápis se dělá až v navazujícím hovoru, po bodu 5 / 6.3, s potvrzením
u každé jednotlivé položky.

Důvod je ten, na kterém stojí celý skill: knihovna je firemní know-how a odpovědnost za
její obsah je uživatelova. Automat, který v neděli v noci sám dopisuje řádky do indexu, tu
odpovědnost tiše přebírá — a chyba se odhalí až za měsíce, kdy už není jasné, co ji
způsobilo. Report tenhle problém nemá.

Když je disk `U:` nedostupný, report je jedna věta o tom, že knihovna nebyla dostupná —
ne diff plný falešných nálezů (viz úvod).

Praktické omezení, které stojí za zmínku, když se uživatel diví, že report nepřišel: úloha
běží jen na tomhle počítači a jen když je zapnutý a má připojený `U:`. Zmeškaný běh se
nedohání, prostě se čeká na další měsíc — nebo se audit spustí ručně.
