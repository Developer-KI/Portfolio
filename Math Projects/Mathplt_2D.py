import matplotlib.pyplot as plt
import numpy as np


x = np.arange(-4*np.pi, 4*np.pi, 0.02)  # values of x from -4pi to 4pi
y1 = 2 * np.sin(2*x + 3)
y2 = np.sin(x)


plt.plot(x, y1, label="2 * Sin(2*x + 3)", color="blue")
plt.plot(x, y2, label="Sin(x)", color="black")
plt.xlabel("Time")
plt.ylabel("Displacement")
plt.title("Sine line chart")
plt.grid(True)
plt.legend()
plt.show()

