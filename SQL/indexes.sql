set verify off

undefine table_name
undefine index_name

column "Index" format a25
column "Partition" format a20
column "Tablespace" format a20
column "Position" format a8
column "Colonne" format a20
column "Status" format a6

Prompt === Indexes de la table
Prompt =======================
select A.index_name "Index", SUBSTR(C.position, 1, 3) "Position", SUBSTR(c.column_name, 1, 30) "Colonne", A.uniqueness "Unique", SUBSTR(A.status, 1, 7) "Status"
from dba_indexes A, dba_cons_columns C
where a.table_name = UPPER('&&Table_name')
and   C.constraint_name = a.index_name
union
select A.index_name "Index", SUBSTR(b.column_position, 1, 3) "Position", SUBSTR(b.column_name , 1, 30) "Colonne", A.uniqueness, SUBSTR(A.status, 1, 7) "Status"
from dba_indexes A, dba_ind_columns B
where a.table_name = UPPER('&&Table_name')
and   b.index_name = a.index_name
/

Prompt === Analyse de profondeur de l'index
Prompt ====================================

analyze index &&index_name validate structure
/

Prompt === l'index est degrade si :
Prompt === Prof. > 5 ou occupation < 70% ou suppression > 10%
Prompt ===  => alter index &&index_name shrink space;
Prompt ===  => alter index &&index_name rebuild partition <partition name>;
Prompt ===  => alter index &&index_name coalesce partition;

select name "Index", blocks "Alloues", lf_blks+ br_blks "Occupes", to_char(height, '9999') "Prof." , pct_used "% occupation", round(decode(lf_rows, 0, 0, del_lf_rows/lf_rows*100)) "% suppression"
from index_stats where name = upper('&&index_name')
/

Prompt === Repartition des lignes par partition
Prompt ========================================
analyze index &&index_name compute statistics
/

SELECT index_name "Index", partition_name "Partition",
       /* tablespace_name "Tablespace", */
       num_rows "Lignes", distinct_keys "distinctes",
       to_char(decode(num_rows, 0 , 0, (distinct_keys / num_rows) * 100), '990.00') "      %"
       /*, high_value "Valeur haute" */
FROM sys.dba_ind_partitions
WHERE index_name=upper('&&index_name') ORDER BY partition_position;

