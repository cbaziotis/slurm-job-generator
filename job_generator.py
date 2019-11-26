import argparse
import os
import sys


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


##########################################################
# Read arguments
##########################################################
parser = argparse.ArgumentParser()
parser.add_argument('-j', required=True,
                    help="Job name")
parser.add_argument('-t', required=True, default="11:59:00",
                    help="HH:MM:SS Estimated time the job will take.")
parser.add_argument('-e',
                    help="conda environment to be activated.")
parser.add_argument('-c', required=True,
                    help="conda environment to be activated.")
parser.add_argument('-p', type=str, default="pascal",
                    help="pascal partition has a max time-limit of 36 hours."
                         "To get round this, use the pascal-long partition.")
parser.add_argument('-g', type=int, default=1,
                    help="number of gpus.")
parser.add_argument('--high', dest='high', action='store_true',
                    help='Use the high priority account "T2-CS055-GPU".'
                         'The default is low "T2-CS055-SL4-GPU"')

opt = parser.parse_args()

if opt.high:
    account = "T2-CS055-GPU"
else:
    account = "T2-CS055-SL4-GPU"

header = f"""#!/bin/bash

####################################
#     Slurm script template        #
#                                  #
# Submit script: sbatch filename   #
#                                  #
####################################

#SBATCH -A {account}                # Account to be used
#SBATCH --job-name={opt.j}          # the job name
#SBATCH --output={opt.j}.%j.out     # the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --error={opt.j}.%j.err      # the job stderr will be dumped here. (%j expands to jobId).
#SBATCH --ntasks=1                  # How many times the command will run. Leave this to 1 unless you know what you are doing
#SBATCH --nodes=1                   # The task will break in so many nodes. Use this if you need many GPUs
#SBATCH --gres=gpu:{opt.g}          # GPUs per node to be allocated
#SBATCH --ntasks-per-node=1         # Same as ntasks
#SBATCH --cpus-per-task=1           # If you need multithreading
#SBATCH --time={opt.t}              # HH:MM:SS Estimated time the job will take. It will be killed if it exceeds the time limit
##SBATCH --mem=32G                   # memory to be allocated per NODE
#SBATCH --partition={opt.p}          
"""

body = f"""
## LOAD MODULES ##
module purge            # clean up loaded modules

# load necessary modules
module load cuda/10.0 cudnn/7.4_cuda-10.0

"""

if opt.e is not None:
    body += f"\nsource activate {opt.e}"

footer = f"""

## Job to be run ##
srun {opt.c}

"""

runner = header + body + footer

write_approval = query_yes_no(f"IS THE GENERATED SCRIPT OK? \n\n" + "=" * 50 +
                              f"\n\n\n {runner}", default="no")

if write_approval:
    with open(f"{opt.j}.sh", "w") as f:
        f.write(header + body + footer)

    ex_approval = query_yes_no(f"Execute the job '{opt.j}' ?", default="no")

    if ex_approval:
        os.system(f"sbatch {opt.j}.sh")

else:
    print("Exiting...")
