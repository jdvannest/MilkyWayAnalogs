# Milky Way Analogs
Built to search Romulus25 Simulation for Milky Way Analogs (via various definitions) and determine any Satellites those halos host.

## MilkyWayAnalogs.py
This script will output data (*.pickle* files) in the directory above the repository.<br />
It requires two flags:
1. -d/--definition [1,2,3,4] The parameters defining a Milky Way Analog<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-1: General Virial Mass Restriction (1e12 < M<sub>vir</sub> < 4e12 M<sub>sol</sub>)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-2: Stellar Mass Restriction (analog for K-band Magnitude restriction in SAGA Survery<sup>2</sup>) (1e10 < M<sub>*</sub> < 1e11 M<sub>sol</sub>)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-3: Stellar Mass Restriction (from 2) plus environmental critieria from the SAGA-I Survey<sup>1</sup><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- No halo with M<sub>K</sub> < M<sub>K,MW</sub>+1 within 700 kpc<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- No halo with M<sub>vir</sub> > 5e12 within 2 R<sub>vir</sub> (of large halo) of Milky Way<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-4: Stellar Mass Restriction (from 2) plus environmental critieria from the SAGA-II Survey<sup>2</sup><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- No halo with M<sub>K</sub> < M<sub>K,MW</sub>-1.6 within 700 kpc<br />
2. -r/--radius [sim,300] The virial radius of Milky Way Halos for determining Satellites or overlapping Halos<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-sim: The *true* virial radius given by the halo finder in the simulation<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-300: The standard value of 300kpc used by the SAGA Survey<sup>1</sup><br />
<br />
Each run of this code will output three files:<br />
1. MilkyWay.< definition >.< radius >.pickle: The data for all of the found Milky Way Analogs.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- ['Mvir', 'Mstar', 'Rvir', 'Vmag', 'Rmag', 'Kmag', 'Bmag', 'Gmag', 'center', 'CumSFH', 'SFR_250Myr', 'Satellites', 'Closest_MW+', 'Closest']<br />
2. Satellite.< definition >.< radius >.pickle: The data for all of the found Satellite Halos.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- ['Mvir', 'Rvir', 'Vmag', 'Kmag', 'Bmag', 'Rmag', 'Gmag', 'Mstar', 'center', 'CumSFH', 'SFR_250Myr', 'Host', 'Orbit', 'Quenched', 'Closest']<br />
3. LargeHalos.pickle: The data for all of the Large Halos (M<sub>vir</sub> >  5e11) in Romulus25.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- ['center', 'Mvir', 'Mstar']<br />

## Plots.py
This script outputs plots (*.png* and *.pdf* files) in the directory ../Plots. THIS DIRECTORY MUST BE CREATED BEFORE RUNNING THE SCRIPT.<br />
The script will prompt the user for a *definition* and *radius* argument (based on the flags explained in the MilkyWayAnalogs.py section) when run. If you want to plot all definitions, simply pass the flag *-a* when running the script.<br />
The details for the data being plotted, how it's calculated, and how the plot is formatted are defined in the script *FormattedPlots/Plots.py*.<br />
Comparison Data for the plots is stored in the folder *AdditionalData*.<br />

### Citations
1: SAGA-I https://arxiv.org/pdf/1705.06743.pdf<br />
2: SAGA-II https://arxiv.org/pdf/2008.12783.pdf<br />
