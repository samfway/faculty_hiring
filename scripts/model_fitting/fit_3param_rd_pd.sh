#!/bin/bash
#PBS -N OPT_3P_rd_pd
#PBS -joe
#PBS -t 0-249
#PBS -q long8gb
#PBS -l pmem=8gb
#PBS -l nodes=1:ppn=1
#PBS -l walltime=23:59:59
OUTPUT_DIR=/Users/sawa6416/Projects/faculty_hiring/optimization_output/
PREFIX=OPT_3P_rd_pd
/Users/sawa6416/Projects/faculty_hiring/scripts/optimize.py -i /Users/sawa6416/Projects/faculty_hiring/data/inst_cs.txt -f /Users/sawa6416/Projects/faculty_hiring/data/faculty_cs_0930.txt -p "rd_pd" > ${OUTPUT_DIR}/${PREFIX}_${PBS_ARRAYID}.txt
