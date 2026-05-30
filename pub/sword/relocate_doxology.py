#!/usr/bin/env python3
"""Siirrä Roomalaiskirjeen doksologia bysanttilaisesta sijainnista KJV-sijaintiin.

FinARK perustuu bysanttilaiseen enemmistötekstiin (Robinson–Pierpont), jossa
Roomalaiskirjeen ylistys (doksologia) sijaitsee luvun 14 lopussa jakeina
14:24–26. Yksikään SWORD-versifikaatio ei tunne jakeita Room 14:24–26, joten
osis2mod liittäisi ne jakeeseen 14:23 (teksti yhdistyisi väärin).

KJV-versifikaatio sijoittaa doksologian jakeisiin Room 16:25–27. Tämä skripti
siirtää nuo kolme jaetta luvun 14 lopusta luvun 16 loppuun ja numeroi ne
uudelleen, jolloin teksti istuu KJV-versifikaatioon täydellisesti ilman
yhtään epäsovitusta.

Itse käännöksen lähde-OSISia (FinARK.xml) EI muokata: muunnos tehdään aina
buildin yhteydessä automaattisesti, joten käännöksen päivittyessä mitään ei
tarvitse muistaa tehdä käsin.

Tekstimuunnos on tarkoituksella tekstipohjainen (ei DOM-uudelleenkirjoitus),
jotta tuloksen muotoilu ja whitespace säilyvät identtisinä lähteen kanssa ja
diff pysyy minimaalisena.

Käyttö:
    python3 relocate_doxology.py SISÄÄN.xml -o ULOS.xml
    python3 relocate_doxology.py SISÄÄN.xml          # tulostaa stdoutiin

Skripti on idempotentti: jos doksologia on jo siirretty (Room 16:25 löytyy),
syöte palautetaan muuttumattomana. Jos odotettua rakennetta ei löydy, skripti
keskeytyy virheeseen — väärin rakennettua moduulia ei synny hiljaisesti.
"""
import argparse
import re
import sys
from typing import NoReturn

# Jakeet jotka siirretään: (vanha Room 14 -jae, uusi Room 16 -jae)
MOVES = [(24, 25), (25, 26), (26, 27)]


def fail(msg: str) -> NoReturn:
    sys.stderr.write(f"relocate_doxology: VIRHE: {msg}\n")
    sys.exit(1)


def relocate(text: str) -> str:
    already_moved = 'osisID="Rom.16.25"' in text
    src_present = 'osisID="Rom.14.24"' in text

    if already_moved and not src_present:
        sys.stderr.write(
            "relocate_doxology: doksologia on jo siirretty (Room 16:25 löytyy) "
            "— syöte palautetaan muuttumattomana.\n"
        )
        return text
    if already_moved and src_present:
        fail("sekä Room 14:24 että Room 16:25 löytyvät — epäselvä lähtötila, keskeytetään.")
    if not src_present:
        fail("Room 14:24 ei löydy — odotettua bysanttilaista doksologiarakennetta ei ole.")

    # 1) Poimi siirrettävät jae-elementit luvusta 14 (container-tyylinen <verse>...</verse>).
    captured = {}
    for old, _ in MOVES:
        m = re.search(rf'<verse osisID="Rom\.14\.{old}">.*?</verse>', text, re.S)
        if not m:
            fail(f"jaetta Room 14:{old} ei löytynyt poimittavaksi.")
        captured[old] = m.group(0)

    # 2) Poista jae-elementit luvusta 14 yhdessä niitä edeltävän whitespacen kanssa,
    #    jolloin luku 14 päättyy siististi jakeeseen 14:23.
    for old, _ in MOVES:
        text, n = re.subn(
            rf'\s*<verse osisID="Rom\.14\.{old}">.*?</verse>', "", text, count=1, flags=re.S
        )
        if n != 1:
            fail(f"jaetta Room 14:{old} ei voitu poistaa luvusta 14.")

    # 3) Numeroi poimitut jakeet uudelleen Room 16 -jakeiksi.
    renumbered = []
    for old, new in MOVES:
        block = captured[old].replace(
            f'osisID="Rom.14.{old}"', f'osisID="Rom.16.{new}"', 1
        )
        renumbered.append(block)

    # 4) Lisää uudelleennumeroidut jakeet luvun 16 viimeisen kappaleen loppuun,
    #    heti jakeen Room 16:24 jälkeen ja ennen kappaleen sulkevaa </p>:tä.
    anchor = re.search(r'<verse osisID="Rom\.16\.24">.*?</verse>', text, re.S)
    if not anchor:
        fail("jaetta Room 16:24 (lisäyksen ankkuri) ei löytynyt.")

    # Lähteen kappalemuotoilu: jokaista jaetta erottaa "\n          \n\n          ".
    sep = "\n          \n\n          "
    insertion = sep + sep.join(renumbered)
    pos = anchor.end()
    text = text[:pos] + insertion + text[pos:]

    # 5) Varmista lopputulos.
    if 'osisID="Rom.14.24"' in text:
        fail("Room 14:24 jäi yhä tekstiin siirron jälkeen.")
    for _, new in MOVES:
        if f'osisID="Rom.16.{new}"' not in text:
            fail(f"Room 16:{new} puuttuu siirron jälkeen.")

    return text


def main() -> "None":
    p = argparse.ArgumentParser(description="Siirrä Room-doksologia 14:24–26 → 16:25–27.")
    p.add_argument("input", help="lähde-OSIS (esim. FinARK.xml)")
    p.add_argument("-o", "--output", help="kohdetiedosto (oletus: stdout)")
    args = p.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    result = relocate(text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        sys.stderr.write(f"relocate_doxology: kirjoitettu {args.output}\n")
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
