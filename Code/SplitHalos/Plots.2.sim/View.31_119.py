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
x31,y31,z31 = Sphere(384.94873046875,[-1177.7840787466039,-5247.918593450322,9426.762844822888])
ax.plot_surface(x31,y31,z31,alpha=.1)
ax.scatter(-1177.7840787466039,-5247.918593450322,9426.762844822888,label='31')
x119,y119,z119 = Sphere(172.821044921875,[-1153.1998631799565,-5200.900158600095,9383.530481808346])
ax.plot_surface(x119,y119,z119,alpha=.1)
ax.scatter(-1153.1998631799565,-5200.900158600095,9383.530481808346,label='119')
x485,y485,z485 = Sphere(109.74884033203125,[-1079.6640178482469,-5293.268456367452,9445.768974046801])
ax.plot_surface(x485,y485,z485,alpha=.1)
ax.scatter(-1079.6640178482469,-5293.268456367452,9445.768974046801,label='485')
x3869,y3869,z3869 = Sphere(48.43902587890625,[-1114.724351277052,-5255.92814167299,9420.379380183278])
ax.plot_surface(x3869,y3869,z3869,alpha=.1)
ax.scatter(-1114.724351277052,-5255.92814167299,9420.379380183278,label='3869')
ax.legend()
plt.show()