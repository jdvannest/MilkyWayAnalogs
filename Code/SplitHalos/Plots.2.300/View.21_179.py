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
x21,y21,z21 = Sphere(456.298828125,[-7693.131463821255,-2126.298061100619,-7107.660018105552])
ax.plot_surface(x21,y21,z21,alpha=.1)
ax.scatter(-7693.131463821255,-2126.298061100619,-7107.660018105552,label='21')
x179,y179,z179 = Sphere(144.83642578125,[-7726.2048984955145,-2142.9480815992374,-7094.10881587745])
ax.plot_surface(x179,y179,z179,alpha=.1)
ax.scatter(-7726.2048984955145,-2142.9480815992374,-7094.10881587745,label='179')
x1456,y1456,z1456 = Sphere(74.50103759765625,[-7536.3871203184135,-1999.291426772884,-7239.812785641952])
ax.plot_surface(x1456,y1456,z1456,alpha=.1)
ax.scatter(-7536.3871203184135,-1999.291426772884,-7239.812785641952,label='1456')
x3637,y3637,z3637 = Sphere(42.804718017578125,[-7574.224588074094,-1956.0054445988185,-6939.849858515364])
ax.plot_surface(x3637,y3637,z3637,alpha=.1)
ax.scatter(-7574.224588074094,-1956.0054445988185,-6939.849858515364,label='3637')
x340,y340,z340 = Sphere(115.570068359375,[-7842.157797088483,-2119.41096012563,-7082.6871537613615])
ax.plot_surface(x340,y340,z340,alpha=.1)
ax.scatter(-7842.157797088483,-2119.41096012563,-7082.6871537613615,label='340')
x3502,y3502,z3502 = Sphere(53.165435791015625,[-7990.912407975417,-2149.9287880022803,-7124.988142894013])
ax.plot_surface(x3502,y3502,z3502,alpha=.1)
ax.scatter(-7990.912407975417,-2149.9287880022803,-7124.988142894013,label='3502')
ax.legend()
plt.show()