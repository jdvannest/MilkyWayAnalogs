import pickle
import numpy as np 
import matplotlib.pylab as plt

f,ax = plt.subplots(1,1)
ax.set_ylabel(r'N$_{sat,vir}$ - N$_{sat,300}$',fontsize=20)
ax.set_xlabel(r'Log(M$_{*}$)',fontsize=20)
ax.tick_params(labelsize=15)
ax.plot([9.5,11],[0,0],c='0.75',linestyle='--',zorder=0)
ax.set_xlim([9.5,11])
ax.set_ylim([-8,8])

nums,names,c,s = ['1','2','7'],[r'M$_{vir}$',r'M$_*$','SAGA II'],['k','r','b'],[7,4.5,3]

for i in [2,1,0]:
    rvir = pickle.load(open(f'../DataFiles/MilkyWay.{nums[i]}.sim.Yov.pickle','rb'))
    r300 = pickle.load(open(f'../DataFiles/MilkyWay.{nums[i]}.300.Yov.pickle','rb'))

    nvir,n300,mvir = [],[],[]
    up,dn,tot = 0,0,0
    for mw in rvir:
        if mw in r300:
            nvir.append(len(rvir[mw]['Satellites']))
            n300.append(len(r300[mw]['Satellites']))
            mvir.append(np.log10(rvir[mw]['Mstar']))
            tot+=1
            if len(r300[mw]['Satellites'])>len(rvir[mw]['Satellites']):
                up+=1
            elif len(r300[mw]['Satellites'])<len(rvir[mw]['Satellites']):
                dn+=1

    if i==2:
        ax.scatter(mvir,np.asarray(nvir)-np.asarray(n300),c=c[i],s=s[i]**2,label=names[i])
    else:
        ax.scatter(mvir,np.asarray(nvir)-np.asarray(n300),edgecolor=c[i],facecolor='None',linewidth=1.5,s=s[i]**2,label=names[i])  
    ax.text(10.9,-6+i,(f'{round(up/tot*100,2)}'+r'$\%\uparrow$'+f', {round(dn/tot*100,2)}'+r'$\%\downarrow$'),fontsize=15,c=c[i],horizontalalignment='right')

ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/RadComp.png',bbox_inches='tight',pad_inches=.1)



for i in [1,2,7]:
    rvir = pickle.load(open(f'../DataFiles/MilkyWay.{i}.sim.Yov.pickle','rb'))
    r300 = pickle.load(open(f'../DataFiles/MilkyWay.{i}.300.Yov.pickle','rb'))

    f,ax = plt.subplots(1,1)
    ax.set_ylabel(r'N$_{sat}$',fontsize=20)
    ax.set_xlabel(r'Log(M$_{*}$)',fontsize=20)
    ax.tick_params(labelsize=15)
    ax.set_xlim([9.5,11])
    ax.set_ylim([-.5,13.5])
    ax.scatter(-1,-1,c='r',marker='^',label=r'R$_{vir}$')
    ax.scatter(-1,-1,c='b',marker='v',label=r'300 kpc')

    up,dn,tot = 0,0,0
    for mw in rvir:
        if mw in r300:
            a = len(rvir[mw]['Satellites'])
            b = len(r300[mw]['Satellites'])
            m = np.log10(rvir[mw]['Mstar'])

            ax.vlines(m,ymin=min([a,b]),ymax=max([a,b]),color='k',zorder=0)
            ax.scatter(m,a,c='r',marker='^')
            ax.scatter(m,b,c='b',marker='v')

            tot+=1
            if a>b:
                dn+=1
            elif a<b:
                up+=1
        
    ax.text(9.65,9.8,(f'{round(up/tot*100,2)}'+r'$\%\uparrow$'),fontsize=15,horizontalalignment='left')
    ax.text(9.65,8.8,f'{round(dn/tot*100,2)}'+r'$\%\downarrow$',fontsize=15,horizontalalignment='left')
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'Data/RadComp.{i}.png',bbox_inches='tight',pad_inches=.1)