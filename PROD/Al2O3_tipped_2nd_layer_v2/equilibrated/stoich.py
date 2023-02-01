import ase

from ase.io.lammpsdata import read_lammps_data

a = read_lammps_data('thermalise11.data', Z_of_type={1:13, 2:28, 3:8}, style='atomic', sort_by_id=True)
cf = a.get_chemical_formula()
# regex to find the number of each element
import re
# find the number of each element
m = re.findall(r'([A-Z][a-z]*)(\d*)', cf)
print(m)
print("Ni/Al ratio = ", int(m[1][1])/int(m[0][1]))