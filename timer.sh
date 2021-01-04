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

# v�rification des param�tres
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

# v�rifications li�es au PID
# par d�faut, le PID est le PID du parent
[[ ${_SHELL_PID} ]] || _SHELL_PID=${PPID}

# v�rification du format & de l'existence du process
[[ ${_SHELL_PID//[0-9]} ]] && {
	# erreur dans le format attendu
	echo "Num�ro de PID '${_SHELL_PID}' erron� !" >&2
	exit 1
}

# le PID existe-t-il ?
ps -p ${_SHELL_PID} &>/dev/null || {
	# echo "Aucun processus pour le PID '${_SHELL_PID}'" >&2
	exit 1
}	

# V�rification du signal � passer
[[ ${_SHELL_SIG} ]] || _SHELL_SIG=SIGUSR1

# pr�cautions d'usage
_SHELL_SIG="${_SHELL_SIG^^}"
_SHELL_SIG="SIG${_SHELL_SIG#SIG}"

_SIG_LISTE="$(builtin kill -l)"
# on v�rifie si c'est un signale valide
[[ "${_SIG_LISTE}" == *${_SHELL_SIG}\)* || "${_SIG_LISTE}" == *\)\ ${_SHELL_SIG}[[:space:]]* ]] || {
	echo "Signal '${_SHELL_SIG}' non valide !" >&2
	exit 1
}

# v�rification du d�lai
# par d�faut, le timestamp est de 60sec
[[ ${_SHELL_TIMESTAMP} ]] || _SHELL_TIMESTAMP=60
[[ ${_SHELL_TIMESTAMP//[0-9]} ]] && {
	# erreur dans le format attendu
	echo "D�lai '${_SHELL_TIMESTAMP}' non valide !" >&2
	exit 1
}
startTimer
