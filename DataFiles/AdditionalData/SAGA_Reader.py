import pickle

Hosts = {}
Satellites = {}

with open('SAGA_Hosts.csv') as f:
    host = f.readlines()
    del host[0]

with open('SAGA_Satellites.csv') as f:
    sats = f.readlines()
    del sats[0]

for line in host:
    l = line.split(',')
    hid = l[0]
    Hosts[hid] = {}
    Hosts[hid]['Alias'] = l[1]
    Hosts[hid]['Kmag'] = float(l[6])
    Hosts[hid]['Satellites'] = []


for line in sats:
    l = line.split(',')
    hid = l[1]
    Satellites[hid] = {}
    Satellites[hid]['D_proj'] = float(l[4])
    Satellites[hid]['Rmag'] = float(l[7])
    Satellites[hid]['Vmag'] = float(l[7])+.2
    Satellites[hid]['Mstar'] = 10**float(l[10])
    Satellites[hid]['Host'] = l[0]
    Satellites[hid]['Quenched'] = True if l[11]=='N' else False
    Hosts[l[0]]['Satellites'].append(hid)
    

out = open('SAGA_Hosts.pickle','wb')
pickle.dump(Hosts,out)
out.close()
out = open('SAGA_Satellites.pickle','wb')
pickle.dump(Satellites,out)
out.close()