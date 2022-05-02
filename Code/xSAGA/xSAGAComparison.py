import pickle,argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--definition", choices=['1','2','3','4'],required=True)
parser.add_argument("-r", "--radius",choices=['sim','300'],required=True)
args = parser.parse_args()

sats = pickle.load(open(f'../DataFiles/Satellite.{args.definition}.{args.radius}.pickle','rb'))
host = pickle.load(open(f'../DataFiles/MilkyWay.{args.definition}.{args.radius}.pickle','rb'))
sers = pickle.load(open('SersicFits.pickle','rb'))

out = open(f'xSAGAComparison.{args.definition}.{args.radius}.txt','w')
out.writelines(f'HostID\tHost_Mstar\tHost_Sersic\tSatID\tSat_Mstar\tSat_pos\n')

for mw in host:
    mw_id = int(mw)
    mw_cen = host[mw]['center']
    mw_ms = host[mw]['Mstar']
    mw_n = sers[mw]['par'][2]
    for s in host[mw]['Satellites']:
        sat_id = int(s)
        sat_cen = sats[s]['center']
        sat_ms = sats[s]['Mstar']

        out.writelines(f'{mw_id}\t{mw_ms}\t{mw_n}\t{sat_id}\t{sat_ms}\t{sat_cen-mw_cen}\n')

out.close()