import matplotlib.pylab as plt
import numpy as np
import matplotlib.cm
import matplotlib as mpl
import statistics
import xlrd
import pickle
from matplotlib import colors
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator, ScalarFormatter)

def wrap(relpos,scale=1,boxsize=25e3):
#author: Michael Tremmel
#scale = 1/1+z
    bphys = boxsize*scale
    bad = np.where(np.abs(relpos) > bphys/2.)
    if type(bphys) == np.ndarray:
        relpos[bad] = -1.0 * (relpos[bad] / np.abs(relpos[bad])) * np.abs(bphys[bad] - np.abs(relpos[bad]))
    else:
        relpos[bad] = -1.0 * (relpos[bad]/np.abs(relpos[bad])) * np.abs(bphys - np.abs(relpos[bad]))
    return

def t_at_sffrac(h1,formfrac):
#author: Anna Wright
    '''
    Calculates time at which halo has formed given fraction of stars
    Inputs: h1 - halo object (e.g., sim[123][142])
            formfrac - fraction of stars formed (e.g., 0.5 for t50)
    Outputs: tfrac - time at which h1 formed 100*formfrac % of its stars in Gyr
    '''

    cumsfh = h1
    cind = next(x[0] for x in enumerate(cumsfh) if x[1] > formfrac)
    tfrac = 0.01*cind # t50, t20 or whatever in Gyr

    return tfrac

def SnM(Nsat,Ms):
	#Calculates specific frequency of Nsat normalized to Log(stellar mass)
	return(Nsat*10**((np.log10(Ms) - 10.6)))

def SnD(Nsat,D):
	#Calculates specific frequency of Nsat normalized to distance to large halo [Mpc]
	return(Nsat*10**((D/1000 - 5)))

def SnE(Nsat,E):
	#Calculates specific frequency of Nsat normalized to Environmental Density
	return(Nsat*10**((E - 4)))

def SnN(Nsat,N):
    #Calculates specific frequency of Nsat normalized to 10th neighbor distance
    return(Nsat*10**((N/1000 - 4)))

def SatelliteCountHistogram(host,rest,rad,over,path=''):
    '''
    Takes a dictionary output from satallite generation
    and plots the histogram of satellite counts.
    Use host criteria type and radius type for file extenstions
    '''
    y = []
    for h in host:
        y.append(len(host[h]['Satellites']))
    x = np.arange(-.5,max(y)+1.5,1)
    f,ax = plt.subplots(1,1)
    try:
        ax.set_ylim([0,y.count(statistics.mode(y))+2])
    except:
        ax.set_ylim([0,50])
    ax.set_xlim([-.5,max(y)+1.5])
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.hist(y,x,align='mid',color='k')
    ax.set_xlabel(r'N$_{sat}$',fontsize=20)
    ax.set_ylabel('Number of Hosts',fontsize=20)
    ax.tick_params(labelsize=15)
    f.savefig(f'{path}SatelliteCountHistogram.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SatelliteCountHistogram'+'.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def VbandMagnitudeFunction(host,sats,rest,rad,over,path=''):
    x = np.arange(-25,-11,1)
    Y = []
    ct = 0
    for h in host:
        if len(host[h]['Satellites']) == 0:
            pass
        else:
            y = []
            i = 0
            while i < len(x):
                ct = 0
                for sat in host[h]['Satellites']:
                    if sats[str(sat)]['Vmag'] < x[i]:
                        ct += 1
                y.append(ct)
                i += 1
            Y.append(y)

    miny = []
    maxy = []
    meany = []
    erry = []
    i = 0
    while i < len(x):
        m = []
        for y in Y:
            m.append(y[i])
        miny.append(min(m))
        maxy.append(max(m))
        meany.append(np.mean(m))
        erry.append(np.std(m))
        i += 1

    wkbk = xlrd.open_workbook('DataFiles/AdditionalData/M31_Vb.xls')
    wk = wkbk.sheet_by_index(0)

    mwx = []
    mwy = []
    m31x = []
    m31y = []
    line = 0
    while line < 16:
        mwx.append(wk.cell_value(line,0))
        mwy.append(wk.cell_value(line,1))
        line += 1
    line = 0
    while line < 30:
        m31x.append(wk.cell_value(line,3))
        m31y.append(wk.cell_value(line,4))
        line += 1

    wkbk = xlrd.open_workbook('DataFiles/AdditionalData/other.xls')
    wk = wkbk.sheet_by_index(0)

    h148 = []
    h229 = []
    h242 = []
    h329 = []
    line = 1
    while line < 30:
        h148.append(wk.cell_value(line,4))
        line += 1
    while line < 44:
        h229.append(wk.cell_value(line,4))
        line += 1
    while line < 56:
        h242.append(wk.cell_value(line,4))
        line += 1
    while line < 64:
        h329.append(wk.cell_value(line,4))
        line += 1

    h148y = []
    h229y = []
    h242y = []
    h329y = []
    i = 0
    while i < len(x):
        ct = 0
        for h in h148:
            if h < x[i]:
                ct += 1
        h148y.append(ct)
        ct = 0
        for h in h229:
            if h < x[i]:
                ct += 1
        h229y.append(ct)
        ct = 0
        for h in h242:
            if h < x[i]:
                ct += 1
        h242y.append(ct)
        ct = 0
        for h in h329:
            if h < x[i]:
                ct += 1
        h329y.append(ct)
        i += 1

    wkbk = xlrd.open_workbook('DataFiles/AdditionalData/LumFunc.xls')
    wk = wkbk.sheet_by_index(0)
    mwx2 = []
    mwy2 = []
    m31x2 = []
    m31y2 = []
    m101x,m101y,m94x,m94y,m81x,m81y,cenAx,cenAy,ngc4258x,ngc4258y,ngc4631x,ngc4631y=[[],[],[],[],[],[],[],[],[],[],[],[]]
    line = 14
    while line > 1:
        mwx2.append(float(wk.cell_value(line,0))+.2)
        mwy2.append(float(wk.cell_value(line,1)))
        line -= 1
    line = 22
    while line > 1:
        m31x2.append(float(wk.cell_value(line,2))+.2)
        m31y2.append(float(wk.cell_value(line,3)))
        line -= 1
    line = 2
    while wk.cell_value(line,4)!='':
        m101x.append(float(wk.cell_value(line,4)))
        m101y.append(float(wk.cell_value(line,5)))
        line+=1
    line = 2
    while wk.cell_value(line,6)!='':
        m94x.append(float(wk.cell_value(line,6)))
        m94y.append(float(wk.cell_value(line,7)))
        line+=1
    line = 2
    while wk.cell_value(line,8)!='':
        cenAx.append(float(wk.cell_value(line,8)))
        cenAy.append(float(wk.cell_value(line,9)))
        line+=1
    line = 2
    while line<32.5:
        m81x.append(float(wk.cell_value(line,10)))
        m81y.append(float(wk.cell_value(line,11)))
        line+=1
    line=2
    while line<6.5:
        ngc4258x.append(float(wk.cell_value(line,12)))
        ngc4258y.append(float(wk.cell_value(line,13)))
        line+=1
    line=2
    while line<10.5:
        ngc4631x.append(float(wk.cell_value(line,14)))
        ngc4631y.append(float(wk.cell_value(line,15)))
        line+=1

    f,ax = plt.subplots(1,1)
    ax.fill_between(x,miny,maxy,color='0.5',alpha=.5,edgecolor='None')
    #ax.plot(mwx,mwy,color='orange',label='Milky Way')
    #ax.plot(m31x,m31y,color='purple',label='M31')
    ax.plot(mwx2,mwy2,color='orange',label='Milky Way')
    ax.plot(m31x2,m31y2,color='purple',label='M31')
    #ax.plot(m81x[:1]+m81x,[0]+m81y,label='M81',color='b')
    ax.plot(m94x[:1]+m94x,[0]+m94y,label='M94',color='g')
    ax.plot(m101x[:1]+m101x,[0]+m101y,label='M101',color='r')
    #ax.plot(cenAx[:1]+cenAx,[0]+cenAy,label='Cen A',color='brown')
    ax.plot(ngc4258x[:1]+ngc4258x,[0]+ngc4258y,label='NGC4258',color='b')
    ax.plot(ngc4631x[:1]+ngc4631x,[0]+ngc4631y,label='NGC4631',color='brown')
    ax.plot([-1,0],[-1,0],color='0.5',alpha=.5,label='Romulus25')
    ax.set_xlim([-12,-25])
    ax.set_ylim([0,12])
    ax.set_xlabel(r'V [Mag]',fontsize=20)
    ax.set_ylabel(r'N (M$_{V} < $V)',fontsize=20)
    ax.tick_params(labelsize=15,length=5)
    ax.legend(loc='upper right',prop={'size':17})
    f.savefig(f'{path}LuminosityFunction.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LuminosityFunction'+'.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

    #Mean+1Sigma
    f,ax = plt.subplots(1,1)
    ax.fill_between(x,miny,maxy,color='0.5',alpha=.2,edgecolor='None')
    ax.fill_between(x,np.array(meany)+np.array(erry),np.array(meany)-np.array(erry),color='0.5',alpha=.5,edgecolor='None')
    ax.plot(mwx2,mwy2,color='orange',label='Milky Way')
    ax.plot(m31x2,m31y2,color='purple',label='M31')
    ax.plot(m94x[:1]+m94x,[0]+m94y,label='M94',color='g')
    ax.plot(m101x[:1]+m101x,[0]+m101y,label='M101',color='r')
    ax.plot(ngc4258x[:1]+ngc4258x,[0]+ngc4258y,label='NGC4258',color='b')
    ax.plot(ngc4631x[:1]+ngc4631x,[0]+ngc4631y,label='NGC4631',color='brown')
    ax.plot(x,meany,color='k',label='Romulus25')
    ax.set_xlim([-12,-25])
    ax.set_ylim([0,12])
    ax.set_xlabel(r'V [Mag]',fontsize=20)
    ax.set_ylabel(r'N (M$_{V} < $V)',fontsize=20)
    ax.tick_params(labelsize=15,length=5)
    ax.legend(loc='upper right',prop={'size':17})
    f.savefig(f'{path}LuminosityFunction.Mean.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LuminosityFunction'+'.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def MassFunction(host,sats,rest,rad,over,path=''):
    hosts = []
    for mw in host:
        hosts.append(int(mw))

    x = np.arange(5,12.5,.25)
    Y = []
    ct = 0
    for h in host:
        if len(host[h]['Satellites']) == 0:
            pass
        else: #if set(MW[h]['Satellites']).isdisjoint(hosts):
            y = []
            i = 0
            while i < len(x):
                ct = 0
                for sat in host[h]['Satellites']:
                    if sats[str(sat)]['Mstar'] > 10**x[i]:
                        ct += 1
                y.append(ct)
                i += 1
            Y.append(y)

    miny = []
    maxy = []
    i = 0
    while i < len(x):
        m = []
        for y in Y:
            m.append(y[i])
        miny.append(min(m))
        maxy.append(max(m))
        i += 1

    wkbk = xlrd.open_workbook('DataFiles/AdditionalData/MW_M31.xls')
    wk = wkbk.sheet_by_index(0)

    mwx = []
    mwy = []
    m31x = []
    m31y = []
    line = 0
    while line < 52:
        mwx.append(wk.cell_value(line,0))
        mwy.append(wk.cell_value(line,1))
        line += 1
    line = 0
    while line < 78:
        m31x.append(wk.cell_value(line,3))
        m31y.append(wk.cell_value(line,4))
        line += 1

    wkbk = xlrd.open_workbook('DataFiles/AdditionalData/other.xls')
    wk = wkbk.sheet_by_index(0)

    h148 = []
    h229 = []
    h242 = []
    h329 = []
    line = 1
    while line < 30:
        h148.append(wk.cell_value(line,6))
        line += 1
    while line < 44:
        h229.append(wk.cell_value(line,6))
        line += 1
    while line < 56:
        h242.append(wk.cell_value(line,6))
        line += 1
    while line < 64:
        h329.append(wk.cell_value(line,6))
        line += 1

    h148y = []
    h229y = []
    h242y = []
    h329y = []
    i = 0
    while i < len(x):
        ct = 0
        for h in h148:
            if h > x[i]:
                ct += 1
        h148y.append(ct)
        ct = 0
        for h in h229:
            if h > x[i]:
                ct += 1
        h229y.append(ct)
        ct = 0
        for h in h242:
            if h > x[i]:
                ct += 1
        h242y.append(ct)
        ct = 0
        for h in h329:
            if h > x[i]:
                ct += 1
        h329y.append(ct)
        i += 1

    f,ax = plt.subplots(1,1)
    ax.fill_between(x,miny,maxy,color='0.5',alpha=.5)
    ax.plot(mwx,mwy,color='orange',label='Milky Way')
    ax.plot(m31x,m31y,color='purple',label='M31')
    ax.plot(x,h148y,label='Sandra',linestyle='--',color='b')
    ax.plot(x,h229y,label='Ruth',linestyle='--',color='g')
    ax.plot(x,h242y,label='Sonia',linestyle='--',color='r')
    ax.plot(x,h329y,label='Elena',linestyle='--',color='brown')
    ax.plot([-1,0],[-1,0],color='0.5',alpha=.5,label='Rom25')
    ax.set_xlabel('M',fontsize=20)
    ax.set_ylabel(r'N (Log[M$_*$/M$_\odot$]$>$M)',fontsize=20)
    ax.tick_params(labelsize=15,length=5)
    ax.set_ylim([0,12])
    ax.set_xlim([7,11])
    ax.legend(loc='upper right',prop={'size':17})
    f.savefig(f'{path}MassFunction.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/MassFunction'+'.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def NsatVsEnvironment(host,rest,rad,over,path=''):
    x = []
    y = []
    for h in host:
        x.append(host[h]['Closest'][0]/host[h]['Rvir'])
        ct = 0
        for sat in host[h]['Satellites']:
            if str(sat) not in host:
                ct += 1
        y.append(ct)
    
    f,ax = plt.subplots(1,1)
    ax.set_xlim([-1,max(x)+1])
    ax.set_ylim([-.5, max(y)+1])
    ax.set_xlabel(r'D$_{LH}$/R$_{vir}$',fontsize=20)
    ax.set_ylabel(r'N$_{sat}$',fontsize=20)
    ax.tick_params(direction='in',labelsize=15,length=5)
    ax.scatter(x,y,c='k')
    f.savefig(f'{path}NsatVsEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/NsatVsEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def LargestSatelliteDistribution(host,sats,rest,rad,over,path=''):
    x = np.arange(9,12,.1)
    y = []
    for h in host:
        mass = 0
        for sat in host[h]['Satellites']:
            if np.log10(sats[str(sat)]['Mvir']) > mass:
                mass = np.log10(sats[str(sat)]['Mvir'])
        y.append(mass)
    f,ax = plt.subplots(1,1)
    ax.set_xlabel(r'Log(M$_{vir}$/M$_\odot$) of Largest Satellite',fontsize=20)
    ax.set_ylabel('N',fontsize=20)
    ax.tick_params(labelsize=15,length=5)
    ax.set_xlim([9,12])
    #ax.set_ylim([0,10])
    ax.hist(y,x,color='k')
    f.savefig(f'{path}LargestSatelliteDistribution.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LargestSatelliteDistribution.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def LargestSatelliteVsEnvironment(host,sats,rest,rad,over,path=''):
    x1,x2,y1,y2,Y1,Y2 = [[],[],[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) > 0:
            mass = 0
            BigSat = False
            for sat in host[h]['Satellites']:
                if host[h]['Mvir'] > sats[str(sat)]['Mvir'] and sats[str(sat)]['Mvir'] > mass:
                    mass = np.log10(sats[str(sat)]['Mvir'])
                if np.log10(host[h]['Mvir']) < np.log10(sats[str(sat)]['Mvir']):
                    BigSat = True
            if mass > 0:
                if BigSat:
                    y2.append(mass)
                    Y2.append(float(10**mass)/host[h]['Mvir'])
                    x2.append(host[h]['Closest'][0]/host[h]['Rvir'])
                else:
                    y1.append(mass)
                    Y1.append(float(10**mass)/host[h]['Mvir'])
                    x1.append(host[h]['Closest'][0]/host[h]['Rvir'])

    f,ax = plt.subplots(2,2,figsize=(13,10),gridspec_kw={'width_ratios':[4,1]})#,sharex=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    ax[0][0].set_xticks
    ax[0][1].set_xticks([10,20,30,40])
    ax[1][1].set_xticks([10,20,30,40])
    ax[0][0].set_ylim([9.4,11.2])
    ax[0][1].set_ylim([9.4,11.2])
    ax[1][0].set_ylim([-.01,.37])
    ax[1][1].set_ylim([-.01,.37])
    ax[0][0].set_xlim([0,41])
    ax[1][0].set_xlim([0,41])
    ax[0][1].set_xlim([0,40])
    ax[1][1].set_xlim([0,40])
    ax[0][0].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,right=True,labelright=False)
    ax[1][0].tick_params(labelsize=25,direction='in',length=5,top=True,right=True,labelright=False)
    ax[0][1].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,labelleft=False,left=False)
    ax[1][1].tick_params(labelsize=25,direction='in',length=5,top=True,labelleft=False,left=False)
    ax[0][0].set_ylabel(r'Log(M$_{vir}$/M$_\odot$) of\\Largest Satellite',fontsize=35)
    ax[0][0].scatter(x1,y1,c='k')#,label=r'All Satellites Smaller than M$_{vir,host}$')
    ax[0][0].scatter(x2,y2,c='r')#,label=r'Contains Satellite Larger than M$_{vir,host}$')
    ax[1][0].set_xlabel(r'D$_{LH}$/R$_{vir}$',fontsize=35)
    ax[1][0].set_ylabel(r'M$_{sat}$ / M$_{host}$',fontsize=35)
    ax[1][0].scatter(x1,Y1,c='k',label=r'All Satellites Smaller than M$_{vir}$')
    ax[1][0].scatter(x2,Y2,c='r',label=r'Contains Satellite Larger than M$_{vir}$')
    #ax[0][0].legend(loc='upper right',prop={'size':18},frameon=True)
    ax[0][1].hist(y1+y2,np.arange(9.4,11.4,.2),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].hist(Y1+Y2,np.arange(0,.4,.05),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].set_xlabel('N',fontsize=35)
    f.savefig(f'{path}LargestSatelliteVsEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LargestSatelliteVsEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def LargestSatelliteVsNeighborEnvironment(host,sats,rest,rad,over,path=''):
    x1,x2,y1,y2,Y1,Y2 = [[],[],[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) > 0:
            mass = 0
            BigSat = False
            for sat in host[h]['Satellites']:
                if host[h]['Mvir'] > sats[str(sat)]['Mvir'] and sats[str(sat)]['Mvir'] > mass:
                    mass = np.log10(sats[str(sat)]['Mvir'])
                if np.log10(host[h]['Mvir']) < np.log10(sats[str(sat)]['Mvir']):
                    BigSat = True
            if mass > 0:
                if BigSat:
                    y2.append(mass)
                    Y2.append(float(10**mass)/host[h]['Mvir'])
                    x2.append(host[h]['10thNeighbor']/host[h]['Rvir'])
                else:
                    y1.append(mass)
                    Y1.append(float(10**mass)/host[h]['Mvir'])
                    x1.append(host[h]['10thNeighbor']/host[h]['Rvir'])

    f,ax = plt.subplots(2,2,figsize=(13,10),gridspec_kw={'width_ratios':[4,1]})#,sharex=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    ax[0][0].set_xticks
    ax[0][1].set_xticks([10,20,30,40])
    ax[1][1].set_xticks([10,20,30,40])
    ax[0][0].set_ylim([9.4,11.2])
    ax[0][1].set_ylim([9.4,11.2])
    ax[1][0].set_ylim([-.01,.37])
    ax[1][1].set_ylim([-.01,.37])
    ax[0][0].set_xlim([0,41])
    ax[1][0].set_xlim([0,41])
    ax[0][1].set_xlim([0,40])
    ax[1][1].set_xlim([0,40])
    ax[0][0].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,right=True,labelright=False)
    ax[1][0].tick_params(labelsize=25,direction='in',length=5,top=True,right=True,labelright=False)
    ax[0][1].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,labelleft=False,left=False)
    ax[1][1].tick_params(labelsize=25,direction='in',length=5,top=True,labelleft=False,left=False)
    ax[0][0].set_ylabel(r'Log(M$_{vir}$/M$_\odot$) of\\Largest Satellite',fontsize=35)
    ax[0][0].scatter(x1,y1,c='k')#,label=r'All Satellites Smaller than M$_{vir,host}$')
    ax[0][0].scatter(x2,y2,c='r')#,label=r'Contains Satellite Larger than M$_{vir,host}$')
    ax[1][0].set_xlabel(r'D$_{10}$/R$_{vir}$',fontsize=35)
    ax[1][0].set_ylabel(r'M$_{sat}$ / M$_{host}$',fontsize=35)
    ax[1][0].scatter(x1,Y1,c='k',label=r'All Satellites Smaller than M$_{vir}$')
    ax[1][0].scatter(x2,Y2,c='r',label=r'Contains Satellite Larger than M$_{vir}$')
    #ax[0][0].legend(loc='upper right',prop={'size':18},frameon=True)
    ax[0][1].hist(y1+y2,np.arange(9.4,11.4,.2),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].hist(Y1+Y2,np.arange(0,.4,.05),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].set_xlabel('N',fontsize=35)
    f.savefig(f'{path}LargestSatelliteVsNeighborEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LargestSatelliteVsNeighborEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def LargestSatelliteVsHostMass(host,sats,rest,rad,over,path=''):
    x1,x2,y1,y2,Y1,Y2 = [[],[],[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) > 0:
            mass = 0
            BigSat = False
            for sat in host[h]['Satellites']:
                if host[h]['Mvir'] > sats[str(sat)]['Mvir'] and sats[str(sat)]['Mvir'] > mass:
                    mass = np.log10(sats[str(sat)]['Mvir'])
                if np.log10(host[h]['Mvir']) < np.log10(sats[str(sat)]['Mvir']):
                    BigSat = True
            if mass > 0:
                if BigSat:
                    y2.append(mass)
                    Y2.append(float(10**mass)/host[h]['Mvir'])
                    x2.append(np.log10(host[h]['Mstar']))
                else:
                    y1.append(mass)
                    Y1.append(float(10**mass)/host[h]['Mvir'])
                    x1.append(np.log10(host[h]['Mstar']))

    f,ax = plt.subplots(2,2,figsize=(13,10),gridspec_kw={'width_ratios':[4,1]})#,sharex=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    ax[0][0].set_xticks
    ax[0][1].set_xticks([10,20,30,40])
    ax[1][1].set_xticks([10,20,30,40])
    ax[0][0].set_ylim([9.4,11.2])
    ax[0][1].set_ylim([9.4,11.2])
    ax[1][0].set_ylim([-.01,.37])
    ax[1][1].set_ylim([-.01,.37])
    ax[0][0].set_xlim([10,11.2])
    ax[1][0].set_xlim([10,11.2])
    ax[0][1].set_xlim([0,40])
    ax[1][1].set_xlim([0,40])
    ax[0][0].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,right=True,labelright=False)
    ax[1][0].tick_params(labelsize=25,direction='in',length=5,top=True,right=True,labelright=False)
    ax[0][1].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,labelleft=False,left=False)
    ax[1][1].tick_params(labelsize=25,direction='in',length=5,top=True,labelleft=False,left=False)
    ax[0][0].set_ylabel(r'Log(M$_{vir}$/M$_\odot$) of\\Largest Satellite',fontsize=35)
    ax[0][0].scatter(x1,y1,c='k',label=r'All Satellites Smaller than M$_{vir,host}$')
    ax[0][0].scatter(x2,y2,c='r',label=r'Contains Satellite Larger than M$_{vir,host}$')
    ax[1][0].set_xlabel(r'Log(M$_{*,host}$/M$_\odot$)',fontsize=35)
    ax[1][0].set_ylabel(r'M$_{sat}$ / M$_{host}$',fontsize=35)
    ax[1][0].scatter(x1,Y1,c='k',label=r'All Satellites Smaller than M$_{vir}$')
    ax[1][0].scatter(x2,Y2,c='r',label=r'Contains Satellite Larger than M$_{vir}$')
    #ax[0][0].legend(loc='upper right',prop={'size':18},frameon=True)
    ax[0][1].hist(y1+y2,np.arange(9.4,11.4,.2),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].hist(Y1+Y2,np.arange(0,.4,.05),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].set_xlabel('N',fontsize=35)
    f.savefig(f'{path}LargestSatelliteVsHostMass.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LargestSatelliteVsHostMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def LargestSatelliteVsEnvironmentalDensity(host,sats,rest,rad,over,path=''):
    x1,x2,y1,y2,Y1,Y2 = [[],[],[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) > 0:
            mass = 0
            BigSat = False
            for sat in host[h]['Satellites']:
                if host[h]['Mvir'] > sats[str(sat)]['Mvir'] and sats[str(sat)]['Mvir'] > mass:
                    mass = np.log10(sats[str(sat)]['Mvir'])
                if np.log10(host[h]['Mvir']) < np.log10(sats[str(sat)]['Mvir']):
                    BigSat = True
            if mass > 0:
                if BigSat:
                    y2.append(mass)
                    Y2.append(float(10**mass)/host[h]['Mvir'])
                    x2.append(host[h]['EnvDen'])
                else:
                    y1.append(mass)
                    Y1.append(float(10**mass)/host[h]['Mvir'])
                    x1.append(host[h]['EnvDen'])

    f,ax = plt.subplots(2,2,figsize=(13,10),gridspec_kw={'width_ratios':[4,1]})#,sharex=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    ax[0][0].set_xticks
    ax[0][1].set_xticks([10,20,30,40])
    ax[1][1].set_xticks([10,20,30,40])
    ax[0][0].set_ylim([9.4,11.2])
    ax[0][1].set_ylim([9.4,11.2])
    ax[1][0].set_ylim([-.01,.37])
    ax[1][1].set_ylim([-.01,.37])
    ax[0][0].set_xlim([-.5,7])
    ax[1][0].set_xlim([-.5,7])
    ax[0][1].set_xlim([0,40])
    ax[1][1].set_xlim([0,40])
    ax[0][0].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,right=True,labelright=False)
    ax[1][0].tick_params(labelsize=25,direction='in',length=5,top=True,right=True,labelright=False)
    ax[0][1].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,labelleft=False,left=False)
    ax[1][1].tick_params(labelsize=25,direction='in',length=5,top=True,labelleft=False,left=False)
    ax[0][0].set_ylabel(r'Log(M$_{vir}$/M$_\odot$) of\\Largest Satellite',fontsize=35)
    ax[0][0].scatter(x1,y1,c='k')#,label=r'All Satellites Smaller than M$_{vir,host}$')
    ax[0][0].scatter(x2,y2,c='r')#,label=r'Contains Satellite Larger than M$_{vir,host}$')
    ax[1][0].set_xlabel(r'N$_L(<$1 Mpc)',fontsize=35)
    ax[1][0].set_ylabel(r'M$_{sat}$ / M$_{host}$',fontsize=35)
    ax[1][0].scatter(x1,Y1,c='k',label=r'All Satellites Smaller than M$_{vir}$')
    ax[1][0].scatter(x2,Y2,c='r',label=r'Contains Satellite Larger than M$_{vir}$')
    #ax[0][0].legend(loc='upper right',prop={'size':18},frameon=True)
    ax[0][1].hist(y1+y2,np.arange(9.4,11.4,.2),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].hist(Y1+Y2,np.arange(0,.4,.05),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].set_xlabel('N',fontsize=35)
    f.savefig(f'{path}LargestSatelliteVsEnvironmentalDensity.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LargestSatelliteVsEnvironmentalDensity.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def LargestSatelliteStellarVsHostMass(host,sats,rest,rad,over,path=''):
    x1,x2,y1,y2,Y1,Y2 = [[],[],[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) > 0:
            mass = 0
            BigSat = False
            for sat in host[h]['Satellites']:
                if host[h]['Mvir'] > sats[str(sat)]['Mvir'] and sats[str(sat)]['Mstar'] > mass:
                    mass = np.log10(sats[str(sat)]['Mstar'])
                if np.log10(host[h]['Mvir']) < np.log10(sats[str(sat)]['Mvir']):
                    BigSat = True
            if mass > 0:
                if BigSat:
                    y2.append(mass)
                    Y2.append(float(10**mass)/host[h]['Mstar'])
                    x2.append(np.log10(host[h]['Mstar']))
                else:
                    y1.append(mass)
                    Y1.append(float(10**mass)/host[h]['Mstar'])
                    x1.append(np.log10(host[h]['Mstar']))

    f,ax = plt.subplots(2,2,figsize=(13,10),gridspec_kw={'width_ratios':[4,1]})#,sharex=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    ax[0][0].set_xticks
    ax[0][1].set_xticks([10,20,30,40])
    ax[1][1].set_xticks([10,20,30,40])
    ax[0][0].set_ylim([7,11])
    ax[0][1].set_ylim([7,11])
    ax[1][0].semilogy()
    ax[1][0].set_ylim([2e-4,7e-1])
    ax[1][1].set_ylim([2e-4,7e-1])
    ax[1][1].semilogy()
    ax[0][0].set_xlim([10,11.2])
    ax[1][0].set_xlim([10,11.2])
    ax[0][1].set_xlim([0,40])
    ax[1][1].set_xlim([0,40])
    ax[0][0].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,right=True,labelright=False)
    ax[1][0].tick_params(labelsize=25,direction='in',length=5,top=True,right=True,labelright=False)
    ax[0][1].tick_params(labelsize=25,direction='in',length=5,labelbottom=False,labelleft=False,left=False)
    ax[1][1].tick_params(labelsize=25,direction='in',length=5,top=True,labelleft=False,left=False)
    ax[0][0].set_ylabel(r'Log(M$_{*}$/M$_\odot$) of\\Largest Satellite',fontsize=35)
    ax[0][0].scatter(x1,y1,c='k',label=r'All Satellites Smaller than M$_{vir,host}$')
    ax[0][0].scatter(x2,y2,c='r',label=r'Contains Satellite Larger than M$_{vir,host}$')
    ax[1][0].set_xlabel(r'Log(M$_{*,host}$/M$_\odot$)',fontsize=35)
    ax[1][0].set_ylabel(r'M$_{*,sat}$ / M$_{*,host}$',fontsize=35)
    ax[1][0].scatter(x1,Y1,c='k',label=r'All Satellites Smaller than M$_{vir}$')
    ax[1][0].scatter(x2,Y2,c='r',label=r'Contains Satellite Larger than M$_{vir}$')
    #ax[0][0].legend(loc='upper right',prop={'size':18},frameon=True)
    ax[0][1].hist(y1+y2,np.arange(7,11,.5),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].hist(Y1+Y2,np.logspace(-3.69897,-.1549,7),orientation='horizontal',facecolor='None',edgecolor='k')
    ax[1][1].set_xlabel('N',fontsize=35)
    f.savefig(f'{path}LargestSatelliteStellarVsHostMass.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/LargestSatelliteStellarVsHostMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def SatelliteCountVsStellarMassVsEnvironment(host,rest,rad,over,path=''):
    x,y,c = [[],[],[]]
    for h in host:
        x.append(np.log10(host[h]['Mstar']))
        y.append(len(host[h]['Satellites']))
        c.append(host[h]['Closest'][0]/1000.)
    xs,ys = [[],[]]
    wkbk = xlrd.open_workbook('DataFiles/AdditionalData/NvMst.xls')
    wk = wkbk.sheet_by_index(0)
    line = 0
    while line < 8:
        xs.append(wk.cell_value(line,0))
        ys.append(wk.cell_value(line,2))
        line += 1
    wkbk2 = xlrd.open_workbook('DataFiles/AdditionalData/JL.xls')
    wk2 = wkbk2.sheet_by_index(0)
    xjl,yjl,cjl = [[],[],[]]
    line = 1
    while line < 5:
        xjl.append(wk2.cell_value(line,1))
        yjl.append(wk2.cell_value(line,3))
        cjl.append(wk2.cell_value(line,2))
        line += 1

    f,ax = plt.subplots(1,1,figsize=(8,6))
    ax.set_xlabel(r'Log(M$_{*,host}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel(r'N$_{sat}$',fontsize=25)
    ax.xaxis.set_major_locator(MultipleLocator(.5))
    ax.tick_params(which='major',labelsize=15,direction='in', length=6, width=1,top=True,right=True)
    ax.xaxis.set_minor_locator(MultipleLocator(.1))
    ax.tick_params(which='minor',labelsize=0,direction='in', length=3, width=1,top=True,right=True)
    ax.scatter(xs[0],ys[0],label='Rom25',c='k')
    ax.scatter(xjl[0],yjl[0],label='Justice League',c='k',marker='^',s=10**2)
    norm = plt.Normalize(0,max([max(c),max(cjl)]))
    ax.scatter(xs,ys,c='k',marker='*',s=13**2,label='SAGA Paper')
    p = ax.scatter(x,y,c=c,cmap='viridis_r',norm=norm,edgecolor='.3',linewidth=.3)
    ax.scatter(xjl,yjl,c=cjl,cmap='viridis_r',marker='^',s=11**2,norm=norm)
    ax.scatter(wk.cell_value(8,0),wk.cell_value(8,2),marker='*',c='orange',s=13**2,label='MW')
    ax.scatter(wk.cell_value(9,0),wk.cell_value(9,2),marker='*',c='purple',s=13**2,label='M31')
    cbar = f.colorbar(p,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=18)
    cbar.set_label(r'D$_{LH}$ [Mpc]',fontsize=25)
    ax.legend(loc='upper left',bbox_to_anchor=(-.03,1.01),prop={'size':18},frameon=False)
    f.savefig(f'{path}SatelliteCountVsStellarMassVsEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/SatelliteCountVsStellarMassVsEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def StellarMassVsOrbitalDistanceVsT90(host,sats,BB,rest,rad,over,path=''):
    x,y,c,s,S = [[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
    for h in sats:
        if h not in BB:
            rel = sats[h]['center'] - host[sats[h]['Host']]['center']
            wrap(rel,scale=1,boxsize=25e3)
            if sats[h]['Quenched']:
                x[0].append(np.linalg.norm(rel))
                y[0].append(np.log10(sats[h]['Mstar']))
                c[0].append(t_at_sffrac(sats[h]['CumSFH'],.9))
                s[0].append(float(sats[h]['Rvir']))
            else:
                x[1].append(np.linalg.norm(rel))
                y[1].append(np.log10(sats[h]['Mstar']))
                c[1].append(t_at_sffrac(sats[h]['CumSFH'],.9))
                s[1].append(float(sats[h]['Rvir']))
    M = max([max(s[0]),max(s[1])])
    a = 0
    while a < len(s[0]):
        S[0].append((4+(s[0][a]/M)*10)**2)
        a += 1
    a = 0
    while a < len(s[1]):
        S[1].append((4+(s[1][a]/M)*10)**2)
        a += 1
    f, ax = plt.subplots(1,1,figsize=(8,6))
    ax.set_xlim([0,400])
    ax.set_ylim([6.9,10.6])
    ax.scatter(0,0,s=8**2,marker='D',edgecolor='.5',facecolor='None',label='Quenched')
    ax.scatter(0,0,s=10**2,edgecolor='.5',facecolor='None',label='Star Forming')
    ax.tick_params(labelsize=15,direction='in', length=5, width=1,top=True,right=True)
    ax.set_xlabel(r'Distance to Host [kpc]',fontsize=25)
    ax.set_ylabel(r'Log(M$_{*}$/M$_{\odot}$)',fontsize=25)
    norm = plt.Normalize(3,13)
    p = ax.scatter(x[0],y[0],c=c[0],cmap='viridis',s=S[0],norm=norm,marker='D',edgecolor='.5',linewidth=.5)
    ax.scatter(x[1],y[1],c=c[1],cmap='viridis',s=S[1],norm=norm,edgecolor='.5',linewidth=.5)
    cbar = f.colorbar(p,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.set_label(r'$\tau_{90}$ [Gyr]',fontsize=25)
    cbar.ax.tick_params(labelsize=18,length=3)
    ax.legend(loc='upper right',prop={'size':18},ncol=1,frameon=False)
    f.savefig(f'{path}StellarMassVsOrbitalDistanceVsT90.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/StellarMassVsOrbitalDistanceVsT90.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def QuenchedFractionVsStellarMass(host,sats,rest,rad,over,path=''):
    r = np.logspace(7,11,num=10)
    x,dx,y,T = [[],[],[],[]]
    i = 0
    while i < len(r)-1:
        t = 0
        q = 0
        for h in sats:
            if r[i+1] > sats[h]['Mstar'] > r[i]:
                t += 1
                if sats[h]['Quenched']:
                    q += 1
        if t > 0:
            y.append(float(q)/float(t))
        else:
            y.append(0)
        T.append(t)
        x.append((r[i+1]+r[i])/2.)
        dx.append(r[i+1]-r[i])
        i += 1
    f,ax=plt.subplots(1,1)
    ax.set_xlabel(r'M$_{star}$ [M$_{\odot}$]',fontsize=20)
    ax.set_ylabel('Quenched Fraction',fontsize=20)
    ax.set_ylim([0,1.05])
    ax.set_xlim([10**7,10**11.1])
    ax.semilogx()
    ax.tick_params(which='major',labelsize=15,direction='in', length=5, width=1,top=True)
    ax.tick_params(which='minor',labelsize=5,direction='in', length=3, width=1,top=True)
    ax3 =ax.twinx()
    ax3.bar(x,T,width=dx,color='.5',alpha=.5)
    ax3.set_ylim([0,30])
    ax3.set_ylabel('Sample Size',fontsize=20)
    ax3.tick_params(which='major',labelsize=15,direction='in', length=5)
    ax.plot(x,y,c='k')
    ax.plot([10**6,10**12],[.5,.5],c='k',linestyle=':',linewidth=.7)
    ax.plot([10**6,10**12],[1,1],c='k',linestyle=':',linewidth=.7)
    f.savefig(f'{path}QuenchFractionVsStellarMass.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/QuenchFractionVsStellarMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def QuenchedFractionVsOrbitalDistance(host,sats,rest,rad,over,path=''):
    r = np.linspace(0,1,num=11)
    x,dx,y,T = [[],[],[],[]]
    for i in np.arange(len(r)-1):
        t,q = 0,0
        for h in sats:
            o = sats[h]['Orbit'][1] if rad=='sim' else sats[h]['Orbit'][0]/300
            if sats[h]['Mstar']>1e8 and r[i]<o<r[i+1]:
                t+=1
                if sats[h]['Quenched']: q+=1
        ynew = np.nan if t==0 else q/t
        y.append(ynew)
        x.append((r[i+1]-r[i])/2+r[i])
        dx.append(r[i+1]-r[i])
        T.append(t)

    f,ax=plt.subplots(1,1)
    ax.set_xlabel(r'Orbital Distance [R$_{vir}$]',fontsize=20)
    ax.set_ylabel('Quenched Fraction',fontsize=20)
    ax.set_ylim([0,1.05])
    ax.set_xlim([0,1])
    ax.tick_params(which='major',labelsize=15,direction='in', length=5, width=1,top=True)
    ax.tick_params(which='minor',labelsize=5,direction='in', length=3, width=1,top=True)
    ax3 =ax.twinx()
    ax3.bar(x,T,width=dx,color='.5',alpha=.5)
    ax3.set_ylim([0,25])
    ax3.set_ylabel('Sample Size',fontsize=20)
    ax3.tick_params(which='major',labelsize=15,direction='in', length=5)
    ax.plot(x,y,c='k')
    ax.plot([0,1],[.5,.5],c='k',linestyle=':',linewidth=.7)
    ax.plot([0,1],[1,1],c='k',linestyle=':',linewidth=.7)
    f.savefig(f'{path}QuenchFractionVsOrbitalDistance.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/QuenchFractionVsOrbitalDistance.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def QuenchedFractionVsHostStellarMass(host,sats,rest,rad,over,path=''):
    mstar, qf = [[],[]]
    for h in host:
        if len(host[h]['Satellites'])>0:
            mstar.append(host[h]['Mstar'])
            t,q = [0,0]
            for s in host[h]['Satellites']:
                t+=1
                if sats[s]['Quenched']: q+=1
            qf.append(q/t)
    f,ax=plt.subplots(1,1)
    ax.set_xlabel(r'M$_{star}$ [M$_{\odot}$]',fontsize=20)
    ax.set_ylabel('Quenched Fraction',fontsize=20)
    ax.set_ylim([0,1.05])
    ax.set_xlim([10**9.6,10**11.2])
    ax.semilogx()
    ax.tick_params(which='major',labelsize=15,direction='in', length=5, width=1,top=True)
    ax.tick_params(which='minor',labelsize=5,direction='in', length=3, width=1,top=True)
    ax.scatter(mstar,qf,c='k')
    ax.plot([10**9.6,10**11.2],[.5,.5],c='k',linestyle=':',linewidth=.7)
    ax.plot([10**9.6,10**11.2],[1,1],c='k',linestyle=':',linewidth=.7)
    f.savefig(f'{path}QuenchFractionVsHostStellarMass.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/QuenchFractionVsHostStellarMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def StellarMassVsEnvironmentVsAverageSatelliteCount(host,rest,rad,over,path=''):
    y = np.arange(9.4,11.01,.2)
    x = np.arange(0,12,2)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mstar']) > y[r] and x[c+1] > host[h]['Closest'][0]/1000 > x[c]:
                    d.append(len(host[h]['Satellites']))
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(8,4))
    ax.set_xlabel(r'Log(M$_{*}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel(r'D$_{LH}$ [Mpc]',fontsize=25)
    ax.tick_params(which='major',labelsize=20, length=5)
    #norm = plt.Normalize(-1,int(np.amax(C))+1)
    norm = mpl.colors.BoundaryNorm(np.arange(-.5,9.5), mpl.cm.viridis.N)#, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=20)
    #cbar.ax.set_yticklabels(np.arange(1,int(np.amax(C))+1))
    cbar.set_label(r'Average N$_{sat}$',fontsize=25)
    cbar.set_ticks(np.arange(0,11))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.5,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    ax.grid(True,which='major',color='k',linewidth=2)
    f.savefig(f'{path}StellarMassVsEnvironmentVsAverageSatelliteCount.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/StellarMassVsEnvironmentVsAverageSatelliteCount.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def StellarMassVsEnvironmentVsQuenchFraction(host,sat,rest,rad,over,path=''):
    y = np.arange(9.4,11.01,.2)
    x = np.arange(0,12,2)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mstar']) > y[r] and x[c+1] > host[h]['Closest_MW+'][0]/1000 > x[c]:
                    t,q = 0,0
                    for s in host[h]['Satellites']:
                        if sat[s]['Mstar']>1e8:
                            t+=1
                            if sat[s]['Quenched']:q+=1
                    if t>0: d.append(q/t)
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(8,4))
    ax.set_xlabel(r'Log(M$_{*}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel(r'D$_{LH}$ [Mpc]',fontsize=25)
    ax.tick_params(which='major',labelsize=20, length=5)
    norm = plt.Normalize(0,1)
    #norm = mpl.colors.BoundaryNorm([0,1], mpl.cm.viridis.N, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=20)
    #cbar.ax.set_yticklabels(np.arange(1,int(np.amax(C))+1))
    cbar.set_label('Average f$_Q$',fontsize=25)
    #cbar.set_ticks(np.arange(0,1))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.5,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    ax.grid(True,which='major',color='k',linewidth=2)
    f.savefig(f'{path}StellarMassVsEnvironmentVsQuenchFraction.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/StellarMassVsEnvironmentVsQuenchFraction.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def StellarMassVsNeighborEnvironmentVsAverageSatelliteCount(host,rest,rad,over,path=''):
    y = np.arange(9.4,11.01,.2)
    x = np.arange(0,10,2)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mstar']) > y[r] and x[c+1] > host[h]['10thNeighbor']/1000 > x[c]:
                    d.append(len(host[h]['Satellites']))
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(8,3.5))
    ax.set_xlabel(r'Log(M$_{*}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel(r'D$_{10}$ [Mpc]',fontsize=25)
    ax.tick_params(which='major',labelsize=20, length=5)
    #norm = plt.Normalize(-1,int(np.amax(C))+1)
    norm = mpl.colors.BoundaryNorm(np.arange(-.5,10.5), mpl.cm.viridis.N)#, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=20)
    #cbar.ax.set_yticklabels(np.arange(1,int(np.amax(C))+1))
    cbar.set_label('Average N$_{sat}$',fontsize=25)
    cbar.set_ticks(np.arange(0,14))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.5,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    ax.grid(True,which='major',color='k',linewidth=2)
    f.savefig(f'{path}StellarMassVsNeighborEnvironmentVsAverageSatelliteCount.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/StellarMassVsNeighborEnvironmentVsAverageSatelliteCount.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def StellarMassVsMWpEnvironmentVsAverageSatelliteCount(host,rest,rad,over,path=''):
    y = np.arange(9.4,11.01,.2)
    x = np.arange(0,10,2)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mstar']) > y[r] and x[c+1] > host[h]['Closest_MW+'][0]/1000 > x[c]:
                    d.append(len(host[h]['Satellites']))
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(8,3))
    ax.set_xlabel(r'Log(M$_{*}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel('D$_{MW+}$ [Mpc]',fontsize=25)
    ax.tick_params(which='major',labelsize=20, length=5)
    #norm = plt.Normalize(-1,int(np.amax(C))+1)
    norm = mpl.colors.BoundaryNorm(np.arange(-.5,7), mpl.cm.viridis.N)#, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=20)
    cbar.set_label('Average N$_{sat}$',fontsize=25)
    cbar.set_ticks(np.arange(0,int(np.amax(C)+2)))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.6,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    ax.grid(True,which='major',color='k',linewidth=2)
    f.savefig(f'{path}StellarMassVsMWpEnvironmentVsAverageSatelliteCount.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/StellarMassVsMWpEnvironmentVsAverageSatelliteCount.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def StellarMassVsEnvironmentalDensityVsAverageSatelliteCount(host,rest,rad,over,path=''):
    y = np.arange(9.4,11.01,.2)
    x = np.arange(-.5,7.5,1)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mstar']) > y[r] and x[c+1] > host[h]['EnvDen'] > x[c]:
                    d.append(len(host[h]['Satellites']))
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(8,5))
    ax.set_xlabel(r'Log(M$_{*}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel(r'N$_L(<$1 Mpc)',fontsize=25)
    ax.tick_params(which='major',labelsize=20, length=5)
    #norm = plt.Normalize(-1,int(np.amax(C))+1)
    norm = mpl.colors.BoundaryNorm(np.arange(-.5,9.5), mpl.cm.viridis.N)#, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=20)
    #cbar.ax.set_yticklabels(np.arange(1,int(np.amax(C))+1))
    cbar.set_label('Average N$_{sat}$',fontsize=25)
    cbar.set_ticks(np.arange(0,11))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.35,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    for i in y:
        ax.axvline(i,c='k',linewidth=2)
    for i in x:
        ax.plot([min(y),max(y)],[i,i],c='k',linewidth=2)
    f.savefig(f'{path}StellarMassVsEnvironmentalDensityVsAverageSatelliteCount.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/StellarMassVsEnvironmentalDensityVsAverageSatelliteCount.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def EnvironmentDistribution(host,rest,rad,over,path=''):
    y,Y = [[],[]]
    considered = set()
    for h in host:
        Y.append(host[h]['Closest'][0]/1000.)
        #if h not in considered and host[h]['Closest_MW+'][1] not in considered:
        #    y.append(host[h]['Closest_MW+'][0]/1000.)
        #    considered.add(h)
        #    considered.add(host[h]['Closest_MW+'][1])
        a,h2 = host[h]['Closest_MW+']
        if ( min([int(h),int(h2)]) , max([int(h),int(h2)]) ) not in considered:
            y.append(a/1000.)
            considered.add( (min([int(h),int(h2)]) , max([int(h),int(h2)])) )
    x = np.linspace(0,10,50)
    top = 10
    f,ax = plt.subplots(1,1)
    ax.set_xlim([0,10])
    ax.set_ylim([0,top])
    ax.hist(y,x,color='.5',label='D$_{MW+}$')
    ax.hist(Y,x,edgecolor='k',fc=(0,0,0,0),label='D$_{LH}$')
    ax.axvline(.767,linestyle=':',label='MW to M31',color='k')
    ax.set_xlabel('Distance [Mpc]',fontsize=20)
    ax.set_ylabel('N',fontsize=20)
    ax.tick_params(labelsize=15)
    ax.legend(loc='upper right',frameon=False,prop={'size':15})
    f.savefig(f'{path}EnvironmentalDistribution.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/EnvironmentalDistribution.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def SpecificFrequencyStellarMass(host,rest,rad,over,path=''):
    x,y,x0,y0, = [[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) == 0:
            x0.append(np.log10(host[h]['Mstar']))
            y0.append(SnM(len(host[h]['Satellites']),host[h]['Mstar']))
        else:
            x.append(np.log10(host[h]['Mstar']))
            y.append(SnM(len(host[h]['Satellites']),host[h]['Mstar']))
    f,ax = plt.subplots(1,1)
    ax.scatter(x0,y0,c='0.5',label='No Satellites')
    ax.scatter(x,y,c='k')
    ax.set_ylim([-.5,25])
    ax.tick_params(labelsize=15, length=5)
    ax.set_xlabel(r'Log(M$_{*}$/M$_\odot$)',fontsize=20)
    ax.set_ylabel(r'S$_{N}$',fontsize=20)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}SpecificFrequencyMass.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/SpecificFrequencyMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def SpecificFrequencyDistance(host,rest,rad,over,path=''):
    x,y,x0,y0, = [[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) == 0:
            x0.append(host[h]['Closest'][0]/1000)
            y0.append(SnD(len(host[h]['Satellites']),host[h]['Closest'][0]))
        else:
            x.append(host[h]['Closest'][0]/1000)
            y.append(SnD(len(host[h]['Satellites']),host[h]['Closest'][0]))

    f,ax = plt.subplots(1,1)
    ax.scatter(x0,y0,c='0.5',label='No Satellites')
    ax.scatter(x,y,c='k')
    for i in np.arange(len(y)):
        if y[i] > 25:
            ax.text(x[i],23.5,'|\n|')
            ax.text(x[i]-.6,22.5,str(round(y[i],2)),fontsize=12,horizontalalignment='center')
    ax.set_ylim([-.5,25])
    ax.tick_params(labelsize=13, length=5)
    ax.set_xlabel(r'D$_{LH}$ [Mpc]',fontsize=20)
    ax.set_ylabel(r'S$_{N}$',fontsize=20)
    ax.tick_params(labelsize=15)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}SpecificFrequencyEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/SpecificFrequencyEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def SpecificFrequencyNeighborEnvironment(host,rest,rad,over,path=''):
    x,y,x0,y0, = [[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) == 0:
            x0.append(host[h]['Closest'][0]/1000)
            y0.append(SnN(len(host[h]['Satellites']),host[h]['10thNeighbor']))
        else:
            x.append(host[h]['Closest'][0]/1000)
            y.append(SnN(len(host[h]['Satellites']),host[h]['10thNeighbor']))

    f,ax = plt.subplots(1,1)
    ax.scatter(x0,y0,c='0.5',label='No Satellites')
    ax.scatter(x,y,c='k')
    for i in np.arange(len(y)):
        if y[i] > 25:
            ax.text(x[i],23.5,'|\n|')
            ax.text(x[i]-.6,22.5,str(round(y[i],2)),fontsize=12,horizontalalignment='center')
    ax.set_ylim([-.5,25])
    ax.tick_params(labelsize=15, length=5)
    ax.set_xlabel(r'D$_{10}$ [Mpc]',fontsize=20)
    ax.set_ylabel(r'S$_{N}$',fontsize=20)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}SpecificFrequencyNeighborEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/SpecificFrequencyNeighborEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def SpecificFrequencyEnvironmentalDensity(host,rest,rad,over,path=''):
    x,y,x0,y0, = [[],[],[],[]]
    for h in host:
        if len(host[h]['Satellites']) == 0:
            x0.append(host[h]['EnvDen'])
            y0.append(SnE(len(host[h]['Satellites']),host[h]['EnvDen']))
        else:
            x.append(host[h]['EnvDen'])
            y.append(SnE(len(host[h]['Satellites']),host[h]['EnvDen']))

    f,ax = plt.subplots(1,1)
    ax.scatter(x0,y0,c='0.5',label='No Satellites')
    ax.scatter(x,y,c='k')
    for i in np.arange(len(y)):
        if y[i] > 25:
            ax.text(x[i],23.5,'|\n|')
            ax.text(x[i]-.6,22.5,str(round(y[i],2)),fontsize=12,horizontalalignment='center')
    #ax.set_ylim([-.5,25])
    ax.tick_params(labelsize=15, length=5)
    ax.set_xlabel(r'N$_L(<$1 Mpc)',fontsize=20)
    ax.set_ylabel(r'S$_{N}$',fontsize=20)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}SpecificFrequencyEnvironmentalDensity.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/SpecificFrequencyEnvironmentalDensity.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def BinnedSpecificFrequencyStellarMass(host,rest,rad,over,path=''):
    xr = np.arange(9.4,11.2,.05)
    x1,y1,e1,e1u,e1l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < np.log10(host[h]['Mstar']) < xr[i+1]:
                yc.append(SnM(len(host[h]['Satellites']),host[h]['Mstar']))
        if len(yc) > 0:
            y1.append(np.mean(yc))
            #y1.append(np.median(yc))
            x1.append(np.mean([xr[i],xr[i+1]]))
            e1.append(np.std(yc)/np.sqrt(len(yc)))
            e1u.append(np.percentile(yc,75))
            e1l.append(np.percentile(yc,25))
        i += 1
    xr = np.arange(9.4,11.2,.1)
    x2,y2,e2,e2u,e2l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < np.log10(host[h]['Mstar']) < xr[i+1]:
                yc.append(SnM(len(host[h]['Satellites']),host[h]['Mstar']))
        if len(yc) > 0:
            y2.append(np.mean(yc))
            #y2.append(np.median(yc))
            x2.append(np.mean([xr[i],xr[i+1]]))
            e2.append(np.std(yc)/np.sqrt(len(yc)))
            e2u.append(np.percentile(yc,75))
            e2l.append(np.percentile(yc,25))
        i += 1
    xr = np.arange(9.25,11.2,.25)
    x3,y3,e3,e3l,e3u= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < np.log10(host[h]['Mstar']) < xr[i+1]:
                yc.append(SnM(len(host[h]['Satellites']),host[h]['Mstar']))
        if len(yc) > 0:
            y3.append(np.mean(yc))
            #y3.append(np.median(yc))
            x3.append(np.mean([xr[i],xr[i+1]]))
            e3.append(np.std(yc)/np.sqrt(len(yc)))
            e3u.append(np.percentile(yc,75))
            e3l.append(np.percentile(yc,25))
        i += 1
    f,ax = plt.subplots(1,1)
    ax.set_ylim([-.5,15])
    ax.scatter(x1,y1,c='k',label=r'$\Delta$Log[M$_{*}$] = .05')
    ax.errorbar(x1,y1,yerr=e1,c='k')
    #ax.errorbar(x1,y1,yerr=[e1l,e1u],c='k')
    ax.scatter(x2,y2,c='b',label=r'$\Delta$Log[M$_{*}$] = .10')
    ax.errorbar(x2,y2,yerr=e2,c='b')
    #ax.errorbar(x2,y2,yerr=[e2l,e2u],c='b')
    ax.scatter(x3,y3,c='r',label=r'$\Delta$Log[M$_{*}$] = .25')
    ax.errorbar(x3,y3,yerr=e3,c='r')
    #ax.errorbar(x3,y3,yerr=[e3l,e3u],c='r')
    ax.tick_params(labelsize=15, length=5)
    ax.set_xlabel(r'Log(M$_{*}$/M$_\odot$)',fontsize=20)
    ax.set_ylabel(r'S$_{N,mass}$',fontsize=20)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}BinnedSpecificFrequencyMass.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/BinnedSpecificFrequencyMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def BinnedSpecificFrequencyDistance(host,rest,rad,over,path=''):
    xr = np.arange(0,10,.25)
    x1,y1,e1,e1u,e1l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < host[h]['Closest'][0]/1000 < xr[i+1]:
                yc.append(SnD(len(host[h]['Satellites']),host[h]['Closest'][0]))
        if len(yc) > 0:
            y1.append(np.mean(yc))
            #y1.append(np.median(yc))
            x1.append(np.mean([xr[i],xr[i+1]]))
            e1.append(np.std(yc)/np.sqrt(len(yc)))
            e1u.append(np.percentile(yc,75))
            e1l.append(np.percentile(yc,25))
        i += 1
    xr = np.arange(0,10,.5)
    x2,y2,e2,e2u,e2l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < host[h]['Closest'][0]/1000 < xr[i+1]:
                yc.append(SnD(len(host[h]['Satellites']),host[h]['Closest'][0]))
        if len(yc) > 0:
            y2.append(np.mean(yc))
            #y2.append(np.median(yc))
            x2.append(np.mean([xr[i],xr[i+1]]))
            e2.append(np.std(yc)/np.sqrt(len(yc)))
            e2u.append(np.percentile(yc,75))
            e2l.append(np.percentile(yc,25))
        i += 1
    xr = np.arange(0,10,1)
    x3,y3,e3,e3u,e3l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < host[h]['Closest'][0]/1000 < xr[i+1]:
                yc.append(SnD(len(host[h]['Satellites']),host[h]['Closest'][0]))
        if len(yc) > 0:
            y3.append(np.mean(yc))
            #y3.append(np.median(yc))
            x3.append(np.mean([xr[i],xr[i+1]]))
            e3.append(np.std(yc)/np.sqrt(len(yc)))
            e3u.append(np.percentile(yc,75))
            e3l.append(np.percentile(yc,25))
        i += 1
    M = 18
    f,ax = plt.subplots(1,1)
    ax.set_ylim([-.5,15])
    ax.scatter(x1,y1,c='k',label=r'$\Delta$D = .25Mpc')
    ax.errorbar(x1,y1,yerr=e1,c='k')
    #ax.errorbar(x1,y1,yerr=[e1l,e1u],c='k')
    for i in np.arange(len(y1)):
        if y1[i] > M +1:
            pass
            #ax.text(x1[i],M,'|\n|')
            #ax.text(x1[i]-.25,M-.6,str(round(y1[i],2)),fontsize=12)
    ax.scatter(x2,y2,c='b',label=r'$\Delta$D = .50Mpc')
    ax.errorbar(x2,y2,yerr=e2,c='b')
    #ax.errorbar(x2,y2,yerr=[e2l,e2u],c='b')
    for i in np.arange(len(y2)):
        if y2[i] > M+1:
            pass
            #ax.text(x2[i],M,'|\n|')
            #ax.text(x2[i]-.25,M-.6,str(round(y2[i],2)),fontsize=12)
    ax.scatter(x3,y3,c='r',label=r'$\Delta$D = 1.0Mpc')
    ax.errorbar(x3,y3,yerr=e3,c='r')
    #ax.errorbar(x3,y3,yerr=[e3l,e3u],c='r')
    for i in np.arange(len(y3)):
        if y3[i] > M+1:
            pass
            #ax.text(x3[i],M,'|\n|')
            #ax.text(x3[i]-.25,M-.5,str(round(y3[i],2)),fontsize=12)
    ax.tick_params(labelsize=15, length=5)
    ax.set_xlabel(r'D$_{LH}$ [Mpc]',fontsize=20)
    ax.set_ylabel(r'S$_{N,env}$',fontsize=20)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}BinnedSpecificFrequencyEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/BinnedSpecificFrequencyEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def BinnedSpecificFrequencyNeighborEnvironment(host,rest,rad,over,path=''):
    xr = np.arange(0,8,.25)
    x1,y1,e1,e1u,e1l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < host[h]['10thNeighbor']/1000 < xr[i+1]:
                yc.append(SnN(len(host[h]['Satellites']),host[h]['10thNeighbor']))
        if len(yc) > 0:
            y1.append(np.mean(yc))
            #y1.append(np.median(yc))
            x1.append(np.mean([xr[i],xr[i+1]]))
            e1.append(np.std(yc)/np.sqrt(len(yc)))
            e1u.append(np.percentile(yc,75))
            e1l.append(np.percentile(yc,25))
        i += 1
    xr = np.arange(0,8,.5)
    x2,y2,e2,e2u,e2l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < host[h]['10thNeighbor']/1000 < xr[i+1]:
                yc.append(SnN(len(host[h]['Satellites']),host[h]['10thNeighbor']))
        if len(yc) > 0:
            y2.append(np.mean(yc))
            #y2.append(np.median(yc))
            x2.append(np.mean([xr[i],xr[i+1]]))
            e2.append(np.std(yc)/np.sqrt(len(yc)))
            e2u.append(np.percentile(yc,75))
            e2l.append(np.percentile(yc,25))
        i += 1
    xr = np.arange(0,8,1)
    x3,y3,e3,e3u,e3l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < host[h]['10thNeighbor']/1000 < xr[i+1]:
                yc.append(SnN(len(host[h]['Satellites']),host[h]['10thNeighbor']))
        if len(yc) > 0:
            y3.append(np.mean(yc))
            #y3.append(np.median(yc))
            x3.append(np.mean([xr[i],xr[i+1]]))
            e3.append(np.std(yc)/np.sqrt(len(yc)))
            e3u.append(np.percentile(yc,75))
            e3l.append(np.percentile(yc,25))
        i += 1
    M = 18
    f,ax = plt.subplots(1,1)
    ax.set_ylim([-.5,M+1])
    ax.scatter(x1,y1,c='k',label=r'$\Delta$D = .25Mpc')
    ax.errorbar(x1,y1,yerr=e1,c='k')
    #ax.errorbar(x1,y1,yerr=[e1l,e1u],c='k')
    for i in np.arange(len(y1)):
        if y1[i] > M +1:
            pass
            #ax.text(x1[i],M,'|\n|')
            #ax.text(x1[i]-.25,M-.6,str(round(y1[i],2)),fontsize=12)
    ax.scatter(x2,y2,c='b',label=r'$\Delta$D = .50Mpc')
    ax.errorbar(x2,y2,yerr=e2,c='b')
    #ax.errorbar(x2,y2,yerr=[e2l,e2u],c='b')
    for i in np.arange(len(y2)):
        if y2[i] > M+1:
            pass
            #ax.text(x2[i],M,'|\n|')
            #ax.text(x2[i]-.25,M-.6,str(round(y2[i],2)),fontsize=12)
    ax.scatter(x3,y3,c='r',label=r'$\Delta$D = 1.0Mpc')
    ax.errorbar(x3,y3,yerr=e3,c='r')
    #ax.errorbar(x3,y3,yerr=[e3l,e3u],c='r')
    for i in np.arange(len(y3)):
        if y3[i] > M+1:
            pass
            #ax.text(x3[i],M,'|\n|')
            #ax.text(x3[i]-.25,M-.5,str(round(y3[i],2)),fontsize=12)
    ax.tick_params(labelsize=15, length=5)
    ax.set_xlabel(r'D$_{10}$ [Mpc]',fontsize=20)
    ax.set_ylabel(r'S$_{N,env}$',fontsize=20)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}BinnedSpecificFrequencyNeighborEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/BinnedSpecificFrequencyNeighborEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def BinnedSpecificFrequencyEnvironmentalDensity(host,rest,rad,over,path=''):
    xr = np.arange(-.5,7.5,1)
    x1,y1,e1,e1u,e1l= [[],[],[],[],[]]
    i = 0
    while i < len(xr) -1:
        yc = []
        for h in host:
            if xr[i] < host[h]['Closest'][0]/1000 < xr[i+1]:
                yc.append(SnE(len(host[h]['Satellites']),host[h]['EnvDen']))
        if len(yc) > 0:
            y1.append(np.mean(yc))
            #y1.append(np.median(yc))
            x1.append(np.mean([xr[i],xr[i+1]]))
            e1.append(np.std(yc)/np.sqrt(len(yc)))
            e1u.append(np.percentile(yc,75))
            e1l.append(np.percentile(yc,25))
        i += 1
    f,ax = plt.subplots(1,1)
    ax.scatter(x1,y1,c='k',label=r'$\Delta$D = .25Mpc')
    ax.errorbar(x1,y1,yerr=e1,c='k')
    ax.tick_params(labelsize=15, length=5)
    ax.set_xlabel(r'N$_L(<$1 Mpc)',fontsize=20)
    ax.set_ylabel(r'S$_{N,env}$',fontsize=20)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'{path}BinnedSpecificFrequencyEnvironmentalDensity.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=0.1)
    #f.savefig(f'{path}pdf/BinnedSpecificFrequencyEnvironmentalDensity.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=0.1)
    plt.close()

def QuenchedFractionVsEnvironment(host,sats,rest,rad,over,path=''):
    env,qf,tots,qclose,qfar,envclose,envfar = [],[],[],[],[],[],[]
    for mw in host:
        t,q = [0,0]
        for sat in host[mw]['Satellites']:
            if sats[sat]['Mstar']>1e8:
                t+=1
                if sats[sat]['Quenched']:
                    q+=1
        if t>0:
            qf.append(float(q)/float(t)*host[mw]['Mstar']/(10**11))
            d = host[mw]['Closest_MW+'][0]/1000
            env.append(d)
            tots.append(t)
            if d<1:
                qclose.append(float(q)/float(t)*host[mw]['Mstar']/(10**11))
            else:
                qfar.append(float(q)/float(t)*host[mw]['Mstar']/(10**11))
    
    f,ax = plt.subplots(1,1)
    ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=20)
    ax.set_ylabel(r'f$_Q$',fontsize=20)
    ax.tick_params(labelsize=15)
    ax.set_xlim([.06,5])
    ax.set_ylim([-.2,1.03])
    ax.plot([-1,11],[1,1],c='.5',linestyle=':')
    ax.plot([-1,11],[0,0],c='.5',linestyle=':')
    ax.axvline(.767,linestyle='--',label='MW - M31',color='.5',zorder=1)
    #norm = plt.Normalize(1,10)
    norm = mpl.colors.BoundaryNorm(np.arange(.5,max(tots)+1.5), mpl.cm.viridis.N)
    p = ax.scatter(env,qf,s=7**2,c=tots,cmap='viridis',norm=norm,zorder=5)
    cbar = f.colorbar(p,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.set_label(r'N$_{sat}$ [M$_*>10^8$ M$_\odot$]',fontsize=20)
    cbar.set_ticks(np.arange(1,max(tots)+1))
    ax.plot([0,1],[np.mean(qclose),np.mean(qclose)],c='b',label='Pairs',zorder=6)
    ax.plot([1,5],[np.mean(qfar),np.mean(qfar)],c='r',label='Isolated',zorder=6)
    ax.plot([1,1],[np.mean(qclose),np.mean(qfar)],c='k',zorder=6)
    ax.legend(loc='lower left',ncol=3,prop={'size':14.5})
    ax.semilogx()
    f.savefig(f'{path}QuenchedFractionVsEnvironment.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/QuenchedFractionVsEnvironment.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def QuenchedFractionHistograms(host,sats,rest,rad,over,path=''):
    qf,qclose,qfar = [],[],[]
    for mw in host:
        t,q = [0,0]
        for sat in host[mw]['Satellites']:
            if sats[sat]['Mstar']>1e8:
                t+=1
                if sats[sat]['Quenched']:
                    q+=1
        if t>0:
            qf.append(float(q)/float(t))
            if host[mw]['Closest_MW+'][0]<1000:
                qclose.append(float(q)/float(t))
            else:
                qfar.append(float(q)/float(t))

    qf_bins = np.linspace(0,1,11)
    f,ax = plt.subplots(1,1)
    ax.set_xlabel(r'f$_Q$',fontsize=20)
    ax.set_ylabel('N',fontsize=20)
    ax.tick_params(labelsize=15)
    ax.set_xlim([0,1])
    ax.hist(qf,qf_bins,histtype='step',linewidth=2,color='k',label='Total')
    ax.hist(qclose,qf_bins,histtype='step',linewidth=2,color='b',label='Pairs')
    ax.hist(qfar,qf_bins,histtype='step',linewidth=2,color='r',label='Isolated')
    ax.legend(loc='upper right',prop={'size':15})
    f.savefig(f'{path}QuenchedFractionHistograms.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/QuenchedFractionHistograms.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def SAGA_Nsat_Comparison(host,rest,rad,over,path=''):
    SAGAII_Nsat_Data = [4,2,3,3,2,2,6,4,1,2,2,5,0,4,7,2,5,5,3,0,3,1,3,0,2,9,9,4,5,4,2,6,5,1,5,2]
    simdata=[]
    for mw in host:
        simdata.append(len(host[mw]['Satellites']))
    x = np.arange(max([max(simdata),max(SAGAII_Nsat_Data)])+1)
    ys = np.zeros(len(x))
    for i in np.arange(len(x)):
        for count in simdata:
            if x[i] == count:
                ys[i]+=1
    ysn = [i/ys.sum() for i in ys]
    data = np.zeros(len(x))
    for i in np.arange(len(x)):
        for count in SAGAII_Nsat_Data:
            if x[i] == count:
                data[i]+=1
    datan = [i/data.sum() for i in data]
    M = max([max(ysn),max(datan)])
    f,ax = plt.subplots(1,1,figsize=(12,9))
    ax.axvline(5,c='0.65',linestyle='--',zorder=0)
    ax.axvline(9,c='0.65',linestyle='-.',zorder=0)
    ax.plot([-.75,-.3],[1/data.sum(),1/data.sum()],c='k',linewidth=.5)
    ax.plot([-.75,-.3],[1/ys.sum(),1/ys.sum()],c='darkturquoise',linewidth=.5)
    ax.text(4.65,M-.05,'MW',c='.65',rotation=90,fontsize=20)
    ax.text(8.65,M-.05,'M31',c='.65',rotation=90,fontsize=20)
    ax.scatter(x,ysn,c='darkturquoise',s=10**2,label='Romulus 25')
    ax.scatter(x,datan,c='k',marker='*',s=15**2,label='SAGA (Observed)')
    ax.set_xlim([-.5,max(x)+1])
    ax.set_ylim([0,M+0.05])
    ax.set_xlabel(r'$N_{sat}$',fontsize=35)
    ax.set_ylabel(r'$N_{Host}$ (Normalized)',fontsize=35)
    ax.legend(loc='upper right',prop={'size':20})
    ax.xaxis.set_minor_locator(MultipleLocator(.5))
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.tick_params(which='major',labelsize=25,length=10)
    ax.tick_params(which='minor',length=5)
    f.savefig(f'{path}SAGA_Nsat_Comparison.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGA_Nsat_Comparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def SMHM(host,sats,rest,rad,over,path=''):
    mv_mw,ms_mw,mv_sat,ms_sat = [[],[],[],[]]
    for mw in host:
        mv_mw.append(host[mw]['Mvir']/0.8)
        ms_mw.append(.6*host[mw]['Mstar'])
    for sat in sats:
        mv_sat.append(sats[sat]['Mvir']/0.8)
        ms_sat.append(.6*sats[sat]['Mstar'])
    
    f,ax = plt.subplots(1,1)
    ax.semilogx()
    ax.semilogy()
    ax.set_xlim([10**9,2*10**13])
    ax.set_ylim([10**-5,1])
    ax.tick_params(labelsize=15,length=5)
    ax.set_xlabel(r'M$_{vir}$ [M$_\odot$]',fontsize=20)
    ax.set_ylabel(r'M$_*$/M$_{vir}$',fontsize=20)
    ax.scatter(mv_sat,np.array(ms_sat)/np.array(mv_sat),c='r',label='Satellites')
    ax.scatter(mv_mw,np.array(ms_mw)/np.array(mv_mw),c='k',label='MW Anaolgs')
    ax.legend(loc='upper right',prop={'size':15})
    f.savefig(f'{path}SMHM.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SMHM.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def SMHMPeak(host,sats,rest,rad,over,path=''):
    mv_mw,ms_mw,mv_sat,ms_sat = [[],[],[],[]]
    for mw in host:
        mv_mw.append(host[mw]['MvirPeak']/0.8)
        ms_mw.append(.6*host[mw]['Mstar'])
    #for sat in sats:
    #    mv_sat.append(sats[sat]['MvirPeak']/0.8)
    #    ms_sat.append(.6*sats[sat]['Mstar'])
    
    f,ax = plt.subplots(1,1)
    ax.semilogx()
    ax.semilogy()
    ax.set_xlim([10**9,2*10**13])
    ax.set_ylim([10**-5,1])
    ax.tick_params(labelsize=15,length=5)
    ax.set_xlabel(r'M$_{vir,peak}$ [M$_\odot$]',fontsize=20)
    ax.set_ylabel(r'M$_{*,z0}$/M$_{vir,peak}$',fontsize=20)
    #ax.scatter(mv_sat,np.array(ms_sat)/np.array(mv_sat),c='r',label='Satellites')
    ax.scatter(mv_mw,np.array(ms_mw)/np.array(mv_mw),c='k',label='MW Anaolgs')
    ax.legend(loc='upper right',prop={'size':15})
    f.savefig(f'{path}SMHMPeak.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SMHMPeak.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def VirialMassVsEnvironmentVsAverageSatelliteCount(host,rest,rad,over,path=''):
    y = np.arange(10.8,12.8,.2)
    x = np.arange(0,12,2)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mvir']) > y[r] and x[c+1] > host[h]['Closest'][0]/1000 > x[c]:
                    d.append(len(host[h]['Satellites']))
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(10,4))
    ax.set_xlabel(r'Log(M$_{vir}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel(r'D$_{LH}$ [Mpc]',fontsize=25)
    ax.tick_params(which='major',labelsize=15, length=5)
    #norm = plt.Normalize(-1,int(np.amax(C))+1)
    norm = mpl.colors.BoundaryNorm(np.arange(-.5,8.5), mpl.cm.viridis.N)#, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=15)
    #cbar.ax.set_yticklabels(np.arange(1,int(np.amax(C))+1))
    cbar.set_label('Average N$_{sat}$',fontsize=25)
    cbar.set_ticks(np.arange(0,8))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.5,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    ax.grid(True,which='major',color='k',linewidth=2)
    f.savefig(f'{path}VirialMassVsEnvironmentVsAverageSatelliteCount.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/VirialMassVsEnvironmentVsAverageSatelliteCount.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def VirialMassVsNeighborEnvironmentVsAverageSatelliteCount(host,rest,rad,over,path=''):
    y = np.arange(10.8,12.8,.2)
    x = np.arange(0,10,2)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mvir']) > y[r] and x[c+1] > host[h]['Closest'][0]/1000 > x[c]:
                    d.append(len(host[h]['Satellites']))
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(10,3.5))
    ax.set_xlabel(r'Log(M$_{vir}$/M$_{\odot}$)',fontsize=25)
    ax.set_ylabel(r'D$_{10}$ [Mpc]',fontsize=25)
    ax.tick_params(which='major',labelsize=15, length=5)
    #norm = plt.Normalize(-1,int(np.amax(C))+1)
    norm = mpl.colors.BoundaryNorm(np.arange(-.5,9.5), mpl.cm.viridis.N)#, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=15)
    #cbar.ax.set_yticklabels(np.arange(1,int(np.amax(C))+1))
    cbar.set_label('Average N$_{sat}$',fontsize=25)
    cbar.set_ticks(np.arange(0,15))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.5,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    ax.grid(True,which='major',color='k',linewidth=2)
    f.savefig(f'{path}VirialMassVsNeighborEnvironmentVsAverageSatelliteCount.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/VirialMassVsNeighborEnvironmentVsAverageSatelliteCount.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def VirialMassVsEnvironmentalDensityVsAverageSatelliteCount(host,rest,rad,over,path=''):
    y = np.arange(10.2,12.8,.2)
    x = np.arange(-.5,8.5,1)
    C = np.zeros((len(x),len(y)))
    N = np.zeros((len(x),len(y)))
    SD = np.zeros((len(x),len(y)))
    r = 0
    while r < len(y)-1:
        c = 0
        while c < len(x)-1:
            d = []
            for h in host:
                if y[r+1] > np.log10(host[h]['Mvir']) > y[r] and x[c+1] > host[h]['EnvDen'] > x[c]:
                    d.append(len(host[h]['Satellites']))
            if len(d) > 0:
                C[c][r] = np.mean(d)
                SD[c][r] = np.std(d)
            else:
                C[c][r]=-1
            N[c][r] = len(d)
            c += 1
        r += 1
    f,ax = plt.subplots(1,1,figsize=(12,6))
    ax.set_xlabel(r'Log(M$_{vir}$/M$_{\odot}$)',fontsize=35)
    ax.set_ylabel(r'N$_L(<$1 Mpc)',fontsize=35)
    ax.tick_params(which='major',labelsize=20, length=5)
    #norm = plt.Normalize(-1,int(np.amax(C))+1)
    norm = mpl.colors.BoundaryNorm(np.arange(-.5,10.5), mpl.cm.viridis.N)#, extend='min')
    C = np.ma.masked_where(C < 0, C)
    cmap = mpl.cm.get_cmap('viridis')#.copy()
    cmap.set_bad(color='k')
    c = ax.pcolormesh(y,x,C,cmap=cmap,norm=norm,alpha=.5)
    cbar = f.colorbar(c,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.ax.tick_params(labelsize=20)
    #cbar.ax.set_yticklabels(np.arange(1,int(np.amax(C))+1))
    cbar.set_label('Average N$_{sat}$',fontsize=35)
    cbar.set_ticks(np.arange(0,10))
    Size = True
    if Size:
        r = 0
        while r < len(y)-1:
            c = 0
            while c < len(x)-1:
                a = (x[c+1]+x[c])/2
                b = (y[r+1]+y[r])/2
                if C[c][r] > -1:
                    ax.text(b-.086,a-.35,'N: '+str(int(N[c][r]))+'\n'+r'$\sigma$: '+str(round(SD[c][r],2)),fontsize=15)
                c +=1
            r +=1
    ax.set_xticks(y)
    for i in y:
        ax.axvline(i,c='k',linewidth=2)
    for i in x:
        ax.plot([min(y),max(y)],[i,i],c='k',linewidth=2)
    f.savefig(f'{path}VirialMassVsEnvironmentalDensityVsAverageSatelliteCount.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/VirialMassVsEnvironmentalDensityVsAverageSatelliteCount.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def NsatVsLargestSatelliteMass(host,sats,rest,rad,over,path=''):
    Nsat,Mstar = [],[]
    for mw in host:
        if len(host[mw]['Satellites'])>0:
            Nsat.append(len(host[mw]['Satellites']))
            mass = 0
            for sat in host[mw]['Satellites']:
                if sats[sat]['Mstar']>mass: mass = sats[sat]['Mstar']
            Mstar.append(np.log10(mass))
    
    f,ax = plt.subplots(1,1)
    ax.set_xlabel(r'Log(M$_*$/M$_\odot$) of Largest Satellite',fontsize=20)
    ax.set_ylabel(r'N$_{sat}$',fontsize=20)
    ax.tick_params(labelsize=15)
    ax.set_xlim([7,11])
    ax.set_ylim([0,14])
    ax.scatter(Mstar,Nsat,c='k')
    f.savefig(f'{path}NsatVsLargestSatelliteMass.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/NsatVsLargestSatelliteMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def NsatVsLargestSatelliteMagnitude(host,sats,rest,rad,over,path=''):
    Nsat,Mag = [],[]
    for mw in host:
        if len(host[mw]['Satellites'])>0:
            Nsat.append(len(host[mw]['Satellites']))
            mag = 0
            for sat in host[mw]['Satellites']:
                if sats[sat]['Kmag']<mag: mag = sats[sat]['Kmag']
            Mag.append(mag)
    
    f,ax = plt.subplots(1,1)
    ax.set_xlabel(r'M$_K$ of Largest Satellite',fontsize=20)
    ax.set_ylabel(r'N$_{sat}$',fontsize=20)
    ax.tick_params(labelsize=15)
    #ax.set_xlim([7,11])
    ax.set_ylim([0,14])
    ax.scatter(Mag,Nsat,c='k')
    f.savefig(f'{path}NsatVsLargestSatelliteMagnitude.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/NsatVsLargestSatelliteMass.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def SAGAQuenchComparison(host,sats,rest,rad,over,path=''):
    #Log(M*/Msun) = 1.254 + 1.098(g-r)_0 - 0.4M_(r,0)

    with open('DataFiles/AdditionalData/SAGA_Hosts.csv') as f:
        SagaHost = f.readlines()
        del SagaHost[0]
    with open('DataFiles/AdditionalData/SAGA_Satellites.csv') as f:
        SagaSats = f.readlines()
        del SagaSats[0]
    
    SagaMk,SagaQf,SagaMksub,SagaQfsub = [],[],[],[]
    for l in SagaHost:
        line = l.split(',')
        t,q,ts,qs=0,0,0,0
        for s in SagaSats:
            sline = s.split(',')
            if sline[0]==line[0]:
                t+=1
                if sline[11]=='N': q+=1
                if float(sline[10])>8:
                    ts+=1
                    if sline[11]=='N': qs+=1
        if t>0:
            SagaMk.append(float(line[6]))
            SagaQf.append(q/t)
        if ts>0:
            SagaMksub.append(float(line[6]))
            SagaQfsub.append(qs/ts)
    
    with open(f'DataFiles/Satellite.{rest}.{rad}.{over}.BlackHoles.txt') as f:
        bhs = f.readlines()
        bhs = [int(x) for x in bhs]
    mk,qf,mknobh,qfnobh = [],[],[],[]
    for mw in host:
        t,q,tb,qb = 0,0,0,0
        for sat in host[mw]['Satellites']:
            t+=1
            if sats[sat]['Quenched']: q+=1
            if not int(sat) in bhs:
                tb+=1
                if sats[sat]['Quenched']: qb+=1
        if t>0:
            mk.append(host[mw]['Kmag'])
            qf.append(q/t)
        if tb>0:
            mknobh.append(host[mw]['Kmag'])
            qfnobh.append(qb/tb)
    
    f,ax=plt.subplots(1,1,figsize=(8,4.8))
    ax.set_xlim([-21.5,-25.5])
    ax.set_ylim([-.15,1.05])
    ax.set_xlabel(f'M$_K$',fontsize=20)
    ax.set_ylabel(f'f$_q$',fontsize=20)
    ax.tick_params(labelsize=15)
    ax.scatter(SagaMk,SagaQf,c='darkturquoise',label='SAGA II (full)')
    ax.scatter(SagaMksub,SagaQfsub,c='royalblue',label=r'SAGA II ($>10^8$M$_\odot$)')
    ax.scatter(mk,qf,c='k',label='Rom25')
    #ax.scatter(mknobh,qfnobh,c='.5',label='Rom25 (no BH)')
    ax.legend(loc='lower left',prop={'size':12.25})#,ncol=4)
    f.savefig(f'{path}SAGAQuenchComparison.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGAQuenchComparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

    bins = np.arange(-25.5,-21,.5)
    mkb,qfb,qfnb,sqfb,sqfsb=[],[],[],[],[]
    qfbe,qfnbe,sqfbe,sqfsbe=[],[],[],[]
    for i in np.arange(len(bins)-1):
        qfc,qfnc,sqfc,sqfsc=[],[],[],[]
        for m in mk:
            if bins[i]<m<bins[i+1]:
                qfc.append(qf[mk.index(m)])
        for m in mknobh:
            if bins[i]<m<bins[i+1]:
                qfnc.append(qfnobh[mknobh.index(m)])
        for m in SagaMk:
            if bins[i]<m<bins[i+1]:
                sqfc.append(SagaQf[SagaMk.index(m)])
        for m in SagaMksub:
            if bins[i]<m<bins[i+1]:
                sqfsc.append(SagaQfsub[SagaMksub.index(m)])
        mkb.append((bins[i]+bins[i+1])/2)
        qfb.append(np.mean(qfc))
        qfbe.append(np.std(qfc)/np.sqrt(len(qfc)))
        qfnb.append(np.mean(qfnc))
        qfnbe.append(np.std(qfnc)/np.sqrt(len(qfnc)))
        sqfb.append(np.mean(sqfc))
        sqfbe.append(np.std(sqfc)/np.sqrt(len(sqfc)))
        sqfsb.append(np.mean(sqfsc))
        sqfsbe.append(np.std(sqfsc)/np.sqrt(len(sqfsc)))
    
    #with open('DataFiles/AdditionalData/ELVES_Quenching.csv') as f:
    #    L = f.readlines()
    #    del L[:2]
    #ex,ey,eux,euy,elx,ely = [np.zeros(len(L)),np.zeros(len(L)),np.zeros(len(L)),
    #                         np.zeros(len(L)),np.zeros(len(L)),np.zeros(len(L))]
    #for i in np.arange(len(L)):
    #    ex[i],ey[i],eux[i],euy[i],elx[i],ely[i] = L[i].split(',')
    ##x,y,low_e,upp_e from ELVES
    #MW = (-24.132,.6,.384,.781)
    #M31 = (-24.893,.888,.744,.953)

    EH = pickle.load(open('DataFiles/AdditionalData/ELVES_Hosts.pickle','rb'))
    ES = pickle.load(open('DataFiles/AdditionalData/ELVES_Satellites.pickle','rb'))
    el,el_er,els,els_er = [],[],[],[]

    for i in np.arange(len(bins)-1):
        ec,ecs = [],[]
        for m in EH:
            if bins[i]<EH[m]['Kmag']<bins[i+1]:
                t,q,ts,qs = 0,0,0,0
                for s in EH[m]['Satellites']:
                    if 6.75<ES[s]['Mstar']<9.5:
                        t+=ES[s]['Likelihood']
                        if ES[s]['Quenched']: q+=ES[s]['Likelihood']
                    if ES[s]['Mstar']>8:# and ES[s]['Orbit']<150:
                        ts+=ES[s]['Likelihood']
                        if ES[s]['Quenched']: qs+=ES[s]['Likelihood']
                if t>0:
                    ec.append(q/t)
                if ts>0:
                    ecs.append(qs/ts)
        el.append(np.mean(ec))
        el_er.append(np.std(ec)/np.sqrt(len(ec)))
        els.append(np.mean(ecs))
        els_er.append(np.std(ecs)/np.sqrt(len(ecs)))


    f,ax=plt.subplots(1,1,figsize=(8,4.8))
    ax.set_xlim([-23,-25])
    ax.set_ylim([-.3,1.05])
    ax.set_yticks([0,.2,.4,.6,.8,1])
    ax.set_xticks(np.arange(-25,-22.9,.5))
    ax.set_xlabel(f'M$_K$',fontsize=25)
    ax.set_ylabel(f'f$_q$',fontsize=25)
    ax.tick_params(labelsize=18)
    ax.plot([-23,-25],[0,0],c='0.5',linestyle=':')
    ax.plot([-23,-25],[1,1],c='0.5',linestyle=':')
    #ax.fill_between(ex,ely,euy,color='#cb9999',alpha=.3)
    #ax.plot(ex,ey,c='#800000',label='ELVES')
    ax.errorbar(mkb,el,yerr=el_er,capsize=4,c='#800000',zorder=0)
    ax.plot(mkb,el,marker='o',c='#800000',label='ELVES (full)')
    ax.errorbar(mkb,els,yerr=els_er,capsize=4,c='#cb9999',zorder=0)
    ax.plot(mkb,els,marker='o',c='#cb9999',label='ELVES ($>10^8$M$_\odot$)')
    ax.errorbar(mkb,sqfb,yerr=sqfbe,capsize=4,c='g',zorder=0)
    ax.plot(mkb,sqfb,marker='o',c='g',label='SAGA II (full)')
    ax.errorbar(mkb,sqfsb,yerr=sqfsbe,capsize=4,c='yellowgreen',zorder=0)
    ax.plot(mkb,sqfsb,marker='o',c='yellowgreen',label=r'SAGA II ($>10^8$M$_\odot$)')
    ax.errorbar(mkb,qfb,yerr=qfbe,capsize=4,c='k',zorder=0)
    ax.plot(mkb,qfb,marker='o',c='k',label='Rom25')
    #ax.errorbar(MW[0],MW[1],yerr=[[MW[1]-MW[2]],[MW[3]-MW[1]]],capsize=4,c='#800080')
    #ax.scatter(MW[0],MW[1],c='#800080',marker='*',s=9**2,label='Milky Way')
    #ax.errorbar(M31[0],M31[1],yerr=[[M31[1]-M31[2]],[M31[3]-M31[1]]],capsize=4,c='#ffa500')
    #ax.scatter(M31[0],M31[1],c='#ffa500',marker='*',s=9**2,label='M31')
    #ax.plot(mkb,qfnb,marker='o',c='.5',label='Rom25 (no BH)')
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [0,1,2,3,4]
    ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='lower left',prop={'size':13.1},ncol=3)
    f.savefig(f'{path}SAGABinnedQuenchComparison.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGABinnedQuenchComparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

    #Only plot >1e8 subsets
    f=plt.figure(figsize=(8,4.5))
    ax1 = f.add_subplot(111)
    ax1.set_xlim([-23,-25])
    ax2 = ax1.twiny()
    def ms(mk):
        return(-0.36815865*mk+1.65875324) #polyfit from 2.sim.Yov MW sample
    ax2.set_xlim([ms(-23),ms(-25)])
    #ax2.set_xticks([10.2,10.4,10.6,10.8])
    ax1.set_ylim([-.2,1.05])
    ax1.set_yticks([0,.2,.4,.6,.8,1])
    ax1.set_xticks(np.arange(-25,-22.9,.5))
    ax1.set_xlabel(f'M$_K$',fontsize=25)
    ax1.set_ylabel(f'f$_q$',fontsize=25)
    ax2.set_xlabel(r'Approximate Log(M$_*$/M$_\odot$)',fontsize=25)
    ax1.tick_params(labelsize=18,length=8)
    ax2.tick_params(labelsize=18,direction='in',length=8)
    ax1.plot([-23,-25],[0,0],c='0.5',linestyle=':')
    ax1.plot([-23,-25],[1,1],c='0.5',linestyle=':')
    ax1.errorbar(mkb,els,yerr=els_er,capsize=4,c='sandybrown',zorder=0)
    ax1.plot(mkb,els,marker='o',c='sandybrown',label='ELVES')
    ax1.errorbar(mkb,sqfsb,yerr=sqfsbe,capsize=4,c='olivedrab',zorder=0)
    ax1.plot(mkb,sqfsb,marker='o',c='olivedrab',label=r'SAGA II')
    ax1.errorbar(mkb,qfb,yerr=qfbe,capsize=4,c='k',zorder=0)
    ax1.plot(mkb,qfb,marker='o',c='k',label='Romulus25')
    #handles, labels = plt.gca().get_legend_handles_labels()
    #order = [2,0,1]
    #ax1.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='lower left',prop={'size':15},ncol=3)
    ax1.legend(loc='lower left', prop={'size':15}, ncol=3)
    f.savefig(f'{path}SAGABinnedQuenchComparison.Subsets.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGABinnedQuenchComparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

def SAGAMassComparison(host,sats,rest,rad,over,path=''):
    mk,mks,mke,sv,svs,sve=[],[],[],[],[],[]
    #mkt,mkst,mket,svt,svst,svet=0,0,0,0,0,0

    for mw in host:
        mk.append(host[mw]['Kmag'])
    for sat in sats:
        sv.append(sats[sat]['Vmag'])
    
    EH = pickle.load(open('DataFiles/AdditionalData/ELVES_Hosts.pickle','rb'))
    ES = pickle.load(open('DataFiles/AdditionalData/ELVES_Satellites.pickle','rb'))
    for mw in EH:
        mke.append(EH[mw]['Kmag'])
    for sat in ES:
        sve.append(ES[sat]['Vmag'])
    
    with open('DataFiles/AdditionalData/SAGA_Hosts.csv') as f:
        SagaHost = f.readlines()
        del SagaHost[0]
    with open('DataFiles/AdditionalData/SAGA_Satellites.csv') as f:
        SagaSats = f.readlines()
        del SagaSats[0]
    for line in SagaHost:
        mks.append(float(line.split(',')[6]))
    for line in SagaSats:
        svs.append(float(line.split(',')[7])+.2)

    kbins = np.linspace(-25.5,-21.5,21)
    vbins = np.linspace(-22,-8,21)
    f,ax=plt.subplots(1,2,figsize=(9,3))
    plt.subplots_adjust(wspace=0)
    ax[0].set_yticks([])
    ax[1].set_yticks([])
    ax[0].set_xlim([-21.5,-25.5])
    ax[1].set_xlim([-8,-22])
    #ax[0].set_ylim([0,1.05])
    #ax[1].set_ylim([0,1.05])
    ax[0].tick_params(labelsize=15)
    ax[1].tick_params(labelsize=15)
    ax[0].set_xlabel(r'M$_K$',fontsize=23)
    ax[1].set_xlabel(r'M$_V$',fontsize=23)
    ax[0].set_ylabel('Normalized Counts',fontsize=23)
    ax[0].set_title('Hosts',fontsize=23)
    ax[1].set_title('Satellites',fontsize=23)

    ax[0].hist(mk,kbins,color='k',label='Romulus25',histtype='step',density=True,linewidth=2)
    ax[0].hist(mke,kbins,color='sandybrown',label='ELVES',histtype='step',density=True,linewidth=2)
    ax[0].hist(mks,kbins,color='olivedrab',label='SAGA II',histtype='step',density=True,linewidth=2)
    ax[0].legend(loc='upper left',prop={'size':12})

    ax[1].hist(sv,vbins,color='k',histtype='step',density=True,linewidth=2)
    ax[1].hist(sve,vbins,color='sandybrown',histtype='step',density=True,linewidth=2)
    ax[1].hist(svs,vbins,color='olivedrab',histtype='step',density=True,linewidth=2)

    f.savefig(f'{path}SAGAMassComparison.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGAMassComparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(6.4,3.8))
    ax.set_yticks([])
    ax.set_xlim([-21.5,-25.5])
    ax.set_xlabel(r'M$_K$',fontsize=20)
    ax.set_ylabel('Normalized Counts',fontsize=20)
    ax.tick_params(labelsize=15)

    ax.hist(mk,kbins,color='k',label='Romulus25',histtype='step',density=True,linewidth=2)
    ax.hist(mke,kbins,color='sandybrown',label='ELVES',histtype='step',density=True,linewidth=2)
    ax.hist(mks,kbins,color='olivedrab',label='SAGA II',histtype='step',density=True,linewidth=2)
    ax.legend(loc='upper left',prop={'size':15})

    f.savefig(f'{path}SAGAMassComparison.Hosts.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGAMassComparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(6.4,3.8))
    ax.set_yticks([])
    ax.set_xlim([-8,-22])
    ax.set_xlabel(r'M$_V$',fontsize=20)
    ax.set_ylabel('Normalized Counts',fontsize=20)
    ax.tick_params(labelsize=15)

    ax.hist(sv,vbins,color='k',label='Romulus25',histtype='step',density=True,linewidth=2)
    ax.hist(sve,vbins,color='sandybrown',label='ELVES',histtype='step',density=True,linewidth=2)
    ax.hist(svs,vbins,color='olivedrab',label='SAGA II',histtype='step',density=True,linewidth=2)
    #ax.legend(loc='upper left',prop={'size':12})

    f.savefig(f'{path}SAGAMassComparison.Satellites.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGAMassComparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()

    sve = np.array(sve)
    svs = np.array(svs)

    f,ax = plt.subplots(1,1,figsize=(6.4,3.8))
    ax.set_yticks([])
    ax.set_xlim([-8,-22])
    ax.set_xlabel(r'M$_V$',fontsize=20)
    ax.set_ylabel('Normalized Counts',fontsize=20)
    ax.tick_params(labelsize=15)

    ax.hist(sv,vbins,color='k',label='Romulus25',histtype='step',density=True,linewidth=2)
    ax.hist(sve[sve<-12.6],vbins,color='sandybrown',label='ELVES',histtype='step',density=True,linewidth=2)
    ax.hist(svs[svs<-12.6],vbins,color='olivedrab',label='SAGA II',histtype='step',density=True,linewidth=2)
    #ax.legend(loc='upper left',prop={'size':12})

    f.savefig(f'{path}SAGAMassComparison.Satellites.Subset.{rest}.{rad}.{over}.png',bbox_inches='tight',pad_inches=.1)
    #f.savefig(f'{path}pdf/SAGAMassComparison.'+rest+'.'+rad+'.'+over+'.pdf',bbox_inches='tight',pad_inches=.1)
    plt.close()