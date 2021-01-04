#!/bin/bash 

_SHELL_PID=
_SHELL_SIG=SIGUSR1
_SHELL_TIMESTAMP=60

function startTimer {
	while sleep ${_SHELL_TIMESTAMP}s
	do
		# on envoie le signal uniquement si le process existe toujours
		ps -p ${_SHELL_PID} &>/dev/null || return 0
		
		builtin kill -${_SHELL_SIG} ${_SHELL_PID}		
	done
}

# vérification des paramétres
while getopts :s:p:t: option 
do
	case "${option}" in
		p) _SHELL_PID=${OPTARG};;
		s) _SHELL_SIG=${OPTARG};;		
		t) _SHELL_TIMESTAMP=${OPTARG};;
		:) echo "Argument manquant pour l'option '${OPTARG}'" >&2
			exit 1;;
		"?") echo "Option non valide : ${OPTARG}." >&2
			exit 1;;
	esac
done

# vérifications liées au PID
# par défaut, le PID est le PID du parent
[[ ${_SHELL_PID} ]] || _SHELL_PID=${PPID}

# vérification du format & de l'existence du process
[[ ${_SHELL_PID//[0-9]} ]] && {
	# erreur dans le format attendu
	echo "Numéro de PID '${_SHELL_PID}' erroné !" >&2
	exit 1
}

# le PID existe-t-il ?
ps -p ${_SHELL_PID} &>/dev/null || {
	# echo "Aucun processus pour le PID '${_SHELL_PID}'" >&2
	exit 1
}	

# Vérification du signal à passer
[[ ${_SHELL_SIG} ]] || _SHELL_SIG=SIGUSR1

# précautions d'usage
_SHELL_SIG="${_SHELL_SIG^^}"
_SHELL_SIG="SIG${_SHELL_SIG#SIG}"

_SIG_LISTE="$(builtin kill -l)"
# on vérifie si c'est un signale valide
[[ "${_SIG_LISTE}" == *${_SHELL_SIG}\)* || "${_SIG_LISTE}" == *\)\ ${_SHELL_SIG}[[:space:]]* ]] || {
	echo "Signal '${_SHELL_SIG}' non valide !" >&2
	exit 1
}

# vérification du délai
# par défaut, le timestamp est de 60sec
[[ ${_SHELL_TIMESTAMP} ]] || _SHELL_TIMESTAMP=60
[[ ${_SHELL_TIMESTAMP//[0-9]} ]] && {
	# erreur dans le format attendu
	echo "Délai '${_SHELL_TIMESTAMP}' non valide !" >&2
	exit 1
}
startTimer
