# TPV znalostní báze – Codex plugin

Sdílitelný lokální plugin pro technologické postupy, směrnice a školení firmy Mašek – umělecká výroba.

## Co balíček obsahuje

- plugin `tpv-znalostni-baze-codex`,
- skill `tpv-znalostni-baze`,
- firemní šablonu DOCX a pomocné skripty,
- lokální marketplace `masek-interni` pro instalaci do Codexu.

Samotné firemní dokumenty nejsou součástí balíčku. Plugin je čte z cest nastavených v souboru:

`plugins/tpv-znalostni-baze-codex/skills/tpv-znalostni-baze/config.json`

Výchozí konfigurace očekává firemní disk `U:`. Na jiném počítači musí být tato síťová jednotka dostupná pod stejným písmenem, nebo je potřeba cesty v `config.json` upravit.

## Instalace

1. Rozbalte celý balíček do trvalé složky. Po instalaci jej nepřesouvejte ani nemažte.
2. V terminálu přejděte do rozbalené kořenové složky.
3. Přidejte lokální marketplace:

   `codex plugin marketplace add .`

4. Nainstalujte plugin:

   `codex plugin add tpv-znalostni-baze-codex@masek-interni`

5. Otevřete v Codexu novou konverzaci, aby se plugin načetl.

## Aktualizace

Při nové verzi nahraďte rozbalenou složku aktualizovaným balíčkem a plugin znovu přidejte stejným příkazem. Před nahrazením si uchovejte případné místní změny v `config.json`.

## Bezpečnost

Plugin může podle potvrzených pokynů zapisovat do firemní knihovny. Přístup uživatele k disku `U:` proto nastavte jen v rozsahu, který pro práci skutečně potřebuje.
