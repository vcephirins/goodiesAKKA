#!/bin/bash -f
#

#s*****************************************************************************
#s*
#s* SHELL FILENAME : utils.bash
#s*
#s* ROLE :  fonctions utilitaires
#s*
#s* AUTEUR : V. Cephirins (AKKA IS)
#s* PARAMETRES :
#s* SYNOPSIS :
#s*
#s*****************************************************************************

#set -v
#set -x

#VDLIB_HOST="http://tu-mutcalc-pc:8011"
VDLIB_HOST="http://10.120.10.5:8011"
VDLIB_REQUEST="${VDLIB_HOST}/vdlib_www/src/pgsql.php"
VDLIB_CMD="${VDLIB_HOST}/vdlib_www/src/execCmd.php"

# Declaration des constantes
# Liste des repertoires pour la VDLIB
typeset -x VDLIB_REP="configuration fonctions scripts documentation Icones executables library pages_html StyleSheet download"
typeset -x VDLIB_COMPOSANT="fonctions scripts executables"

# Declaration des variables
typeset -xi C_RET=0;

# Declaration du repertoire racine de la vdlib
VDLIB_UTILS_PATH=`dirname $0`                  # Repertoire de l'outil

# INFO LOG function
###################
function fInfoLog {
INFO_DATE=`date '+20%y/%m/%d - %H:%M:%S'`;
INFO_CMD=$(basename $1)
shift
echo "[$INFO_DATE] - $USER from ${HOSTNAME}:/$PWD call '$INFO_CMD' whith  '$@'" >> $VDLIB_PATH/logs/vdlib.log 2>/dev/null
echo "[$INFO_DATE] - $USER from ${HOSTNAME}:/$PWD call '$INFO_CMD' whith  '$@'"
return 0
}

# END function
##############
function fEndProc {
   C_RET=${1:-0};
   if [[ $C_RET -eq 0 || $C_RET -eq 999 ]]
   then
      [[ "$2" != "" ]] && echo $2 >&2
      C_RET=0;
   else
      echo ${2:-"ERROR !"} >&2
   fi;

   exit $C_RET
}

# TEST ERROR function
#####################
function fError {
   C_RET=$?
   if [[ $C_RET -ne 0 ]]
   then
      fEndProc $C_RET "$1";
   fi;
}

# CONFIRM function
##################
function fConfirm {

    typeset -l reponse='';
    while [[ $reponse = '' ]]
    do
       echo ""
       echo ${1:-Confirm}" (y/n/q)."
       printf "Default value 'y' : ";read reponse
       echo ""
       case ${reponse:=y} in
          y) return 0;;
          n) return 1;;
          q) echo "  => Break\n";
             return 2;;
          *) echo "unauthorized value."
             echo "Possible values 'y', 'Y', 'n', 'N', 'q', 'Q'."
             reponse='';;
       esac
    done
}

# VALID function
################
function fValid {

    typeset reponse='';
    while [[ $reponse = '' ]]
    do
       echo ""
       echo ${1:-Confirm}" (y /n /q /Y (Yes for all) /N (No for all))."
       printf "Default value 'y' : ";read reponse
       echo ""
       case ${reponse:=y} in
          y) return 0;;
          Y) return 3;;
          n) return 1;;
          N) return 4;;
          q | Q) echo "  => Break\n";
             return 2;;
          *) echo "unauthorized value."
             echo "Possible values 'y', 'Y (All)', 'n', 'N (All)', 'q', 'Q'."
             reponse='';;
       esac
    done
}

#sf****************************************************************************#
#sf*
#sf* SHELL FUNCTION : Differentes fonctions d'utilisation d'un tableau
#sf*
#sf* ERRORS CODES
#sf*    0  : Ok
#sf*
#sf****************************************************************************#
function fTabCount
{
[[ $# -le 0 ]] && return 1
eval echo \${#${1}[*]}
return 0
}

function fTabGetList
{
[[ $# -le 0 ]] && return 1
for vValue in $(eval echo \${${1}[*]});
do
   echo $vValue;
done

return 0
}

function fTabGetListUnique
{
[[ $# -le 0 ]] && return 1
for vValue in $(eval echo \${${1}[*]});
do
   echo $vValue;
done | sort -u

return 0
}

function fTabGetValue
{
[[ $# -le 1 ]] && return 1
#eval echo \${${1}[$2]}
echo \${${1}[$2]}
return 0
}

function fTabGetIndex
{
[[ $# -le 1 ]] && return 1
typeset -i idxVal=0
typeset -i idxValMax=${3:-4096}
while [[ $idxVal -lt ${idxValMax} ]];
do
   expr "$2" : "$(eval echo \${${1}[idxVal]})" >/dev/null
   [[ $? -eq 0 ]] && break;
   idxVal=idxVal+1
done
if [[ $idxVal -ge ${idxValMax} ]]
then
   echo -1
else
   echo $idxVal
fi

return 0
}

# READ VALUES KEY 
##################
function fGetValuesKey {

 # Fonction de lecture des valeurs d'une clef dans un fichier
 # La clef doit commencer obligatoirement sur la 1ere colonne
 # Plusieurs valeurs sont acceptees : 1 valeur par ligne
 # ex : CLEF=val1
 #      CLEF = val1
 #             val2

 if [[ $# -ne 2 || ( "$1" != "-" && ! -f $1 ) ]]
 then
    echo " fGetValuesKey <file> <key>" >&2
    C_RET=1
    return $C_RET
 fi

 if [[ "$1" == "-" ]]
 then
    FILE=
 else
    FILE=$1
 fi;

 KEY=$2

 awk 'BEGIN {flag=0;}
   /^ *(#.*)*$/ {next;}
   /^'$KEY' *=/ {flag=1;sub("^'$KEY' *= *", "");if($0 != "") print $0; next}
   /^[^ ].*=/ {if (flag == 1) flag=0;next;}
   /.*/ {if (flag == 1) {sub("^ *", ""); print $0;}}
   ' $1

   C_RET=$?
   return $C_RET
}

# CUT STRING into ELEMENTS
function fCut {

 # Fonction de decoupage d'une chaine en elements separes par un espace
 # selon les tailles passees en parametre.
 # ex: fCut 20080415 4 2 2
 # retourne : 2008 04 15

   if [[ $# -le 2 ]]
   then
      echo " fCut <String> s1 s2 ..." >&2
      echo " ex: fCut 20080415 4 2 2 | read YY MM DD"
      C_RET=1
      return $C_RET
   fi

   entree=$1
   shift
   typeset -i size=${#entree}
   typeset -i nbParam=$#
   typeset -i offset=1
   typeset -i length=$1
   while [[ $nbParam -ne 0 ]]
   do
      echo $entree | cut -c$offset-$length
      offset=length+1
      nbParam=nbParam-1
      shift
      if [[ "$1" == "" ]]
      then
         [[ ${offset} -le ${size} ]] && echo $entree | cut -c$offset-
      else
         length=length+$1
      fi
   done | while read elt
   do
      printf "%s " $elt
   done
   echo
}


#trap sigint (2) & sigquit (3)
trap "fEndProc 1 'Processus arrete !'" 2 3

#trap EXIT (0)
#trap DEBUG ( ) : Apres chaque commande
#trap ERR   ( ) : Sur chaque retour de function != 0

