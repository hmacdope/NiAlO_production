# NOTE: This script can be modified for different pair styles 
# See in.elastic for more info.

# Choose potential
pair_style hybrid/overlay eam/alloy edip/multi
pair_coeff * * eam/alloy Mishin-Ni-Al-2009.eam.alloy Ni NULL
pair_coeff * * edip/multi NiAlO.edip Ni O



# Setup neighbor style
neighbor 1.0 nsq
neigh_modify once no every 1 delay 0 check yes

# Setup minimization style
min_style	     cg
min_modify	     dmax ${dmax} line quadratic

# Setup output
thermo		1
thermo_style custom step temp pe press pxx pyy pzz pxy pxz pyz lx ly lz vol
thermo_modify norm no
