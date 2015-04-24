
from __future__ import print_function

import os
from glob import glob
from fnmatch import fnmatch
import subprocess
from copy import copy

# path to the parallella reference design, paths relative 
# to parallalle_elink/test
REF_DESIGN_DIR = '../parallella_oh'


def create_cmdfile(cmdfile):
    """ create a new command file, basically replacing the paths
    """
    root, cmdfn = os.path.split(cmdfile)

    with open(cmdfile, 'r') as ff, open('elink.cmd', 'w') as newfile:
        for line in ff:
            chunks = line.strip().split(' ')
            mhunks = copy(chunks)
            found = False if '-y' in chunks[0] else True
            for ii,cc in enumerate(chunks):
                if 'elink_tb' in cc:
                    found = False
                elif os.path.isdir(os.path.join(root, cc)):
                    newpath = os.path.join(root, cc)
                    assert os.path.isdir(newpath)
                    mhunks[ii] = newpath
                    found = True
                elif os.path.isfile(os.path.join(root, cc)):
                    newpath = os.path.join(root, cc)
                    assert os.path.isfile(newpath)
                    mhunks[ii] = newpath
                    found = True

            if found:
                newfile.write(' '.join(mhunks) + '\n')

    return 


def get_reference_design_file_list(refpath=None):
    """ get all the files for the design

    This function attempts to extract the latest elink reference
    design.  This is used as a model to compare against the 
    MyHDL implementation.
    """
    if refpath is None:
        refpath = REF_DESIGN_DIR

    # find the elink.cmd file (iverilog sim) 
    cmdfile, elinktop = None, None
    for root, dirs, files in os.walk(refpath):
        for ff in files:
            if fnmatch(ff, 'elink.cmd'):
                cmdfile = os.path.join(root, ff)
                # create local version of build file
                create_cmdfile(cmdfile)
                break
                
            if fnmatch(ff, 'elink.v'):
                elinktop = os.path.join(root, ff)
                break
                
        if cmdfile is not None and elinktop is not None:
            break

    # grab all the verilog files
    # this grabs more files than needed ... lazy 
    vfiles = []
    for root, dirs, files in os.walk(refpath):
        vfiles += glob(os.path.join(root, "*.v"))

    return vfiles, elinktop, cmdfile


if __name__ == '__main__':
    refpath = '../../parallella_oh'
    files, elink, cmdfile = get_reference_design_file_list(refpath)
    subprocess.call(['iverilog', '-f' 'elink.cmd'] + files)


        
        