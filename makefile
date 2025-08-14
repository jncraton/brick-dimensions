all: test brick-dimensions.csv

brick-dimensions.csv: ldraw_parts.txt
	python3 brick-volume.py $< > $@

parts.csv:
	wget https://cdn.rebrickable.com/media/downloads/parts.csv.gz
	gzip --decompress parts.csv.gz

test:
	python3 -m doctest brick-volume.py

ldraw_parts.txt: parts.csv
	python3 gen_ldraw_parts.py > $@

clean:
	rm -rf __pycache__
	rm -f parts.csv parts.csv.gz
	rm -f ldraw_parts.txt
	rm -f brick-dimensions.csv
	rm -f part_categories.csv
