import argparse,pickle,pynbody,sys,time,warnings
import numpy as np
import matplotlib.pylab as plt
warnings.filterwarnings("ignore")
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

parser = argparse.ArgumentParser()
parser.add_argument('-d','--definition',choices=['1','2','3','4','5','6','7'],required=True)
parser.add_argument('-r','--radius',choices=['sim','300'],required=True)
parser.add_argument('-m','--main',type=int,required=True)
parser.add_argument('-a','--alt',type=int,required=True)
parser.add_argument('-s1','--sat1',type=int,required=True)
parser.add_argument('-s2','--sat2',type=int)
args = parser.parse_args()

d,r = args.definition,args.radius
mw = pickle.load(open(f'../../DataFiles/MilkyWay.{d}.{r}.Yov.pickle','rb'))
sat = pickle.load(open(f'../../DataFiles/Satellite.{d}.{r}.Yov.pickle','rb'))
halos = [args.main,args.alt,args.sat1]
if args.sat2 is not None: halos.append(args.sat2)

print(f'Rendering {halos[0]}-{halos[1]} System')
Rvir = mw[str(halos[0])]['Rvir']
x,y,z = [],[],[]

for halo in halos:
    try:
        x.append(mw[str(halo)]['center'][0])
        y.append(mw[str(halo)]['center'][1])
        z.append(mw[str(halo)]['center'][2])
    except:
        x.append(sat[str(halo)]['center'][0])
        y.append(sat[str(halo)]['center'][1])
        z.append(sat[str(halo)]['center'][2])

cen = [np.mean([min(x),max(x)]),np.mean([min(y),max(y)]),np.mean([min(z),max(z)])]

print('\tLoading simulation...')
s = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192')
s.physical_units()
h = s.halos(dosort=True)
myprint('\tSimulation Loaded',clear=True)

print('\tCentering...')
pynbody.transformation.inverse_translate(s.ancestor,cen)
myprint('\tCentered',clear=True)
filt = pynbody.filt.Sphere(Rvir)

n,t = [2,1,.5],['Full','Zoom','Tight']

for i in [0,1,2]:
    f = plt.figure()
    print('\tRendering Full...')
    ts = time.time()
    pynbody.plot.stars.render(s[filt].s,width=n[i]*Rvir,resolution=1000,filename=f'Plots.{d}.{r}/Render.{t[i]}.{halos[0]}_{halos[1]}.png')
    tf = time.time()
    myprint(f'\t{t[i]} Rendered in {round((tf-ts)/60,2)} minutes',clear=True)

    cirH = plt.Circle((x[0]-cen[0],y[0]-cen[1]),Rvir,color='w',fill=False)
    f.gca().add_artist(cirH)
    try:
        cirA = plt.Circle((x[1]-cen[0],y[1]-cen[1]),mw[str(halos[1])]['Rvir'],color='w',fill=False)
    except:
        cirA = plt.Circle((x[1]-cen[0],y[1]-cen[1]),sat[str(halos[1])]['Rvir'],color='w',fill=False)
    f.gca().add_artist(cirA)
    cirS1 = plt.Circle((x[2]-cen[0],y[2]-cen[1]),sat[str(halos[2])]['Rvir'],color='r',fill=False)
    f.gca().add_artist(cirS1)
    if args.sat2 is not None:
        cirS2 = plt.Circle((x[3]-cen[0],y[3]-cen[1]),sat[str(halos[3])]['Rvir'],color='r',fill=False)
        f.gca().add_artist(cirS2)
    f.savefig(f'Plots.{d}.{r}/Render.{t[i]}.{halos[0]}_{halos[1]}.Labeled.png',bbox_inches='tight',pad_inches=.1)