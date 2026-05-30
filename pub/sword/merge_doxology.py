#!/usr/bin/env python3
"""Yhdistä Roomalaiskirjeen doksologia (14:24–26) jakeeseen 14:23.

FinARK perustuu bysanttilaiseen enemmistötekstiin (Robinson–Pierpont), jossa
Roomalaiskirjeen ylistys sijaitsee luvun 14 lopussa jakeina 14:24–26. Yksikään
SWORD-versifikaatio ei tunne jakeita Room 14:24–26.

Jos teksti syötetään sellaisenaan osis2modille, se "liittää" jakeet 24–26
jakeeseen 14:23, mutta säilyttää niiden sisäiset jae-milestonet. And Bible
näyttää tällöin jakeesta 14:23 vain ENSIMMÄISEN jae-milestonea edeltävän osan
— eli pelkän alkuperäisen 14:23-tekstin, ja doksologia jää näkymättä.

Tämä skripti yhdistää jakeiden 24–26 tekstin osaksi jaetta 14:23 yhtenä
kelvollisena jakeena, ja merkitsee alkuperäiset jaenumerot tekstin sisään
sulkeisiin, esim:

    <verse osisID="Rom.14.23">
      ...14:23-teksti. (24) 14:24-teksti (25) 14:25-teksti (26) 14:26-teksti
    </verse>

Erilliset jae-elementit 14:24–26 poistetaan. Näin koko doksologia näkyy
And Biblessä jakeen 14:23 yhteydessä.

Itse käännöksen lähde-OSISia (FinARK.xml) EI muokata: muunnos tehdään aina
buildin yhteydessä automaattisesti, joten käännöksen päivittyessä mitään ei
tarvitse muistaa tehdä käsin.

Käyttö:
    python3 merge_doxology.py SISÄÄN.xml -o ULOS.xml
    python3 merge_doxology.py SISÄÄN.xml          # tulostaa stdoutiin

Skripti on idempotentti: jos jaetta 14:24 ei enää ole (yhdistys jo tehty),
syöte palautetaan muuttumattomana. Jos odotettua rakennetta ei löydy, skripti
keskeytyy virheeseen — väärin rakennettua moduulia ei synny hiljaisesti.
"""
import argparse
import re
import sys
from typing import NoReturn

# Jakeet jotka yhdistetään jakeeseen 14:23.
MERGE = [24, 25, 26]


def fail(msg: str) -> NoReturn:
    sys.stderr.write(f"merge_doxology: VIRHE: {msg}\n")
    sys.exit(1)


def verse_inner(text: str, verse: int) -> str:
    """Palauta jakeen Rom 14:<verse> tekstisisältö yhdelle riville tiivistettynä."""
    m = re.search(rf'<verse osisID="Rom\.14\.{verse}">(.*?)</verse>', text, re.S)
    if not m:
        fail(f"jaetta Room 14:{verse} ei löytynyt.")
    return " ".join(m.group(1).split())


def merge(text: str) -> str:
    src_present = 'osisID="Rom.14.24"' in text

    if not src_present:
        sys.stderr.write(
            "merge_doxology: jaetta Room 14:24 ei löydy (yhdistys jo tehty?) "
            "— syöte palautetaan muuttumattomana.\n"
        )
        return text

    # 1) Poimi jakeiden 23–26 tekstit.
    parts = {v: verse_inner(text, v) for v in (23, *MERGE)}

    # 2) Rakenna yhdistetty 14:23-teksti: 23-teksti (24) ... (25) ... (26) ...
    merged = parts[23]
    for v in MERGE:
        merged += f" ({v}) {parts[v]}"

    # 3) Korvaa 14:23-jae-elementti yhdistetyllä tekstillä (säilytä muotoilu).
    old23 = re.search(r'<verse osisID="Rom\.14\.23">.*?</verse>', text, re.S)
    if not old23:
        fail("jaetta Room 14:23 ei löytynyt korvattavaksi.")
    new23 = f'<verse osisID="Rom.14.23">\n            {merged}\n          </verse>'
    text = text[: old23.start()] + new23 + text[old23.end():]

    # 4) Poista erilliset jae-elementit 14:24–26 (niitä edeltävine välilyönteineen).
    for v in MERGE:
        text, n = re.subn(
            rf'\s*<verse osisID="Rom\.14\.{v}">.*?</verse>', "", text, count=1, flags=re.S
        )
        if n != 1:
            fail(f"jaetta Room 14:{v} ei voitu poistaa.")

    # 5) Varmista lopputulos.
    for v in MERGE:
        if f'osisID="Rom.14.{v}"' in text:
            fail(f"Room 14:{v} jäi yhä erilliseksi jakeeksi yhdistyksen jälkeen.")
        if f"({v})" not in text:
            fail(f"merkintä ({v}) puuttuu yhdistetystä jakeesta 14:23.")

    return text


def main() -> None:
    p = argparse.ArgumentParser(description="Yhdistä Room-doksologia 14:24–26 jakeeseen 14:23.")
    p.add_argument("input", help="lähde-OSIS (esim. FinARK.xml)")
    p.add_argument("-o", "--output", help="kohdetiedosto (oletus: stdout)")
    args = p.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    result = merge(text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        sys.stderr.write(f"merge_doxology: kirjoitettu {args.output}\n")
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
