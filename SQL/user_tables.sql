set verify off

undefine table_name
define table_name=&table

column "Index" format a25
column "Partition" format a20
column "Tablespace" format a20
column "Position" format a8
column "Colonne" format a20
column "Status" format a6

Prompt === Indexes de la table
Prompt =======================
select A.index_name "Index", SUBSTR(C.position, 1, 3) "Position", SUBSTR(c.column_name, 1, 30) "Colonne", A.uniqueness "Unique", SUBSTR(A.status, 1, 7) "Status"
from user_indexes A, user_cons_columns C
where a.table_name = UPPER('&&Table_name')
and   C.constraint_name = a.index_name
union
select A.index_name "Index", SUBSTR(b.column_position, 1, 3) "Position", SUBSTR(b.column_name , 1, 30) "Colonne", A.uniqueness, SUBSTR(A.status, 1, 7) "Status"
from user_indexes A, user_ind_columns B
where a.table_name = UPPER('&&table_name')
and   b.index_name = a.index_name
/

Prompt === Repartition des lignes par partition
Prompt ========================================
Prompt Faire une analyse de la table si necessaire : 
Prompt analyze table <<owner>>.&&table_name compute statistics
/

column "Table" format a20
column "Blocks" format '99999990'
column "used" format '99999990'
column "% used" format '990.00'
column "avg len" format '99990' NOPRINT


SELECT table_name "Table", partition_name "Partition",
       /* tablespace_name "Tablespace", */
       num_rows "Lignes" ,
       blocks + empty_blocks "Blocks",
       blocks "used",
       blocks / (blocks + empty_blocks) * 100 "% used",
       avg_row_len "avg len"
       /*, high_value "Valeur haute" */
FROM sys.user_tab_partitions
WHERE table_name=upper('&&table_name') ORDER BY partition_position;

