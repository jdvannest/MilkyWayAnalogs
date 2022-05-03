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
x17,y17,z17 = Sphere(511.8408203125,[5702.418446608224,-11234.544988516082,7558.397947998016])
ax.plot_surface(x17,y17,z17,alpha=.1)
ax.scatter(5702.418446608224,-11234.544988516082,7558.397947998016,label='17')
x110,y110,z110 = Sphere(195.7855224609375,[5430.689478154964,-10936.042557297105,7582.403621382381])
ax.plot_surface(x110,y110,z110,alpha=.1)
ax.scatter(5430.689478154964,-10936.042557297105,7582.403621382381,label='110')
x446,y446,z446 = Sphere(114.23492431640625,[5409.310926708268,-11017.159233415045,7666.703166803977])
ax.plot_surface(x446,y446,z446,alpha=.1)
ax.scatter(5409.310926708268,-11017.159233415045,7666.703166803977,label='446')
ax.legend()
plt.show()