import pickle

for n in [(d,r) for  d in [1,2,3,4,5,6,7] for r in ['sim','300']]:
    mw = pickle.load(open(f'../../DataFiles/MilkyWay.{n[0]}.{n[1]}.Yov.pickle','rb'))
    sat = pickle.load(open(f'../../DataFiles/Satellite.{n[0]}.{n[1]}.Yov.pickle','rb'))

    hosts,TextLog = [],['Host\tSat\tAlt\n']

    for s in sat:
        if len(sat[s]['AlternateHosts'])>0:
            TextLog.append(f"{sat[s]['Host']} - {s} - {sat[s]['AlternateHosts'][0]}\n")
            hosts.append([sat[s]['Host'],sat[s]['AlternateHosts'][0],s])
    
    if len(TextLog)>1:
        out = open(f'List.{n[0]}.{n[1]}.txt','w')
        out.writelines(TextLog)
        out.close()
    
    line,H_old,A_old = 1,0,0
    while line < len(hosts):
        h = hosts[line]
        if h[0] == H_old and h[1] == A_old:
            PlotText.append(f"x{h[2]},y{h[2]},z{h[2]} = Sphere({sat[h[2]]['Rvir']},[{sat[h[2]]['center'][0]},{sat[h[2]]['center'][1]},{sat[h[2]]['center'][2]}])\n")
            PlotText.append(f"ax.plot_surface(x{h[2]},y{h[2]},z{h[2]},alpha=.1)\n")
            PlotText.append(f"ax.scatter({sat[h[2]]['center'][0]},{sat[h[2]]['center'][1]},{sat[h[2]]['center'][2]},label='{h[2]}')\n")
            line+=1
        else:
            if line > 1:
                PlotText.append("ax.legend()\n")
                PlotText.append("plt.show()")
                out = open(f'Plots.{n[0]}.{n[1]}/View.{H_old}_{A_old}.py','w')
                out.writelines(PlotText)
                out.close()
            with open('PlotHeader.txt') as f:
                PlotText = f.readlines()
            PlotText.append('\n')
            PlotText.append(f"x{h[0]},y{h[0]},z{h[0]} = Sphere({mw[h[0]]['Rvir']},[{mw[h[0]]['center'][0]},{mw[h[0]]['center'][1]},{mw[h[0]]['center'][2]}])\n")
            PlotText.append(f"ax.plot_surface(x{h[0]},y{h[0]},z{h[0]},alpha=.1)\n")
            PlotText.append(f"ax.scatter({mw[h[0]]['center'][0]},{mw[h[0]]['center'][1]},{mw[h[0]]['center'][2]},label='{h[0]}')\n")
            try:
                PlotText.append(f"x{h[1]},y{h[1]},z{h[1]} = Sphere({mw[h[1]]['Rvir']},[{mw[h[1]]['center'][0]},{mw[h[1]]['center'][1]},{mw[h[1]]['center'][2]}])\n")
                PlotText.append(f"ax.plot_surface(x{h[1]},y{h[1]},z{h[1]},alpha=.1)\n")
                PlotText.append(f"ax.scatter({mw[h[1]]['center'][0]},{mw[h[1]]['center'][1]},{mw[h[1]]['center'][2]},label='{h[1]}')\n")
            except:
                PlotText.append(f"x{h[1]},y{h[1]},z{h[1]} = Sphere({sat[h[1]]['Rvir']},[{sat[h[1]]['center'][0]},{sat[h[1]]['center'][1]},{sat[h[1]]['center'][2]}])\n")
                PlotText.append(f"ax.plot_surface(x{h[1]},y{h[1]},z{h[1]},alpha=.1)\n")
                PlotText.append(f"ax.scatter({sat[h[1]]['center'][0]},{sat[h[1]]['center'][1]},{sat[h[1]]['center'][2]},label='{h[1]}')\n")
            PlotText.append(f"x{h[2]},y{h[2]},z{h[2]} = Sphere({sat[h[2]]['Rvir']},[{sat[h[2]]['center'][0]},{sat[h[2]]['center'][1]},{sat[h[2]]['center'][2]}])\n")
            PlotText.append(f"ax.plot_surface(x{h[2]},y{h[2]},z{h[2]},alpha=.1)\n")
            PlotText.append(f"ax.scatter({sat[h[2]]['center'][0]},{sat[h[2]]['center'][1]},{sat[h[2]]['center'][2]},label='{h[2]}')\n")
            H_old,A_old = h[0],h[1]
            line+=1