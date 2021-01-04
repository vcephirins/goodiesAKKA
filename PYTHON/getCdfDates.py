#! /bin/env python
"""getCdfDates.py - Lecture des dates d'un fichier au format cdf

Usage : python getCdfDates.py <cdffile> <desc>

<cdffile> doit correspondre au pattern suivant :

<chemin-d-access>/<namefile>.bin

"""

# HEADER

# IMPORT

import    os
import logging
# import numpy as np
import pycdf
from datetime import datetime
import time
from utilsCDPP import logInit

# Global variables
logger = logging.getLogger(__name__)
logInit(level='debug')

def display_cdf(filename, desc):

    cdf = pycdf.CDF(filename)

    print("R%04d %s" %(0, cdf[desc][0]))
    print("R%04d %s" %(len(cdf[desc]), cdf[desc][-1]))


from sys import argv, exit

if __name__ == "__main__":

    if(len(argv) < 2):

        print(__doc__)
        exit(100)

#    for datafile in argv [1:]:
#        display_cdf(datafile, ":10")
    datafile = argv[1]
#    desc = argv[2]

    display_cdf(datafile, "epoch_tt2000")
