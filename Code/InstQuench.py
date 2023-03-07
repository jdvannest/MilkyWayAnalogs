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
Data = {}
Old = {}
halos = []
for f in [(i,j,k) for i in [1,2,3,4,5,6,7] for j in ['sim','300'] for k in ['Yov','Nov']]:
    sats = pickle.load(open(f'../DataFiles/Satellite.{f[0]}.{f[1]}.{f[2]}.pickle','rb'))
    for s in sats:
        if int(s) not in halos: 
            halos.append(int(s))
            Data[str(s)] = {}
            Data[str(s)]['Mstar'] = sats[s]['Mstar']
            Old[str(s)] = sats[s]['Quenched']
halos.sort()
print(f'{len(halos)} halos to analyze')

s = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192')
s.physical_units()
h = s.halos(dosort=True)

print(f'\tWriting Quench Data: 0.00%')
prog = 0
for hid in halos:
    current = {}
    halo = h.load_copy(hid)
    sfr,ix = calc_inst_sf(halo)
    current['SFR'] = sfr
    try:
        current['Quenched'] = True if sfr.sum()/Data[str(hid)]['Mstar']<1e-11 else False
    except:
        current['Quenched'] = Old[str(hid)]
    Data[str(hid)] = current
    prog+=1
    myprint(f'\tWriting Quench Data: {round(prog/len(halos)*100,2)}%',clear=True)


pickle.dump(Data,open('../DataFiles/InstantaneousQuenching.pickle','wb'))
pickle.dump(Old,open('../DataFiles/250MyrQuenching.pickle','wb'))
