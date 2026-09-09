#!/bin/bash
# Převede vygenerovaný Markdown technologický postup na .docx k tisku.
# Použití: ./md_to_docx.sh postup.md postup.docx
#
# Pandoc na Windows často není na PATH (winget ho instaluje do LOCALAPPDATA a PATH se
# projeví až v novém shellu). Proto ho hledáme i na obvyklých místech, místo abychom
# spadli na "command not found" a nutili uživatele řešit instalaci uprostřed práce.
set -e

find_pandoc() {
  if command -v pandoc >/dev/null 2>&1; then
    command -v pandoc
    return 0
  fi
  local candidates=(
    "$LOCALAPPDATA/Pandoc/pandoc.exe"
    "$PROGRAMFILES/Pandoc/pandoc.exe"
    "/c/Program Files/Pandoc/pandoc.exe"
    "$HOME/AppData/Local/Pandoc/pandoc.exe"
    "/usr/local/bin/pandoc"
    "/opt/homebrew/bin/pandoc"
  )
  for c in "${candidates[@]}"; do
    [ -x "$c" ] && { echo "$c"; return 0; }
  done
  return 1
}

PANDOC="$(find_pandoc)" || {
  echo "Pandoc nenalezen. Nainstaluj ho a spusť znovu:" >&2
  echo "  winget install --id JohnMacFarlane.Pandoc -e --accept-package-agreements --accept-source-agreements" >&2
  echo "  (macOS: brew install pandoc / Linux: apt install pandoc)" >&2
  exit 127
}

# Firemní šablona stylů, pokud existuje vedle skillu — dá dokumentu vzhled vzoru T.1.3.1
# místo pandocího defaultu. Když chybí, převod proběhne normálně bez ní.
REFDOC="$(dirname "$0")/../assets/reference.docx"
if [ -f "$REFDOC" ]; then
  "$PANDOC" "$1" --reference-doc="$REFDOC" -o "$2"
else
  "$PANDOC" "$1" -o "$2"
fi

echo "Hotovo: $2"
