# FinARK SWORD-moduulin build
#
# Rakentaa asennettavan SWORD-moduulin (zText) lähde-OSISista FinARK.xml.
#
# Vaatii työkalut:
#   osis2mod   (The SWORD Project -työkalut, esim. paketti libsword-utils)
#   python3
#   zip
#
# Käyttö:
#   make            # rakentaa pub/sword/FinARK.zip
#   make clean      # poistaa väliaikaiset build-tiedostot
#   make distclean  # poistaa myös valmiin FinARK.zip:n
#
# Buildin vaiheet:
#   1. merge_doxology.py yhdistää Roomalaiskirjeen doksologian (Room 14:24–26)
#      jakeeseen 14:23 yhdeksi kelvolliseksi KJV-jakeeksi, jaenumerot tekstin
#      sisään sulkeisiin merkiten. Ks. CLAUDE.md kohta "Versifikaatio".
#   2. osis2mod luo zText-moduulin KJV-versifikaatiolla (ZIP-pakkaus,
#      BOOK-lohkot).
#   3. Moduulidata + mods.d/finark.conf paketoidaan FinARK.zip:ksi siinä
#      hakemistorakenteessa jota SWORD/And Bible odottaa
#      (mods.d/ + modules/texts/ztext/finark/).

MODULE   := FinARK
V11N     := KJV
OSIS     := pub/sword/FinARK.xml
CONF     := pub/sword/mods.d/finark.conf
MERGE    := pub/sword/merge_doxology.py
ZIP      := pub/sword/FinARK.zip

BUILDDIR := build
NORMOSIS := $(BUILDDIR)/FinARK.norm.xml
STAGEDIR := $(BUILDDIR)/stage
MODDATA  := $(STAGEDIR)/modules/texts/ztext/finark

.PHONY: all module clean distclean
all: $(ZIP)
module: $(ZIP)

# 1) Yhdistä Room-doksologia 14:24–26 jakeeseen 14:23.
$(NORMOSIS): $(OSIS) $(MERGE)
	@mkdir -p $(BUILDDIR)
	python3 $(MERGE) $(OSIS) -o $(NORMOSIS)

# 2)+3) Luo moduuli osis2modilla, kokoa paketti ja paketoi zip.
$(ZIP): $(NORMOSIS) $(CONF)
	@rm -rf $(STAGEDIR)
	@mkdir -p $(MODDATA) $(STAGEDIR)/mods.d
	osis2mod $(MODDATA) $(NORMOSIS) -z z -b 4 -v $(V11N)
	cp $(CONF) $(STAGEDIR)/mods.d/finark.conf
	@rm -f $(ZIP)
	cd $(STAGEDIR) && zip -r -X "$(abspath $(ZIP))" mods.d modules >/dev/null
	@echo "Valmis: $(ZIP)"

clean:
	rm -rf $(BUILDDIR)

distclean: clean
	rm -f $(ZIP)
