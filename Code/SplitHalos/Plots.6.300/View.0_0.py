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
x54,y54,z54 = Sphere(266.9219970703125,[-4066.3775280597724,-2185.3089845337145,8263.633420955975])
ax.plot_surface(x54,y54,z54,alpha=.1)
ax.scatter(-4066.3775280597724,-2185.3089845337145,8263.633420955975,label='54')
ax.legend()
plt.show()ax.legend()
plt.show()ax.legend()
plt.show()