# Workflow: review a schválení draftu TPP

Cíl: bezpečně převést zápis TPP ze stavu `draft` na `ověřeno` — po výslovném textovém
potvrzení, s kontrolou kolizí proti realitě na disku, nikdy tiše a nikdy hromadně bez
potvrzení u každého záznamu zvlášť.

Doplňuje workflow zapis-postupu (ten zapisuje
nové drafty, tenhle je schvaluje/zamítá).

Kategorie a jejich celé názvy podsložek jsou v `kategorie.json` (vedle tohoto souboru).

## 1. Kdo schvaluje

Schvaluje kdokoli z týmu TPV (Mikuláš, Pavel, Matouš i další) — tenhle workflow
**neověřuje identitu**. Na začátku review session se jen zeptej: "Kdo schvaluje? (jméno
pro záznam)" — jméno/potvrzení schvalovatele se zapíše k výslednému záznamu (do
`INDEX.md`, poznámka sloupce). Nejde
o autentizaci, jen o evidenci, kdo review udělal.

## 2. Najdi drafty

1. Načti `INDEX.md`, najdi všechny řádky se stavem `draft` (případně `revize` — úpravy
   čekající na re-review, viz workflow zapis-postupu bod 5 "Úprava existujícího záznamu").
   Review pracuje **výhradně se stavy `draft` a `revize`**. Stav `existující` (i jeho
   varianty) je finální stav dokumentů z doby před skillem — k review se automaticky
   nenabízí a nikdy se nepřeklápí hromadně.
2. Pokud uživatel řekl konkrétní kód (např. "schval T.TPP.OBR.7"), pracuj jen s tím.
   Jinak vypiš seznam čekajících draftů (kód, název, datum zápisu) a zeptej se, kterým
   začít, nebo jestli projít všechny popořadě.
3. **Vždy zpracovávej drafty po jednom.** I když jich čeká víc a uživatel řekne "projdi
   všechny", projdi je v sérii — u každého samostatný náhled + samostatné výslovné
   potvrzení. Nikdy neschvaluj víc záznamů jedním "ano".

## 3. Ověř kolizi kódu proti realitě na disku

Pro každý draft, než ho ukážeš k rozhodnutí:

1. Zjisti kategorii a číslo z kódu (např. `T.TPP.OBR.7` → kategorie OBR, číslo 7).
2. Vylistuj **skutečný obsah** příslušné kategorijní podsložky na disku (ne jen INDEX.md —
   index může driftovat).
3. Zkontroluj, jestli pod stejným kódem existuje **víc než jeden soubor** (potvrzená kolize
   v knihovně — např. dva různé soubory se stejným kódem `T.TPP.OBR.3`, viz varovný blok
   v hlavičce `INDEX.md`).
   - Pokud ano: **STOP.** Nikdy neschvaluj kolidující kód automaticky. Nahlas kolizi
     uživateli přesně — které soubory se pod stejným kódem perou, jaký mají obsah/rozdíl —
     a vyžádej explicitní rozhodnutí, jak dál (přečíslovat jeden z nich? sloučit? nechat
     kolizi a zapsat jinam?). Bez tohoto rozhodnutí review daného draftu nepokračuje.
4. Pokud kolize není, pokračuj k náhledu.

## 4. Ukaž náhled draftu

Než cokoli změníš, ukaž v chatu:

- Plný obsah draftu (nebo aspoň hlavičku + shrnutí sekcí Postup/Parametry/Nešvary/BOZP,
  pokud je dlouhý — na vyžádání celý text).
- Aktuální stav v `INDEX.md` (řádek, jak vypadá teď).
- Co se změní: stav `draft` → `ověřeno`, datum review, jméno schvalovatele. Stav se
  eviduje **výhradně v `INDEX.md`** — v souboru samotném se nemění nic.

Ukaž to jako **diff/přehled před-po**, ne jen tvrzení že je to v pořádku.

## 5. Vyžádej potvrzení

Zeptej se: "Schválit `T.TPP.<KAT>.<n>` jako ověřeno? (napiš 'ano, schvaluji' nebo popiš, co
upravit)"

**Platí přísněji než u workflow zapis-postupu:** nestačí holé "ano" ani klik/reakce —
vyžaduj výslovné textové potvrzení, které se jasně vztahuje ke schválení (např. "ano,
schvaluji", "schválit OBR.7", "potvrzuji"). Pokud je odpověď nejednoznačná ("ok", "jo",
emoji), doptej se znovu jasně, co tím uživatel myslí — nezapisuj na základě dohadu.

Pokud uživatel místo potvrzení navrhne úpravu obsahu draftu: to není úkol tohoto workflow
(úpravy dělá zapis-postupu, viz jeho bod 5 "Úprava existujícího záznamu") — nasměruj ho
tam, tenhle draft zůstává ve stavu `draft`/`revize` beze změny.

## 6. Zápis schválení

Po výslovném potvrzení:

1. V `INDEX.md`: změň stav řádku z `draft` (nebo `revize`) na `ověřeno`, dopiš datum
   review a jméno/iniciály schvalovatele do poznámky.
2. Schválený soubor samotný se **nemění** — stav je jen v `INDEX.md`, aby existoval jediný
   zdroj stavu.
3. Potvrď uživateli: kód, nový stav, kdo schválil, kdy — a kam přesně bylo zapsáno
   (řádek v `INDEX.md` + plná cesta ke schválenému souboru).
4. Pokud čekají další drafty, vrať se k bodu 2 pro další (znovu s vlastním potvrzením) —
   ptej se, jestli pokračovat dalším, nebo skončit.

## 7. Zamítnutí draftu

Pokud uživatel draft zamítne (není v pořádku, nepoužije se):

1. Zeptej se, jestli chce draft **ponechat ve stavu draft** (k dopracování později přes
   workflow zapis-postupu) nebo **smazat**.
2. Ponechání: nic nemaž, jen případně dopiš poznámku do `INDEX.md`, proč byl zamítnut
   (na vyžádání uživatele).
3. **Smazání: nikdy automaticky.** Vyžaduj doslovné textové potvrzení — uživatel musí
   napsat přesný název souboru (celý, ne jen kód) nebo jasné klíčové slovo domluvené v tu
   chvíli (např. napsat "SMAZAT T.TPP.OBR.7 Soustružení nábytkových nohou.md"). Holé
   "ano"/"smaž to"/klik nestačí.
4. Po potvrzení smaž soubor z kategorijní podsložky **a** odstraň/přeškrtni řádek
   v `INDEX.md` (jasně označ jako smazáno, ne jen tiše zmizí — např. přesunout do sekce
   "Zamítnuté/smazané" v INDEX.md, pokud existuje, jinak smazat řádek a zmínit to
   v potvrzovací zprávě uživateli).
5. Potvrď uživateli, co přesně bylo smazáno.

## Bezpečnostní pravidla

Platí kompletně `bezpecnostni-pravidla.md` (vedle tohoto souboru, sdílené napříč celým
skillem). Specifikum tohoto workflow navíc: žádná identita/ověření schvalovatele — jen
záznam jména, kdokoli z TPV může schválit (viz bod 1 výše — nejde o autentizaci).
