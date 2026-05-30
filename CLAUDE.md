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
`libsword-utils`), `zip`.

### Buildin vaiheet

1. **`osis2mod`** luo zText-moduulin suoraan lähde-OSISista: `-z z`
   (ZIP-pakkaus), `-b 4` (BOOK-lohkot), `-v KJV` (versifikaatio).
2. Moduulidata + `pub/sword/mods.d/finark.conf` paketoidaan `FinARK.zip`:ksi
   rakenteeseen jota SWORD/And Bible odottaa (`mods.d/` + `modules/texts/ztext/finark/`).

`pub/sword/FinARK.xml` on totuuden lähde.

## Versifikaatio: KJV

FinARK on **bysanttilaiseen enemmistötekstiin** (Robinson–Pierpont) perustuva
66-kirjainen protestanttinen Raamattu, jonka jaenumerointi seuraa
Kirkkoraamattu 1933/38:n (perinteistä, KJV-tyyppistä) järjestystä.

Versifikaatioksi valittiin **KJV**. Perustelut (testattu osis2modilla koko
tekstillä):

| Versifikaatio | Tulos | Epäsovituksia |
|---|---|---|
| KJV | ✅ | 3 (Rom 14:24–26 → liitetään 14:23:een) |
| NRSV | ✅ | 3 (Rom 14:24–26 → liitetään 14:23:een) |
| German | ❌ **jumittuu** (timeout) | 138 |

- **German on väärä** vaikka esim. FinRK (Raamattu Kansalle) käyttää sitä:
  se numeroi jakeet eri tavalla (mm. 2Kor 13, Psalmien otsikot) ja sai tällä
  tekstillä 138 epäsovitusta sekä **jumitti osis2modin**.
- **NRSV toimii**, mutta on kriittisen tekstin versifikaatio — käsitteellisesti
  väärästä traditiosta bysanttilaiselle tekstille.
- **KJV** vastaa tekstitraditiota (sisältää natiivisti mm. Mark 16:9–20,
  Joh 7:53–8:11, 1 Joh 5:7, Room 16:24).

### Roomalaiskirjeen doksologia (tietoinen kompromissi)

Käännös sijoittaa Roomalaiskirjeen ylistyksen bysanttilaiseen tapaan luvun 14
loppuun jakeina **Room 14:24–26**, eikä luku 16 sisällä jakeita 16:25–27.
Yksikään SWORD-versifikaatio ei tunne jakeita Room 14:24–26, joten osis2mod
liittää nämä kolme jaetta jakeen **Room 14:23** loppuun (teksti säilyy, ei
katoa — vain jaenumerointi yhdistyy).

Tämä on tietoinen, hyväksytty kompromissi: doksologia pidetään käännöksen
bysanttilaisessa sijainnissa eikä sitä siirretä KJV:n vakiosijaintiin
(16:25–27). Lähde-OSISia ei muokata buildissa, joten käännöksen päivitykset
menevät läpi sellaisinaan.

## Hakemistot

- `pub/` — käännöksen julkiset tiedostot (usfm, vpl, csv, json, kuvat)
- `pub/sword/FinARK.xml` — lähde-OSIS (totuuden lähde)
- `pub/sword/mods.d/finark.conf` — SWORD-moduulin konfiguraatio
- `pub/sword/FinARK.zip` — valmis, asennettava SWORD-moduuli (generoitu)
- `build/` — buildin väliaikaistiedostot (gitignored)
