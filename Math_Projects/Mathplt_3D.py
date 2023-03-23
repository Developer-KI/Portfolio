import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = plt.axes(projection='3d')

z_line = np.linspace(0, 20, 1000)
x_line = np.sin(z_line)
y_line = np.cos(z_line)
ax.plot3D(x_line, y_line, z_line, 'orange')

plt.grid(True)
plt.show()
