from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def Sphere(r,cen):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_pre = r * np.outer(np.cos(u), np.sin(v))
    y_pre = r * np.outer(np.sin(u), np.sin(v))
    z_pre = r * np.outer(np.ones(np.size(u)), np.cos(v))
    x_new = x_pre+cen[0]
    y_new = y_pre+cen[1]
    z_new = z_pre+cen[2]
    return(x_new,y_new,z_new)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x62,y62,z62 = Sphere(257.415771484375,[8512.81626535103,-9126.87074341409,-11715.871334926956])
ax.plot_surface(x62,y62,z62,alpha=.1)
ax.scatter(8512.81626535103,-9126.87074341409,-11715.871334926956,label='62')
x139,y139,z139 = Sphere(171.7529296875,[8650.865714888245,-9390.055301990044,-11479.79785267284])
ax.plot_surface(x139,y139,z139,alpha=.1)
ax.scatter(8650.865714888245,-9390.055301990044,-11479.79785267284,label='139')
x216,y216,z216 = Sphere(179.3365478515625,[8619.160401087285,-9204.197850348171,-11489.500899194927])
ax.plot_surface(x216,y216,z216,alpha=.1)
ax.scatter(8619.160401087285,-9204.197850348171,-11489.500899194927,label='216')
ax.legend()
plt.show()