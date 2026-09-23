#!/bin/bash
#SBATCH --account=def-eporte2
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3G
#SBATCH --time=0:10:00

module load python/3.11.5
source 
export PYTHONPATH="Code:$PYTHONPATH"
python /home/mpelland/links/projects/def-eporte2/mpelland/predictability/Code/remote_main.py 'base_config.yaml' 'count'
