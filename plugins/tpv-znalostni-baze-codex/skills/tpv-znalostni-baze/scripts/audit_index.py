#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deterministický diff mezi obsahem knihovny na disku a jejími indexy.

Součást skillu tpv-znalostni-baze, workflow `kontrola-indexu.md` (bod 2 a §6.2) a
`obecna-znalostni-baze.md` (§1, krok 0).

Skript POUZE čte a tiskne. Nic nezapisuje, nemaže, needituje a nerozhoduje o kolizích —
interpretace a jakýkoli zápis do knihovny zůstává na Claudovi a uživateli.

Složka THN (config → general_kb_excluded_dirs) se vynechává už při průchodu stromem.
Z THN se nikdy nevypíše název souboru; ověřuje se jen existence položek z
general_kb_thn_allowlist.

Použití:
    python scripts/audit_index.py --index oba
    python scripts/audit_index.py --index tpp --kategorie OBR
    python scripts/audit_index.py --index obecna --json

Návratové kódy: 0 = proběhlo, 2 = kořen knihovny nedostupný / chybí konfigurace.
"""

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / 'config.json'
KATEGORIE_PATH = SKILL_ROOT / 'references' / 'kategorie.json'

# Reálné dokumenty. Ostatní přípony (zámky Office, náhledy, dočasné soubory) se ignorují.
DOC_EXT = {
    '.md', '.doc', '.docx', '.dot', '.dotm', '.rtf', '.txt',
    '.xls', '.xlsx', '.xlsm', '.csv',
    '.ppt', '.pptx', '.pdf', '.ai', '.eps',
}
SKIP_NAMES = {'.ds_store', 'thumbs.db', 'desktop.ini'}

TPP_CODE_RE = re.compile(r'T\.TPP\.([A-Za-zÁ-Žá-ž]{1,4})\.(\d+(?:\.\d+)*)')


def die(msg):
    sys.stderr.write('CHYBA: %s\n' % msg)
    raise SystemExit(2)


def load_json(path, popis):
    if not path.exists():
        die('%s nenalezen: %s' % (popis, path))
    try:
        with path.open(encoding='utf-8') as fh:
            return json.load(fh)
    except ValueError as exc:
        die('%s není validní JSON (%s): %s' % (popis, exc, path))


def is_doc(path):
    if path.name.startswith('~$') or path.name.startswith('.~'):
        return False
    if path.name.lower() in SKIP_NAMES:
        return False
    return path.suffix.lower() in DOC_EXT


def norm(text):
    """Porovnávací tvar cesty: lomítka dopředu, bez úvodního ./, malá písmena."""
    return text.replace('\\', '/').lstrip('./').strip().lower()


def check_root(path, popis):
    if not path.exists() or not path.is_dir():
        die('%s — cesta je nedostupná nebo neexistuje: %s\n'
            'Prázdný výpis odpojeného disku vypadá jako smazaná knihovna — audit se '
            'nedokončil, nehlas nic jako chybějící.' % (popis, path))


# ---------------------------------------------------------------- TPP (INDEX.md)

def parse_index_tpp(path):
    """Vrátí {kód: {'kategorie':…, 'radek':…}} z tabulek INDEX.md.

    Kategorie se bere z posledního `## ` nadpisu nad tabulkou. Kód se čistí od
    varovných značek (⚠️ apod.) a formátování.
    """
    if not path.exists():
        return None
    zaznamy = {}
    kategorie = None
    for radek in path.open(encoding='utf-8'):
        strip = radek.strip()
        if strip.startswith('## '):
            kategorie = strip[3:].strip()
            continue
        if not strip.startswith('|'):
            continue
        bunky = [b.strip() for b in strip.strip('|').split('|')]
        if not bunky:
            continue
        m = TPP_CODE_RE.search(bunky[0])
        if not m:
            continue
        kod = m.group(0)
        zaznamy[kod] = {'kategorie': kategorie, 'radek': strip}
    return zaznamy


def scan_tpp(library_root, tpp_dir, kategorie_map, jen_kategorie=None,
             sluzebni_soubory=()):
    koren = library_root / tpp_dir
    check_root(koren, 'Složka TPP (library_root/tpp_dir)')

    na_disku = {}       # kod -> [cesty]
    mimo_rozsah = []    # soubory v kořeni tpp_dir nebo bez rozpoznaného kódu
    neznama_slozka = []

    for polozka in sorted(koren.iterdir()):
        if polozka.is_file():
            # Samotný index a pracovní poznámky nejsou dokumenty knihovny.
            if is_doc(polozka) and polozka.name not in sluzebni_soubory:
                mimo_rozsah.append(polozka.name)
            continue
        zkratky = [z for z, nazev in kategorie_map.items() if nazev == polozka.name]
        if not zkratky:
            neznama_slozka.append(polozka.name)
            continue
        zkratka = zkratky[0]
        if jen_kategorie and zkratka.upper() != jen_kategorie.upper():
            continue
        for soubor in sorted(polozka.rglob('*')):
            if not soubor.is_file() or not is_doc(soubor):
                continue
            m = TPP_CODE_RE.search(soubor.name)
            rel = str(soubor.relative_to(koren))
            if not m:
                mimo_rozsah.append(rel)
                continue
            na_disku.setdefault(m.group(0), []).append(rel)

    return na_disku, mimo_rozsah, neznama_slozka


def audit_tpp(cfg, kategorie_map, jen_kategorie):
    library_root = Path(cfg['library_root'])
    # INDEX.md i poznamky-kontext.md leží uvnitř složky TPP, ne v kořeni knihovny.
    index_path = library_root / cfg['tpp_dir'] / cfg['index_file']
    sluzebni = (cfg['index_file'], cfg.get('context_notes_file', ''))

    na_disku, mimo_rozsah, neznama_slozka = scan_tpp(
        library_root, cfg['tpp_dir'], kategorie_map, jen_kategorie, sluzebni)
    v_indexu = parse_index_tpp(index_path)

    vysledek = {
        'index_soubor': str(index_path),
        'index_existuje': v_indexu is not None,
        'pocet_na_disku': len(na_disku),
        'pocet_v_indexu': 0 if v_indexu is None else len(v_indexu),
        'chybi_v_indexu': [],
        'chybi_na_disku': [],
        'kolize_kodu': [],
        'mimo_rozsah': sorted(mimo_rozsah),
        'nezname_slozky': sorted(neznama_slozka),
    }

    for kod, cesty in sorted(na_disku.items()):
        if len(cesty) > 1:
            vysledek['kolize_kodu'].append({'kod': kod, 'soubory': cesty})
        if v_indexu is not None and kod not in v_indexu:
            vysledek['chybi_v_indexu'].append({'kod': kod, 'soubory': cesty})

    if v_indexu is not None:
        for kod in sorted(v_indexu):
            if kod not in na_disku:
                if jen_kategorie:
                    kat = (v_indexu[kod]['kategorie'] or '')
                    if not kat.upper().startswith(jen_kategorie.upper()):
                        continue
                vysledek['chybi_na_disku'].append(
                    {'kod': kod, 'kategorie': v_indexu[kod]['kategorie']})

    return vysledek


# -------------------------------------------------- obecná báze (INDEX-smernice.md)

BULLET_RE = re.compile(r'^\s*[-*]\s')
BACKTICK_RE = re.compile(r'`([^`]+)`')


def parse_index_obecna(path):
    """Vrátí {normalizovaná cesta: původní zápis} z odrážek INDEX-smernice.md."""
    if not path.exists():
        return None
    cesty = {}
    for radek in path.open(encoding='utf-8'):
        if not BULLET_RE.match(radek):
            continue
        for kus in BACKTICK_RE.findall(radek):
            kus = kus.strip()
            if '/' not in kus and '\\' not in kus:
                continue
            if Path(kus).suffix.lower() not in DOC_EXT:
                continue
            cesty[norm(kus)] = kus
    return cesty


def scan_obecna(cfg):
    koren = Path(cfg['general_kb_root'])
    check_root(koren, 'Kořen obecné báze (general_kb_root)')

    vyloucene = {n.lower() for n in cfg.get('general_kb_excluded_dirs', [])}
    vyloucene.add(cfg['tpp_dir'].lower())
    # library_root leží uvnitř general_kb_root; TPP podsložku pokrývá audit INDEX.md.
    tpp_abs = (Path(cfg['library_root']) / cfg['tpp_dir']).resolve()

    nalezene = {}

    def projdi(slozka):
        try:
            polozky = sorted(slozka.iterdir())
        except OSError as exc:
            sys.stderr.write('POZOR: nelze číst %s (%s)\n' % (slozka, exc))
            return
        for polozka in polozky:
            if polozka.is_dir():
                if polozka.name.lower() in vyloucene:
                    continue          # THN se neprochází — ani kvůli výpisu názvů
                if polozka.name.startswith('.'):
                    continue
                try:
                    if polozka.resolve() == tpp_abs:
                        continue
                except OSError:
                    pass
                projdi(polozka)
            elif polozka.is_file() and is_doc(polozka):
                rel = str(polozka.relative_to(koren))
                nalezene[norm(rel)] = rel

    projdi(koren)
    return nalezene


def zkontroluj_allowlist(cfg):
    """Jediný povolený kontakt s THN: existuje allowlistovaný soubor?"""
    koren = Path(cfg['general_kb_root'])
    vysledek = []
    for nazev in cfg.get('general_kb_thn_allowlist', []):
        nalezeno = False
        for slozka in cfg.get('general_kb_excluded_dirs', []):
            if (koren / slozka / nazev).exists():
                nalezeno = True
                break
        vysledek.append({'soubor': nazev, 'existuje': nalezeno})
    return vysledek


def podobne(a, b):
    """Hrubý odhad přejmenování: shodný název souboru, nebo jeden je prefixem druhého."""
    na, nb = Path(a).name.lower(), Path(b).name.lower()
    if na == nb:
        return True
    kratsi, delsi = sorted([na, nb], key=len)
    return len(kratsi) >= 12 and delsi.startswith(kratsi[:12])


def audit_obecna(cfg):
    koren = Path(cfg['general_kb_root'])
    index_path = koren / cfg['general_kb_index_file']

    na_disku = scan_obecna(cfg)
    v_indexu = parse_index_obecna(index_path)

    vysledek = {
        'index_soubor': str(index_path),
        'index_existuje': v_indexu is not None,
        'pocet_na_disku': len(na_disku),
        'pocet_v_indexu': 0 if v_indexu is None else len(v_indexu),
        'chybi_v_indexu': [],
        'chybi_na_disku': [],
        'mimo_rozsah_vylouceno': 0,
        'pravdepodobne_prejmenovano': [],
        'thn_allowlist': zkontroluj_allowlist(cfg),
    }
    if v_indexu is None:
        return vysledek

    # Položky indexu, které leží ve vyloučených složkách (THN), se na disku vůbec
    # neprocházejí — nesmí se tedy vykázat jako „chybí na disku“. Jen se spočítají.
    vyloucene = [d.lower() for d in cfg.get('general_kb_excluded_dirs', [])]

    def je_vyloucena(rel):
        prvni = str(rel).replace('/', '\\').split('\\')[0].lower()
        return prvni in vyloucene

    chybi_v_indexu = [na_disku[k] for k in sorted(na_disku) if k not in v_indexu]
    chybi_na_disku = []
    for k in sorted(v_indexu):
        if k in na_disku:
            continue
        if je_vyloucena(v_indexu[k]):
            vysledek['mimo_rozsah_vylouceno'] += 1
            continue
        chybi_na_disku.append(v_indexu[k])

    parovane_disk, parovane_index = set(), set()
    for stary in chybi_na_disku:
        for novy in chybi_v_indexu:
            if novy in parovane_disk:
                continue
            if podobne(stary, novy):
                vysledek['pravdepodobne_prejmenovano'].append(
                    {'v_indexu': stary, 'na_disku': novy})
                parovane_disk.add(novy)
                parovane_index.add(stary)
                break

    vysledek['chybi_v_indexu'] = [c for c in chybi_v_indexu if c not in parovane_disk]
    vysledek['chybi_na_disku'] = [c for c in chybi_na_disku if c not in parovane_index]
    return vysledek


# ------------------------------------------------------------------------- výstup

def vypis_seznam(nadpis, polozky, formatovac=str):
    print('  %s: %d' % (nadpis, len(polozky)))
    for p in polozky:
        print('    - %s' % formatovac(p))


def vypis_tpp(v):
    print('=== TPP (%s) ===' % v['index_soubor'])
    if not v['index_existuje']:
        print('  INDEX.md neexistuje — TPP báze zatím nebyla zaindexovaná.')
    print('  Na disku: %d kódů | v indexu: %d záznamů'
          % (v['pocet_na_disku'], v['pocet_v_indexu']))
    vypis_seznam('Chybí v indexu', v['chybi_v_indexu'],
                 lambda x: '%s  (%s)' % (x['kod'], ', '.join(x['soubory'])))
    vypis_seznam('Chybí na disku', v['chybi_na_disku'],
                 lambda x: '%s  [%s]' % (x['kod'], x['kategorie']))
    vypis_seznam('Kolize kódu', v['kolize_kodu'],
                 lambda x: '%s  (%s)' % (x['kod'], ' | '.join(x['soubory'])))
    vypis_seznam('Mimo rozsah (informace, ne drift)', v['mimo_rozsah'])
    if v['nezname_slozky']:
        vypis_seznam('Podsložky neznámé v kategorie.json', v['nezname_slozky'])
    print('')


def vypis_obecna(v):
    print('=== Obecná báze (%s) ===' % v['index_soubor'])
    if not v['index_existuje']:
        print('  INDEX-smernice.md neexistuje — obecná báze zatím nebyla zaindexovaná '
              '(viz obecna-znalostni-baze.md bod 1).')
    print('  Na disku: %d dokumentů | v indexu: %d cest'
          % (v['pocet_na_disku'], v['pocet_v_indexu']))
    vypis_seznam('Chybí v indexu', v['chybi_v_indexu'])
    vypis_seznam('Chybí na disku', v['chybi_na_disku'])
    vypis_seznam('Pravděpodobně přejmenováno/přesunuto (odhad)',
                 v['pravdepodobne_prejmenovano'],
                 lambda x: '%s  ->  %s' % (x['v_indexu'], x['na_disku']))
    for a in v['thn_allowlist']:
        print('  THN allowlist: %s — %s'
              % (a['soubor'], 'existuje' if a['existuje'] else 'NENALEZEN'))
    print('  Položek indexu ve vyloučených složkách (nekontrolováno): %d'
          % v['mimo_rozsah_vylouceno'])
    print('  (Zbytek složky THN se neprochází a do diffu nepatří.)')
    print('')


def main():
    p = argparse.ArgumentParser(
        description='Diff disk vs. index pro skill tpv-znalostni-baze. Nic nezapisuje.')
    p.add_argument('--index', choices=['tpp', 'obecna', 'oba'], default='oba')
    p.add_argument('--kategorie', help='omez TPP audit na jednu kategorii (např. OBR)')
    p.add_argument('--json', action='store_true', help='strojový výstup')
    args = p.parse_args()

    cfg = load_json(CONFIG_PATH, 'config.json')
    kategorie_map = {k: v for k, v in load_json(KATEGORIE_PATH, 'kategorie.json').items()
                     if not k.startswith('_')}

    for klic in ('library_root', 'tpp_dir', 'index_file',
                 'general_kb_root', 'general_kb_index_file'):
        if klic not in cfg:
            die('v config.json chybí klíč "%s"' % klic)

    out = {}
    if args.index in ('tpp', 'oba'):
        out['tpp'] = audit_tpp(cfg, kategorie_map, args.kategorie)
    if args.index in ('obecna', 'oba'):
        out['obecna'] = audit_obecna(cfg)

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if 'tpp' in out:
            vypis_tpp(out['tpp'])
        if 'obecna' in out:
            vypis_obecna(out['obecna'])
        print('Skript nic nezapsal. Rozhodnutí a případný zápis do knihovny '
              'patří uživateli (kontrola-indexu.md body 4–6).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
