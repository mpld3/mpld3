import numpy as np
import matplotlib.pyplot as plt
import mpld3

#----------------------------------------------------------------------
# create the figure and axes
fig, ax = plt.subplots(2, 2, figsize=(8, 8),
                       subplot_kw={'facecolor':'#EEEEEE'})

for axi in ax.flat:
    axi.grid(color='white', linestyle='solid')

#----------------------------------------------------------------------
# first plot: an image
x = np.linspace(-2, 2, 20)
y = x[:, None]
X = np.zeros((20, 20, 4))

X[:, :, 0] = np.exp(- (x - 1) ** 2 - (y) ** 2)
X[:, :, 1] = np.exp(- (x + 0.71) ** 2 - (y - 0.71) ** 2)
X[:, :, 2] = np.exp(- (x + 0.71) ** 2 - (y + 0.71) ** 2)
X[:, :, 3] = np.exp(-0.25 * (x ** 2 + y ** 2))

ax[0, 0].imshow(X)
ax[0, 0].set_title('An Image')
ax[0, 0].grid()

#----------------------------------------------------------------------
# second plot: scatter
x = np.random.normal(size=100)
y = np.random.normal(size=100)
c = np.random.random(100)
s = 100 + 500 * np.random.random(100)

ax[0, 1].scatter(x, y, c=c, s=s, alpha=0.3)
ax[0, 1].set_title('A Scatter Plot')

#----------------------------------------------------------------------
# third plot: some random lines
x = np.linspace(0, 10, 100)
y = np.sin(x)
dy = 0.4

ax[1, 0].plot(x, y, '--k', lw=2)

for i in range(20):
    y_plot = np.convolve(np.ones(5) / 5., np.random.normal(y, dy), mode='same')
    ax[1, 0].plot(x, y_plot, '-b', lw=2, alpha=0.1)

ax[1, 0].set_title('Transparent Lines')

#----------------------------------------------------------------------
# fourth plot: filled regions
x = np.linspace(0, 4 * np.pi, 100)
y1 = np.sin(x / 2)
y2 = np.sin(x)

ax[1, 1].fill_between(x, y1, y2, where=y1 > y2,
                      color='blue', alpha=0.3)
ax[1, 1].fill_between(x, y1, y2, where=y1 <= y2,
                 color='red', alpha=0.3)
ax[1, 1].set_title('fill_between()')

mpld3.show()
