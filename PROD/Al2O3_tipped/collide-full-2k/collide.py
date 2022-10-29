from operator import truediv
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-speed', dest='speed', type=float, required=True)
parser.add_argument('-file', dest='file', type=str, required=True)
parser.add_argument('--eam', dest='eam', action='store_true')
args = parser.parse_args()



with open(args.file, 'r') as r:
    lines = r.readlines()
    for line in lines:
        if 'xlo xhi' in line:
            toks = line.split()
            xlo = float(toks[0])
            xhi = float(toks[1])
        if 'ylo yhi' in line:
            toks = line.split()
            ylo = float(toks[0])
            yhi = float(toks[1])
        if 'zlo zhi' in line:
            toks = line.split()
            zlo = float(toks[0])
            zhi = float(toks[1])

with open('min_ke.dat', 'r') as d:
    lines = d.readlines()
    min_ke = int(lines[0])

           
buffer=10
half_z = (zhi -zlo)/2

with open(f'collide_{args.speed}.run', 'w') as f:
    if args.eam:
        f.write(f"""
# Impact of  nanolaminate, {args.speed} km/s.

# simulation construction

units      metal
dimension  3
boundary   p p p
atom_style atomic
region       left    block         {xlo -buffer}  {xhi+buffer} {ylo -buffer}  {yhi+buffer} {zlo} {half_z}
region      right    block         {xlo -buffer}  {xhi+buffer} {ylo -buffer}  {yhi+buffer} {half_z} {zhi}

# Read pre-thermalised data, reset timestep
read_data {args.file}
timestep   0.00025
reset_timestep 0

# Set potentials
pair_style eam/alloy
pair_coeff * * Mishin-Ni-Al-2009.eam.alloy Al Ni

# Thermodynamic acquire settings
thermo_style custom step time temp press pe ke etotal vol
thermo 1000
dump    atomdump all atom 1000 contract.lammpstrj
compute spatialbins all chunk/atom bin/1d z lower 0.01 ids every compress no units reduced
compute bintemps    all temp/chunk spatialbins temp com yes
compute ke all ke
compute temp all temp

fix     temp_bias          all ave/chunk 1 10 10 spatialbins temp bias bintemps file temp.bias.dat
fix     velocity_z         all ave/chunk 1 10 10 spatialbins vz file vz.dat
fix     kinetic_energy     all ave/time 1 10 10 c_ke file ke.dat
fix     temp     all ave/time 1 10 10 c_temp file temp.dat

# Set microcanonical ensemble
fix     microcanonical     all nve

# Thump dynamics
group          g_left      region left
group         g_right      region right
velocity       g_left      set   NULL NULL {10*args.speed/2} units box sum yes
velocity      g_right      set  NULL NULL {-10*args.speed/2} units box sum yes
fix      box_contract      all deform 1 z vel {-20*args.speed/2} remap v units box
run {min_ke}
unfix box_contract
run {4000000-min_ke}
""")
    else:
        f.write(f"""
# Impact of  nanolaminate, {args.speed} km/s.

# simulation construction
units      metal
dimension  3
boundary   p p p
atom_style atomic
region       left    block         {xlo -buffer}  {xhi+buffer} {ylo -buffer}  {yhi+buffer} {zlo} {half_z}
region      right    block         {xlo -buffer}  {xhi+buffer} {ylo -buffer}  {yhi+buffer} {half_z} {zhi}
thermo 1

# Read pre-thermalised data, reset timestep
read_data {args.file}
timestep   0.00025
reset_timestep 0

# Set potentials
pair_style hybrid/overlay eam/alloy edip/multi
pair_coeff * * eam/alloy Mishin-Ni-Al-2009.eam.alloy Al Ni NULL
pair_coeff * * edip/multi NiAlO.edip Al Ni O

# Thermodynamic acquire settings
thermo_style custom step time temp press pe ke etotal vol
thermo 1000
dump    atomdump all atom 10000 contract.lammpstrj
compute spatialbins all chunk/atom bin/1d z lower 0.01 ids every compress no units reduced
compute bintemps    all temp/chunk spatialbins temp com yes
compute ke all ke
compute temp all temp

fix     temp_bias          all ave/chunk 1 10 10 spatialbins temp bias bintemps file temp.bias.dat
fix     velocity_z         all ave/chunk 1 10 10 spatialbins vz file vz.dat
fix     kinetic_energy     all ave/time 1 10 10 c_ke file ke.dat
fix     temp               all ave/time 1 10 10 c_temp file temp.dat

# Set microcanonical ensemble
fix     microcanonical     all nve

# Thump dynamics
group          g_left      region left
group         g_right      region right
velocity       g_left      set  NULL NULL {10*args.speed/2} units box sum yes
velocity      g_right      set  NULL NULL {-10*args.speed/2} units box sum yes
fix      box_contract      all deform 1 z vel {-20*args.speed/2} remap v units box
run {min_ke}
unfix box_contract
run {2000000-min_ke}
write_restart restart.init
write_dump restart.dump 
""")

if not args.eam:
    with open(f'collide_{args.speed}_continue.run', 'w') as f:
        f.write(
f"""# Impact of  nanolaminate, {args.speed} km/s.

# simulation construction
units      metal
dimension  3
boundary   p p p
atom_style atomic
region       left    block         {xlo -buffer}  {xhi+buffer} {ylo -buffer}  {yhi+buffer} {zlo} {half_z}
region      right    block         {xlo -buffer}  {xhi+buffer} {ylo -buffer}  {yhi+buffer} {half_z} {zhi}
thermo 1

# Read restart
read_data restart.data
timestep   0.00025
reset_timestep 0

# Set potentials
pair_style hybrid/overlay eam/alloy edip/multi
pair_coeff * * eam/alloy Mishin-Ni-Al-2009.eam.alloy Al Ni NULL
pair_coeff * * edip/multi NiAlO.edip Al Ni O

# Thermodynamic acquire settings
thermo_style custom step time temp press pe ke etotal vol
thermo 1000
dump    atomdump all atom 10000 contract.lammpstrj
compute spatialbins all chunk/atom bin/1d z lower 0.01 ids every compress no units reduced
compute bintemps    all temp/chunk spatialbins temp com yes
compute ke all ke
compute temp all temp

fix     temp_bias          all ave/chunk 1 10 10 spatialbins temp bias bintemps file temp.bias.dat
fix     velocity_z         all ave/chunk 1 10 10 spatialbins vz file vz.dat
fix     kinetic_energy     all ave/time 1 10 10 c_ke file ke.dat
fix     temp               all ave/time 1 10 10 c_temp file temp.dat

# Set microcanonical ensemble
fix     microcanonical     all nve


run {2000000}
write_restart restart1.init
write_dump restart1.dump 
""")