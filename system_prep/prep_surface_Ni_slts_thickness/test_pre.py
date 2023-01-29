import MDAnalysis as mda


datafiles = ['pre' + str(i) + '.data' for i in range(1, 11)]

for i, dfile in enumerate(datafiles):
    print(dfile)
    u = mda.Universe(dfile, atom_style='id type x y z')
    ts = u.trajectory.ts
    zslice = ts.positions[:, 2]
    zmin = zslice.min()
    zmax = zslice.max()
    print(zmin, zmax)
    ts.positions[:, 2] -= zmin
    ts.dimensions[2] = zmax - zmin + 0.2
    u.atoms.write(f'pre-clean_{i+1}_{2*((i+1)*1000)}_O.data')
    u.atoms.write(f'pre-clean_{i+1}_{2*((i+1)*1000)}_O.pdb')
