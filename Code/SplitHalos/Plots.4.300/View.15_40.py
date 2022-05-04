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
x15,y15,z15 = Sphere(518.6767578125,[-9889.536375261336,-5152.592818446135,7922.715708860165])
ax.plot_surface(x15,y15,z15,alpha=.1)
ax.scatter(-9889.536375261336,-5152.592818446135,7922.715708860165,label='15')
x40,y40,z40 = Sphere(324.920654296875,[-10043.582222319097,-5423.022549401406,8001.510751295253])
ax.plot_surface(x40,y40,z40,alpha=.1)
ax.scatter(-10043.582222319097,-5423.022549401406,8001.510751295253,label='40')
x591,y591,z591 = Sphere(106.97174072265625,[-9859.904743382862,-5215.764332151185,7973.465047701876])
ax.plot_surface(x591,y591,z591,alpha=.1)
ax.scatter(-9859.904743382862,-5215.764332151185,7973.465047701876,label='591')
ax.legend()
plt.show()