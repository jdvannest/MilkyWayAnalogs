import pickle, os
import numpy as np

def Plot(file,halo,rad,x,y,z):
    file.append(f"x{halo},y{halo},z{halo} = Sphere({rad},[{x},{y},{z}])\n")
    file.append(f"ax.plot_surface(x{halo},y{halo},z{halo},alpha=.1)\n")
    file.append(f"ax.scatter({x},{y},{z},label='{halo}')\n")

for n in [(d,r) for  d in [1,2,3,4,5,6,7] for r in ['sim','300']]:
    mw = pickle.load(open(f'../../DataFiles/MilkyWay.{n[0]}.{n[1]}.Yov.pickle','rb'))
    sat = pickle.load(open(f'../../DataFiles/Satellite.{n[0]}.{n[1]}.Yov.pickle','rb'))
    os.system(f'rm Plots.{n[0]}.{n[1]}/View.*')
    os.system(f'rm List.{n[0]},{n[1]}.txt')

    hosts,TextLog = [],['Host-Sat-Alt\tClosest\tT-Index\n']

    for s in sat:
        if len(sat[s]['AlternateHosts'])>0:
            cenh,cens,cena = mw[sat[s]['Host']]['center'] , sat[s]['center'] , mw[sat[s]['AlternateHosts'][0]]['center']
            mh,ms,ma = mw[sat[s]['Host']]['Mvir'] , sat[s]['Mvir'] , mw[sat[s]['AlternateHosts'][0]]['Mvir']
            closest = 'Yes' if np.linalg.norm(cenh-cens)<np.linalg.norm(cena-cens) else 'No'
            index = 'Yes' if (mh/np.linalg.norm(cenh-cens)**3)>(ma/np.linalg.norm(cena-cens)**3) else 'No'
            TextLog.append(f"{sat[s]['Host']} - {s} - {sat[s]['AlternateHosts'][0]}\t{closest}\t{index}\n")
            hosts.append([sat[s]['Host'],sat[s]['AlternateHosts'][0],s])
    
    if len(TextLog)>1:
        out = open(f'List.{n[0]}.{n[1]}.txt','w')
        out.writelines(TextLog)
        out.close()
    
    line,H_old,A_old,started = 0,0,0,False
    while line < len(hosts):
        h = hosts[line]
        if h[0] == H_old and h[1] == A_old:
            Plot(PlotText,h[2],sat[h[2]]['Rvir'],sat[h[2]]['center'][0],sat[h[2]]['center'][1],sat[h[2]]['center'][2])
            line+=1
        else:
            if started:
                PlotText.append("ax.legend()\n")
                PlotText.append("plt.show()")
                out = open(f'Plots.{n[0]}.{n[1]}/View.{H_old}_{A_old}.py','w')
                out.writelines(PlotText)
                out.close()
                started = False

            with open('Header.txt') as f:
                PlotText = f.readlines()
            started = True
            PlotText.append('\n')
            Plot(PlotText,h[0],mw[h[0]]['Rvir'],mw[h[0]]['center'][0],mw[h[0]]['center'][1],mw[h[0]]['center'][2])
            #try:
            Plot(PlotText,h[1],mw[h[1]]['Rvir'],mw[h[1]]['center'][0],mw[h[1]]['center'][1],mw[h[1]]['center'][2])
            #except:
            #    Plot(PlotText,h[1],sat[h[1]]['Rvir'],sat[h[1]]['center'][0],sat[h[1]]['center'][1],sat[h[1]]['center'][2])
            Plot(PlotText,h[2],sat[h[2]]['Rvir'],sat[h[2]]['center'][0],sat[h[2]]['center'][1],sat[h[2]]['center'][2])
            H_old,A_old = h[0],h[1]
            line+=1
    
    PlotText.append("ax.legend()\n")
    PlotText.append("plt.show()")
    out = open(f'Plots.{n[0]}.{n[1]}/View.{H_old}_{A_old}.py','w')
    out.writelines(PlotText)
    out.close()
    started = False