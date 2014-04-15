"""Plot to test text"""
import matplotlib.pyplot as plt
import mpld3

fig, ax = plt.subplots(2, 2, sharex='col', sharey='row')
fig.subplots_adjust(hspace=0.3)

for i in range(2):
    for j in range(2):
        txt = '({i}, {j})'.format(i=i, j=j)
        ax[i, j].set_title(txt, size=14)
        ax[i, j].text(0.5, 0.5, txt, size=40, ha='center')
        ax[i, j].grid(True, color='lightgray')
        ax[i, j].set_xlabel('xlabel')
        ax[i, j].set_ylabel('ylabel')

mpld3.show()
