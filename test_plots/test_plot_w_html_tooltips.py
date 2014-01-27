"""Plot to test HTML tooltip plugin

As a data explorer, I want to add rich information to each point in a
scatter plot, as details-on-demand"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from mpld3 import plugins, fig_to_d3

css = """
table
{
border-collapse: collapse;
}
th
{
color: #ffffff;
background-color: #000000;
}
td
{
background-color: #cccccc;
}
table, th, td
{
font-family:Arial, Helvetica, sans-serif;
border: 1px solid black;
text-align: right;
}
"""

def main():
    fig, ax = plt.subplots()

    N = 50
    df = pd.DataFrame(index=range(N))
    df['x'] = np.random.randn(N)
    df['y'] = np.random.randn(N)
    df['z'] = np.random.randn(N)

    labels = []
    for i in range(N):
        label = df.ix[[i], :].T
        label.columns = ['Row {0}'.format(i)]
        labels.append(str(label.to_html()))  # .to_html() is unicode, so make leading 'u' go away with str()

    points = ax.plot(df.x, df.y, 'o', color='k', mec='w', ms=15, mew=1, alpha=.9)

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    tooltip = plugins.PointHTMLTooltip(
        points[0], labels, voffset=10, hoffset=10, css=css)
    plugins.connect(fig, tooltip)

    return fig

if __name__ == '__main__':
    fig = main()
    print fig_to_d3(fig)

