import ase

from ase.io.lammpsdata import read_lammps_data

a = read_lammps_data('thermalise11.data', Z_of_type={1:13, 2:28, 3:8}, style='atomic', sort_by_id=True)
a.write("OUTPUT2.xyz", format="xyz")
