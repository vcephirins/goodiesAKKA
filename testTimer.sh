#!/bin/bash

trap fUsr1 SIGUSR1
trap fAwake SIGALRM
trap fAbrt SIGABRT

typeset -i cpt=0
typeset -i lCurrentTime=$(date "+%s")

function fUsr1 {
   typeset -i lElapsedTime=$(date "+%s")-${lCurrentTime};
   echo "Elapsed time: "$(date -d "@${lElapsedTime}" "+%Mm %Ss")
}

function fAwake {
   typeset -i lElapsedTime=$(date "+%s")-${lCurrentTime};
   echo "=> Reveil: "$(date -d "@${lElapsedTime}" "+%Mm %Ss")
}

function fAbrt {
   typeset -i lElapsedTime=$(date "+%s")-${lCurrentTime};
   echo "=> Timeout: "$(date -d "@${lElapsedTime}" "+%Mm %Ss")
   exit 1
}

# Info
coproc TIMER1 { ./timer.sh -t 2 -p $$ ; }

# timeout
# coproc TIMEOUT { ./timer.sh -s SIGKILL -t 10 -p $$; }
coproc TIMEOUT { ./timer.sh -s SIGABRT -t 10 -p $$; }

# Reveil
coproc AWAKE { ./timer.sh -s SIGALRM -t 3 -p $$; }

echo ${TIMER1_PID}
echo ${TIMEOUT_PID}
echo ${AWAKE_PID}

for cpt in {1..15}
do
	ps -f -p $TIMER1_PID --no-headers
	ps -f -p $TIMEOUT_PID --no-headers
	ps -f -p $AWAKE_PID --no-headers
	# sleep 20
        sleep 1
done
