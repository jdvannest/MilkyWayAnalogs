#Code written by Jordan Van Nest, 08/2020
import pickle, sys, argparse, os
import numpy as np 

parser = argparse.ArgumentParser(description="Searches Romulus25 for Milky Way Analogs"
                                +" and identifies their Satellite halos."+
                                " Outputs pickle files in run directory.", 
                                usage="SAGA_Data.py -d 1 -r sim")
parser.add_argument("-d", "--definition", help="Definition for Milky Way Analog\n"+
                                                "1: By General Virial Mass Restricition\n"+
                                                "2: By Stellar Mass Restriction from K-band Magnitude\n"+
                                                "3: Method 2 + Environmental Restrictions (SAGAI)\n"+
                                                "4: Method 2 + Environmental Restrictions (SAGAII)\n"+
                                                "5,6,7: 2,3,4 but with explicit K-band Mag",
                                                choices=['1','2','3','4','5','6','7'],required=True)
parser.add_argument("-r", "--radius", help="Radius for definition satellites\n"+
                                            "sim: The true virial radii from the simulations\n"+
                                            "300: The SAGA value of 300 kpc",
                                            choices=['sim','300'],required=True)
parser.add_argument("-o", "--overlapping", help="Include Overlapping Analogs",
                                           action='store_true')
args = parser.parse_args()

#Define output variables
output_path="DataFiles/"
overlap = 'Yov' if args.overlapping else 'Nov'

#This function clears the previous line printed in the terminal before printing
#when the 'clear' flag is set to True
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

def gband(b,v):
    return(v + 0.6*(b-v) - 0.12)

#The wrap function accounts for the simulation's periodic boundary conditions
#when considiering distances between objects
def wrap(relpos,scale=1,boxsize=25e3):
#author: Michael Tremmel
#scale = 1/1+z
    bphys = boxsize*scale
    bad = np.where(np.abs(relpos) > bphys/2.)
    if type(bphys) == np.ndarray:
        relpos[bad] = -1.0*(relpos[bad]/np.abs(relpos[bad]))*np.abs(bphys[bad]-np.abs(relpos[bad]))
    else:
        relpos[bad] = -1.0*(relpos[bad]/np.abs(relpos[bad]))*np.abs(bphys-np.abs(relpos[bad]))
    return

#Load in Romulus25 and the desired halo properties
print('Loading Database...')
os.environ['TANGOS_DB_CONNECTION'] = '/myhome2/users/munshi/Romulus/data_romulus25.working.db'
import tangos
rom = tangos.get_simulation('cosmo25')
hnum, cen, mvir, rvir, vmag, rmag, kmag, bmag, mstar, csfh, sfr = rom[-1].calculate_all(
                                'halo_number()','shrink_center','Mvir','max_radius',
                                'AB_V','AB_R','AB_K','AB_B','Mstar','CumSFH','SFR_encl_250Myr')
myprint('Database Loaded',clear=True)

#Apply photometric correction to stellar mass
mstar = mstar*.5
#Convert Magnitudes from AB to Vega: https://www.astronomy.ohio-state.edu/martini.10/usefuldata.html
vmag = vmag - 0.02
rmag = rmag - 0.21
kmag = kmag - 1.85
bmag = bmag + 0.09

#Initialize Data output Dictionaries and LogFile
MilkyWays = {} 
Satellites = {} 
LargeHalos = {} 
TextLog = ['Initial Milky Way Sample:\n']

#Find Large Halos (Mvir > 5e11)
print('Searching for Large Halos...')
for i in np.arange(len(hnum)):
    if mvir[i] > 5e11:
        LargeHalos[str(hnum[i])] = {}
        LargeHalos[str(hnum[i])]['center'] = cen[i]
        LargeHalos[str(hnum[i])]['Mvir'] = mvir[i]
        LargeHalos[str(hnum[i])]['Mstar'] = mstar[i]
myprint(f'{len(LargeHalos)} Large Halos Found',clear=True)

#Find Milky Way Analogs
print('Searching for Milky Way Analogs...')
if args.definition == '1':
    #previous (lb,ub) values: (1e11.5,1e12.5),(1e11,1e12.6),(5e11,3e12),(1e12,4e12)
    #                         1.08e12 +/- 15% from https://arxiv.org/abs/2111.09327   
    criteria,lower_bound,upper_bound,cname = mvir,10**11.5,10**12.5,'Mvir'
elif args.definition in ['2','3','4']:
    #previous (lb,ub) values: (10**10.2,10**10.9)
    criteria,lower_bound,upper_bound,cname = mstar,1e10,1e11,'Mstar'
else:
    criteria,lower_bound,upper_bound,cname = kmag,-24.6,-23,'Kmag'

original = []
for i in np.arange(len(hnum)):
    if lower_bound < criteria[i] < upper_bound:
        MilkyWays[str(hnum[i])] = {}
        MilkyWays[str(hnum[i])]['Mvir'] = mvir[i]
        MilkyWays[str(hnum[i])]['Mstar'] = mstar[i]
        MilkyWays[str(hnum[i])]['Rvir'] = rvir[i]
        MilkyWays[str(hnum[i])]['Vmag'] = vmag[i]
        MilkyWays[str(hnum[i])]['Rmag'] = rmag[i]
        MilkyWays[str(hnum[i])]['Kmag'] = kmag[i]
        MilkyWays[str(hnum[i])]['Bmag'] = bmag[i]
        MilkyWays[str(hnum[i])]['Gmag'] = gband(bmag[i],vmag[i])
        MilkyWays[str(hnum[i])]['center'] = cen[i]
        MilkyWays[str(hnum[i])]['CumSFH'] = csfh[i]
        MilkyWays[str(hnum[i])]['SFR_250Myr'] = sfr[i]
        MilkyWays[str(hnum[i])]['Satellites'] = [] #Empty array for indexes of satellites of this MW
        MilkyWays[str(hnum[i])]['EnvDen'] = 0 #Number of neighbors w/in 1Mpc where Mvir>1e11 Msol
        #MilkyWays[str(hnum[i])]['MvirPeak'] = max(rom[-1][int(hnum[i])].calculate_for_progenitors('Mvir')[0])
        original.append(str(hnum[i]))
myprint(f'{len(MilkyWays)} Milky Way Analogs Found',clear=True)

#Writie original list to Text Log
original.sort()
TextLog.append('\t'+', '.join(original)+'\n')
TextLog.append(f'\tTotal: {len(original)}\n')
TextLog.append('Removed Overlapping Pairs:\n')

#Remove any MW Analogs with overlapping Virial Radii if desired
if not args.overlapping:
    overlapping = []
    for mw1 in MilkyWays:
        for mw2 in MilkyWays:
            if not mw1 == mw2:
                distance = MilkyWays[mw1]['center'] - MilkyWays[mw2]['center']
                wrap(distance)
                if np.linalg.norm(distance) < ( (MilkyWays[mw1]['Rvir']+MilkyWays[mw1]['Rvir']) if args.radius=='sim' else 600):
                    if mw1 not in overlapping:
                        overlapping.append(mw1)
                    if mw2 not in overlapping:
                        overlapping.append(mw2)
                    TextLog.append(f'\t{mw1} - {mw2}\n')
    for mw in overlapping:
        del MilkyWays[mw]
    print(f'\t{len(overlapping)} Milky Ways removed due to overlapping Rvir')#: {overlapping}')
    TextLog.append(f'\tTotal: {len(overlapping)}\n')

#Apply environmental criteria if applicable
if args.definition in ['3','4','6','7']:
    TextLog.append('Removed due to K-Mag neighbor (MW - Neigbor):\n')
    # No K < K_MW+1 within 700kpc (from John W.) : SAGAI sec 2.2
    # No halo with K < K_MW-1.6 within 700kpc (from John W.) : SAGAII sec 2.1.2
    remove = []
    for mw in MilkyWays:
        for i in np.arange(len(hnum)):
            if not mw == str(hnum[i]):
                if kmag[i] < ( (MilkyWays[mw]['Kmag'] - 1.6) if args.definition in ['4','7'] else (MilkyWays[mw]['Kmag'] + 1) ):
                    distance = cen[i] - MilkyWays[mw]['center']
                    wrap(distance)
                    if np.linalg.norm(distance) < 700:
                        if mw not in remove:
                            remove.append(mw)
                            TextLog.append(f'\t{mw} - {hnum[i]}\n')
    for mw in remove:
        del MilkyWays[mw]
    print(f'\t{len(remove)} Milky Ways removed to due Kband Neigbor Restrictions')
    if args.definition in ['3','6']:
        TextLog.append('Removed due to massive neighbor (MW - Neigbor):\n')
        # No Mvir > 5*10^12 within 2 Rvir (Rvir of massive) : SAGAI sec 2.2
        MassiveHalos = {}
        for i in np.arange(len(hnum)):
            if mvir[i] > 5e12:
                MassiveHalos[str(hnum[i])] = {}
                MassiveHalos[str(hnum[i])]['center'] =  cen[i]
                MassiveHalos[str(hnum[i])]['Rvir'] =  rvir[i]
        remove = []
        for mw in MilkyWays:
            for mh in MassiveHalos:
                distance = MilkyWays[mw]['center'] - MassiveHalos[mh]['center']
                wrap(distance)
                if np.linalg.norm(distance) < (2*MassiveHalos[mh]['Rvir']):
                    if mw not in remove:
                        remove.append(mw)
                        TextLog.append(f'\t{mw} - {mh}\n')
        for mw in remove:
            del MilkyWays[mw]
        print(f'\t{len(remove)} Milky Ways removed to due Massive Neigbor Restrictions')

#Determine Final Milky Way Analog Count
print(f'{len(MilkyWays)} Milky Way Analogs Considered')

#Determine Closest MW+ and Satellites for Milky Way Analogs
print(f'Finding Satellite Halos...')
for mw in MilkyWays:
    rad = 300 if args.radius=='300' else MilkyWays[mw]['Rvir']
    mw_plus_id,mw_plus_dist,neighbors = [[],[],[]]
    for i in np.arange(len(hnum)):
        if mstar[i] < 1e7 or rmag[i] > -10.8 or str(hnum[i])==mw:
            pass #Outside Rom25 resolution limit or outside SAGA detection limit
        else:   #Satellite Halos
            distance = MilkyWays[mw]['center'] - cen[i]
            wrap(distance)
            #Check for satellite
            if np.linalg.norm(distance) < rad:
                if str(hnum[i]) not in Satellites:
                    Satellites[str(hnum[i])] = {}
                    Satellites[str(hnum[i])]['Mvir'] = mvir[i]
                    Satellites[str(hnum[i])]['Rvir'] = rvir[i]
                    Satellites[str(hnum[i])]['Vmag'] = vmag[i]
                    Satellites[str(hnum[i])]['Kmag'] = kmag[i]
                    Satellites[str(hnum[i])]['Bmag'] = bmag[i]
                    Satellites[str(hnum[i])]['Rmag'] = rmag[i]
                    Satellites[str(hnum[i])]['Gmag'] = gband(bmag[i],vmag[i])
                    Satellites[str(hnum[i])]['Mstar'] = mstar[i]
                    Satellites[str(hnum[i])]['center'] = cen[i]
                    Satellites[str(hnum[i])]['CumSFH'] = csfh[i]
                    Satellites[str(hnum[i])]['SFR_250Myr'] = sfr[i]
                    Satellites[str(hnum[i])]['Host'] = mw
                    Satellites[str(hnum[i])]['Orbit'] = [np.linalg.norm(distance),
                                                         np.linalg.norm(distance)/MilkyWays[mw]['Rvir']]
                    Satellites[str(hnum[i])]['AlternateHosts'] = []
                    MilkyWays[mw]['Satellites'].append(str(hnum[i]))
                else:
                    if args.overlapping:
                        #See if new host is old massive, and update host if so
                        if MilkyWays[mw]['Mstar'] > MilkyWays[Satellites[str(hnum[i])]['Host']]['Mstar']:
                            #Remove satellite from previous host, and make previous host an alternate
                            Satellites[str(hnum[i])]['AlternateHosts'].append(Satellites[str(hnum[i])]['Host'])
                            MilkyWays[Satellites[str(hnum[i])]['Host']]['Satellites'].remove(str(hnum[i]))
                            #Update satellite with new host info, and add satellite to host
                            Satellites[str(hnum[i])]['Host'] = mw
                            Satellites[str(hnum[i])]['Orbit'] = [np.linalg.norm(distance),
                                                                 np.linalg.norm(distance)/MilkyWays[mw]['Rvir']]
                            MilkyWays[mw]['Satellites'].append(str(hnum[i]))
                        else:
                            Satellites[str(hnum[i])]['AlternateHosts'].append(mw)
                    else:
                        sys.exit(f'Satellite {hnum[i]} has multiple hosts!!!')
            #Check for distances for nearest MW+
            if args.definition in ['5','6','7']:
                if criteria[i] < upper_bound: # MW+ sized halos
                    mw_plus_dist.append(np.linalg.norm(distance))
                    mw_plus_id.append(str(hnum[i]))
            else:
                if criteria[i] > lower_bound: # MW+ sized halos
                    mw_plus_dist.append(np.linalg.norm(distance))
                    mw_plus_id.append(str(hnum[i]))
            #Check for EnvDen
            if np.linalg.norm(distance)<1000 and mvir[i]>1e11:
                MilkyWays[mw]['EnvDen']+=1
        #Find distances to galaxies with M*>1e9 for 10th nearest neighbor
        if mstar[i]>1e9:
            distance = MilkyWays[mw]['center'] - cen[i]
            wrap(distance)
            neighbors.append(np.linalg.norm(distance))
    #Determine closest MW+
    MilkyWays[mw]['Closest_MW+'] = [min(mw_plus_dist),
                                    mw_plus_id[mw_plus_dist.index(min(mw_plus_dist))]]
    #Determine distance to 10th nearest neighbor
    neighbors.sort()
    MilkyWays[mw]['10thNeighbor'] = neighbors[9]
myprint(f'{len(Satellites)} Satellite Halos Found',clear=True)

#Remove MWs with a too large satellite and their other satellites
#Remove satellites that are also in MW range
too_large_satellite,mw_like_sats = [],[]
for mw in MilkyWays:
    for sat in MilkyWays[mw]['Satellites']:
        if Satellites[sat]['Mvir']>MilkyWays[mw]['Mvir'] and mw not in too_large_satellite: too_large_satellite.append(mw)
        if args.definition in ['5','6','7']:
            if Satellites[sat][cname]<upper_bound:
                mw_like_sats.append(sat)
                MilkyWays[mw]['Satellites'].remove(sat)
        else:
            if Satellites[sat][cname]>lower_bound:
                mw_like_sats.append(sat)
                MilkyWays[mw]['Satellites'].remove(sat)
TextLog.append('Removed due to massive satellite:\n')
#Find and remove associated satellites
bad_sats = []
for mw in too_large_satellite:
    for sat in MilkyWays[mw]['Satellites']: bad_sats.append(sat)
    del MilkyWays[mw]
    TextLog.append(f'\t{mw}\n')
for sat in bad_sats: del Satellites[sat]
#Find sats with bad MW as an alternate, remove mwlike sats
for sat in Satellites:
    for mw in too_large_satellite:
        if mw in Satellites[sat]['AlternateHosts']: Satellites[sat]['AlternateHosts'].remove(mw)
TextLog.append('Removed MW-like satellites:\n')
for sat in mw_like_sats:
    del Satellites[sat]
    TextLog.append(f'\t{sat}\n')
print(f'Removed {len(too_large_satellite)} Milky Ways and {len(bad_sats)} Satellites due to overmassive satellite')
print(f'Remvoed {len(mw_like_sats)} Milky Way-like Satellites')

#Determine Satellite Quenching
for s in Satellites:
    #if t_at_sffrac(satfile[h]['CumSFH'],.99) < 11:
    if float(Satellites[s]['SFR_250Myr'][-1])/float(Satellites[s]['Mstar']) < 1e-11:   
        Satellites[s]['Quenched'] = True
    else:
        Satellites[s]['Quenched'] = False

#Determine Closest Large Halo to Milky Way Analogs and Satellites
print('Calculating Closest Large Halo to MW Analogs and Satellites...')
for mw in MilkyWays:
    lh_id,lh_dist = [[],[]]
    for lh in LargeHalos:
        if not mw == lh:
            distance = MilkyWays[mw]['center'] - LargeHalos[lh]['center']
            wrap(distance)
            lh_dist.append(np.linalg.norm(distance))
            lh_id.append(lh)
    MilkyWays[mw]['Closest'] = [min(lh_dist),lh_id[lh_dist.index(min(lh_dist))]]
for s in Satellites:
    lh_id,lh_dist = [[],[]]
    for lh in LargeHalos:
        if not s == lh:
            distance = Satellites[s]['center'] - LargeHalos[lh]['center']
            wrap(distance)
            lh_dist.append(np.linalg.norm(distance))
            lh_id.append(lh)
    Satellites[s]['Closest'] = [min(lh_dist),lh_id[lh_dist.index(min(lh_dist))]]
myprint('Closest Large Halos Found',clear=True)

#Output Data Files
print('Creating Data Files...')
out = open(output_path + f'MilkyWay.{args.definition}.{args.radius}.{overlap}.pickle','wb')
pickle.dump(MilkyWays,out)
out.close()
out = open(output_path + f'Satellite.{args.definition}.{args.radius}.{overlap}.pickle','wb')
pickle.dump(Satellites,out)
out.close()
out = open(output_path + f'LargeHalos.pickle','wb')
pickle.dump(LargeHalos,out)
out.close()
myprint('Data Files Written',clear=True)

#Output Text Log
from datetime import datetime
done = datetime.now()
out = open(output_path+f'Logs/TextLog.{args.definition}.{args.radius}.{overlap}.txt','w')
out.writelines(['Last Run:\n',f'\t{done.month}-{done.day}-{done.year}, {done.hour}:{done.minute}:{done.second} CT\n']+TextLog)
out.close()

#Writeout Halo List in Text File
MilkyWayHalos,SatelliteHalos,LargeHalosList = [],[],[]
for mw in MilkyWays:
    MilkyWayHalos.append(f'{mw}\n')
with open(output_path + f'MilkyWay.{args.definition}.{args.radius}.{overlap}.Halos.txt','w') as f:
    f.writelines(MilkyWayHalos)
for sat in Satellites:
    SatelliteHalos.append(f'{sat}\n')
with open(output_path + f'Satellite.{args.definition}.{args.radius}.{overlap}.Halos.txt','w') as f:
    f.writelines(SatelliteHalos)
for lh in LargeHalos:
    LargeHalosList.append(f'{lh}\n')
with open(output_path + f'LargeHalos.Halos.txt','w') as f:
    f.writelines(LargeHalosList)