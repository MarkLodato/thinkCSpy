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
	lore -pN -b thinkCSpy.book
	mv *.html html
	tar czvf ../english2e.tgz ../english2e
