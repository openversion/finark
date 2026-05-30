# CLAUDE.md — FinARK

Avoin Raamatunkäännös (FinARK) -repo. Sisältää käännöksen julkaisutiedostot
(`pub/`) sekä SWORD-moduulin buildin And Bible -sovellusta varten.

## SWORD-moduulin rakentaminen

Asennettava SWORD-moduuli (`pub/sword/FinARK.zip`) rakennetaan lähde-OSISista
`pub/sword/FinARK.xml`. Build-ketju on repon juuren **Makefilessa**:

```sh
make            # rakentaa pub/sword/FinARK.zip
make clean      # poistaa väliaikaiset build/-tiedostot
make distclean  # poistaa myös FinARK.zip:n
```

Tarvittavat työkalut: `osis2mod` (The SWORD Project, esim. paketti
`libsword-utils`), `python3`, `zip`.

### Buildin vaiheet

1. **`pub/sword/merge_doxology.py`** yhdistää Roomalaiskirjeen doksologian
   (Room 14:24–26) jakeeseen 14:23 (ks. alla) → `build/FinARK.norm.xml`.
2. **`osis2mod`** luo zText-moduulin: `-z z` (ZIP-pakkaus), `-b 4` (BOOK-lohkot),
   `-v KJV` (versifikaatio). Yhdistämisen jälkeen **0 epäsovitusta**.
3. Moduulidata + `pub/sword/mods.d/finark.conf` paketoidaan `FinARK.zip`:ksi
   rakenteeseen jota SWORD/And Bible odottaa (`mods.d/` + `modules/texts/ztext/finark/`).

`pub/sword/FinARK.xml` on totuuden lähde; **älä muokkaa sitä doksologian takia
käsin** — muunnos tehdään aina buildissa, joten käännöksen päivittyessä mitään
ei tarvitse muistaa tehdä.

## Versifikaatio: KJV

FinARK on **bysanttilaiseen enemmistötekstiin** (Robinson–Pierpont) perustuva
66-kirjainen protestanttinen Raamattu, jonka jaenumerointi seuraa
Kirkkoraamattu 1933/38:n (perinteistä, KJV-tyyppistä) järjestystä.

Versifikaatioksi valittiin **KJV**. Perustelut (testattu osis2modilla koko
tekstillä):

| Versifikaatio | Tulos | Epäsovituksia |
|---|---|---|
| KJV (+ doksologian yhdistys) | ✅ | **0** |
| KJV / NRSV (ilman yhdistystä) | ✅ | 3 (Rom 14:24–26 → liitetään 14:23:een) |
| German | ❌ **jumittuu** (timeout) | 138 |

- **German on väärä** vaikka esim. FinRK (Raamattu Kansalle) käyttää sitä:
  se numeroi jakeet eri tavalla (mm. 2Kor 13, Psalmien otsikot) ja sai tällä
  tekstillä 138 epäsovitusta sekä **jumitti osis2modin**.
- **NRSV toimii**, mutta on kriittisen tekstin versifikaatio — käsitteellisesti
  väärästä traditiosta bysanttilaiselle tekstille.
- **KJV** vastaa tekstitraditiota (sisältää natiivisti mm. Mark 16:9–20,
  Joh 7:53–8:11, 1 Joh 5:7, Room 16:24).

### Roomalaiskirjeen doksologia

Käännös sijoittaa Roomalaiskirjeen ylistyksen bysanttilaiseen tapaan luvun 14
loppuun jakeina **Room 14:24–26**, eikä luku 16 sisällä jakeita 16:25–27.
Yksikään SWORD-versifikaatio ei tunne jakeita Room 14:24–26.

Jos teksti syötetään sellaisenaan osis2modille, se "liittää" jakeet 24–26
jakeeseen 14:23 mutta säilyttää niiden sisäiset jae-milestonet. **And Bible
näyttää tällöin jakeesta 14:23 vain ensimmäistä jae-milestonea edeltävän
osan** — eli pelkän alkuperäisen 14:23-tekstin, ja doksologia jää näkymättä.

Siksi `merge_doxology.py` yhdistää jakeiden 24–26 tekstin osaksi jaetta 14:23
yhtenä kelvollisena KJV-jakeena ja merkitsee alkuperäiset jaenumerot tekstin
sisään sulkeisiin:

> …on syntiä. **(24)** Mutta hänelle, joka voi teitä vahvistaa… **(25)** mutta
> joka nyt on tuotu ilmi… **(26)** Hänelle, ainoalle viisaalle Jumalalle…

Doksologia pidetään siis käännöksen bysanttilaisessa sijainnissa (luvun 14
lopussa), ei KJV:n vakiosijainnissa (16:25–27). Skripti on idempotentti ja
keskeytyy virheeseen, jos odotettua rakennetta ei löydy (väärin rakennettua
moduulia ei synny hiljaisesti).

## Hakemistot

- `pub/` — käännöksen julkiset tiedostot (usfm, vpl, csv, json, kuvat)
- `pub/sword/FinARK.xml` — lähde-OSIS (totuuden lähde)
- `pub/sword/mods.d/finark.conf` — SWORD-moduulin konfiguraatio
- `pub/sword/merge_doxology.py` — yhdistää Room 14:24–26 jakeeseen 14:23
- `pub/sword/FinARK.zip` — valmis, asennettava SWORD-moduuli (generoitu)
- `build/` — buildin väliaikaistiedostot (gitignored)
