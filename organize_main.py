import argparse
import organizer
import sys
import os
import yaml
import shutil
from pathlib import Path

## Command line input ##
parser = argparse.ArgumentParser(
    description=(
        'Launches the organizing step. \n'
        'yaml must have: source_folder: folder for files to organize \n'
        'yaml must have: organized_folder: folder for organized files \n'
        'yaml must have: text_folder: folder for text files \n'
        'yaml must have: model_folder: folder for model files \n'
        'yaml can have organizing_opts: dictionary of options for organizing \n'
        'yaml can have extracting_opts: dictionary of options for extracting \n'
        'yaml can have formating_opts: dictionary of options for formatting \n'
        )
    ,epilog=(
        'Note list of files to process. \n'

    )
    ,formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("config_file",type = str
                    ,help = "YAML configuration file")
parser.add_argument('--venv', default = True, type=bool,
                    help = "Whether to transform .cha to flo files in the virtual environment.")
parser.add_argument('--organize', '-o', default = True, type=bool,
                    help = "Whether to transform .cha to flo files in the virtual environment.")
parser.add_argument('--write_model', '-w', default = True, type=bool,
                    help = "Whether to transform write the model file.")

args = parser.parse_args()

## YAML config loading ##
with open(args.config_file) as f:
    config = yaml.safe_load(f)

######
#Flags
######
#Test if in a virtual environment (venv, virtualenv, conda)
invenv = (sys.prefix != sys.base_prefix  # venv / virtualenv
or os.environ.get("VIRTUAL_ENV") is not None  # venv / virtualenv (belt & suspenders)
or os.environ.get("CONDA_DEFAULT_ENV") is not None  # conda
or os.environ.get("CONDA_PREFIX") is not None )         #whether we are in a virtual environmnent

#######
# paths
######
source_folder = config["source_folder"]
organized_folder = config["organized_folder"]
text_folder = config["text_folder"]
model_folder = config["model_folder"]

mo_opts = config.get("organizing_opts", {})
me_opts = config.get("extracting_opts",{})
cha2text_opts = config.get("formating_opts",{})


###########
# actual fx
##########
me = organizer.MainExtractor(organized_folder,text_folder,model_folder,**me_opts)

if args.organize:
    #first step in organizing the data
    mo = organizer.MainOrganizer(source_folder,organized_folder,**mo_opts)
    mo.organize()

if args.write_model:
    #Extract stat model variables
    me.build_participant_doc()

#step 2 of organizing the data
if invenv:
    if args.venv:
        me.cha2text(text_folder,**cha2text_opts)
    else:
        print("Change flag of invenv to False or run manually outside of virtual environment")
else:
    me.cha2text(text_folder,**cha2text_opts)

#Copy config file for safe keeping
fname = Path(args.config_file).name
npath = Path(text_folder)
shutil.copy(args.config_file, npath / fname)