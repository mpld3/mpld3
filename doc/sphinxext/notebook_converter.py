import sys
import os
import glob
import shutil
import jinja2

from IPython.nbformat import current as nbformat
from IPython.nbconvert.exporters import HTMLExporter


INDEX_TEMPLATE = jinja2.Template("""
.. _{{ sphinx_tag }}:

Notebook Examples
=================

{% for notebook in notebooks %}
- :download:`{{ notebook }} <{{ notebook }}.html>`
  [:download:`raw <{{notebook}}.ipynb>`]

{% endfor %}
""")


def main(app):
    static_dir = os.path.join(app.builder.srcdir, '_static')
    target_dir = os.path.join(app.builder.srcdir, 'notebooks')
    source_dir = os.path.abspath(os.path.join(app.builder.srcdir,
                                              '..', 'notebooks'))

    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    nbroots = []
    exporter = HTMLExporter(template_file='full')

    for nb_src in glob.glob(os.path.join(source_dir, '*.ipynb')):
        print("converting notebook {0}".format(nb_src))
        basedir, nbname = os.path.split(nb_src)
        nb_dest = os.path.join(target_dir, nbname)
        shutil.copyfile(nb_src, nb_dest)

        with open(nb_dest, 'r') as f:
            nb_json = nbformat.reads_json(f.read())

        (body, resources) = exporter.from_notebook_node(nb_json)

        root, ext = os.path.splitext(nbname)
        nb_html_dest = os.path.join(target_dir, root + '.html')
        with open(nb_html_dest, 'w') as f:
            f.write(body)

        nbroots.append(root)

    with open(os.path.join(target_dir, 'index.rst'), 'w') as f:
        f.write(INDEX_TEMPLATE.render(notebooks=nbroots,
                                      sphinx_tag='notebook-examples'))


def setup(app):
    app.connect('builder-inited', main)
