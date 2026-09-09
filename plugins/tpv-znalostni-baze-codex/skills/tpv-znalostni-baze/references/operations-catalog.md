# Katalog operací (fixní, dle T.1.3.1 vzoru)

Katalog dodává **informace o jednotlivých operacích**: číslo, název, kontrolní otázky,
případně technologické poznámky a související dokumentaci. **Čísla a názvy jsou fixní** —
použij přesně tato čísla a názvy. Zaškrtává se ☒ (aktivní) / ☐ (neaktivní) podle toho, co
se pro danou zakázku reálně použije.

**Pořadí řádků v téhle tabulce NENÍ technologické pořadí.** Je to evidenční číselník —
posloupnost operací určuje výhradně uživatel:

1. Pořadí zadané uživatelem se zachová přesně tak, jak ho zadal.
2. Když ho uživatel později změní, platí ta pozdější změna — je finální.
3. Nikdy nepřeskládávej operace podle pořadí v katalogu, podle číselného kódu, podle
   abecedy, podle pořadí nalezených výsledků ani podle vlastní domněnky.
4. Když uživatel pořadí nezadal a nejde ho jednoznačně odvodit, nevymýšlej si posloupnost
   a nevydávej ji za ověřený fakt — označ ji jako **návrh k potvrzení**.
5. Na technologické riziko v zadaném pořadí smíš upozornit, ale pořadí sám nezměníš.
6. Vždy rozlišuj, co je pořadí od uživatele a co je informace převzatá z katalogu.

Pro párování času zmíněného ve volném textu k operaci (`tvorba-technologickeho-postupu.md`
krok 5) použij
`cas-klicova-slova.json` vedle tohoto souboru — hotová vyhledávací tabulka
klíčové slovo → kód operace, není potřeba to odvozovat z názvu za běhu.

| Číslo | Operace |
|---|---|
| 999031 | Skenování |
| 999027 | Grafická příprava |
| 999029 | PC příprava programu |
| 999030 | Příprava materiálu |
| 999035 | Seřízení, nastavení |
| 999040 | NC frézování 3 osá |
| 999041 | NC frézování 5 osá |
| 999048 | Soustružení |
| 999049 | Soustruh - frézování |
| 999045 | Spodní fréza – ruční frézování |
| 999050 | Kalibrování, kartáčování |
| 999052 | Broušení |
| 999055 | Bubnování |
| 999056 | Vibrování |
| 999053 | Laser |
| 999060 | Kompletace, dokončení, zhotovení |
| 999070 | Lakování nebo moření |
| 999090 | Tisk tampon |
| 999092 | Tisk digitální dřevo |
| 999160 | Vrtání |
| 999170 | Řezání |
| 999200 | Výstupní kontrola |
| 999002 | Malování sochy, obrazy |
| 999011 | Šití kompletní (+navazování, balení) |
| 999025 | Odlití výrobku |

## Kontrolní seznamy pro nejčastější operace (z existujícího vzoru)

**999027 Grafická příprava / Tvorba modelu / tech. dokumentace**
- Jaký bude vstupní materiál? (řezivo / plošný materiál, ze skladu, na objednávku, od zákazníka)
- Je materiál dostupný skladem nebo je potřeba objednat?
- Vím všechny potřebné rozměry k výrobě? Mám skicu nebo výkres?
- Zvýraznil jsem důležité rozměry, které je potřeba kontrolovat?

**999029 PC příprava programu**
- Vím kde se nachází nulový bod / offset?
- Mám tool_list, vím jaké nástroje a offsety se budou používat?
- Znám pořadí operací programu?
- Mám udělaný postproces a uložený CNC program?
- Jsou nástroje dostupné?

**999035 Seřízení, nastavení**
- Zkontroluji rozměr polotovaru a materiál
- Nastavím nulový bod / offset podle dodaných informací
- Nastavím korekce nástrojů / délky / poloměry / kapsy
- Upnu polotovar a zkontroluji bezpečné upnutí
- Vše projdu ještě jednou a provedu kontrolu po sobě
- První kus si nechám schválit, že je OK
- Přípravky popisuji názvem a číslem zakázky

**999200 Výstupní kontrola**
- Kontrola kvality
- Kontrola počtů hotových kusů / zmetků
- Zapsání informací na výrobní list
- Naskladnění / zabalení k odeslání

Pro ostatní operace (999040 NC frézování, 999060 Kompletace...) kontrolní seznam ve vzoru chybí — kroky se doplňují napřímo (číslovaný seznam), případně odkazem na T.TPP.* postup z knihovny.
