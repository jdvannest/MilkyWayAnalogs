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
x30,y30,z30 = Sphere(404.60205078125,[-4236.856067265382,-2316.2858899132243,8412.807776780784])
ax.plot_surface(x30,y30,z30,alpha=.1)
ax.scatter(-4236.856067265382,-2316.2858899132243,8412.807776780784,label='30')
x87,y87,z87 = Sphere(201.446533203125,[-4291.744528599294,-2201.473955254971,8383.27361266435])
ax.plot_surface(x87,y87,z87,alpha=.1)
ax.scatter(-4291.744528599294,-2201.473955254971,8383.27361266435,label='87')
x2219,y2219,z2219 = Sphere(64.03350830078125,[-4476.801141451872,-2129.858413159985,8391.19410294945])
ax.plot_surface(x2219,y2219,z2219,alpha=.1)
ax.scatter(-4476.801141451872,-2129.858413159985,8391.19410294945,label='2219')
ax.legend()
plt.show()