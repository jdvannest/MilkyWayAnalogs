import os,pickle,pymp,pynbody,sys,warnings
import numpy as np
from scipy.optimize import curve_fit as cf 
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)
def sersic(r, mueff, reff, n):
    return mueff + 2.5*(0.868*n-0.142)*((r/reff)**(1./n) - 1)
warnings.filterwarnings("ignore")

halos = []
for f in [(i,j,k) for i in [1,2,3,4,5,6,7] for j in ['sim','300'] for k in ['Yov','Nov']]:
    sats = pickle.load(open(f'../DataFiles/Satellite.{f[0]}.{f[1]}.{f[2]}.pickle','rb'))
    hosts = pickle.load(open(f'../DataFiles/MilkyWay.{f[0]}.{f[1]}.{f[2]}.pickle','rb'))
    for s in sats:
        if int(s) not in halos: 
            halos.append(int(s))
    for h in hosts:
        if int(h) not in halos:
            halos.append(int(h))
halos.sort()
print(f'{len(halos)} halos to analyze')

print('Loading Simulation...')
s = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192')
s.physical_units()
h = s.halos(dosort=True)
os.environ['TANGOS_DB_CONNECTION'] = '/nobackupp2/jvannest/DATABASE/data_romulus25.working.db'
import tangos
rom = tangos.get_simulation('cosmo25')
hnum, cen, rad = rom[-1].calculate_all('halo_number()','shrink_center','max_radius')
myprint('Simulation Loaded',clear=True)

SBData = pymp.shared.dict()
prog=pymp.shared.array((1,),dtype=int)
print(f'\tWriting SB Profiles: {round(prog[0]/len(halos)*100,2)}%')
with pymp.Parallel(10) as pl:
    for i in pl.xrange(len(halos)):
        current = {}
        hid = halos[i]
        halo = h[hid]
        pynbody.analysis.angmom.faceon(halo)
        R = rad[np.where(hnum==hid)[0][0]]
        p = pynbody.analysis.profile.Profile(halo.s,type='lin',min=0,max=R,ndim=2,nbins=int(R/0.1))
        for band in ['b','v','r']:
            current[f'sb,{band}'] = p[f'sb,{band}']
            current['rbins'] = p['rbins']
            r,rbins = p[f'sb,{band}'],p['rbins']
            smooth = np.nanmean(np.pad(r.astype(float),(0,3-r.size%3),mode='constant',constant_values=np.nan).reshape(-1,3),axis=1)
            try:
                y = smooth[:np.where(smooth>32)[0][0]+1]
            except:
                y = smooth
            x = np.arange(len(y))*0.3 + 0.15
            x[0] = 0.05
            if True in np.isnan(y):
                x = np.delete(x,np.where(np.isnan(y)==True))
                y = np.delete(y,np.where(np.isnan(y)==True))
            r0 = x[int(len(x)/2)]
            m0 = np.mean(y[:3])
            try:
                par,ign = cf(sersic,x,y,p0=(m0,r0,1),bounds=([10,0,0.5],[40,100,16.5]))
                current[f'Mueff,{band}'] = par[0]
            except:
                current[f'Mueff,{band}'] = np.NaN
        SBData[str(hid)] = current
        prog[0]+=1
        myprint(f'\tWriting SB Profiles: {round(prog[0]/len(halos)*100,2)}%',clear=True)

Data = {}
for hid in SBData:
    Data[hid] = SBData[hid]
pickle.dump(Data,open('../DataFiles/SBProfiles.pickle','wb'))