import matplotlib.pyplot as plt

x_points = []
y_points = []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.set_title("Live Mouse Movement")
ax2.set_title("Heatmap Preview")

def on_move(event):
    if event.xdata is not None and event.ydata is not None:
        x_points.append(event.xdata)
        y_points.append(event.ydata)

        # live scatter update
        ax1.clear()
        ax1.scatter(x_points, y_points, s=5, color="blue")
        ax1.set_title("Live Mouse Movement")

        # live heatmap update
        ax2.clear()
        ax2.hexbin(x_points, y_points, gridsize=20, cmap="inferno")
        ax2.set_title("Heatmap Preview")

        plt.pause(0.01)

fig.canvas.mpl_connect("motion_notify_event", on_move)

plt.show()