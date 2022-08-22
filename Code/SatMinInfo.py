import pickle
import numpy as np

file_path = '../DataFiles/'

defs,rads,over = [1,2,3,4,5,6,7],['sim','300'],['Yov','Nov']

print('def\tr\tOverlap\tMstar\tM_R\tNpart')
for r in rads:
    print('------------------------------------------------------------------------------------------------')
    for d in defs:
        for o in over:
            sat = pickle.load(open(f'{file_path}Satellite.{d}.{r}.{o}.pickle','rb'))
            Mstar,Mr,Npart= [],[],[]
            for s in sat:
                Mstar.append(round(np.log10(sat[s]['Mstar']),3))
                Mr.append(sat[s]['Rmag'])
                Npart.append(0)
            ov = 'Yes' if o=='Yov' else 'No'
            print(f'{d}\t{r}\t{ov}\t{min(Mstar)}\t{max(Mr)}\t{min(Npart)}')