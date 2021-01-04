#! /bin/env python
"""

Usage: Creer un fichier json depuis un modele et un fichier catalogue

"""

# HEADER

# IMPORT

import sys
import argparse
import logging
from datetime import datetime as dt
from utilsCDPP import logInit
import json
from collections import OrderedDict
import re as regex
from copy import deepcopy

# Global variables
_debug = False
logger = logging.getLogger(__name__)
logInit(level='debug')

patternIgnore = regex.compile("^\s*$|^\s*#.*$")
patternEndOfLine = regex.compile("(^[^#]*)(#.*)?\n$")
patternVariable = regex.compile("(.*)\$\{([_A-Z0-9]+)\}(.*)")

class DataObject(object):
    """ Gestionnaire de lecture et ecriture d'un objet json a partir d'un fichier modele
    """
    def __init__(self, modele=None, indent=4):
        self.modele = modele
        self.indent = indent
        self.data = None

        if(modele is not None):
           self.readJson()

    def __str__(self):
        return json.dumps(self.data, indent=self.indent)

    def __repr__(self):
        return "{0} {1}".format(self.__class__, json.dumps(self.data, indent=self.indent))

    def readJson(self):
        """
        Lecture du fichier json
        """
        with open(self.modele, 'r') as f:
            self.data = json.load(f, object_pairs_hook=OrderedDict)
            f.close()

    def writeJson(self, data, output='stdout'):
        """
        Ecriture du fichier json
        """
        if(data is None):
            data = self.data

        if(output == 'stdout'):
            print(json.dumps(data, indent=self.indent))
        else:
            with open(output, 'w') as f:
                json.dump(data, f, indent=self.indent)
                f.close()

class Struct(object):
    """ Gestionnaire de lecture du fichier des structures
    """
    def __init__(self, struct=None):
        self.struct = struct
        self.tabEntetes = None
        self.tabModeles = None

        if(struct is not None):
           self.readStruct()

    def __str__(self):
        return json.dumps(self.tabEntetes, indent=4) + "\n" + json.dumps(self.tabModeles, indent=4)

    def __repr__(self):
        return "{0} {1}".format(self.__class__, json.dumps(self.tabEntetes, indent=4)) + "\n" + \
               "{0} {1}".format(self.__class__, json.dumps(self.tabModeles, indent=4))

    def readStruct(self):
        """
        Lecture du fichier des structures
        """
        with open(self.struct, 'r') as input:

            self.tabEntetes = {}
            self.tabModeles = {}

            for line in input:
                # Ignore les lignes vides ou les commentaires
                if(patternIgnore.search(line)): continue

                # Ligne d'entete
                if(line.find("NODE_ID=") >= 0):
                    entete = {}
                    # Suppression des commentaires en fin de ligne
                    # et decoupage en dictionnaire clef=valeur
                    values = patternEndOfLine.search(line).group(1).split()
                    for clef,valeur in [val.split("=") for val in values]:
                        entete[clef] = valeur
                    self.tabEntetes[entete.get("NODE_ID")] = entete

                # Ligne des modeles
                if(line.startswith(": ", 1)):
                    # Suppression des commentaires en fin de ligne
                    # et decoupage en dictionnaire clef=valeur
                    values = patternEndOfLine.search(line).group(1).split(": ")
                    self.tabModeles[values[0]] = values[1]

            if(_debug):
                print("[DEBUG] STRUCT")
                print(self)

class Catalog(object):
    """ Gestionnaire de lecture du fichier catalog
    """
    def __init__(self, catalog=None):
        self.name = catalog
        self.data = None

        if(self.name is not None):
           self.readCatalog()

    def readCatalog(self):
        """
        Lecture du fichier des catalogues
        """
        with open(self.name, 'r') as input:

            self.data = []

            for line in input:
                # Ignore les lignes vides ou les commentaires
                if(patternIgnore.search(line)): continue

                # Suppression des commentaires en fin de ligne
                # et decoupage en dictionnaire clef=valeur
                values = patternEndOfLine.search(line).group(1).split()
                self.data.append(values)

            if(_debug):
                print(self.data)

            input.close()

def replaceTag(valeur=None):
    """
    Remplace dans une string les TAGs par ses valeurs
    Les infos sont recherches respectivement :
       - Dans l'entete du modele (Constantes)
       - Dans les donnees du catalogue
       - Calculees (current date, md5, ...)
    Un TAG est represente sous la forme : ${TAG}
    """
    valTag = valeur

    if(type(valeur) is str):

        # Recupere la valeur reelle de la donnee
        # et recherche d'un TAG
        m = patternVariable.search(valeur)
        while(m):
            # Si un TAG  est trouve
            keyTag = m.group(2)

            # Recherche d'abord dans les constantes de l'entete
            valTag = modeleEntete.get(keyTag)

            if(valTag is None):
                # Recherche ensuite dans les donnees du catalogue
                if(keyTag in modeleCatalog):
                    valTag = line[modeleCatalog.index(keyTag) + 1]

                if(valTag is None):
                    # Traitement des cas particuliers
                    # Ajout des informations supplementaires (date, ...)
                    if(keyTag == "CURRENT_DATE"):
                        valTag = dt.now().strftime("%Y-%m-%dT%H:%M:%S")

            if(valTag is None):
                # Valeur du TAG non trouvee : sortie
                break

            # Reconstruction de la valeur entiere
            valTag = m.group(1) + valTag + m.group(3)

            # Recherche iterative des TAGs
            m = patternVariable.search(valTag)

    return valTag

def searchTag(clef, valeur=None):
    """
    Parcours recursif d'un arbre json pour le remplacement des TAGs
    """
    bOk = True
    bStatus = True

    if(type(valeur) is str):
        # Si la valeur est une string alors remplacement des TAGs
        valTag = replaceTag(valeur)
        if(valTag is None):
            print("[ERROR] Tag is not defined : '%s' for key '%s'" % (valeur, clef))
            bOk = False
        else:
           valeur = valTag

    elif(type(valeur) is OrderedDict):
        # Parcours recursif du dico
        for clef, valTag in valeur.items():
            bStatus, valeur[clef] = searchTag(clef, valTag)
            bOk &= bStatus

    elif(type(valeur) is list):
        # Parcour recursif de la liste
        idxVal = 0
        for element in valeur:
            bStatus, valeur[idxVal] = searchTag(clef, element)
            bOk &= bStatus
            idxVal += 1

    elif(valeur is None):
        # Rien a faire
        pass
    else:
        # Type not defined
        bOk = False
        print('[ERROR] unknown type "%s" for Key "%s"' % (type(valeur), clef))

    return (bOk, valeur)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Genere un fichier json au format REGARDS.\n\nAuthor : V. Cephirins\nDate  : 26/02/2018", 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    groupDebug = parser.add_mutually_exclusive_group()
    groupDebug.add_argument("-x", "--debug", dest="_debug", action="store_true", help=argparse.SUPPRESS)
    groupDebug.add_argument("-q", "--quiet", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0", help=argparse.SUPPRESS)
    parser.add_argument("-i", "--indent", type=int, help="indentation des lignes du fichier json", default=4)
    parser.add_argument("-o", "--output", type=str, help="Nom du fichier json a generer. par defaut la sortie standard.", default="stdout")
    parser.add_argument("model", type=str, help="Fichier du modele json a generer.")
    parser.add_argument("struct", type=str, help="Fichier des structures des infos du catalogue.")
    parser.add_argument("catalog", type=str, help="Fichier catalogue des informations.")

    args = parser.parse_args()

    if(args._debug):
        _debug = args._debug
        print(dir())

    # Lecture du fichier modele
    dataObject = DataObject(modele=args.model, indent=args.indent)

    # Lecture du fichier structure
    struct = Struct(struct=args.struct)

    # Lecture du fichier catalogue
    catalog = Catalog(catalog=args.catalog)

    #import pdb
    #pdb.set_trace()

    # Chargement du modele globale
    jsonGlobal = dataObject.data["modeles"]["modele_global"]

    # Indicateur du bon deroulement des remplacements
    bOkAll= True
    bOk = True
    bStatus = True
    numLine = 0

    # Mise a jour des infos
    for line in catalog.data:
        numLine += 1

        # Recupere le modele
        modele = line[0]
        key = line[1]

        # Recupere l'entete du modele
        modeleEntete = struct.tabEntetes[key]
        if(_debug): print(modeleEntete)

        # Recupere le format des donnees du catalogue
        modeleCatalog = struct.tabModeles[modele].split()
        if(_debug): print(modeleCatalog)

        # Chargement du modele json des donnees
        jsonData = deepcopy(dataObject.data["modeles"]["modele_" + modele])
        bStatus, jsonData = searchTag("root", jsonData)
        bOk &= bStatus

        # Chargement du modele json des objets
        jsonDataObject = deepcopy(dataObject.data["modeles"]["modele_do"])
        bStatus, jsonDataObject = searchTag("root", jsonDataObject)
        bOk &= bStatus

        # Valorisation du modele
        jsonData["properties"]["contentInformations"].append(jsonDataObject)
        jsonGlobal["features"].append(jsonData)

        if(bOk is False):
            bOkAll = False
            print("[ERROR] at line '%d' from catalog '%s'" % (numLine, catalog.name))
            # Arret du process en cours
            break

    if(bOkAll is False):
        print("[ERROR] Json file is not generated !")

    if(bOkAll or _debug):
        # Creation du json dataObject
        dataObject.writeJson(data=jsonGlobal, output=args.output);

    sys.exit(bOkAll)
