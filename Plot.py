import argparse,pickle,sys,os,warnings
from Code.FormattedPlots.PlotFunctions import *

warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser(description='', usage='')
parser.add_argument('-a','--all', dest='all', action='store_true')
args = parser.parse_args()

#paths to datafiles and image outputs
datafile_path = "DataFiles/"
output_path = "Plots/"

#Function for pulling in specified criteria to plot
def Query(prompt='',options=[]):
    looping = True
    while looping:
        response = str(input(prompt))
        if response in options:
                looping = False
        else:
            print('Invalid')
    return(response)

#Comment out Plots to ignore
def PLOT(S,MW,LH,rest,rad,over,output_path):
    SatelliteCountHistogram(MW,rest,rad,over,output_path)
    VbandMagnitudeFunction(MW,S,rest,rad,over,output_path)
    MassFunction(MW,S,rest,rad,over,output_path)
    NsatVsEnvironment(MW,rest,rad,over,output_path)
    LargestSatelliteDistribution(MW,S,rest,rad,over,output_path)
    LargestSatelliteVsEnvironment(MW,S,rest,rad,over,output_path)
    LargestSatelliteVsNeighborEnvironment(MW,S,rest,rad,over,output_path)
    LargestSatelliteVsHostMass(MW,S,rest,rad,over,output_path)
    LargestSatelliteVsEnvironmentalDensity(MW,S,rest,rad,over,output_path)
    LargestSatelliteStellarVsHostMass(MW,S,rest,rad,over,output_path)
    SatelliteCountVsStellarMassVsEnvironment(MW,rest,rad,over,output_path)
    StellarMassVsOrbitalDistanceVsT90(MW,S,LH,rest,rad,over,output_path)
    QuenchedFractionVsStellarMass(MW,S,rest,rad,over,output_path)
    QuenchedFractionVsOrbitalDistance(MW,S,rest,rad,over,output_path)
    QuenchedFractionVsHostStellarMass(MW,S,rest,rad,over,output_path)
    QuenchedFractionVsEnvironment(MW,S,rest,rad,over,output_path)
    QuenchedFractionHistograms(MW,S,rest,rad,over,output_path)
    StellarMassVsEnvironmentVsAverageSatelliteCount(MW,rest,rad,over,output_path)
    StellarMassVsEnvironmentVsQuenchFraction(MW,S,rest,rad,over,output_path)
    StellarMassVsMWpEnvironmentVsAverageSatelliteCount(MW,rest,rad,over,output_path)
    StellarMassVsNeighborEnvironmentVsAverageSatelliteCount(MW,rest,rad,over,output_path)
    StellarMassVsEnvironmentalDensityVsAverageSatelliteCount(MW,rest,rad,over,output_path)
    EnvironmentDistribution(MW,rest,rad,over,output_path)
    SpecificFrequencyStellarMass(MW,rest,rad,over,output_path)
    SpecificFrequencyDistance(MW,rest,rad,over,output_path)
    SpecificFrequencyNeighborEnvironment(MW,rest,rad,over,output_path)
    SpecificFrequencyEnvironmentalDensity(MW,rest,rad,over,output_path)
    BinnedSpecificFrequencyStellarMass(MW,rest,rad,over,output_path)
    BinnedSpecificFrequencyDistance(MW,rest,rad,over,output_path)
    BinnedSpecificFrequencyNeighborEnvironment(MW,rest,rad,over,output_path)
    BinnedSpecificFrequencyEnvironmentalDensity(MW,rest,rad,over,output_path)
    SAGA_Nsat_Comparison(MW,rest,rad,over,output_path)
    SAGAQuenchComparison(MW,S,rest,rad,over,output_path,BHCheck=True)
    SAGAQuenchComparison(MW,S,rest,rad,over,output_path,BHCheck=False)
    SAGAMassComparison(MW,S,rest,rad,over,output_path)
    NsatVsLargestSatelliteMass(MW,S,rest,rad,over,output_path)
    NsatVsLargestSatelliteMagnitude(MW,S,rest,rad,over,output_path)

if not args.all:
    rest = Query('Milky Way Restricion (1,2,3,4,5,6,7): ',['1','2','3','4','5','6','7'])
    rad = Query('Milky Way Radius (sim,300): ',['300','sim'])
    over = Query('Allow Overlapping Analogs? (Yov,Nov): ',['Yov','Nov'])
    S = pickle.load(open(f'{datafile_path}Satellite.{rest}.{rad}.{over}.pickle','rb'))
    MW = pickle.load(open(f'{datafile_path}MilkyWay.{rest}.{rad}.{over}.pickle','rb'))
    LH = pickle.load(open(f'{datafile_path}LargeHalos.pickle','rb'))
    PLOT(S,MW,LH,rest,rad,over,output_path)
else:
    progress = ['|']+['-']*28+['|']
    print(''.join(progress))
    i = 1
    for rest in ['1','2','3','4','5','6','7']:
        for rad in ['sim','300']:
            for over in ['Yov','Nov']:
                S = pickle.load(open(f'{datafile_path}Satellite.{rest}.{rad}.{over}.pickle','rb'))
                MW = pickle.load(open(f'{datafile_path}MilkyWay.{rest}.{rad}.{over}.pickle','rb'))
                LH = pickle.load(open(f'{datafile_path}LargeHalos.pickle','rb'))
                PLOT(S,MW,LH,rest,rad,over,output_path)
                progress[i] = u'\u2588'
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print(''.join(progress))
                i+=1