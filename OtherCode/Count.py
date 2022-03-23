import pickle

file_path = '../DataFiles/'

defs,rads = [[1,2,3,4,5,6,7],['sim','300']]

print('def\tr\tN_mw\tN_sat\tmax(N)\td_min\tEnvDen')
for r in rads:
    print('------------------------------------------------------')
    for d in defs:
        mw = pickle.load(open(f'{file_path}MilkyWay.{d}.{r}.pickle','rb'))
        sat = pickle.load(open(f'{file_path}Satellite.{d}.{r}.pickle','rb'))
        n_sats,dist,env = [[],[],[]]
        for m in mw:
            n_sats.append(len(mw[m]['Satellites']))
            dist.append(mw[m]['Closest'][0])
            env.append(mw[m]['EnvDen'])
        print(f'{d}\t{r}\t{len(mw)}\t{len(sat)}\t{max(n_sats)}\t{int(min(dist))}\t{max(env)}')