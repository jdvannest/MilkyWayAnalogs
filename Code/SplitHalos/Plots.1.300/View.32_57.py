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
x32,y32,z32 = Sphere(374.908447265625,[-4829.631909832067,322.11329724631275,4145.952313613309])
ax.plot_surface(x32,y32,z32,alpha=.1)
ax.scatter(-4829.631909832067,322.11329724631275,4145.952313613309,label='32')
x57,y57,z57 = Sphere(252.716064453125,[-4662.208227274223,284.1985332274595,4088.2110815239894])
ax.plot_surface(x57,y57,z57,alpha=.1)
ax.scatter(-4662.208227274223,284.1985332274595,4088.2110815239894,label='57')
x2524,y2524,z2524 = Sphere(56.34307861328125,[-4686.593006071536,284.5815714732115,4007.66749472348])
ax.plot_surface(x2524,y2524,z2524,alpha=.1)
ax.scatter(-4686.593006071536,284.5815714732115,4007.66749472348,label='2524')
x156,y156,z156 = Sphere(168.121337890625,[-4789.546676295655,335.210425130083,4320.971790073507])
ax.plot_surface(x156,y156,z156,alpha=.1)
ax.scatter(-4789.546676295655,335.210425130083,4320.971790073507,label='156')
x2702,y2702,z2702 = Sphere(58.319091796875,[-4700.86126390017,475.27920035291584,4185.323430079697])
ax.plot_surface(x2702,y2702,z2702,alpha=.1)
ax.scatter(-4700.86126390017,475.27920035291584,4185.323430079697,label='2702')
x3543,y3543,z3543 = Sphere(52.150726318359375,[-4704.558728249789,203.69347458306572,4266.442358142314])
ax.plot_surface(x3543,y3543,z3543,alpha=.1)
ax.scatter(-4704.558728249789,203.69347458306572,4266.442358142314,label='3543')
ax.legend()
plt.show()