import argparse,os

parser = argparse.ArgumentParser()
parser.add_argument("-m","--mwonly",action="store_true")
parser.add_argument("-b","--bhonly",action="store_true")
args = parser.parse_args()

for d in [1,2,3,4,5,6,7]:
    for r in ['sim','300']:
        for o in ['','-o']:
            #os.chdir('/myhome2/users/vannest/MilkyWayAnalogs')
            if not args.bhonly: os.system(f'/myhome2/users/vannest/anaconda3/bin/python MilkyWayAnalogs.py -d {d} -r {r} {o}')
            if not args.mwonly: os.system(f'/myhome2/users/vannest/anaconda3/bin/python Code/BlackHoleFinder.py -d {d} -r {r} {o}')
