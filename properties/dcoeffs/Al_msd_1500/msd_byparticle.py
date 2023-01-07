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
for i in range(MSD.results.msds_by_particle.shape[1]):
    ax.plot(lagtimes, MSD.results.msds_by_particle[:,i])
ax.plot(lagtimes, msd)
plt.xlabel('lag time (ps)')
plt.ylabel('MSD ($\AA^3$)')
plt.savefig("msd_byparticle.png")
plt.show()

