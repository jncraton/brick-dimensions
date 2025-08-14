all: test brick-dimensions.csv

ldraw:
	wget https://library.ldraw.org/library/updates/complete.zip
	unzip complete.zip

brick-dimensions.csv: ldraw_parts.txt
	python3 brick-dimensions.py $< > $@

parts.csv:
	wget https://cdn.rebrickable.com/media/downloads/parts.csv.gz
	gzip --decompress parts.csv.gz

test:
	python3 -m doctest brick-dimensions.py

ldraw_parts.txt: parts.csv ldraw
	python3 gen_ldraw_parts.py > $@

clean:
	rm -rf __pycache__
	rm -f parts.csv parts.csv.gz
	rm -f ldraw_parts.txt
	rm -f brick-dimensions.csv
	rm -f part_categories.csv
