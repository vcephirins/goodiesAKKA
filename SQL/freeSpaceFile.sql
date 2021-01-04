set verify off
set linesize 80

undefine TS_NAME;

column "Name" format a30

SELECT /*+ use_hash(d v) */ 
       regexp_replace(d.file_name, '.*/', '') "Name", 
       v.status "Status", 
       TO_CHAR((d.bytes / 1024 / 1024), '99999990.000') "Size (M)", 
       TO_CHAR(NVL(d.bytes - s.bytes, 0) / 1024 / 1024, '99999990.000') "Used (M)",
       to_char((nvl(d.bytes - s.bytes, 0) / d.bytes) * 100, '990.00') "% used"
FROM sys.dba_data_files d, 
     v$datafile v, 
     (SELECT file_id, SUM(bytes) bytes  FROM sys.dba_free_space  
--      WHERE tablespace_name like upper('%&&TS_NAME%') 
      GROUP BY file_id) s 
WHERE (s.file_id (+)= d.file_id) 
AND (d.tablespace_name like upper('%&&TS_NAME%'))
AND (d.file_name = v.name)
order by Name
/

