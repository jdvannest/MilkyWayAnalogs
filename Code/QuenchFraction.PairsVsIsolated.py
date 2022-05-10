import pickle
import numpy as np

print('def\trad\tf_Q(Pairs)\tf_Q(Iso)')
print('----------------------------------------')

for n in [(d,r) for  d in [1,2,3,4,5,6,7] for r in ['sim','300']]:
    M = pickle.load(open(f'../DataFiles/MilkyWay.{n[0]}.{n[1]}.Yov.pickle','rb'))
    S = pickle.load(open(f'../DataFiles/Satellite.{n[0]}.{n[1]}.Yov.pickle','rb'))

    qfp,qfi = [],[]
    for mw in M:
        t,q = 0,0
        for sat in M[mw]['Satellites']:
            if S[sat]['Mstar']>1e8:
                t+=1
                if S[sat]['Quenched']: q+=1
        if t>0:
            if M[mw]['Closest_MW+'][0]<1000: qfp.append(q/t)
            else: qfi.append(q/t)
    
    print(f'{n[0]}\t{n[1]}\t{round(np.mean(qfp),2)}\t\t{round(np.mean(qfi),2)}')