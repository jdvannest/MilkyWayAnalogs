import os,pymp,pynbody,pickle,sys
import numpy as np
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

def calc_dynamical_time(rho):
    #Author: Ray Sharma
    """Calculates dynamical time given gas particle density
    Args:
        rho (float): Gas particle density
    Returns:
        tdyn (pynbody.array.SimArray): Dynamical time in seconds
    """
    tdyn = 1.0 / np.sqrt(rho * 4.0 * np.pi * pynbody.units.G)
    return tdyn.in_units("s")

def calc_inst_sf(halo, temp_cut=1e4, density_cut=0.2, c_star=0.15):
    #Author: Ray Sharma
    """Calculate instantaneous star formation rates based on Dickey+(2020). Finds SFR from star-forming gas.
    Args:
        h (pynbody.halo): Pynbody halo object
    Returns:
        instsf (float): Instantaneous star formation rate
    """

    # Read in files
    ngas = len(halo.g)
    instsf = np.zeros(ngas)
    sfeff = np.zeros(ngas)

    if ngas == 0:
        return instsf, np.array([])

    gas_temp = halo.g["temp"].in_units("K")
    gas_mass = halo.g["mass"].in_units("Msol")
    gas_metallicity = halo.g["metals"]
    gas_density = halo.g["rho"].in_units("m_p cm**-3")

    delta_t = pynbody.array.SimArray(1e6*3.15569*1e7)
    delta_t.units = "s"

    tdyn = calc_dynamical_time(gas_density)

    ix_sf = (gas_temp <= temp_cut) & (halo.g["rho"].in_units("m_p cm**-3") >= density_cut)  # Star forming gas conditions

    if ix_sf.sum() == 0:
        return instsf, np.array([])

    '''mean_Z = np.average(
        gas_metallicity[ix_sf], weights=gas_mass[ix_sf]
    )  # Mass-weighted mean metallicity of star-forming gas
    ix_Z = np.isclose(
        gas_metallicity, mean_Z, rtol=1e-2, atol=1e-5
    )  # Gas with metallicity near star-forming gas'''

    sfeff[ix_sf] = 1.0 - np.exp(-1.0 * c_star * delta_t / tdyn[ix_sf])
    instsf[ix_sf] = gas_mass[ix_sf] * sfeff[ix_sf]
    return instsf, ix_sf

#Load in all halos to be analyzed
halos,Mstar = [],{}
for f in [(i,j,k) for i in [1,2,3,4,5,6,7] for j in ['sim','300'] for k in ['Yov','Nov']]:
    hosts = pickle.load(open(f'../DataFiles/MilkyWay.{f[0]}.{f[1]}.{f[2]}.pickle','rb'))
    for mw in hosts:
        if int(mw) not in halos: 
            halos.append(int(mw))
            Mstar[str(mw)] = hosts[mw]['Mstar']
halos.sort()
print(f'{len(halos)} halos to analyze')

s = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192')
s.physical_units()
h = s.halos(dosort=True)

Data = pymp.shared.dict()
print(f'\tWriting SFR Data: 0.00%')
prog=pymp.shared.array((1,),dtype=int)
with pymp.Parallel(10) as pl:
    for i in pl.xrange(len(halos)):
        current,hid = {},halos[i]
        halo = h.load_copy(hid)
        sfr,ix = calc_inst_sf(halo)
        #current['SFR_array'] = sfr <--- Makes file too large for github
        current['SFR'] = sfr.sum()/1e6
        current['sSFR'] = (sfr.sum()/1e6)/Mstar[str(hid)]
        current['Mstar'] = Mstar[str(hid)]
        Data[str(hid)] = current
        prog[0]+=1
        myprint(f'\tWriting SFR Data: {round(prog[0]/len(halos)*100,2)}%',clear=True)

Out = {}
for hid in Data:
    Out[hid] = Data[hid]
pickle.dump(Out,open('../DataFiles/HostSFR.pickle','wb'))
