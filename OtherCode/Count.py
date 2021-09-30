import pickle

file_path = '../DataFiles/'

defs,rads = [[1,2,3,4],['sim','300']]

for r in rads:
    for d in defs:
        mw = pickle.load(open(f'{file_path}MilkyWay.{d}.{r}.pickle','rb'))
        sat = pickle.load(open(f'{file_path}Satellite.{d}.{r}.pickle','rb'))
        print(f'{d}-{r}: {len(mw)} MWs, {len(sat)} Sats')