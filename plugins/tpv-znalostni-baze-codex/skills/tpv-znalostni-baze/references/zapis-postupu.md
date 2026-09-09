# Workflow: zápis nového TPP do knihovny

Cíl: z volného textu/diktátu uživatele vytvořit strukturovaný záznam TPP, zařadit ho do
knihovny, aktualizovat `INDEX.md` — bezpečně, bez tichého přepsání čehokoli.

Tohle je jeden z workflow tohoto skillu — `config.json` a `references/`
soubory zmíněné níže jsou společné pro všechny (leží v kořeni skillu, resp. vedle
tohoto souboru), ne duplikované zvlášť pro tenhle workflow.

Kategorie a jejich celé názvy podsložek (PM, OBR, PU, M, MO, O, L, T) jsou v
`kategorie.json` (vedle tohoto souboru) — použij tenhle soubor místo odhadování názvu
podsložky.

## 1. Zjisti, o co jde (volný text + našeptávání)

Uživatel popíše nový postup volně (text/diktát). Neposílej mu prázdný formulář. Místo toho:

1. Z volného textu vytáhni, co jde vytáhnout automaticky.
2. Doptej se JEN na chybějící kritické věci, a nabídni možnosti (našeptávání), aby uživatel
   nemusel psát od nuly:
   - **Kategorie** — nabídni existující (dle `kategorie.json`) + možnost "jiná/nová".
   - **Krátký název** (pro nadpis a název souboru).
   - **Kroky postupu** — pokud v textu chybí pořadí, zeptej se na pořadí kroků.
   - **Klíčové parametry** (materiál, nástroj, otáčky/rychlost posuvu, ředění, časy... podle
     kategorie — u OBR/PM nabídni technické parametry, u PU nabídni materiál/ředění/postup
     vrstev, u M/O nabídni recepturu/poměry).
   - **Kdy se postup použije** (na jaké produkty/situace se vztahuje) — důležité pro pozdější
     vyhledání a pro detekci kolize.
   - **BOZP** — pokud jde o nebezpečnou operaci (stroje, chemikálie), zeptej se na bezpečnostní
     upozornění; pokud ne, přeskoč beze ptaní.
3. Nepokládej víc otázek najednou, než je nutné — max. jedno kolo doplňujících otázek, pak
   ukaž návrh.
4. Zároveň nech doběhnout **poradce** (`poradce.md` vedle tohoto souboru) — když už na
   téma něco v knihovně nebo ve školicích materiálech existuje, řekni to teď, ne až po
   zápisu. Uživatel se pak sám rozhodne, jestli píše nový záznam, nebo rozšiřuje
   existující. Tohle je něco jiného než kontrola kolize kódu (bod 3) — ta hlídá čísla,
   poradce hlídá obsah.

## 2. Urči kód TPP (kategorie + číslo)

**Nikdy nespoléhej jen na INDEX.md pro číslování — může být neaktuální vůči realitě**
(index už dřív driftoval, viz varovný blok v hlavičce `INDEX.md`).

Postup:
1. Zjisti reálný název kategorijní podsložky z `kategorie.json`. Pokud kategorie
   neexistuje, navrhni založení nové podsložky a potvrď název s uživatelem.
2. Vylistuj **skutečný obsah** té podsložky (soubory `T.TPP.<KAT>.<n>...`) a najdi nejvyšší
   použité číslo `n` (včetně podčísel typu `.1`, `.2`).
3. Zkontroluj i `INDEX.md` pro stejnou kategorii.
4. Navrhni uživateli další volné číslo = max(reálné soubory, INDEX) + 1. Ukaž mu, z čeho jsi
   vycházel, ať vidí případný nesoulad.
5. Pokud najdeš nesoulad mezi INDEX.md a realitou (soubor bez záznamu v indexu), uprav to
   MIMO tento zápis — jen na to uživatele upozorni a nabídni „chceš rovnou doplnit i chybějící
   staré záznamy do indexu (workflow kontrola-indexu)?". Neopravuj INDEX bez potvrzení.

## 3. Kontrola kolize

- **Tvrdá kolize (blok)**: navržený kód už existuje jako soubor → nikdy nepřepisuj automaticky.
  Zeptej se, jestli jde o ÚPRAVU existujícího záznamu (pak jdi do postupu "úprava" v bodě 5),
  nebo o chybu v číslování (navrhni jiné volné číslo).
- **Měkká kolize (varování, neblokuje)**: v rámci stejné kategorie existuje záznam s podobným
  názvem/klíčovými slovy (např. nový zápis o lakování je blízký existujícímu PU.4). Upozorni:
  "Tohle vypadá podobně jako T.TPP.PU.4 (Lakování složitých součástí typ B) — je to skutečně
  nový, odlišný postup, nebo varianta/úprava existujícího?" Nech rozhodnutí na uživateli.

## 4. Ukaž návrh, počkej na potvrzení

Než cokoli zapíšeš, ukaž kompletní návrh v chatu ve finální podobě (ne jen shrnutí).

**Hlavička musí přesně odpovídat formátu existujících TPP dokumentů v knihovně**
(ověřeno na `T.TPP.O.1` a `T.TPP.OBR.2` — obojí mají identickou hlavičku, liší se jen tělem):

```
T.TPP.<KAT>.<n> <Název>

Cíl: <krátce, proč tenhle postup existuje / co má zajistit>

Obsah: Pracovní postup 
Touto směrnicí se řídí: <kdo — např. Programátor NC kódu, Pracovníci stolárny>
_________________________________________
Umístění tištěné verze:  
Za aktuálnost zodpovídá: TPV
Poslední úprava dne: <datum>

Při změně pracovního postupu informovat TPV, která aktualizuje tuto směrnici.

Pomůcky: <seznam, pokud relevantní>

### Postup
1. ...
2. ...

### Parametry / materiál
- ...

### Nejčastější nešvary
- ... (jen pokud relevantní — starší TPP tuhle sekci nemívají zvlášť, ale je to
  zlepšení, ne odchylka od standardu — zachovávat)

### BOZP
- ... (jen pokud relevantní)

**Zdroj zápisu:** <kdo/odkud, datum>
```

Poznámka: existující TPP v knihovně tělo postupu často nestrukturují do sekcí
(Postup/Parametry/Nešvary/BOZP) — píšou volný text/odrážky. Nový zápis touhle skillem
naopak VŽDY strukturuje tělo do sekcí výše (uživatelovo rozhodnutí — čitelnější než
volný text původních TPP). Mění se jen hlavička, ne tělo.

Zeptej se: "Zapsat takto do knihovny jako `T.TPP.<KAT>.<n>`? (ano / uprav X)". Nezapisuj bez
výslovného potvrzení.

## 5. Zápis (nový záznam)

Po potvrzení:
1. Vytvoř soubor `T.TPP.<KAT>.<n> <Název>.md` v příslušné kategorijní podsložce
   (`<library_root>/<tpp_dir>/<kategorijní podsložka>/`). **Výchozí formát je `.md`.**
   Pokud si uživatel výslovně vyžádá Word, vytvoř navíc/místo toho `.docx` se stejným
   obsahem (hlavička dle bodu 4, tělo strukturované). Starší lidmi psané `.doc/.docx`
   se nedotýkat, nekonvertovat.
2. Přidej řádek do `INDEX.md` do příslušné tabulky kategorie (nebo založ novou sekci, pokud jde
   o novou kategorii): Kód | Název | Stav=`draft` | dnešní datum | krátká poznámka.
   Stav je `draft`, dokud nezpracuje workflow review-zapisu.

   Legální hodnoty stavu v `INDEX.md`: `draft` (nový zápis čeká na review), `revize`
   (úprava čeká na re-review), `ověřeno` (prošlo review) a `existující` (včetně variant
   `existující — KOLIZE`, `existující — referenční pomůcka`). **`existující` je finální
   stav** starých provozních dokumentů z doby před skillem — nepřeklápí se na `draft` ani
   na `ověřeno`, nikdy ho neměň hromadně a nový zápis ho nedostává. Stav žije výhradně
   v `INDEX.md`, ne v hlavičce dokumentu.
3. Obě operace (nový soubor + update INDEX.md) proveď jako jednu logickou akci, ne odděleně
   v čase — ať INDEX nikdy chvilku neodpovídá realitě.
4. Potvrď uživateli, kam přesně bylo zapsáno (plná cesta) a jaký status záznam má.

### Úprava existujícího záznamu (místo nového)

Ukaž **diff** (staré vs. nové znění), vyžaduj doslovné textové potvrzení (uživatel musí
napsat přesný kód záznamu, např. "PU.3", nebo slovo "PŘEPSAT") — viz
`bezpecnostni-pravidla.md` bod 2. Po potvrzení uprav soubor a v INDEX.md nastav
stav `revize` (dokud neprojde review), aktualizuj datum a poznámku.

### Mazání

Tento workflow nikdy nic nemaže — mazání dělá workflow review-zapisu (zamítnuté drafty)
nebo kontrola-indexu (chybějící řádky v indexu).

## 6. Neformální kontext (vrstva B) — volitelné

Pokud uživatel při diktátu zmíní postřeh, který NENÍ hotový standardizovaný postup (jen
"mimochodem, tohle se nám osvědčilo..."), nabídni zápis do `poznamky-kontext.md` místo
formálního TPP zápisu — nízkotřecí, bez čísla/kódu. Formát zápisu je jediný a je popsaný
v `tvorba-technologickeho-postupu.md` bodu 9b; drž se ho. Vždy označ jako NEOVĚŘENO.
Na rozdíl od bodu 9b tenhle zápis **nabídni a počkej na potvrzení** — automatický (bez
dotazu) je jen ten v kroku 9b.

## Bezpečnostní pravidla

Platí kompletně `bezpecnostni-pravidla.md` (vedle tohoto souboru, sdílené napříč celým
skillem). Specifika tohoto workflow navíc: nový zápis má vždy status `draft`, dokud
neprojde workflow review-zapisu — tenhle workflow sám nic neschvaluje.
