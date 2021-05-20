#! /bin/env python3.7
# coding=utf-8
"""

Usage : python createJsonFile.py [-h] [-v] [-i <n>] [-n <n>] [-o <outPathFile>] <model> <catalogue> ...
Creer un fichier json depuis un modele et un fichier catalogue.

[-h] or [--help] : Cette aide.
[-v] or [--verbose] : Mode verbeux.
[-i] or [--indent] : indentation des lignes du fichier json en sortie.
[-n] or [--number] : Limite du nombre de SIP. 0 (defaut) pour pas de limite.
[-s] or [--sep] : Separateur de champ du catalogue. ';' par defaut.
[-o] or [--outPathFile] : Nom du fichier json a generer avec le format <path>/<filename>.json. Par defaut la sortie standard.
<model> : Fichier du modele json a generer avec le format <path>/<filename>
<catalog> : Fichier(s) catalogue(s) des informations avec le format <path>/<patternFilename>
            Le caractere '-' permet de lire sur l'entree standard.

"""
# IMPORT

import getopt
import glob
import hashlib
import json
import os
import re as regex
import sys
from copy import deepcopy
from datetime import datetime as dt
from enum import Enum
from sys import argv, exit
from typing import List

from PIL import Image

from regardsError import *

# Global variables
__author__ = "Vincent Cephirins"
__date__ = "28 Janvier 2021"
__version__ = "1.0"

_debug = False
_verbose = False

_OK = 0
_ERROR = 1
_FATAL = 2

# Pattern globales
patternIgnore = regex.compile("^\s*$|^\s*#.*$")
patternEndOfLine = regex.compile("(^[^#]*)(#.*)?\n$")
patternVariable = regex.compile("(.*)\${([_A-Z0-9]+)}(.*)", regex.IGNORECASE)
patternFn = regex.compile("(.*)\$\${([^}]+)}(.*)", regex.IGNORECASE)


# noinspection PyShadowingNames
class JsonObject(object):
    """ Gestionnaire de lecture et ecriture dans un fichier d'un objet json
    """

    def __init__(self, modele=None, indent=4):
        self.modele = modele
        self.indent = indent
        self.data = None

        if modele is not None:
            self.readJson()

    def __str__(self):
        return json.dumps(self.data, indent=self.indent)

    def __repr__(self):
        return "{0} {1}".format(self.__class__, json.dumps(self.data, indent=self.indent))

    def readJson(self):
        """
        Lecture du fichier json
        """
        try:
            with open(self.modele, 'r') as f:
                # self.data = json.load(f, object_pairs_hook=OrderedDict)
                self.data = json.load(f)
        except json.decoder.JSONDecodeError as je:
            raise RegardsError("[ERROR] Incorrect file '%s'" % self.modele, je)

    def writeJson(self, data, output='stdout'):
        """
        Ecriture du fichier json
        """
        if data is None:
            data = self.data

        if output == 'stdout':
            print(json.dumps(data, indent=self.indent))
        else:
            with open(output, 'w') as f:
                json.dump(data, f, indent=self.indent)

    @staticmethod
    def replaceTag(valeur=None):
        """
        Remplace dans une string les TAGs par ses valeurs
        Les infos sont recherches respectivement :
           - Dans l'entete du modele (Constantes)
           - Dans les donnees du catalogue
        Un TAG est represente sous la forme : ${TAG}
        """
        valTag = valeur

        if type(valeur) is str:

            # Recupere la valeur reelle de la donnee
            # et recherche d'un TAG
            res = patternVariable.search(valeur)
            valType = "str"

            if res:
                # Si un TAG  est trouve
                keyTag = res.group(2)

                # Recherche d'abord dans les constantes de l'entete
                valTag = constantes.get(keyTag)

                if valTag is None:
                    # Recherche ensuite dans les donnees du catalogue
                    colonne = colonnes.get(keyTag)
                    if colonne is not None:
                        try:
                            # RC)cupC(re la valeur sur le champ
                            valTag = line[colonne.get("pos")]

                            # RC)cupC(re le type de la valeur
                            valType = colonne.get("type")
                        except IndexError:
                            raise RegardsError("[ERROR] list index out of range for '%s'" % keyTag)

                if valTag is None:
                    # Valeur du TAG non trouvee : sortie
                    raise RegardsNotFound("[ERROR] Tag is not defined for key '%s'" % valeur)

                # Reconstruction de la valeur entiere
                valTag = res.group(1) + valTag + res.group(3)

                # Conversion de type
                if valType == "int":
                    valTag = int(valTag)
                elif valType == "float":
                    valTag = float(valTag)
                elif valType == "boolean":
                    valTag = bool(valTag)

                # Recherche recursive des TAGs
                valTag = JsonObject.replaceTag(valTag)

        return valTag

    @staticmethod
    def replaceFn(valeur=None):
        """
        Calcul des fonctions
        Une fonction est representee sous la forme : $${NAME, [PARAM1, ...]}
        """
        valTag = valeur

        if type(valeur) is str:

            # Recupere la fonction et ses parametres
            # et recherche d'un TAG
            res = patternFn.search(valeur)
            if res:
                # Si une fonction est trouvee, calcul de la fonction
                valTag = functions.call(res.group(2))

                # Reconstruction de la valeur entiere
                if type(valTag) is str:
                    valTag = res.group(1) + valTag + res.group(3)

                # Recherche recursive des fonctions
                valTag = JsonObject.replaceFn(valTag)

        return valTag

    def searchTag(self, key: str, value=None):
        """
        Parcours recursif d'un arbre json pour le remplacement des TAGs
        """
        if type(value) is str:
            # Si la valeur est une string alors remplacement des TAGs
            value = JsonObject.replaceTag(value)

            # Appel des fonctions
            value = JsonObject.replaceFn(value)

        elif type(value) is dict:
            # Parcours recursif du dico
            for key, valTag in value.items():
                value[key] = self.searchTag(key, valTag)

        elif type(value) is list:
            # Parcour recursif de la liste
            idxVal = 0
            for element in value:
                value[idxVal] = self.searchTag(key, element)
                idxVal += 1

        elif value is None or type(value) is int or type(value) is float or type(value) is bool:
            # Rien a faire
            pass
        else:
            # Type not defined
            raise RegardsError('[ERROR] unknown type "%s" for Key "%s"' % (type(value), key))

        return value


class Catalog(object):

    def __init__(self, path, sep=";"):
        """

        :param path: Pattern path and filename to search
        :param sep: string separator. ';' by default.
        """
        self.path = path
        self.sep = sep

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path

    @staticmethod
    def searchCatalogFiles(path, sep=';'):
        """
        Find json files with pattern path and filename.
        Return a sorted and unique item list.

        :param path: Pattern path and filename to search
        :param sep: string separator. ';' by default.
        :return: A list of catalog found
        """
        catalogs = []
        if path == '-':
            # EntrC)e standard
            catalogs.append(Catalog(os.path.normpath("stdin"), sep))
        else:
            if not os.path.isdir(path):
                listDir = glob.glob(path)
                for file in listDir:
                    # Si rC)pertoire alors appel recursif
                    if not os.path.isdir(file):
                        # Normalise le path
                        catalogs.append(Catalog(os.path.normpath(file), sep))
        return catalogs

    def readCatalog(self, sep=None) -> List[str]:
        """
        Lecteur du fichier des catalogues

        :return: Un gC)nC)rateur de lecture d'un fichier catalog.
        """
        # try:
        if sep is None:
            sep = self.sep

        if self.path == "stdin":
            for lLine in sys.stdin:
                # Ignore les lignes vides ou les commentaires
                if patternIgnore.search(lLine): continue

                # Suppression des commentaires en fin de ligne
                # et decoupage des champs
                values = patternEndOfLine.search(lLine).group(1).split(sep=sep)
                yield values
        else:
            with open(self.path, 'r') as entry:
                for lLine in entry:
                    # Ignore les lignes vides ou les commentaires
                    if patternIgnore.search(lLine): continue

                    # Suppression des commentaires en fin de ligne
                    # et decoupage des champs
                    values = patternEndOfLine.search(lLine).group(1).split(sep=sep)
                    yield values

        # except:
        #     formatted_lines = traceback.format_exc().splitlines()
        #     print(formatted_lines[-1], file=sys.stderr)
        #     exit(1)


class Unit(Enum):
    O = (1, "o")
    KIO = (1024, "Kio")
    MIO = (1024 * 1024, "Mio")
    GIO = (1024 * 1024 * 1024, "Gio")
    TIO = (1024 * 1024 * 1024 * 1024, "Tio")

    def __init__(self, multi, label):
        self.multi = multi
        self.unit = label

    @property
    def size(self):
        return self.multi

    @property
    def label(self):
        return self.label


class Functions(object):

    @staticmethod
    def listFunctions():
        return [(val[1], val[2], val[3]) for val in Functions.functions.values() if val[2] is not None]

    def __str__(self):
        return "\n".join(Functions.listFunctions())

    def call(self, cmd):
        cmdName = []
        cmdParams = []
        try:
            # Decodage de la commande
            elts = regex.split("[ ,]+", cmd)
            cmdName = elts[0].upper()
            cmdParams.append(self)
            if elts[1] != '':
                cmdParams.extend(elts[1:])

            # Test si la fonction existe
            try:
                functions.functions[cmdName]
            except:
                listFn = "\n   ".join(
                    [val[1] + ": " + val[3] + ", syntax: " + val[2] for val in Functions.functions.values() if
                     val[2] is not None])
                message = "[ERROR] Function not found : %s\nAvailable functions : \n   %s" % (
                    cmdName, listFn)
                raise RegardsError(message)

            result = functions.functions[cmdName][0](*cmdParams)
            return result

        except (KeyError, TypeError, IndexError):
            message = "[ERROR] Syntax : %s" % functions.functions[cmdName][2]
            raise RegardsError(message)

        except Exception as ex:
            raise RegardsError("[ERROR] Function : %s" % cmdName, ex)

    def basename(self, filename):
        return os.path.basename(filename)

    def basenameid(self, filename):
        return os.path.splitext(os.path.basename(filename))[0]

    def dirname(self, filename):
        return os.path.dirname(filename)

    def md5sum(self, filename):
        # Calcul du checksum MD5
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def now(self, format="%Y-%m-%dT%H:%M:%S"):
        return dt.now().strftime(format)

    def sizeFile(self, filename, unit="O"):
        size = os.stat(filename).st_size / (Unit[unit]).size
        return int(size)

    def sizeImage(self, filename):
        # Calcul de la taille de l'image
        with Image.open(filename) as img:
            return img.size

    functions = {
        "BASENAME": [basename, "BASENAME", "$${BASENAME, <filename>}", "Return name of file"],
        "BASENAMEID": [basenameid, "BASENAMEID", "$${BASENAMEID, <filename>}",
                       "Return name of file without extension"],
        "DIRNAME": [dirname, "DIRNAME", "$${DIRNAME, <filename>}", "Return path of file"],
        "MD5SUM": [md5sum, "MD5SUM", "$${MD5SUM, <local filename>}", "Return md5 checksum"],
        "NOW": [now, "NOW", "$${NOW, [format date]}", "Return Date with format by default %Y-%m-%dT%H:%M:%S"],
        "SIZE": (sizeFile, "SIZE", "$${SIZE, <local filename> [, O|KIO|MIO|GIO|TIO}]",
                 "Return size file in unit (octet by default)"),
        "SIZEIMAGE": [sizeImage, "SIZEIMAGE", "$${SIZEIMAGE, <local filename>}",
                      "Return image size in pixel (width, heigh)"]
    }


if __name__ == "__main__":
    opts = args = None
    indent = 4
    nbFeaturesMax = 0
    sep = ";"
    outPathFile = "stdout"
    modeleFile = None
    patternFiles = None

    try:
        opts, args = getopt.getopt(argv[1:], "hvi:n:s:o:",
                                   ["help", "verbose", "indent", "number", "sep", "outPathFile"])
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
        elif opt in ("-i", "--indent"):
            indent = int(arg)
        elif opt in ("-n", "--number"):
            nbFeaturesMax = int(arg)
        elif opt in ("-s", "--sep"):
            sep = int(arg)
        elif opt in ("-o", "--outPathFile"):
            # DC)construction du nom pour le modC(le et la numC)rotation
            outPathFile, ext = os.path.splitext(arg)
        else:
            assert False, "unhandled option: %s" % (opt,)

    if len(args) < 2:
        print(__doc__)
        exit(100)

    modeleFile = args[0]
    patternFiles = args[1:]

    if _verbose:
        # Parametres d'appel
        print("Parameters: " + " ".join(argv[1:]))

    try:
        # Chargement du modele
        dataObject = JsonObject(modele=modeleFile, indent=indent)

        # Chargement de la structure des donnC)es
        struct = dataObject.data["global"]

        # Ajout des constantes COMMON par modC(le
        if struct["COMMON"].get("constantes"):
            for modelid in struct.keys():
                newModel = deepcopy(struct["COMMON"]["constantes"])
                newModel.update(struct[modelid]["constantes"])
                struct[modelid]["constantes"] = newModel
                if _verbose: print("%s: %s" % (modelid, struct[modelid]["constantes"]))

        # Ajout des colonnes COMMON par modC(le
        if struct["COMMON"].get("colonnes"):
            for modelid in struct.keys():
                newModel = deepcopy(struct["COMMON"]["colonnes"])
                newModel.update(struct[modelid]["colonnes"])
                struct[modelid]["colonnes"] = newModel
                if _verbose: print("%s: %s" % (modelid, struct[modelid]["colonnes"]))

        # PrC)paration des rC)sultats json par modC(le
        jsonResultGlobal = {i: {"nbFiles": 0, "nb": 0, "data": {}} for i in struct.keys()}
        if _debug: print("=>  Available model(s): %s\n" % jsonResultGlobal)

        # functions
        functions = Functions()

        # Indicateur du bon deroulement des remplacements
        numLine = 0
        jsonDataObject = None

        # import pdb
        # pdb.set_trace()

        # Recherche des fichiers catalogues
        listCatalogs = []
        for pattern in patternFiles:
            listCatalogs.extend(Catalog.searchCatalogFiles(pattern))

        if len(listCatalogs) == 0:
            print("No catalog found !")
            sys.exit(_OK)

        print("%d catalog(s) found: " % len(listCatalogs))
        print("\n".join([str(name) for name in listCatalogs]))
        print("\nJson file(s) created:")

        # Boucle sur tous les catalog
        for catalog in listCatalogs:
            # Lecture du fichier catalogue
            modelid = None
            for line in catalog.readCatalog():
                try:
                    numLine += 1

                    # Recupere le modele
                    modelid = line[0]
                    try:
                        jsonModel = jsonResultGlobal[modelid]

                        # Recupere la structure du modele
                        modelStruct = struct[modelid]

                    except KeyError as ke:
                        raise RegardsError("Model '%s' not found !" % modelid)

                    modeleDesc = modelStruct.get("modele_desc")

                    # Recupere les constantes
                    constantes = modelStruct.get("constantes")

                    # Recupere La dC)finition des champs du catalogue
                    colonnes = modelStruct.get("colonnes")

                    # On regarde si la limite du nombre d'objets est atteinte
                    if nbFeaturesMax != 0 and jsonModel["nb"] >= nbFeaturesMax:
                        # Ecriture du fichier et rC)initialisation d'un nouveau
                        jsonModel["nbFiles"] += 1
                        outputName = "%s_%s_%d_%d.json" % (outPathFile, modelid, jsonModel["nbFiles"], jsonModel["nb"])
                        dataObject.writeJson(data=jsonModel["data"], output=outputName)
                        print(outputName)
                        jsonModel["nb"] = 0

                    # Valorisation d'un nouveau header C  la premiC(re ligne
                    if jsonModel["nb"] == 0:
                        jsonModel["data"] = dataObject.searchTag("root",
                                                                 deepcopy(
                                                                     dataObject.data["modeles"][modeleDesc["header"]]))

                    # Chargement et valorisation du modele json des donnees depuis la racine
                    jsonDataObject = deepcopy(dataObject.data["modeles"][modeleDesc["body"]])
                    jsonDataObject = dataObject.searchTag("root", jsonDataObject)

                    # Sauvegarde dans le model appropriC)
                    jointure = jsonModel["data"]
                    for node in modeleDesc["join"]:
                        try:
                            jointure = jointure[node]
                        except Exception as te:
                            raise RegardsError("[ERROR] Check key '%s' for %s" % (node, jointure), te)

                    jointure.append(jsonDataObject)

                    # incrC)mente le nombre d'objets
                    jsonModel["nb"] += 1

                except KeyError as ke:
                    raise RegardsError(
                        "[ERROR] Key error %s at line '%d' from catalog '%s' with model '%s'" % (
                            ke, numLine, catalog, modelid), ke)

                except RegardsError as re:
                    raise RegardsError(
                        "[ERROR] at line '%d' from catalog '%s' with model '%s'" % (numLine, catalog, modelid), re)

        # Creation des derniers fichiers json
        for modelid in jsonResultGlobal.keys():
            jsonModel = jsonResultGlobal[modelid]
            if jsonModel["nb"] > 0:
                jsonModel["nbFiles"] += 1
                outputName = "%s_%s_%d_%d.json" % (outPathFile, modelid, jsonModel["nbFiles"], jsonModel["nb"])
                dataObject.writeJson(data=jsonResultGlobal[modelid]["data"], output=outputName)
                print(outputName)

    except RegardsError as we:
        print(we, file=sys.stderr)

    sys.exit(0)

