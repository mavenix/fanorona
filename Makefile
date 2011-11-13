# $Id: Makefile 57 2008-01-02 07:42:01Z gassla $
VERSION=0.6
REPO=`svn info | grep URL | awk '{print $$2}'`
REV=`cat /tmp/fanorona.revision`
TMPDIR=/tmp
CURDIR=`pwd`
RM=-rm -rf
DATE=`date -R`

LANGDIR=/usr/share/locale
LANGUAGES=mg fr

all:
	@echo Available targets: dist deb clean
dist:
	# subversion
	svn up
	svn info | grep Revision | awk '{print $$2}' > $(TMPDIR)/fanorona.revision
	$(RM) $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)
	svn co $(REPO) $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)
	# generate ChangeLog
	cd $(TMPDIR)/fanorona-$(VERSION)~svn$(REV) && svn2cl --group-by-day
	cd $(TMPDIR) && tar --exclude='.svn' -czvf fanorona-$(VERSION)~svn$(REV).tar.gz fanorona-$(VERSION)~svn$(REV)
	mkdir -p $(CURDIR)/dist && mv -f $(TMPDIR)/fanorona-$(VERSION)~svn$(REV).tar.gz $(CURDIR)/dist/

deb: dist
	ln -s -f $(CURDIR)/dist/fanorona-$(VERSION)~svn$(REV).tar.gz $(TMPDIR)/fanorona_$(VERSION)~svn$(REV).orig.tar.gz
	# generate debian/changelog
	cd $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)/ && \
	sed -e "s/@REV@/$(REV)/" $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)/debian/changelog.in | \
	sed -e "s/@DATE@/$(DATE)/" | \
	sed -e "s/@VERSION@/$(VERSION)/" > $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)/debian/changelog && \
	sed -e "s/@VERSION@/$(VERSION)/" $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)/fanorona > $(TMPDIR)/fanorona.fanorona && \
	mv -f $(TMPDIR)/fanorona.fanorona $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)/fanorona && \
	sed -e "s/@VERSION@/$(VERSION)/" $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)/setup.py > $(TMPDIR)/fanorona.setup.py && \
	mv -f $(TMPDIR)/fanorona.setup.py $(TMPDIR)/fanorona-$(VERSION)~svn$(REV)/setup.py && \
	debuild -us -uc

%.mo: %.po
	msgfmt $< -o $@

translations: $(LANGUAGES:%=lang/%/LC_MESSAGES/fanorona.mo)

update-translations:
	find lib/fanorona -type d -name '.svn' -prune -o -name '*.py' -print | xargs xgettext -o lang/fanorona.pot

clean:
	$(RM) $(CURDIR)/po/*.mo
	$(RM) $(CURDIR)/dist
	$(RM) $(TMPDIR)/fanorona_$(VERSION)~svn*
	$(RM) $(TMPDIR)/fanorona-$(VERSION)~svn*
	$(RM) $(TMPDIR)/fanorona.*

.PHONY: dist clean deb
