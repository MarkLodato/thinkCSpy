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
	mkdir -p html/
	lore --config template=template.tpl -pN -b thinkCSpy.book
	mv *.html html
	cp -r illustrations html/
	cp -r resources html/
	cp -r files2copy/* html/
	mv .bzr ../
	mv .bzrignore ../
	rm -f html/thinkCSpy2.tgz
	tar czvf ../thinkCSpy2.tgz ../english2e
	mv ../thinkCSpy2.tgz html/
	mv ../.bzr .
	mv ../.bzrignore .

# Don't run this unless you are Jeff Elkner copying the output to ibiblio ;-)
export:
	rsync -avz -e ssh --delete html/ login.ibiblio.org:thinkCSpy2/

clean:
	rm -rf html
