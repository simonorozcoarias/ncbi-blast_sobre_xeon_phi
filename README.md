# BIOS-ParallelBlast: Optimized sequences alignment parallelization on Xeon Phi

Usage of supercomputing in science is more necessary every day, due to the large amount of data that researches have to analyze to obtain significant results. Many-cores technologies such as Intel Xeon Phi were developed as an alternative to accelerate these studies and its use in supercomputers and especially in bioinformatics is more common nowadays, but the results are not good enough when high-demand software is executed in heterogeneous clusters. This research shows a wrapper that achieves parallelization optimally using NCBI-Blast on CPUs and Xeon Phi nodes, the main goal here is to reduce execution times and to demonstrate the usefulness that many-cores technologies contribute in applied sciences.

# Usage
ParallelBlast-2.5.py -i <Sequences input file> -b BlastType <blastx, blastn, blastp> -q AnalysisType <prot, nucl> -d <Database to compared with> -e <evalue> -o <Output filename> -t <Parallelization scheme [TP]> -m <Machines file> -j <Job Directory> -p <Splitter Way [f|l|s|p]>
  
# Utilities
  1. Create Blast-compliant database use
  ParallelBlast-2.5.py -c
  
	2. Show error table (Useful for debugging)
  ParallelBlast-2.5.py -w

NOTE: NCBI-Blast executables (both for CPUs and MICs) must be set up in PATH variable. For doing that, is necessary to change load variable into source code of ParallelBlast-2.5.py with your own paths.

# Reference
If you used this software or a part of it, please cite:

Orozco-Arias, S., Camargo-Forero, L., Correa, J. C., Guyot, R., & Cristancho, M. (2017). BIOS-ParallelBlast: Paralelización optimizada de alineamiento de secuencias sobre Xeon Phi. Ingeniería, investigación y tecnología, 18(4), 423-432.
