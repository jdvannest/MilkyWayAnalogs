import pickle

loop = True
while loop:
    method = input('Quenching Method (inst/250): ')
    if method in ['inst','250']: loop = False
    else: print('Invalid Input')
app = '250Myr' if method=='250' else 'Instantaneous'

Quenching = pickle.load(open(f'DataFiles/{app}Quenching.pickle','rb'))

for f in [(i,j,k) for i in [1,2,3,4,5,6,7] for j in ['sim','300'] for k in ['Yov','Nov']]:
    sats = pickle.load(open(f'DataFiles/Satellite.{f[0]}.{f[1]}.{f[2]}.pickle','rb'))
    for s in sats:
        if method=='250':
            sats[s]['Quenched'] = Quenching[s]
        else:
            sats[s]['Quenched'] = Quenching[s]['Quenched']
    pickle.dump(sats,open(f'DataFiles/Satellite.{f[0]}.{f[1]}.{f[2]}.pickle','wb'))