# coding: utf-8
"""generateQuicklook.py - Generate quicklook from image file

Use : python generateQuicklook.py [-h|--help]
         [-o|--outdir <path>]
         [-f | --format <extension>]
         [-s | --size <width x height>]
         [-S | --fixedSize <width x height>]
         [-s | --rotate <degree>]
         <imagefile> <type ...>

[-h] or [--help] : This help
[-o | --outdir] Path to save generated quicklook
[-f | --format] Output format with extension ("png" (default), jpg", "tiff", "gif", "bmp", "pdf")
[-s | --size] Force size of generated quicklook with same ratio
[-S | --fixedSize] Force size of generated quicklook with exactly width and height
[-r | --rotate] Rotates the image with number of degrees in counter clockwise direction
<imagefile> Path for accessing to image source <path>/<imagename>
<type ...>  One or more type of quicklook to generate: 'A' (128x128), 'B" (264x403), 'C' (621x950) or "TN' (thumbnail)

ex :
     # Generate quicklooks A, B, C and thumbnail
     python generateQuicklook.py monImage.gif A B C TN

     # Generate quicklook B with jpeg format and size 125x110 (keep ratio)
     python generateQuicklook.py --format jpg --size 125x110 monImage.gif B

     # Generate quicklook B with jpeg format and exactly size 125x110
     python generateQuicklook.py --fixedSize 125x110 monImage.gif B
"""

# IMPORT
from builtins import isinstance
import sys, os, getopt

from PIL import Image

# Définition des tailles Quicklook pour le SIPAD
ImagesProp = {
    # "dpi", "sizeinch", "extension"
    "default": (100, 2.36, "png"),
    # "suffiwe", "format", "taille(width, height)"
    "TN": ("tn", "png", (128, 128)),
    "A": ("A", "png", (128, 128)),
    "B": ("B", "png", (264, 403)),
    "C": ("C", "png", (621, 950)),
    }

#=======================================================================================================================
# generateImage
#=======================================================================================================================
def generateImage(image, prop, suffixe=None, ext=None, size=None, fixedSize=None, rotate=None):
    # Valeurs par défaut
    propDpi, propInch, propFormat = ImagesProp.get("default")
    disposition = 0   # Protrait
    propSuffixe = ""
    tn = False        # Thumbnail à False

    # Calcul de la disposition en fonction de l'image source
    if image.width > image.height:
        # Paysage
        disposition = 1

    if isinstance(prop, str):
        # Le nom de du type d'image est fourni
        propSuffixe, propFormat, propSize = ImagesProp.get(prop.upper())
        if prop.upper() == "TN": tn = True
    else:
        # Propiétés specifiques
        propSuffixe, propFormat, propSize = prop

    if disposition == 0:
        propSize = propSize
    else:
        propSize = propSize[::-1]

    # Valeurs independantes spécifiques
    if suffixe is not None: propSuffixe = suffixe
    if ext is not None: propFormat = ext

    # Calcul de la taille
    if fixedSize is not None:
        propSize = fixedSize
    else:
        if size is not None:
            propSize = size

        # Calcul de conservation des proportions
        width, height = propSize
        if disposition == 1:
            coef = image.width / width
            propSize = (width, int(image.height / coef))
        else:
            coef = image.height / height
            propSize = (int(image.width / coef), height)

    if tn:
        fig = image.thumbnail(propSize, Image.LANCZOS)
        fig = image
    else:
        fig = image.resize(propSize, Image.LANCZOS)

    if rotate is not None:
        fig = fig.rotate(rotate, expand=1)

    # Calcul du nouveau suffixe
    extension = propSuffixe + "." + propFormat

    return (fig, extension)


if __name__ == '__main__':
    outdir = "."
    fmt = None
    size=None
    fixedSize=None
    rotate=None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:f:s:S:r:", ["help", "outdir", "format", "size", "fixedSize", "rotate"])
    except getopt.GetoptError as err:
            print(err)
            print(__doc__)
            sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(__doc__)
            sys.exit()
        elif opt in ("-o", "--outdir"):
            outdir = arg
        elif opt in ("-f", "--format"):
            fmt = arg
        elif opt in ("-s", "--size"):
            size = arg.split("x")
            if len(size) != 2:
                print(__doc__)
                sys.exit(2)
            size = [int(size) for size in size]
        elif opt in ("-S", "--fixedSize"):
            fixedSize = arg.split("x")
            if len(fixedSize) != 2:
                print(__doc__)
                sys.exit(2)
            fixedSize = [int(size) for size in fixedSize]
        elif opt in ("-r", "--rotate"):
            rotate = int(arg)
        else:
            assert False, "unhandled option"

    if len(args) < 2:
        print(__doc__)
        sys.exit(2)

    imageSrc = args[0]
    image = Image.open(imageSrc, "r")

    # read info from filename
    dirname, basename = os.path.split(imageSrc)
    basename, ext = os.path.splitext(basename)

    # Trier la liste pour que le format TN doit toujours être en dernier (modifie l'image source)
    listFmt = args[1:]
    listFmt.sort()
    listKeys =  tuple(ImagesProp.keys())

    for type in listFmt:
        if type not in listKeys:
            print("format error: %s" % (type,))
            print(__doc__)
            sys.exit(2)

    for type in listFmt:
        ql, ext = generateImage(image, type, ext=fmt, size=size, fixedSize=fixedSize, rotate=rotate)
        savename = "%s/%s%s" % (outdir, basename, ext)
        ql.save(savename)

