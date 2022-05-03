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
x26,y26,z26 = Sphere(400.115966796875,[-6337.475077779437,1485.6731930064398,-324.05515436948923])
ax.plot_surface(x26,y26,z26,alpha=.1)
ax.scatter(-6337.475077779437,1485.6731930064398,-324.05515436948923,label='26')
x151,y151,z151 = Sphere(162.2467041015625,[-6210.970577967716,1375.9411136214203,-352.3219871384611])
ax.plot_surface(x151,y151,z151,alpha=.1)
ax.scatter(-6210.970577967716,1375.9411136214203,-352.3219871384611,label='151')
x1725,y1725,z1725 = Sphere(65.10162353515625,[-6318.7478637622235,1458.551514728121,-406.6556874585533])
ax.plot_surface(x1725,y1725,z1725,alpha=.1)
ax.scatter(-6318.7478637622235,1458.551514728121,-406.6556874585533,label='1725')
ax.legend()
plt.show()