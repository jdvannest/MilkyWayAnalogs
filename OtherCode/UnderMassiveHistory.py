import os,pickle

halos = [312,212,227,226,217,254,280,205,338,235]

print('Loading Database...')
os.environ['TANGOS_DB_CONNECTION'] = '/myhome2/users/munshi/Romulus/data_romulus25.working.db'
import tangos
rom = tangos.get_simulation('cosmo25')[-1]

Data={}

for h in halos:
    Data[str(h)] = {}
    t,mstar,mvir = rom[h].calculate_for_progenitors('t()','Mstar','Mvir')
    Data[str(h)]['t'] = t
    Data[str(h)]['Mstar'] = mstar
    Data[str(h)]['Mvir'] = mvir

out = open('Data/UnderMassiveHistoryData.pickle','wb')
pickle.dump(Data,out)
out.close()