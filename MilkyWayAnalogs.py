#Code written by Jordan Van Nest, 08/2020
import pickle, sys, argparse, os, datetime
import numpy as np 

output_path="../"

parser = argparse.ArgumentParser(description="Searches Romulus25 for Milky Way Analogs"
                                +" and identifies their Satellite halos."+
                                " Outputs pickle files in run directory.", 
                                usage="SAGA_Data.py -d 1/2/3 -r sim/300")
parser.add_argument("-d", "--definition", help="Definition for Milky Way Analog\n"+
                                                "1: By General Virial Mass Restricition\n"+
                                                "2: By Stellar Mass Restriction from K-band Magnitude\n"+
                                                "3: Method 2 + Environmental Restrictions (SAGAI)\n"+
                                                "4: Method 2 + Environmental Restrictions (SAGAII)"
                                                ,choices=['1','2','3','4'],required=True)
parser.add_argument("-r", "--radius", help="Radius for definition satellites\n"+
                                            "sim: The true virial radii from the simulations\n"+
                                            "300: The SAGA value of 300 kpc"
                                            ,choices=['sim','300'],required=True)
args = parser.parse_args()

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
        relpos[bad] = -1.0 * (relpos[bad] / np.abs(relpos[bad])) * np.abs(bphys[bad] - np.abs(relpos[bad]))
    else:
        relpos[bad] = -1.0 * (relpos[bad]/np.abs(relpos[bad])) * np.abs(bphys - np.abs(relpos[bad]))
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

#Initialize Data output Dictionaries
MilkyWays = {} 
Satellites = {} 
LargeHalos = {} 

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
    criteria = mvir
    ##previous (lb,ub) values: (5e11,3e12),(1e12,4e12)
    lower_bound = 1e12  
    upper_bound = 4e12
else:
    criteria = mstar
    ##previous (lb,ub) values: (10**10.2,10**10.9)
    lower_bound = 10**10 #if args.definition == '4' else 10**10.2
    upper_bound = 10**11 #if args.definition == '4' else 10**10.9

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
myprint(f'{len(MilkyWays)} Milky Way Analogs Found',clear=True)

#Remove any MW Analogs with overlapping Virial Radii
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
for mw in overlapping:
    del MilkyWays[mw]
print(f'\t{len(overlapping)} Milky Ways removed due to overlapping Rvir')#: {overlapping}')

#Apply environmental criteria if applicable
if args.definition in ['3','4']:
    # No K < K_MW+1 within 700kpc (from John W.) : SAGAI sec 2.2
    # No halo with K < K_MW-1.6 within 700kpc (from John W.) : SAGAII sec 2.1.2
    remove = []
    for mw in MilkyWays:
        for i in np.arange(len(hnum)):
            if not mw == str(hnum[i]):
                if kmag[i] < ( (MilkyWays[mw]['Kmag'] - 1.6) if args.definition=='4' else (MilkyWays[mw]['Kmag'] + 1) ):
                    distance = cen[i] - MilkyWays[mw]['center']
                    wrap(distance)
                    if np.linalg.norm(distance) < 700:
                        if mw not in remove:
                            remove.append(mw)
    for mw in remove:
        del MilkyWays[mw]
    print(f'\t{len(remove)} Milky Ways removed to due Kband Neigbor Restrictions')
    if args.definition == '3':    
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
        for mw in remove:
            del MilkyWays[mw]
        print(f'\t{len(remove)} Milky Ways removed to due Massive Neigbor Restrictions')

#Determine Final Milky Way Analog Count
print(f'{len(MilkyWays)} Milky Way Analogs Considered')

#Determine Closest MW+ and Satellites for Milky Way Analogs
print(f'Finding Satellite Halos...')
for mw in MilkyWays:
    rad = 300 if args.radius=='300' else MilkyWays[mw]['Rvir']
    mw_plus_id,mw_plus_dist = [[],[]]
    for i in np.arange(len(hnum)):
        if mstar[i] < 1e7 or rmag[i] > -10.8 or str(hnum[i])==mw:
            pass #Outside Rom25 resolution limit or outside SAGA detection limit
        else:   #Satellite Halos
            distance = MilkyWays[mw]['center'] - cen[i]
            wrap(distance)
            if np.linalg.norm(distance) < rad:
                if str(hnum[i]) in Satellites:
                    sys.exit(f'Satellite {hnum[i]} has multiple hosts!!!')
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
                MilkyWays[mw]['Satellites'].append(str(hnum[i]))
            if criteria[i] > lower_bound: # MW+ sized halos
                mw_plus_dist.append(np.linalg.norm(distance))
                mw_plus_id.append(str(hnum[i]))
    MilkyWays[mw]['Closest_MW+'] = [min(mw_plus_dist),
                                    mw_plus_id[mw_plus_dist.index(min(mw_plus_dist))]]
myprint(f'{len(Satellites)} Satellite Halos Found',clear=True)

#Determine Satellite Quenching
for s in Satellites:
    ######## if t_at_sffrac(satfile[h]['CumSFH'],.99) < 11:
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
out = open(output_path + f'MilkyWay.{args.definition}.{args.radius}.pickle','wb')
pickle.dump(MilkyWays,out)
out.close()
out = open(output_path + f'Satellite.{args.definition}.{args.radius}.pickle','wb')
pickle.dump(Satellites,out)
out.close()
out = open(output_path + f'LargeHalos.pickle','wb')
pickle.dump(LargeHalos,out)
out.close()
myprint('Data Files Written',clear=True)

#Update Log File
print('Updating Log File...')
now = datetime.datetime.now()
try:
    with open(output_path + 'SAGA.log.txt','r') as log:
        l = log.readlines()
except:
    l = ['Criteria\tMW\tSatellites\tMaxCount\tLastRun','1','2','3','4','1_300','2_300','3_300','4_300']

satcount = []
for mw in MilkyWays:
    satcount.append(len(MilkyWays[mw]['Satellites']))

line = int(args.definition)
if args.radius == '300':
    line += 4
    R = '_300'
else:
    R = ''
l[line] = (f'{args.definition}{R}\t{len(MilkyWays)}\t{len(Satellites)}\t'
            +f'{max(satcount)}\t{now.hour}:{now.minute}:{now.second}-'
            +f'{now.month}/{now.day}/{now.year}\n')
log = open(output_path + 'SAGA.log.txt','w')
log.writelines(l)
log.close()
myprint('Log File Updated',clear=True)