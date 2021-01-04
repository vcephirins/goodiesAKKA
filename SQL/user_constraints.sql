set verify off

undefine table_name
undefine index_name

column "Name" format a25
column "Type" format a7
column "Table" format a20
column "Status" format a7
column "reference" format a25

Prompt === contraintes de la table
Prompt ===========================
select C.CONSTRAINT_NAME "Name", 
       DECODE(C.CONSTRAINT_TYPE, 'U', 'UNIQUE', 'P', 'PRIMARY', 'C', 'CHECK', 'R', 'FOREIGN', 'AUTRE') "Type", 
       C.TABLE_NAME "Table", status "Status", R_CONSTRAINT_NAME "Reference"
from user_constraints C
where table_name like UPPER('%&&Table_name%')
order by "Table", "Name"
/

