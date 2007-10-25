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
	lore -pN -b thinkCSpy.book
	mv *.html html
	cp -r illustrations html/
	cp -r resources/* html/
	tar czvf ../english2e.tgz ../english2e

clean:
	rm -rf html
