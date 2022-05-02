import pickle
import numpy as np
import matplotlib.pylab as plt

Data = pickle.load(open('Data/UnderMassiveHistoryData.pickle','rb'))

for h in Data:
    f,ax = plt.subplots(1,1,figsize=(6,6))

    ax.plot(Data[h]['t'],Data[h]['Mvir'],c='k',label=r'M$_{vir}$')
    ax.plot(Data[h]['t'],Data[h]['Mstar'],c='k',linestyle='--',label=r'M$_*$')
    ax.semilogy()
    ax2 = ax.twinx()
    ax2.plot(Data[h]['t'],Data[h]['Mstar']/Data[h]['Mvir'],c='r')
    ax.set_xlim([0,14])
    ax.set_ylim([1e5,5e11])
    ax2.set_ylim([0,.5])

    ax.set_title(f'Halo {h}',fontsize=15)
    ax.set_xlabel('Time [Gyr]',fontsize=15)
    ax.set_ylabel(r'Mass [M$_\odot$]',fontsize=15)
    ax2.set_ylabel(r'M$_*$/M$_{vir}$',fontsize=15)
    ax2.yaxis.label.set_color('red')
    ax.tick_params(which='both',labelsize=10)
    ax2.tick_params(which='both',labelsize=10)
    ax.legend(loc='upper left',prop={'size':12})

    f.savefig(f'Data/MassHistory.{h}.png',bbox_inches='tight',pad_inches=.1)
    plt.close()