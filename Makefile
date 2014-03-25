VERSION=0.2

GENERATED_FILES = \
	mpld3/js/mpld3.v$(VERSION)git.js \
	mpld3/js/mpld3.v$(VERSION)git.min.js \
	component.json


javascript: npm $(GENERATED_FILES)

npm:
	@npm install

mpld3/js/mpld3.v$(VERSION)git.js: $(shell node_modules/.bin/smash --ignore-missing --list src/mpld3.js) package.json
	@rm -f $@
	node_modules/.bin/smash src/mpld3.js | node_modules/.bin/uglifyjs - -b indent-level=2 -o $@
	@chmod a-w $@

mpld3/js/mpld3.v$(VERSION)git.min.js: mpld3/js/mpld3.v$(VERSION)git.js bin/uglify
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

build : javascript submodule
	python setup.py build

inplace : build
	python setup.py build_ext --inplace

install : build
	python setup.py install
