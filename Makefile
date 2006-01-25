# Makefile
#
# FileExtractor
# Michael Pilgermann
# mpilgerm@glam.ac.uk
#
# last change Makefile: 2005-05-14
#
# global parameters
TITLE=		"File Extractor"
URL=		"kkfileextractor.sourceforge.net"
HELP_DIR=	help
HELP_ZIPNAME=	fileextractorhelp.zip
HELP_HTMLS=	\
		$(HELP_DIR)/installation.htm \
		$(HELP_DIR)/overview.htm \
		$(HELP_DIR)/research.htm \
		$(HELP_DIR)/signatures.htm 
HELP_PIC_DIR=	$(HELP_DIR)/pics
HELP_PICS=	$(HELP_PIC_DIR)/background.jpg \
		$(HELP_PIC_DIR)/background2.jpg \
		$(HELP_PIC_DIR)/background3.jpg \
		$(HELP_PIC_DIR)/background4.jpg
HELP_CONFIGS=	\
		$(HELP_DIR)/general.hhc \
		$(HELP_DIR)/general.hhk \
		$(HELP_DIR)/general.hhp  

API_DOC_DIR=	api/

# program names
EPYDOC=		/usr/bin/epydoc 
ZIP=		/usr/bin/zip 
ZIP_PAR=	-j
MKDIR=		mkdir
RM=		rm

$(API_DOC_DIR):
	$(MKDIR) $(API_DOC_DIR)

api-docs:	$(API_DOC_DIR)
	$(EPYDOC) --inheritance listed -o $(API_DOC_DIR) -n $(TITLE) -u $(URL) -c blue --no-private *.py

docs:   api-docs


$(HELP_ZIPNAME):	$(HELP_CONFIGS) $(HELP_HTMLS) 
	$(ZIP) $(ZIP_PAR) $(HELP_ZIPNAME) $(HELP_CONFIGS) $(HELP_HTMLS)

help: $(HELP_ZIPNAME)

clean:
	$(RM) *.pyc imagegenerator/*.pyc
