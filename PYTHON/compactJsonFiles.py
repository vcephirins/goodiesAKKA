# coding=utf-8
"""compactJsonFiles.py - Compacte une liste de fichiers json au format regards.

Usage : python compactJsonFiles.py [-h] [-v] [-r] [-i <n>] [-n <n>] [-o <outPathFile>] <inPathFile> ...

[-h] or [--help] : Cette aide.
[-v] or [--verbose] : Mode verbeux.
[-r] or [--recursive] : Parcours récursif du répertoire d'entrée.
[-i] or [--indent] : indentation des lignes du fichier json en sortie.
[-n] or [--number] : Limite du nombre de SIP. 0 (defaut) pour pas de limite.
[-o] or [--outPathFile] : Avec le format <path>/<filename>.json
<inPathFile> : Avec le format <path>/<patternFilename>


"""

# IMPORT
import glob
import os
import sys
from sys import argv, exit
import getopt

import json
from collections import OrderedDict
from copy import deepcopy

# Global variables
__author__ = "Vincent Cephirins"
__date__ = "28 Janvier 2021"
__version__ = "1.0"

# Global variables
_debug = False
_verbose = False

_OK = 0
_ERROR = 1
_FATAL = 2

#__all__ = ["compactJsonFiles"]

class DataObject(object):
    """ Gestionnaire de lecture et ecriture d'un fichier json
    """
    def __init__(self, entry=None, indent=4):
        self.entry = entry
        self.indent = indent
        self.data = None

        if entry is not None:
           self.readJson()

    def __str__(self):
        return json.dumps(self.data, indent=self.indent)

    def __repr__(self):
        return "{0} {1}".format(self.__class__, json.dumps(self.data, indent=self.indent))

    def readJson(self):
        """
        Lecture du fichier json
        """
        with open(self.entry, 'r') as f:
            self.data = json.load(f, object_pairs_hook=OrderedDict)
            f.close()

    def writeJson(self, data, output='stdout'):
        """
        Ecriture du fichier json
        """
        if data is None:
            data = self.data

        if output == 'stdout':
            print(json.dumps(data, indent=self.indent))
        else:
            # Création du répertoire si nécessaire
            dirname = os.path.dirname(output)
            if dirname != "" :
                os.makedirs(os.path.dirname(output), exist_ok=True)

            with open(output, 'w', newline='\n') as f:
                json.dump(data, f, indent=self.indent)
                f.close()

def searchJsonFiles(path, recursive = False):
    """
    Find json files with pattern path and filename.
    Return a sorted and unique item list.

    :param path: Pattern path and filename to search
    :type recursive: Recursive search method
    :return: A list of files found
    """
    fichiers=[]
    if os.path.isdir(path): fichiers.extend(searchJsonFiles(path + '/*', recursive))
    else:
        listDir = glob.glob(path)
        for file in listDir:
            # Si répertoire alors appel recursif
            if os.path.isdir(file):
                if recursive:
                    fichiers.extend(searchJsonFiles(file, recursive))
            else:
                # Ne traite que les fichiers d'extension .json
                name, extension = os.path.splitext(file)
                if extension == ".json":
                    # Normalise le path
                    fichiers.append(os.path.normpath(file))
    return fichiers

if __name__ == "__main__":
    opts = args = None
    recursive = False
    indent = 4
    nbFeaturesMax = 0
    outPathFile = "stdout"
    root = "stdout"
    intPathFile = None

    try:
        opts, args = getopt.getopt(argv[1:], "hvri:n:o:", ["help", "verbose", "recursive", "indent", "number", "outPathFile"])
    except getopt.GetoptError as err:
        print(err)
        print(__doc__)
        exit(_FATAL)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(__doc__)
            exit(_OK)
        elif opt in ("-v", "--verbose"):
            _verbose = True
        elif opt in ("-r", "--recursive"):
            recursive = True
        elif opt in ("-i", "--indent"):
            indent = int(arg)
        elif opt in ("-n", "--number"):
            nbFeaturesMax = int(arg)
        elif opt in ("-o", "--outPathFile"):
            # Déconstruction du nom pour la numérotation
            root, ext = os.path.splitext(arg)
        else:
            assert False, "unhandled option: %s" % (opt,)

    if len(args) < 1:
        print(__doc__)
        exit(100)

    if _verbose:
        # Parametres d'appel
        print("Parametres: "+ " ".join(argv[1:]))

    # Indicateurs du bon deroulement des opérations
    bOkAll= True
    bOk = True

    # Recherche des fichiers json à compacter
    listFiles = []
    for pattern in args:
        listFiles.extend(searchJsonFiles(pattern, recursive))

    if len(listFiles) == 0:
        print("Pas de fichier trouvé !")
        sys.exit(_OK)

    # Tri et suppression des doublons
    listFiles = sorted(set(listFiles))

    if _verbose:
        print("\n".join(listFiles))

    print("%7d fichier(s) en entree" % len(listFiles))

    # Lectures des fichiers json et assemblage des features
    jsonGlobal = None
    sessionGlobal = None
    nbFiles = 0
    nbFilesSIP = 1
    nbFeatures = 0
    nbFeaturesTotal = 0

    for jsonFile in listFiles:
        # Lecture du fichier
        jsonData = DataObject(entry=jsonFile, indent=indent)

        # Contrôles du json
        if jsonData.data["type"] != "FeatureCollection":
            print("Fichier %s ignoré: Pas de FeatureCollection !" % (jsonFile,))
            continue

        if jsonGlobal is None:
            # Cas du premier fichier qui sert de collecteur
            jsonGlobal = jsonData

            # Mémorise l'attribut session
            sessionGlobal = jsonGlobal.data["metadata"]["session"]

            # Construction du nom
            if root != "stdout":
                outPathFile = "%s_%d.json" % (root, nbFilesSIP)

        # Compare la session pour les suivants
        session = jsonData.data["metadata"]["session"]
        if session != sessionGlobal:
            print("Fichier %s ignoré: Sessions : %s <> %s" % (jsonFile, sessionGlobal, session))
            continue

        # Pointeur sur les features
        jsonDataFeatures = jsonData.data["features"]

        # Si c'est le premier fichier (nbfeatures == 0), alors on passe au suivant
        # Sinon
        if nbFeatures != 0:
            # Contrôle du nombre de SIP max
            if nbFeaturesMax != 0 and nbFeatures + len(jsonDataFeatures) > nbFeaturesMax:
                # Ecriture du jsonGlobal
                jsonGlobal.writeJson(data=jsonGlobal.data, output=outPathFile)
                print("Fichier SIP '%s', nb SIP: %5d" % (outPathFile, nbFeatures,))

                # Initialisation d'un nouveau fichier collecteur
                jsonGlobal = jsonData
                nbFeatures = 0
                nbFilesSIP += 1

                # Mémorise l'attribut session
                sessionGlobal = jsonGlobal.data["metadata"]["session"]

                # Construction du nom
                if root != "stdout":
                    outPathFile = "%s_%d.json" % (root, nbFilesSIP)
            else:
                # Récupération des features (Copie physique de l'arbre)
                jsonDataFeatures = deepcopy(jsonData.data["features"])

                # Ajout de la copie dans le collecteur
                jsonGlobal.data["features"].extend(jsonDataFeatures)

        # Comptabilisation des features par fichier et au total
        nbFeatures += len(jsonDataFeatures)
        nbFeaturesTotal += len(jsonDataFeatures)

        # Nb features
        if _verbose:
            print("Entrée '%-40s', nb SIP: %5d" % (jsonFile, len(jsonDataFeatures),))

        nbFiles += 1

    # Creation du json final
    if jsonGlobal is not None:
        jsonGlobal.writeJson(data=jsonGlobal.data, output=outPathFile)
        print("Fichier SIP '%s', nb SIP: %5d" % (outPathFile, nbFeatures,))

    print("%7d fichier(s) traite(s)" % nbFiles)
    print("%7d SIP" % nbFeaturesTotal)
    print("%7d fichier(s) SIP" % nbFilesSIP)

    sys.exit(_OK)

