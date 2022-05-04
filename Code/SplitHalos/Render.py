import pickle,pynbody,sys
import numpy as np
import matplotlib.pylab as plt 
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

print('Loading simulation...')
s = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192')
s.physical_units()
h = s.halos(dosort=True)
myprint('Simulation Loaded',clear=True)

d,r = ['1','sim']
mw = pickle.load(open(f'../../DataFiles/MilkyWay.{d}.{r}.Yov.pickle','rb'))
sat = pickle.load(open(f'../../DataFiles/Satellite.{d}.{r}.Yov.pickle','rb'))

halos = [27,61,2688,3481]
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

print('Centering...')
pynbody.transformation.inverse_translate(s.ancestor,cen)
myprint('Centered',clear=True)
filt = pynbody.filt.Sphere(Rvir)
f = plt.figure()
print('Rendering...')
pynbody.plot.stars.render(s[filt].s,width=2*Rvir,filename=f'Plots.{d}.{r}/Render.{halos[0]}_{halos[1]}.png')
myprint('Rendered',clear=True)

cirH = plt.Circle((x[0]-cen[0],y[0]-cen[1]),Rvir,color='w',fill=False)
f.gca().add_artist(cirH)
cirA = plt.Circle((x[1]-cen[0],y[1]-cen[1]),Rvir,color='w',fill=False)
f.gca().add_artist(cirA)
cirS1 = plt.Circle((x[2]-cen[0],y[2]-cen[1]),Rvir,color='r',fill=False)
f.gca().add_artist(cirS1)
cirS2 = plt.Circle((x[3]-cen[0],y[3]-cen[1]),Rvir,color='r',fill=False)
f.gca().add_artist(cirS2)
f.savefig(f'Plots.{d}.{r}/Render.{halos[0]}_{halos[1]}.Labeled.png',bbox_inches='tight',pad_inches=.1)
print('Done')