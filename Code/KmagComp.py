import pickle
import numpy as np
import matplotlib.pylab as plt
import matplotlib.patches as patches

k = pickle.load(open('../DataFiles/MilkyWay.5.sim.pickle','rb'))
st = pickle.load(open('../DataFiles/MilkyWay.2.sim.pickle','rb'))

mv1,km1 = [[],[]]
mv2,km2 = [[],[]]

for m in k:
    mv2.append(np.log10(k[m]['Mvir']))
    km2.append(k[m]['Kmag'])
for m in st:
    mv1.append(np.log10(st[m]['Mvir']))
    km1.append(st[m]['Kmag'])

ux,uy,lx,ly = [[],[],[],[]]
with open('KmagSAGABounds.csv') as f:
    lines = f.readlines()
for line in lines:
    l = line.split(',')
    if l[0]!='':
        ux.append(-1*float(l[0][1:]))
        uy.append(float(l[1]))
    if l[2]!='':
        lx.append(-1*float(l[2][1:]))
        ly.append(float(l[3]))

u = np.polyfit(ux,uy,2)
x1 = np.linspace(-24.62,-22,100)
l = np.polyfit(lx,ly,2)
x2 = np.linspace(-25.09,-22,100)


f,ax = plt.subplots(1,1)
rect = patches.Rectangle((-25.1,11.4),3.1,1.6,linestyle='--',edgecolor='0.5',facecolor='none')
ax.add_patch(rect)
ax.plot(x1,u[0]*x1**2+u[1]*x1+u[2],c='0.5',label='SAGA-I Fig. 2')
ax.plot(x2,l[0]*x2**2+l[1]*x2+l[2],c='0.5')
ax.scatter(km1,mv1,s=5**2,c='k',label=r'$10^{10}<$Log(M$_{*}$)$<10^{11}$')
ax.scatter(km2,mv2,s=6**2,edgecolor='r',facecolor='None',linewidth=1.3,label=r'$-24.6<$M$_K<-23$')
ax.set_ylim([10.9,13.2])
ax.set_xlim([-26,-21])
ax.set_xlabel(r'M$_K$',fontsize=15)
ax.set_ylabel(r'Log(M$_{vir}$/M$_\odot$)',fontsize=15)
ax.legend(loc='upper right',prop={'size':13})
f.savefig('Data/KmagComp.png',bbox_inches='tight',pad_inches=.1)