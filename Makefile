
all: build

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
