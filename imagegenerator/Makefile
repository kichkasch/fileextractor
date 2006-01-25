# Makefile
#
# SignatureCreator for FileExtractor
# Michael Pilgermann
# mpilgerm@glam.ac.uk
#
# last change Makefile: 2005-05-15
#
# global parameters
TITLE=		"ImageGenerator for FileExtractor"
URL=		"http://sourceforge.net/projects/kkfileextractor/"

API_DOC_DIR=	api-ig/

# program names
EPYDOC=		/usr/bin/epydoc 
ZIP=		/usr/bin/zip 
ZIP_PAR=	-j
MKDIR=		mkdir
RM=		rm

$(API_DOC_DIR):
	$(MKDIR) $(API_DOC_DIR)

api-docs:	$(API_DOC_DIR)
	$(EPYDOC) --inheritance listed -o $(API_DOC_DIR) -n $(TITLE) -u $(URL) -c blue *.py

docs:   api-docs

clean:
	$(RM) *.pyc
