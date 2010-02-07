# Makefile for FileExtractor
#
# global parameters
TITLE=		"File Extractor"
URL=		"http://freshmeat.net/projects/fileextractor"
HELP_DIR=	help
HELP_ZIPNAME=	fileextractorhelp.zip
HELP_HTMLS=	\
		$(HELP_DIR)/terminology.htm \
		$(HELP_DIR)/overview.htm \
		$(HELP_DIR)/userguide.htm \
		$(HELP_DIR)/signatures.htm \
		$(HELP_DIR)/quickstart/quick_guide.html
HELP_PIC_DIR=	$(HELP_DIR)/pics
HELP_PICS=	 \
		$(HELP_DIR)/felogo2.png \
		$(HELP_DIR)/quickstart/*.jpg
HELP_CONFIGS=	\
		$(HELP_DIR)/general.hhc \
		$(HELP_DIR)/general.hhk \
		$(HELP_DIR)/general.hhp  

API_DOC_DIR=	api/

PACKAGE_NAME =fileextractor
VERSION=	"1.0.3"

# for UBUNTU Launchpad upload of deb package
PGP_KEYID ="1B09FB51"
BUILD_VERSION = "0ubuntu1"

# program names
EPYDOC=		/usr/bin/epydoc 
ZIP=		/usr/bin/zip 
ZIP_PAR=	-j
MKDIR=		mkdir
RM=		rm
PYTHON=         python


$(API_DOC_DIR):
	$(MKDIR) $(API_DOC_DIR)

api-docs:	$(API_DOC_DIR)
	$(EPYDOC) --inheritance listed -o $(API_DOC_DIR) -n $(TITLE) -u $(URL) -c blue --no-private *.py

docs:   api-docs


$(HELP_ZIPNAME):	$(HELP_CONFIGS) $(HELP_HTMLS) 
	$(ZIP) $(ZIP_PAR) $(HELP_ZIPNAME) $(HELP_CONFIGS) $(HELP_HTMLS) $(HELP_PICS)

help: $(HELP_ZIPNAME)

clean:
	$(RM) -f *.pyc imagegenerator/*.pyc
	$(RM) -rf build/template
	$(RM) -f apidoc.tar.gz
	$(RM) -f build/$(PACKAGE_NAME)-$(VERSION).orig.tar.gz
	$(RM) -rf build/$(PACKAGE_NAME)-$(VERSION)
	$(RM) -f build/*ppa.upload

sdist:
	$(PYTHON) setup.py sdist --formats=gztar,zip
	
	
# here go instructions for building Desktop packages
# 1. Ubuntu deb
 
# All up-to-date information must be applied to sub dir build/debian in advance
sdist_ubuntu: sdist
	export DEBFULLNAME="Michael Pilgermann"
	export DEBEMAIL="kichkasch@gmx.de"
	cp dist/$(PACKAGE_NAME)-$(VERSION).tar.gz build/$(PACKAGE_NAME)-$(VERSION).orig.tar.gz
	(cd build && tar -xzf $(PACKAGE_NAME)-$(VERSION).orig.tar.gz)
	cp -r build/debian build/$(PACKAGE_NAME)-$(VERSION)/
	cp README build/$(PACKAGE_NAME)-$(VERSION)/debian/README.Debian
	dch -m -c build/$(PACKAGE_NAME)-$(VERSION)/debian/changelog
	cp build/$(PACKAGE_NAME)-$(VERSION)/debian/changelog build/debian
	(cd build/$(PACKAGE_NAME)-$(VERSION)/ && dpkg-buildpackage -S -k$(PGP_KEYID))
 
ppa_upload: sdist_ubuntu
	(cd build/ && dput --config dput.config kichkasch-ppa $(PACKAGE_NAME)_$(VERSION)-$(BUILD_VERSION)_source.changes)
