cd $OUTILS_SVA/SQL
sqlplus -s $ORACLE_OWNER/$ORACLE_PWD <<EOF
whenever sqlerror exit 2
@init

set timing on;

$*;
exit 0;
EOF

