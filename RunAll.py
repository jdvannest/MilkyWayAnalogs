import os

for d in [1,2,3,4,5,6,7]:
    for r in ['sim','300']:
        for o in ['','-o']:
            #os.chdir('/myhome2/users/vannest/MilkyWayAnalogs')
            os.system(f'/myhome2/users/vannest/anaconda3/bin/python MilkyWayAnalogs.py -d {d} -r {r} {o}')