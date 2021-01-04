#! /bin/env python
"""
@author: Vincent Cephirins

<desc> peut prendre les valeurs suivantes :
Byte order : 
@ : Native endian
< : Little endian
> : Big endian

Type : name            (type[size in byte(s)])
x : pad byte           (bytes)
c : char               (byte[1])
b : signed char        (integer[1])
B : unsigned char      (integer[1])
? : bool               (bool[1])
h : short              (integer[2])
H : unsigned short     (integer[2])
h : int                (integer[4])
I : unsigned int       (integer[4])
i : int                (integer[4])
l : long               (integer[4])
L : unsigned long      (integer[4])
q : long long          (integer[8])
Q : unsigned long long (integer[8])
e : float IEEE 754 binary 16 (float[2])
f : float              (float[4])
d : double             (float[8])
s : string             (bytes)
p : pascal string      (bytes)
P : void *             (integer)

exemples :
# Afficher les infos du fichier
readFile exemple.dat '>' '>H10x7H55xf'

# Afficher toutes les lignes
readFile exemple.dat '>' '>H10x7H55xf' '-' -c -n

# Afficher la premiere et derniere ligne
readFile exemple.dat '>' '>H10x7H55xf' '1,$'

# Afficher les 3 premieres lignes, 5,10, 20 jusqu'a la fin, en Big endian : 1 Ushort, ignorer 10 bytes, 7 Ushort, ignorer 55 bytes, 1 float
readFile exemple.dat '>' '>H10x7H55xf' '-3,5,10,20-'

"""

__author__="Vincent Cephirins"
__date__="13-NOV-2018"
__version__="1.00"

# HEADER

# IMPORT
import os
import sys
import traceback
import argparse
# import logging
import numpy
import re as regex
from datetime import datetime
# from utilsCDPP import logInit
from struct import *

# Global variables

__all__ = ["printException",
           "readFile"]

def printException(message=None, exit=True):
    """
    Affichage d'un message d'erreur applicatif ou systeme.
    Sortie du programme si exit est vrai.

        message est le applicatif ou None si le message systeme doit etre affiche
        exit, boolean vaut True (defaut) pour une sortie du programme
    """

    # if not message provided, get the traceback of errors to be a little more
    # useful for the developer
    if message is not None:
        mess = message
    else:
        # get the traceback
        mess = traceback.format_exc()

    # show error
    print(mess, file=sys.stderr)

    if exit:
        sys.exit(1)

    # return the message
    return mess

def readFile (datafile, descriptions, lines="-", bNumline=False, format=True, sep=';'):
    """
    """

    try:
       count = 0
       interval = "1-"
       intervals = []
       idxInterval = 0
   
       if (lines):
          intervals = regex.split(r"[,]", lines.replace(" ", ""))
          interval = intervals[idxInterval]
   
       if (len(descriptions) > 1):
          sizeHeader = calcsize(descriptions[0])
          sizeColumns = calcsize(descriptions[1])
       else:
          sizeColumns = calcsize(descriptions[0])
   
       with open(datafile, "rb") as input:
           if (len(descriptions) > 1):
              # Lecture de l'entete
              header = input.read(sizeHeader)
              print(sep.join([(str(val)) for val in unpack(descriptions[0], header)]))
              desc = descriptions[1]
           else:
              desc = descriptions[0]
   
           nextRecord = input.read(sizeColumns)
           count += 1
   
           pattern = regex.compile("-+")
           num = []
           deb = end = 0
           while nextRecord:
               record = nextRecord
               if (len(num) == 0):
                   num = pattern.split(interval)
                   if (len(num[0]) == 0):
                       deb = 0
                   else:
                       if (num[0] == "$"):
                           deb = -1
                       else:
                           deb = int(num[0])
   
                   if (len(num) == 1):
                       end = deb
                   elif (len(num[1]) == 0 or num[1] == "$"):
                       end = -1
                   else:
                       end = int(num[1])
   
               if (deb != -1 and deb <= count  and (count <= end or end == -1)):
                   if (format == True):
                       # Format binaire
                       yield unpack(desc, record)
                   else:
                       # Format ascii
                       if (bNumline == True):
                           yield "%d%s%s" % (count, sep, sep.join([(str(val)) for val in unpack(desc, record)]))
                       else:
                           yield sep.join([(str(val)) for val in unpack(desc, record)])
   
               if (end != -1 and count >= end):
                   idxInterval += 1
                   if (idxInterval >= len(intervals)): break
                   interval = intervals[idxInterval]
                   num = []
   
               nextRecord = input.read(sizeColumns)
               if (nextRecord): count += 1
   
           # Cas de la derniere ligne
           if (deb == -1):
               if (bNumline == True):
                   yield "%d%s%s" % (count, sep, sep.join([(str(val)) for val in unpack(desc, record)]))
               else:
                   yield sep.join([(str(val)) for val in unpack(desc, record)])
   
           input.close()

    except ValueError as ve:
        message += "[ERREUR] Valeur invalide : %s" % (ve.args[0])
        printException(message, True)
        raise

    except Exception as e:
        printException("[ERREUR]" + str(e), True)
        raise

    finally: pass
 
global _debug

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lecteur de fichier binaire.\n\nAuthor : V. Cephirins\nDate  : 26/02/2018",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-x", action="store_true", help=argparse.SUPPRESS)
    group.add_argument("-q", "--quiet", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("-l", "--lines", type=str, dest="lines", help="Liste des lignes a extraire 'n[-m][,]...' ou \
                            m et n sont des valeurs entieres croissantes positives ou '$' pour la dernier ligne.") #, default="-")
    parser.add_argument("-s", "--sep", type=str, dest="sep", help="Separateur des champs (';' par defaut).", default=";")
    parser.add_argument("-n", "--numline", action="store_true", help="Affiche les numeros de lignes")
    parser.add_argument("-c", "--count", action="store_true", help="Compte le nombre de lignes")
    parser.add_argument("binfile", help="doit correspondre au pattern suivant : <chemin-d-access>/<namefile>")
    parser.add_argument("desc", help="Descripteur(s) du fichier ([Header] record).", nargs=2)

    args = parser.parse_args()

    if (args.binfile == "-"): inputFile = "/dev/stdin"
    else: inputFile = args.binfile

    if (args.lines is None):
        sizeFile = os.stat(inputFile).st_size

        # Info sur le fichier
        if (len(args.desc) > 1):
            # Avec un entete
            sizeHeader = calcsize(args.desc[0])
            sizeDesc = calcsize(args.desc[1])
            sizeData = sizeFile - sizeHeader
            print("file size = %d, header size = %d, record size = %d, number of record(s) = %d" % (sizeFile, sizeHeader, sizeDesc, sizeData / sizeDesc))
            if (sizeData % sizeDesc):
                print("Warning : %s byte(s) not read !" % (sizeData % sizeDesc))
                exit(1)
        else:
            sizeDesc = calcsize(args.desc[0])
            print("file size = %d, record size = %d, number of record(s) = %d" % (sizeFile, sizeDesc, sizeFile / sizeDesc))
            if (sizeFile % sizeDesc):
                print("Warning : %s byte(s) not read !" % (sizeFile % sizeDesc))
                exit(1)

    else:
        nbCount = 0
        for line in readFile(inputFile, args.desc, args.lines, args.numline, False, args.sep):
           nbCount += 1
           print(line);
     
        if (args.count == True): print("%d line(s)" % (nbCount))

