import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button


def on_next(event):
    i = min(i + 1, 3)


fig, ax = plt.subplots(figsize=(6, 6))
button_prev = Button(plt.axes([0.4, 0.01, 0.09, 0.04]), "Previous")
button_next = Button(plt.axes([0.51, 0.01, 0.09, 0.04]), "Next")

ax.set_xlim(-1, 2)
ax.set_ylim(-1, 2)

# ax.plot([0, 1], [0, 1], "o")


def on_next(event):
    print("next")
    ax.plot([0, 1], [0, 1], "o")
    ax.lines[0].set_alpha(0.5)
    # ax.lines[0].set_xdata([0, 1, 1.5])
    # ax.lines[0].set_ydata([1, 0, 1.5])
    plt.draw()


button_next.on_clicked(on_next)

plt.show()
