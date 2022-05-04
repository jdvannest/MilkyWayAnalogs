import os,warnings
warnings.filterwarnings("ignore")

for d in [1,2,3,4,5,6,7]:
    for r in ['sim','300']:
        print(f'---------- {d}.{r} ----------')
        os.chdir(f'Plots.{d}.{r}')
        try:
            os.system('rm *.png')
        except:
            pass
        views = os.listdir()
        systems = []
        for v in views:
            if v.split('.')[0]=='View': systems.append(v.split('.')[1].split('_'))

        os.chdir('..')
        try:
            with open(f'List.{d}.{r}.txt') as f:
                SatList = f.readlines()
                del SatList[0]

            for s in systems:
                for line in SatList:
                    l = line.split(' - ')
                    if l[0] == s[0]: s.append(l[1])

            for s in systems:
                if len(s)==4:
                    os.system(f'/myhome2/users/vannest/anaconda3/bin/python Render.py -d {d} -r {r} -m {s[0]} -a {s[1]} -s1 {s[2]} -s2 {s[3]}')
                else:
                    os.system(f'/myhome2/users/vannest/anaconda3/bin/python Render.py -d {d} -r {r} -m {s[0]} -a {s[1]} -s1 {s[2]}')
        except:
            pass