#!/bin/bash
#PBS -N OPT_rd_pr_gg_rh
#PBS -joe
#PBS -t 0-249
#PBS -q long8gb
#PBS -l pmem=8gb
#PBS -l nodes=1:ppn=1
#PBS -l walltime=47:59:59
FINAL_DIR=/Users/sawa6416/Projects/faculty_hiring/optimization_output/results_files/
OUTPUT_DIR=/scratch/Users/sawa6416/optimization_output
TAG=rd_pr_gg_rh

/Users/sawa6416/Projects/faculty_hiring/scripts/optimize.py -i /Users/sawa6416/Projects/faculty_hiring/data/inst_cs.txt -f /Users/sawa6416/Projects/faculty_hiring/data/faculty_cs_0930.txt -p "rd_pr_gg_rh" > ${OUTPUT_DIR}/OPT_${TAG}_${PBS_ARRAYID}.txt
cat ${OUTPUT_DIR}/OPT_${TAG}_*.txt > ${FINAL_DIR}/RES_${TAG}.txt
