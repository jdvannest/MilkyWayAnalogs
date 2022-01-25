import argparse,pickle,sys,os,warnings
from FormattedPlots.Plots import *

warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser(description='', usage='')
#parser.add_argument('-h','--host',help='Milky Way Def Type (1,2,3)',required=True,type=str,choices=['1','2','3'])
#parser.add_argument('-r','--radius',help='Radius Type (sim,300)',required=True,type=str,choices=['sim','300'])
parser.add_argument('-a','--all', dest='all', action='store_true')
args = parser.parse_args()

datafile_path = "DataFiles/"
output_path = "DataFiles/Plots/"

if not args.all:
    looping = True 
    while looping:
        rest = str(input('Milky Way Restricion (1,2,3,4): '))
        if rest in ['1','2','3','4']:
            looping = False
        else:
            print('Invalid')
    looping = True 
    while looping:
        rad = str(input('Milky Way Radius (sim,300): '))
        if rad in ['300','sim']:
            looping = False
        else:
            print('Invalid')
    if rad == 'sim':
        T = '.sim'
    else:
        T = '.300'
    S = pickle.load(open(datafile_path+'Satellite.'+rest+T+'.pickle','rb'))
    MW = pickle.load(open(datafile_path+'MilkyWay.'+rest+T+'.pickle','rb'))
    BB = pickle.load(open(datafile_path+'LargeHalos.pickle','rb'))
    # SatelliteCountHistogram(MW,rest,rad,output_path)
    # VbandMagnitudeFunction(MW,S,rest,rad,output_path)
    # MassFunction(MW,S,rest,rad,output_path)
    # NsatVsEnvironment(MW,rest,rad,output_path)
    # LargestSatelliteDistribution(MW,S,rest,rad,output_path)
    LargestSatelliteVsEnvironment(MW,S,rest,rad,output_path)
    # SatelliteCountVsStellarMassVsEnvironment(MW,rest,rad,output_path)
    # StellarMassVsOrbitalDistanceVsT90(MW,S,BB,rest,rad,output_path)
    # QuenchedFractionVsOrbitalDistance(MW,S,rest,rad,output_path)
    # StellarMassVsEnvironmentVsAverageSatelliteCount(MW,rest,rad,output_path)
    # StellarMassVsMWpEnvironmentVsAverageSatelliteCount(MW,rest,rad,output_path)
    # EnvironmentDistribution(MW,rest,rad,output_path)
    # SpecificFrequncyStellarMass(MW,rest,rad,output_path)
    # SpecificFrequncyDistance(MW,rest,rad,output_path)
    # BinnedSpecificFrequncyStellarMass(MW,rest,rad,output_path)
    # BinnedSpecificFrequncyDistance(MW,rest,rad,output_path)
    # #T90VsT50(MW,S,rest,rad,output_path)
    # QuenchedFractionVsEnvironment(MW,S,rest,rad,output_path)
    # SAGA_Nsat_Comparison(MW,rest,rad,output_path)
    # SMHM(MW,S,rest,rad,output_path)
else:
    progress = ['|',' ',' ',' ',' ',' ',' ',' ',' ','|']
    i = 1
    restrictions = ['1','2','3','4']
    radii = ['sim','300']
    for rest in restrictions:
        for rad in radii:
            if i > 1:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
            print(''.join(progress))
            if rad == 'sim':
                T = '.sim'
            else:
                T = '.300'
            S = pickle.load(open(datafile_path+'Satellite.'+rest+T+'.pickle','rb'))
            MW = pickle.load(open(datafile_path+'MilkyWay.'+rest+T+'.pickle','rb'))
            BB = pickle.load(open(datafile_path+'LargeHalos.pickle','rb'))
            # SatelliteCountHistogram(MW,rest,rad,output_path)
            # VbandMagnitudeFunction(MW,S,rest,rad,output_path)
            # MassFunction(MW,S,rest,rad,output_path)
            # NsatVsEnvironment(MW,rest,rad,output_path)
            # LargestSatelliteDistribution(MW,S,rest,rad,output_path)
            LargestSatelliteVsEnvironment(MW,S,rest,rad,output_path)
            # SatelliteCountVsStellarMassVsEnvironment(MW,rest,rad,output_path)
            # StellarMassVsOrbitalDistanceVsT90(MW,S,BB,rest,rad,output_path)
            # QuenchedFractionVsOrbitalDistance(MW,S,rest,rad,output_path)
            # StellarMassVsEnvironmentVsAverageSatelliteCount(MW,rest,rad,output_path)
            # StellarMassVsMWpEnvironmentVsAverageSatelliteCount(MW,rest,rad,output_path)
            # EnvironmentDistribution(MW,rest,rad,output_path)
            # SpecificFrequncyStellarMass(MW,rest,rad,output_path)
            # SpecificFrequncyDistance(MW,rest,rad,output_path)
            # BinnedSpecificFrequncyStellarMass(MW,rest,rad,output_path)
            # BinnedSpecificFrequncyDistance(MW,rest,rad,output_path)
            # #T90VsT50(MW,S,rest,rad,output_path)
            # QuenchedFractionVsEnvironment(MW,S,rest,rad,output_path)
            # SAGA_Nsat_Comparison(MW,rest,rad,output_path)
            # SMHM(MW,S,rest,rad,output_path)
            progress[i] = u'\u2588'
            i+=1
            if i > (len(radii)+len(restrictions)):
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print(''.join(progress))