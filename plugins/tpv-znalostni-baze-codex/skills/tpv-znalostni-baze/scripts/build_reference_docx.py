"""Postaví assets/reference.docx — šablonu stylů pro pandoc převod postupů do .docx.

Nevytváří se ručně: bere se firemní vzor (.dotm) jako zdroj pravdy pro písmo, velikost,
jazyk a stránku, a ten se "naroubuje" na pandocí výchozí reference.docx. Ruční editace
výsledku se při dalším přegenerování ztratí — měň tenhle skript.

Vstup:  assets/ref_default.docx
        (vyrob: pandoc --print-default-data-file reference.docx > assets/ref_default.docx)
Výstup: assets/reference.docx

Cesty se neodvozují od pracovního adresáře — vstup i výstup leží vedle skriptu
(`../assets/`) a cesta k firemní šabloně `.dotm` je v `config.json` → `docx_template`.
Skript jde tedy spustit odkudkoli a nemá v sobě žádnou napevno zadanou cestu na disk U:.
"""
import zipfile, re, os, json
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG = SKILL_ROOT / 'config.json'

if not CONFIG.exists():
    raise SystemExit('CHYBA: nenalezen config.json (%s) — skript musí zůstat ve složce '
                     'scripts/ uvnitř skillu.' % CONFIG)
with CONFIG.open(encoding='utf-8') as fh:
    cfg = json.load(fh)
if 'docx_template' not in cfg:
    raise SystemExit('CHYBA: v config.json chybí klíč "docx_template" (cesta k firemní '
                     'šabloně .dotm).')

TPL = cfg['docx_template']
SRC = str(SKILL_ROOT / 'assets' / 'ref_default.docx')
DST = str(SKILL_ROOT / 'assets' / 'reference.docx')

if not os.path.exists(TPL):
    raise SystemExit('CHYBA: firemní šablona není dostupná: %s\n'
                     'Zkontroluj připojení disku U: a klíč "docx_template" v config.json.'
                     % TPL)
if not os.path.exists(SRC):
    raise SystemExit('CHYBA: chybí vstupní %s\n'
                     'Vyrob ho: pandoc --print-default-data-file reference.docx > "%s"'
                     % (SRC, SRC))

# Rozměry stránky v twipech: A4 (11906x16838). Firemní .dotm i reálné vyplněné postupy
# mají Letter (12240x15840) — to je ale stará chyba v šabloně, která se jen kopírovala dál,
# ne záměr. Tiskne se na A4, takže tady je A4 správně a záměrně se šablonou nesouhlasí.
PG_W, PG_H = 11906, 16838
MARGIN = 1417  # 2,5 cm

# Nadpisy podle reálného postupu: název zakázky tučně 16 pt, hlavička operace tučně 11 pt,
# obojí černě. Pandocí default je modrý bezpatkový 20/16 pt — na dílenském papíře cizí.
HEADING_LOOK = {'Heading1': 32, 'Heading2': 22, 'Heading3': 24, 'Heading4': 24}

tpl = zipfile.ZipFile(TPL)
theme = tpl.read('word/theme/theme1.xml')
tpl_styles = tpl.read('word/styles.xml').decode('utf8')
docdefaults = re.search(r'<w:docDefaults>.*?</w:docDefaults>', tpl_styles, re.S).group(0)

# Šablona používá novější jmenné prostory (w14/w15/w16 — např. w14:ligatures), které
# pandocí styles.xml nedeklaruje. Ponechat je znamená nevalidní XML a Word soubor
# odmítne jako poškozený. Jsou to čistě kosmetické doplňky, takže je zahazujeme.
docdefaults = re.sub(r'<w1[456][^>]*/>', '', docdefaults)
docdefaults = re.sub(r'<w1[456][^>]*>.*?</w1[456][^>]*>', '', docdefaults, flags=re.S)


def patch_heading(styles_xml, style_id, half_points):
    """Zčerná, ztuční a zmenší jeden nadpisový styl na firemní vzhled."""
    m = re.search(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % style_id, styles_xml, re.S)
    if not m:
        return styles_xml
    block = m.group(0)
    block = re.sub(r'<w:color[^/]*/>', '', block)              # pryč s modrou accent1
    block = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="%d"/>' % half_points, block)
    block = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="%d"/>' % half_points, block)
    if '<w:b/>' not in block:
        # Pořadí prvků uvnitř w:rPr je dané schématem (rFonts → b → ... → color → sz).
        # Pandoc styly načte a znovu serializuje, takže prvek na špatném místě tiše zahodí
        # — proto se tučné vkládá až za <w:rFonts/>, ne hned za <w:rPr>.
        block = re.sub(r'(<w:rFonts[^>]*/>)', r'\1<w:b/><w:bCs/>', block, count=1)
    return styles_xml.replace(m.group(0), block)


src = zipfile.ZipFile(SRC)
out = zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED)

for item in src.infolist():
    data = src.read(item.filename)
    if item.filename == 'word/theme/theme1.xml':
        data = theme
    elif item.filename == 'word/styles.xml':
        s = data.decode('utf8')
        # převzít docDefaults ze šablony (12pt, cs-CZ, řádkování) místo pandocích
        s = re.sub(r'<w:docDefaults>.*?</w:docDefaults>', docdefaults.replace('\\', '\\\\'), s, count=1, flags=re.S)
        # nadpisy ať používají fonty z firemního motivu, ne natvrdo Calibri Light
        s = s.replace('w:ascii="Calibri Light" w:hAnsi="Calibri Light"',
                      'w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"')
        for sid, sz in HEADING_LOOK.items():
            s = patch_heading(s, sid, sz)
        data = s.encode('utf8')
    elif item.filename == 'word/document.xml':
        s = data.decode('utf8')
        # Pandocí default žádné pgSz/pgMar nemá, takže je doplňujeme do sectPr —
        # pořadí prvků v sectPr je dané schématem, pgSz/pgMar jdou až za footnotePr.
        s = re.sub(r'<w:pgSz[^/]*/>', '', s)
        s = re.sub(r'<w:pgMar[^/]*/>', '', s)
        s = s.replace('</w:sectPr>',
                      '<w:pgSz w:w="%d" w:h="%d"/>'
                      '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" '
                      'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
                      % (PG_W, PG_H, MARGIN, MARGIN, MARGIN, MARGIN))
        data = s.encode('utf8')
    out.writestr(item, data)

out.close()

# Kontrola, že je výsledek platný OOXML. Word na nevalidní XML reaguje hláškou
# "soubor je poškozený" bez vysvětlení, takže se to musí chytit tady, ne u uživatele.
from xml.dom import minidom
chk = zipfile.ZipFile(DST)
bad = []
for name in chk.namelist():
    if name.endswith('.xml') or name.endswith('.rels'):
        try:
            minidom.parseString(chk.read(name))
        except Exception as e:
            bad.append(f'{name}: {e}')
if bad:
    raise SystemExit('NEVALIDNÍ XML:\n' + '\n'.join(bad))

print('OK', DST, os.path.getsize(DST), '- všechny XML části validní')
