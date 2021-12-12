import pickle

file_path = '../DataFiles/'

defs,rads = [[1,2,3,4],['sim','300']]

print('def\tr\tN_mw\tN_sat\tmax(N)\td_min')
for r in rads:
    for d in defs:
        mw = pickle.load(open(f'{file_path}MilkyWay.{d}.{r}.pickle','rb'))
        sat = pickle.load(open(f'{file_path}Satellite.{d}.{r}.pickle','rb'))
        n_sats,dist = [[],[]]
        for m in mw:
            n_sats.append(len(mw[m]['Satellites']))
            dist.append(mw[m]['Closest'][0])
        print(f'{d}\t{r}\t{len(mw)}\t{len(sat)}\t{max(n_sats)}\t{min(dist)}')