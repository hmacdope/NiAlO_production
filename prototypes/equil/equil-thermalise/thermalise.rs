#!/bin/bash
#PBS -P y35
#PBS -l walltime=4:00:00
#PBS -l ncpus=32
#PBS -l mem=8GB
#PBS -l jobfs=8GB
#PBS -l software=lammps
#PBS -l wd
 
module unload intel-fc intel-cc openmpi
module load openmpi/2.1.1
module load lammps/11Aug17
n=8
mpirun -map-by ppr:$((8/$n)):socket:PE=$n lmp_openmpi -sf omp -pk omp $n < thermalise.run > thermalise.out
