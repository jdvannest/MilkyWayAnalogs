import pickle, sys, argparse, os, datetime, warnings, pynbody, pymp
import numpy as np 
from scipy.optimize import curve_fit
warnings.filterwarnings("ignore")
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)
def sersic(r, mueff, reff, n):
    return mueff + 2.5*(0.868*n-0.142)*((r/reff)**(1./n) - 1)

datafilepath = "../DataFiles/"
outputpath = ""

defs = ['1','2','3','4']
rads = ['sim','300']

halo_ids = []

for d in defs:
    for r in rads:
        mw = pickle.load(open(f'{datafilepath}MilkyWay.{d}.{r}.pickle','rb'))
        sat = pickle.load(open(f'{datafilepath}Satellite.{d}.{r}.pickle','rb'))
        for haloid in mw:
            if int(haloid) not in halo_ids:
                halo_ids.append(int(haloid))
        for haloid in sat:
            if int(haloid) not in halo_ids:
                halo_ids.append(int(haloid))
halo_ids.sort()
print('Halo list generated')


print('Loading Rom25')
s = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192')
s.physical_units()
h = s.halos(dosort=True)
myprint('Rom25 Loaded',clear=True)


print('Writing: 0.00%')
Data=pymp.shared.dict()
progress = pymp.shared.array((1,),dtype=int)
with pymp.Parallel(10) as pl:
    for i in pl.xrange(len(halo_ids)):
        current = {'rbins':[],'sb,r':[],'par':[np.nan,np.nan,np.nan]}
        halo = h.load_copy(halo_ids[i])
        halo.physical_units()
        profile = False
        try:
            pynbody.analysis.angmom.faceon(halo)
            R = pynbody.analysis.halo.virial_radius(halo,overden=200)
            p = pynbody.analysis.profile.Profile(halo.s,type='lin',min=0,max=R,ndim=2,nbins=int(R/0.1))
            current['rbins'] = p['rbins']
            current['sb,r'] = p['sb,r']
            raw = p['sb,r']
            profile = True
        except:
            profile = False
        if profile:
            try:
                smooth = np.nanmean(np.pad(raw.astype(float),(0,3-raw.size%3),mode='constant',constant_values=np.nan).reshape(-1,3),axis=1)
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
                par,ign = curve_fit(sersic,x,y,p0=(m0,r0,1))#,bounds=([10,0,0.5],[40,100,16.5]))
                current['par'] = par
            except:
                err=1
        with pl.lock:
            progress[0]+=1
            Data[str(halo_ids[i])] = current
            del current
            myprint(f'Writing: {round(float(progress[0])/len(halo_ids)*100,2)}%',clear=True) 

Data_out = {}
for h in halo_ids:
    Data_out[str(h)] = Data[str(h)]
out = open(f'{outputpath}SersicFits.pickle','wb')
pickle.dump(Data_out,out)
out.close()
myprint('DataFile written',clear=True)