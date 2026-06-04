import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0,10,200)
y = np.cos(x) +np.random.normal(0,0.1,200)

plt.plot(x,y)

plt.title("Random Wave")
plt.show()