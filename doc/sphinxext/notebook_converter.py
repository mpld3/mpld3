import sys
import os
import glob
import shutil
import jinja2

import nbformat
from nbconvert.exporters import HTMLExporter


INDEX_TEMPLATE = jinja2.Template("""
.. _{{ sphinx_tag }}:

Notebook Examples
=================

.. toctree::
   {% for notebook in notebooks %}
   ./{{ notebook }}
   {% endfor %}

""")


RST_TEMPLATE = jinja2.Template("""
{{ title }}
{% for c in title %}={% endfor %}

[
:download:`{{ nbroot }}.html <rendered/{{ nbroot }}.html>`
|
:download:`{{ nbroot }}.ipynb <{{ nbroot }}.ipynb>`
]

.. raw:: html

    <iframe src="../_downloads/{{ nbroot }}.html"
      width="100%" height="400px"></iframe>

""")


def get_notebook_title(nb_json, default=None):
    """Determine a suitable title for the notebook.

    This will return the text of the first header cell.
    If that does not exist, it will return the default.
    """
    cells = nb_json['cells']
    for cell in cells:
        if cell['cell_type'] == 'heading':
            return cell['source']
    return default


def main(app):
    static_dir = os.path.join(app.builder.srcdir, '_static')
    target_dir = os.path.join(app.builder.srcdir, 'notebooks')
    source_dir = os.path.abspath(os.path.join(app.builder.srcdir,
                                              '..', 'notebooks'))

    rendered_dir = os.path.join(target_dir, 'rendered')

    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if not os.path.exists(rendered_dir):
        os.makedirs(rendered_dir)

    nbroots = []
    nbtitles = []
    exporter = HTMLExporter()
    exporter.template_name = 'full'

    for nb_src in glob.glob(os.path.join(source_dir, '*.ipynb')):
        print("converting notebook {0}".format(nb_src))
        basedir, nbname = os.path.split(nb_src)
        nb_dest = os.path.join(target_dir, nbname)
        shutil.copyfile(nb_src, nb_dest)

        with open(nb_dest, 'r') as f:
            nb_json = nbformat.reads(f.read(), as_version = 4)

        (body, resources) = exporter.from_notebook_node(nb_json)

        root, ext = os.path.splitext(nbname)
        nb_html_dest = os.path.join(rendered_dir, root + '.html')
        with open(nb_html_dest, 'w') as f:
            f.write(body)

        nbroots.append(root)
        nbtitles.append(get_notebook_title(nb_json, root))

    for nbroot, nbtitle in zip(nbroots, nbtitles):
        with open(os.path.join(target_dir, nbroot + '.rst'), 'w') as f:
            f.write(RST_TEMPLATE.render(title=nbtitle, nbroot=nbroot))

    with open(os.path.join(target_dir, 'index.rst'), 'w') as f:
        f.write(INDEX_TEMPLATE.render(notebooks=nbroots,
                                      sphinx_tag='notebook-examples'))


def setup(app):
    app.connect('builder-inited', main)
