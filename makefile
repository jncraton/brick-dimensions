all: test

test:
	python3 brick-volume.py --ldraw_path /usr/share/ldraw /usr/share/ldraw/parts/3039.dat
  