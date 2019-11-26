#!/bin/bash

####################################
#     Slurm script template        #
#                                  #
# Submit script: sbatch filename   #
#                                  #
####################################

#SBATCH -A T2-CS055-SL4-GPU                # Account to be used
#SBATCH --job-name=test          # the job name
#SBATCH --output=test.%j.out     # the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --error=test.%j.err      # the job stderr will be dumped here. (%j expands to jobId).
#SBATCH --ntasks=1                  # How many times the command will run. Leave this to 1 unless you know what you are doing
#SBATCH --nodes=1                   # The task will break in so many nodes. Use this if you need many GPUs
#SBATCH --gres=gpu:3          # GPUs per node to be allocated
#SBATCH --ntasks-per-node=1         # Same as ntasks
#SBATCH --cpus-per-task=1           # If you need multithreading
#SBATCH --time=00:11:11              # HH:MM:SS Estimated time the job will take. It will be killed if it exceeds the time limit
##SBATCH --mem=32G                   # memory to be allocated per NODE
#SBATCH --partition=pascal          

## LOAD MODULES ##
module purge            # clean up loaded modules

# load necessary modules
module load cuda/10.0 cudnn/7.4_cuda-10.0


source activate seq3

## Job to be run ##
srun python myscript.py -a 1 -b 2 -c 3

