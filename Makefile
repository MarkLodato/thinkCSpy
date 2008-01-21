#-------------------------------------------------------------------------------
#
#  How to Think Like a Computer Scientist: Learning with Python  2nd Edition
#
#  make - creates xhtml book version.
#  make book - xhtml book version only.
#              No other versions are currently supported by this book's input files.
#
#-------------------------------------------------------------------------------

build:	book

book:
	mkdir -p xhtml/
	lore --config template=template.tpl -pN -b thinkCSpy.book
	mv *.html xhtml
	cp -r illustrations xhtml/
	cp -r resources xhtml/
	cp -r files2copy/* xhtml/
	mv .bzr ../
	mv .bzrignore ../
	rm -f xhtml/thinkCSpy2.tgz
	tar czvf ../thinkCSpy2.tgz ../english2e
	mv ../thinkCSpy2.tgz xhtml/
	mv ../.bzr .
	mv ../.bzrignore .

# Don't run this unless you are Jeff Elkner copying the output to ibiblio ;-)
export:
	rsync -avz -e ssh --delete xhtml/ login.ibiblio.org:obp/thinkCS/python/english2e/

# Don't run this unless you are Jeff Elkner pushing the changes to launchpad ;-)
push:
	bzr push bzr+ssh://jelkner@bazaar.launchpad.net/~jelkner/thinkcspy/english2e

clean:
	rm -rf xhtml
