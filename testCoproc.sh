#!/bin/bash

# The simplified example that demonstrates usefulness of two coproc to
# implement "forked pipe". If the line matches in some bash evaluation (in
# bash), it is sent to one filter coproc, if it is evaluated as
# non-matching, it is sent to another coproc. You will see the warning
# here, but the script itself seems to work.

# Clone stdout to 3
exec 3>&1
# Run TRA filtering letter "a"
coproc TRA ( sed s/a/A/g >&3 )
# Run TRB filtering letter "b"
coproc TRB ( sed s/b/B/g >&3 ) 

while read ; do
        case $REPLY in
        /* )
                echo "$REPLY" >&${TRB[1]}
                ;;
        * )
                echo "$REPLY" >&${TRA[1]}
                ;;
        esac
done

# Close input (otherwise script will not end on EOF).
eval exec ${TRA[1]}\>\&-
eval exec ${TRB[1]}\>\&-

# Wait to finish (otherwise script will output data after its return).
wait
echo "End"
