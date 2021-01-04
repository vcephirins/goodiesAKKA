set linesize 80

undefine index_name

column "Index" format a20
column "Partition" format a20
column "Tablespace" format a20

Prompt === Repartition des lignes par partition
Prompt ========================================
SELECT index_name "Index", partition_name "Partition",
       /* tablespace_name "Tablespace", */ 
       num_rows "Lignes", distinct_keys "distinctes", 
       to_char(decode(num_rows, 0 , 0, (distinct_keys / num_rows) * 100), '990.00') "%"
       /*, high_value "Valeur haute" */ 
FROM sys.dba_ind_partitions 
WHERE index_name=upper('&&index_name') ORDER BY partition_position;

