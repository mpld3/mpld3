GENERATED_FILES = \
	mpld3.js \
	mpld3.min.js \
	component.json


all: $(GENERATED_FILES) build

.PHONY: clean all test

test:
	@npm test

src/start.js: package.json bin/start
	bin/start > $@

mpld3.js: $(shell node_modules/.bin/smash --ignore-missing --list mpld3/js/mpld3.js) package.json
	@rm -f $@
	node_modules/.bin/smash mpld3/js/mpld3.js | node_modules/.bin/uglifyjs - -b indent-level=2 -o $@
	@chmod a-w $@

mpld3.min.js: mpld3.js bin/uglify
	@rm -f $@
	bin/uglify $< > $@

%.json: bin/% package.json
	@rm -f $@
	bin/$* > $@
	@chmod a-w $@

clean:
	rm -f -- $(GENERATED_FILES)

sync_current : mplexporter
	rsync -r mplexporter/mplexporter mpld3/

submodule : mplexporter
	python setup.py submodule

build : submodule
	python setup.py build

inplace : build
	python setup.py build_ext --inplace

install : build
	python setup.py install
