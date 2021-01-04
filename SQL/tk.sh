#!/bin/ksh
OLD_PWD=$PWD
cd $ADMIN_GAIA/bdump
name=$(basename $(ls -rt $(print ${1:-'*'}.trc) | awk '/trc$/{print $1;exit}'))
if [[ "$name" == "." ]]
then
   print pas de fichier !
   exit 0;
fi;

sed /APPNAME/d $name > $OLD_PWD/result.trc
cd $OLD_PWD
tkprof result.trc result.res explain=$ORACLE_OWNER/$ORACLE_OWNER sys=no
rm result.trc
rm $name #>/dev/null 2>&1
name=result_$(date +"%Y%m%d_%H%M%S").res
mv result.res $name
cat $name

