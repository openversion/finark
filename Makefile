# FinARK SWORD-moduulin build
#
# Rakentaa asennettavan SWORD-moduulin (zText) lähde-OSISista FinARK.xml.
#
# Vaatii työkalut:
#   osis2mod   (The SWORD Project -työkalut, esim. paketti libsword-utils)
#   zip
#
# Käyttö:
#   make            # rakentaa pub/sword/FinARK.zip
#   make clean      # poistaa väliaikaiset build-tiedostot
#   make distclean  # poistaa myös valmiin FinARK.zip:n
#
# Buildin vaiheet:
#   1. osis2mod luo zText-moduulin KJV-versifikaatiolla (ZIP-pakkaus,
#      BOOK-lohkot). Ks. CLAUDE.md kohta "Versifikaatio".
#   2. Moduulidata + mods.d/finark.conf paketoidaan FinARK.zip:ksi siinä
#      hakemistorakenteessa jota SWORD/And Bible odottaa
#      (mods.d/ + modules/texts/ztext/finark/).

MODULE   := FinARK
V11N     := KJV
OSIS     := pub/sword/FinARK.xml
CONF     := pub/sword/mods.d/finark.conf
ZIP      := pub/sword/FinARK.zip

BUILDDIR := build
STAGEDIR := $(BUILDDIR)/stage
MODDATA  := $(STAGEDIR)/modules/texts/ztext/finark

.PHONY: all module clean distclean
all: $(ZIP)
module: $(ZIP)

# Luo moduuli osis2modilla, kokoa paketti ja paketoi zip.
$(ZIP): $(OSIS) $(CONF)
	@rm -rf $(STAGEDIR)
	@mkdir -p $(MODDATA) $(STAGEDIR)/mods.d
	osis2mod $(MODDATA) $(OSIS) -z z -b 4 -v $(V11N)
	cp $(CONF) $(STAGEDIR)/mods.d/finark.conf
	@rm -f $(ZIP)
	cd $(STAGEDIR) && zip -r -X "$(abspath $(ZIP))" mods.d modules >/dev/null
	@echo "Valmis: $(ZIP)"

clean:
	rm -rf $(BUILDDIR)

distclean: clean
	rm -f $(ZIP)
