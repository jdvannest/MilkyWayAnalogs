import pickle

Hosts = {}
Satellites = {}

with open('ELVES_Hosts_Data.txt') as f:
    host = f.readlines()

with open('ELVES_Satellites_Data.txt') as f:
    sats = f.readlines()

for line in host:
    hid = line.split('\t')[0]
    if hid[:4]=='NGC ': hid = f'NGC{hid[4:]}'
    Hosts[hid] = {}
    Hosts[hid]['Mstar'] = float(line.split('\t')[7])
    Hosts[hid]['Kmag'] = float(line.split('\t')[3])
    Hosts[hid]['KmagGroup'] = float(line.split('\t')[4])
    Hosts[hid]['Satellites'] = []


for line in sats:
    sid = line[:15].rstrip(' ')
    Satellites[sid] = {}
    Satellites[sid]['Host'] = line[15:23].rstrip(' ')
    Satellites[sid]['Mstar'] = float(line[88:93])
    Satellites[sid]['Quenched'] = True if line[124:130].rstrip(' ')=='True' else False
    Satellites[sid]['Orbit'] = float(line[41:47])
    Satellites[sid]['Likelihood'] = float(line[136:140])
    Hosts[line[15:23].rstrip(' ')]['Satellites'].append(sid)

out = open('ELVES_Hosts.pickle','wb')
pickle.dump(Hosts,out)
out.close()
out = open('ELVES_Satellites.pickle','wb')
pickle.dump(Satellites,out)
out.close()