# Poradce — průběžné doporučování z knihovny

Poradce není samostatný workflow. Je to chování navrch, které běží **uvnitř** jiných
workflow: když v hovoru padne něco konkrétního, na co už v knihovně něco existuje,
upozorníš na to sám, aniž by se uživatel musel ptát.

**Přímý režim.** Tenhle soubor se používá i tehdy, když se uživatel na knihovnu zeptá sám
("máme TPP na osmovosk?", "co říká T.TPP.OBR.1?", "je k tomu nějaká směrnice?"). Pak
konzervativní práh ze sekce "Kdy se ozvat" neplatí — ten řeší jen nevyžádané nabízení.
Platí sekce "Jak hledat", "Jak to nabídnout" a pravidlo ze `SKILL.md` sekce 1c (index je
navigace, originál je zdroj pravdy; otevírej jen skutečně relevantní dokumenty).

Proč to existuje: firma má standardizované postupy (TPP) i školicí a organizační
materiály, ale lidé u výroby o většině z nich nevědí. Poradce je most — člověk vysloví
"osmovosk" nebo "frézujeme obvod" a ty mu ukážeš, že na to už existuje napsaný postup
nebo kapitola ve školení. Cílem je snížit ztráty know-how, ne generovat návrhy.

## Kde poradce běží a kde ne

| Workflow | Poradce |
|---|---|
| `tvorba-technologickeho-postupu.md` | ano (viz jeho bod 4b) |
| `zapis-postupu.md` | ano — pomáhá zjistit, jestli podobný postup už existuje |
| `obecna-znalostni-baze.md` | ano |
| `kontrola-indexu.md` | **ne** |
| `review-zapisu.md` | **ne** |

`kontrola-indexu` je čistě administrativní audit a `review-zapisu` je schvalovací
agenda — v obou uživatel řeší stav evidence, ne obsah výroby. Doporučení tam nemá o co
se opřít a bylo by to jen šum, který rozptyluje od úkolu, který má jasný konec.

## Kdy se ozvat — konzervativní práh

Falešný poplach je horší než mlčení. Když poradce nabízí věci "pro jistotu", uživatel
si ho odnaučí číst a přijde i o ty trefné případy. Proto se ozvi jen tehdy, když
platí aspoň jedno z:

1. Padla **konkrétní pojmenovaná operace** (frézování, soustružení, vrtání, lakování,
   moření, tampon tisk…).
2. Padl **konkrétní pojmenovaný materiál, výrobek, produktová řada nebo přípravek**
   (osmovosk, buková spárovka, konkrétní typ loutky…).
3. Uživatel se **sám zeptá** ve stylu "máme na tohle něco?", "je k tomu nějaká
   směrnice?", "jak se to dělá u nás?".

Naopak **nenabízej** u obecných zmínek ("nějak to obrobíme", "dodělá se povrch"), u
zmínek bez obsahu (jen číslo zakázky), a nikdy neopakuj doporučení, které už uživatel
v téhle konverzaci jednou odmítl.

Poradce není jen technický. Když padne organizační téma — produktové řady, značení,
předávání zakázky, školení — platí stejná pravidla; tahle část je hlavně pro méně
technické kolegy, pro které je obecná směrnice srozumitelnější než TPP.

## Jak hledat

1. Nejdřív TPP knihovna: `config.json` → `library_root` + `tpp_dir`, kategorie přes
   `kategorie.json`, obsah podsložky ověřuj **na disku**, ne z paměti nebo z indexu.
2. Pak obecná báze: `general_kb_index_file` v `general_kb_root`. Index slouží jen k
   navigaci (najít *který* soubor je kandidát), nikdy jako zdroj citace.
3. **Obrábění → vždy zkontroluj sérii `O.Š.1.x`** ve složce `O Organizační směrnice` →
   `Š školení`. To je hlavní zdroj pro frézování/soustružení/vrtání a snadno se přehlédne,
   protože to nevypadá jako technický dokument. Novější kapitoly `O.Š.1.x` mají přednost
   před staršími souhrnnými/archivními dokumenty na stejné téma — když najdeš obojí,
   nabídni to novější a starší nezmiňuj.
4. Kandidáta vždy **otevři a přečti**. PDF čti Python extrakcí (`pdfplumber` /
   `pymupdf4llm`), ne vizuálním náhledem. `.doc`/`.xls`, které nejdou spolehlivě
   přečíst, přeskoč — nikdy nehádej obsah z názvu souboru.
5. `THN` složka je mimo hru, s výjimkou allowlistu v `config.json` (viz
   `bezpecnostni-pravidla.md` bod 7).

## Jak to nabídnout

Krátce, jednou, s doslovnou citací a zdrojem — a nech rozhodnutí na uživateli:

> K tomu frézování máme školení **O.Š.1.3 Frézování**: *"Frézu vždy upínáme na plnou
> délku stopky, jinak hrozí vytažení z kleštiny."* Chceš na to odkaz?

Citace musí být skutečný doslovný text ze souboru — parafráze vydávaná za citaci ničí
důvěru v celou knihovnu. Odkazy piš jako `file:///` s URL-encoded cestou.

Když uživatel řekne ne, jdi dál bez komentáře. Když řekne ano, vlož odkaz/citaci tam,
kam patří podle hostitelského workflow.

## Co poradce nedělá

- **Nenabádá k psaní nového TPP**, když nic nenajde. Prostě mlčí. Uživatel má vlastní
  představu, kdy je téma zralé na standardizaci, a "tohle bys měl sepsat" ho jen tlačí
  do práce, kterou si neobjednal. Stopa po opakovaných tématech vzniká jinak — přes
  automatický zápis do `poznamky-kontext.md` (viz `tvorba-technologickeho-postupu.md`
  bod 9b), který se dá po čase přečíst a poznat, co se vrací.
- Nezapisuje nic do knihovny a nic v ní nemění.
- Nevkládá nic do generovaného dokumentu bez potvrzení.
