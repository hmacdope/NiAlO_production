import MDAnalysis as mda
import MDAnalysis.analysis.msd as msd
import matplotlib.pyplot as plt
import numpy as np

u = mda.Universe("prep.data","unwrapped.lammpstrj", format="lammpsdump", atom_style="id type x y z")

MSD = msd.EinsteinMSD(u, select='all', msd_type='xyz', fft=True)
MSD.run()

msd =  MSD.results.timeseries
print(MSD.results.msds_by_particle)
print(MSD.results.msds_by_particle.shape)



nframes = MSD.n_frames
timestep = 0.25 # this needs to be the actual time between frames (ps)
lagtimes = np.arange(nframes)*timestep # make the lag-time axis
fig = plt.figure()
ax = plt.axes()
# plot the actual MSD
ax.plot(lagtimes, msd)
plt.xlabel('lag time (ps)')
plt.ylabel('MSD ($\AA^3$)')
plt.savefig("msd.png")
from scipy.stats import linregress

plt.show()
linear_model = linregress(lagtimes,msd)
slope = linear_model.slope
error = linear_model.rvalue
std_err = linear_model.stderr
# dim_fac is 3 as we computed a 3D msd with 'xyz'
D = slope * 1/(2*MSD.dim_fac)
print("D (AA^3/ps) = ", D, " with error ", std_err)
