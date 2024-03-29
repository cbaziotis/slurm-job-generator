#!/bin/bash


while getopts abcde opt; do
    case $opt in
        a) flag1="SET"
        ;;
        b) flag2="SET"
        ;;
        c) optflag1="SET"
        ;;
        d) optflag2="SET"
        ;;
        e) optflag3="SET"
        ;;
    esac
done

####################################
#     XXXX slurm script template   #
#                                  #
# Submit script: sbatch filename   #
#                                  #
####################################

#SBATCH --job-name=test_job       # DO NOT FORGET TO CHANGE THIS
#SBATCH --output=test_job.%j.out  # DO NOT FORGET TO CHANGE THIS. the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --error=test_job.%j.err   # DO NOT FORGET TO CHANGE THIS. the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --ntasks=1                # How many times the command will run. Leave this to 1 unless you know what you are doing
#SBATCH --nodes=1                 # The task will break in so many nodes. Use this if you need many GPUs
#SBATCH --gres=gpu:1              # GPUs per node to be allocated
#SBATCH --ntasks-per-node=1       # Same as ntasks
#SBATCH --cpus-per-task=1         # If you need multithreading
#SBATCH --time=0:01:00            # HH:MM:SS Estimated time the job will take. It will be killed if it exceeds the time limit
#SBATCH --mem=1G                  # memory to be allocated per NODE
#SBATCH --partition=gpu           # gpu: Job will run on one or more of the nodes in gpu partition. ml: job will run on the ml node

export I_MPI_FABRICS=shm:dapl

if [ x$SLURM_CPUS_PER_TASK == x ]; then
  export OMP_NUM_THREADS=1
else
  export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
fi


## LOAD MODULES ##
module purge            # clean up loaded modules 

# load necessary modules
module use ${HOME}/modulefiles
module load gnu/6.4.0
module load intel/19.0.0
module load openblas/0.2.20
module load cuda/9.2.148
module load caffe2/201809
module load slp/0.1.0

## RUN YOUR PROGRAM ##
srun python test.py

