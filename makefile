all: test

parts.csv:
	wget https://cdn.rebrickable.com/media/downloads/parts.csv.gz
	gzip --decompress parts.csv.gz

ldraw_parts.txt: parts.csv
	python3 gen_ldraw_parts.py > $@

test:
	python3 brick-volume.py --ldraw_path /usr/share/ldraw /usr/share/ldraw/parts/3039.dat
	python3 brick-volume.py --ldraw_path /usr/share/ldraw /usr/share/ldraw/parts/3005.dat
	python3 brick-volume.py --ldraw_path /usr/share/ldraw /usr/share/ldraw/parts/3001.dat
	python3 brick-volume.py --ldraw_path /usr/share/ldraw /usr/share/ldraw/parts/3029.dat

clean:
	rm -f parts.csv parts.csv.gz
	rm -f ldraw_parts.txt
