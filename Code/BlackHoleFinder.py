import sys, argparse, os
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--definition",choices=['1','2','3','4','5','6','7'],required=True)
parser.add_argument("-r", "--radius",choices=['sim','300'],required=True)
parser.add_argument("-o", "--overlapping",action='store_true')
args = parser.parse_args()

#Define output variables
output_path="DataFiles/"
overlap = 'Yov' if args.overlapping else 'Nov'

with open(output_path+f'MilkyWay.{args.definition}.{args.radius}.{overlap}.Halos.txt') as f:
    MilkyWayHalos = f.readlines()
    MilkyWayHalos = [int(x) for x in MilkyWayHalos]
with open(output_path+f'Satellite.{args.definition}.{args.radius}.{overlap}.Halos.txt') as f:
    SatelliteHalos = f.readlines()
    SatelliteHalos = [int(x) for x in SatelliteHalos]

#Load in Romulus25
print('Loading Database...')
os.environ['TANGOS_DB_CONNECTION'] = '/myhome2/users/munshi/Romulus/data_romulus25.working.db'
import tangos
rom = tangos.get_simulation('cosmo25')[-1]
myprint('Database Loaded',clear=True)

BHMilkyWays,BHSatellites = [],[]
#print('Finding Milky Way Black Holes...')
#for mw in MilkyWayHalos:
#    if 'BH' in rom[mw].keys(): BHMilkyWays.append(f'{mw}\n')
#myprint(f'{len(BHMilkyWays)} Milky Way Black Holes Found.',clear=True)
print('Finding Satellite Black Holes...')
for sat in SatelliteHalos:
    if 'BH' in rom[sat].keys(): BHSatellites.append(f'{sat}\n')
myprint(f'{len(BHSatellites)} Satellite Black Holes Found.',clear=True)

#with open(output_path + f'MilkyWay.{args.definition}.{args.radius}.{overlap}.BlackHoles.txt','w') as f:
#    f.writelines(BHMilkyWays)
with open(output_path + f'Satellite.{args.definition}.{args.radius}.{overlap}.BlackHoles.txt','w') as f:
    f.writelines(BHSatellites)
print(f'BH Files Written for {args.definition}-{args.radius}-{overlap}')
