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
	mv *.xhtml html
	cp -r illustrations html/
	cp -r resources/* html/
	mv .bzr ../
	tar czvf ../thinkCSpy2.tgz ../english2e
	mv ../thinkCSpy2.tgz html/
	mv ../.bzr .

# Don't run this unless you are Jeff Elkner copying the output to ibiblio ;-)
export:
	rsync -avz -e ssh --delete html/ login.ibiblio.org:thinkCSpy2/

clean:
	rm -rf html
