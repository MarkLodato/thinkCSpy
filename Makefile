#-------------------------------------------------------------------------------
#
#  How to Think Like a Computer Scientist: Learning with Python  2nd Edition
#
#  make - creates xhtml book version.
#
#  make book - xhtml book version only.
#              No other versions are currently supported by this book's
#              input files.
#
#  make clean - removes xhtml directory
#
#-------------------------------------------------------------------------------

build:	book

book:
	mkdir -p xhtml/
	lore --config template=template.tpl --config ext=".xhtml" -pN -b thinkCSpy.book
	mv *.xhtml xhtml
	# Next two lines are only there until a better solution is added to lore
	cat dex_top.inc dex.html dex_bottom.inc > xhtml/dex.xhtml
	rm dex.html
	# end of Index creation. 
	cp -r illustrations xhtml/
	cp -r resources xhtml/
	cp -r activities xhtml/
	cp -r files2copy/* xhtml/
	mv .bzr ../
	mv .bzrignore ../
	rm -f xhtml/thinkCSpy2.tgz
	tar czvf ../thinkCSpy2.tgz ../english2e
	mv ../thinkCSpy2.tgz xhtml/
	mv ../.bzr .
	mv ../.bzrignore .

clean:
	rm -rf xhtml
