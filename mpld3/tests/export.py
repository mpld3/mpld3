import uuid
import subprocess
import mpld3
import multiprocessing
import os
import diffimg
import visualize_tests 
from functools import partial

HTML_TEMPLATE = """
<html>
<head>

<style type="text/css">
.fig {{
  height: 500px;
}}
{extra_css}
</style>
</head>

<body>
<div id="wrap">
    <div class="figures">
        {figures}
    </div>
</div>
<script>
    var draw_figures = function(){{
        var commands = [{js_commands}];
        for (i = 0; i < commands.length; i++) {{
            commands[i](mpld3);
        }}
    }}
    draw_figures()
</script>
</body>
</html>
"""

MPLD3_TEMPLATE = """
<div class="fig" id="fig{figid:03d}"></div>
"""

JS_TEMPLATE = """
function(mpld3){{
  {extra_js}
  mpld3.draw_figure("fig{figid:03d}", {figure_json});
}},
"""

def is_images_identical(image_path_1, image_path_2, output_bool=True):
    percentage_diff = diffimg.diff(image_path_1, image_path_2, delete_diff_file=True)
    if output_bool:
        return True if percentage_diff == 0 else False
    return percentage_diff 

def snapshot_mpld3_plot(plot_filename, output_folder, output_file_path=None):
    assert output_file_path or output_folder, "output_file_path or output_folder is required"
    result = visualize_tests.ExecFile(plot_filename)
    figures = {} 
    html_fig_id_format = "fig{fig_id:03d}"
    html_fig_ids = []
    for fig_id, (fig, extra_js, extra_css) in enumerate(result.iter_json()):
        figures.setdefault("js", []).append(JS_TEMPLATE.format(
                figid=fig_id, 
                figure_json=fig,
                extra_js=extra_js
            )
        )
        figures.setdefault("html", []).append(
            MPLD3_TEMPLATE.format(figid=fig_id)
        )
        html_fig_ids.append(html_fig_id_format.format(fig_id=fig_id))

    if not figures.get("html"):
        return
    figures_html = "".join(figures.get("html"))
    js_script = "".join(figures.get("js"))

    rendered = HTML_TEMPLATE.format(
        figures=figures_html,
        js_commands=js_script,
        extra_css=""
    )
    
    temp_folder = os.path.join(output_folder, "temp/")
    output_html_path = os.path.join(temp_folder, "_snapshot_{id}.html".format(id=uuid.uuid4().hex))

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    f = open(output_html_path, 'w+')
    f.write(rendered)
    f.close()

    if not output_file_path:
        output_file_path = snapshot_path(plot_filename, output_folder) 

    command = [
        mpld3.SCREENSHOT_BIN, 
        output_html_path,
        output_file_path,
        mpld3.urls.D3_LOCAL,
        mpld3.urls.MPLD3_LOCAL,
    ]
    subprocess.check_call(command)

    os.remove(output_html_path) if os.path.exists(output_html_path) else None
    return output_file_path

def snapshot_path(plot_filename, base_path=None):
    filename = ".".join(plot_filename.split("/")[-1].split(".")[0:-1])+".jpeg"
    return os.path.join(base_path, filename) 

def snapshot_multiple_mpld3_plots(plot_filenames, output_folder):
    assert output_folder, "output_folder is required"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pool = multiprocessing.Pool(multiprocessing.cpu_count()) 
    return pool.map(partial(snapshot_mpld3_plot, plot_filenames, **{
        "output_folder": output_folder
    }))

def snapshot_mpld3_plots_consecutive(plot_filenames, output_folder):
    assert output_folder, "output_folder is required"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    results = []
    for plot_filename in plot_filenames:
        results.append(snapshot_mpld3_plot(plot_filename, output_folder=output_folder))
    return results
