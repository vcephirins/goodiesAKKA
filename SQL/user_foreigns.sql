set verify off

undefine table_name
undefine index_name

column "Name" format a30
column "Type" format a7
column "Table" format a30
column "ref indexe" format a30
column "ref table" format a30
column "ref colonne" format a30

Prompt === Foreign key de la table
Prompt ===========================
select A.TABLE_NAME "Table", 
       A.CONSTRAINT_NAME "Name", 
       A.R_CONSTRAINT_NAME "ref indexe",
       C.TABLE_NAME "ref table",
       C.COLUMN_NAME "ref colonne"
from user_constraints A, user_ind_columns C
where A.table_name like UPPER('%&&Table_name%')
and A.CONSTRAINT_TYPE = 'R'
and C.index_name = A.r_constraint_name
order by "Table", "Name"
/

