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
x27,y27,z27 = Sphere(406.524658203125,[9908.992294005177,-10730.675696985887,11864.525273076593])
ax.plot_surface(x27,y27,z27,alpha=.1)
ax.scatter(9908.992294005177,-10730.675696985887,11864.525273076593,label='27')
x61,y61,z61 = Sphere(266.17431640625,[9793.893478933136,-10652.377705028546,11617.544805254503])
ax.plot_surface(x61,y61,z61,alpha=.1)
ax.scatter(9793.893478933136,-10652.377705028546,11617.544805254503,label='61')
x2688,y2688,z2688 = Sphere(54.821014404296875,[9899.255845380736,-10622.711953423128,11748.586176232713])
ax.plot_surface(x2688,y2688,z2688,alpha=.1)
ax.scatter(9899.255845380736,-10622.711953423128,11748.586176232713,label='2688')
x3481,y3481,z3481 = Sphere(52.738189697265625,[9894.902007512568,-10708.178268199339,11577.145632313039])
ax.plot_surface(x3481,y3481,z3481,alpha=.1)
ax.scatter(9894.902007512568,-10708.178268199339,11577.145632313039,label='3481')
ax.legend()
plt.show()