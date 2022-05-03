import pickle

file_path = '../DataFiles/'

defs,rads,over = [1,2,3,4,5,6,7],['sim','300'],['Yov','Nov']

print('def\tr\tOverlap\tN_mw\tN_sat\tmax(N)\tDist(LH)\tDist(10th)\tEnvDen\tN_split')
for r in rads:
    print('------------------------------------------------------------------------------------------------')
    for d in defs:
        for o in over:
            mw = pickle.load(open(f'{file_path}MilkyWay.{d}.{r}.{o}.pickle','rb'))
            sat = pickle.load(open(f'{file_path}Satellite.{d}.{r}.{o}.pickle','rb'))
            n_sats,dist_lh,dist_10,env,n_split = [],[],[],[],0
            for m in mw:
                n_sats.append(len(mw[m]['Satellites']))
                dist_lh.append(int(mw[m]['Closest'][0]))
                dist_10.append(int(mw[m]['10thNeighbor']))
                env.append(mw[m]['EnvDen'])
            for s in sat:
                if len(sat[s]['AlternateHosts'])>0: n_split+=1
            ov = 'Yes' if o=='Yov' else 'No'
            print(f'{d}\t{r}\t{ov}\t{len(mw)}\t{len(sat)}\t{max(n_sats)}\t{int(min(dist_lh)):03d}-{int(max(dist_lh))}\t{min(dist_10):04d}-{max(dist_10)}\t{max(env)}\t{n_split}')