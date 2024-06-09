all: cu.svg datapath.svg

%.svg: %.drawio
	draw.io --export --format svg $<

clean: cu.svg datapath.svg
	rm -rf $^
