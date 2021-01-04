set verify off
set linesize 80

undefine TS_NAME

column "TS Name" format a20
column "Path Name" format a80 NOPRINT
column "File Name" format a20
column "Size (M)" format '99,999,990.900'
column "Used (M)" format '99999990.000'
column "% used" format '990.00'

SELECT d.status "Status", d.tablespace_name "TS Name", 
       d.extent_management "Extent Management", 
       NVL(a.bytes / 1024 / 1024, 0) "Size (M)", 
       NVL(a.bytes - NVL(f.bytes, 0), 0)/1024/1024 "Used (M)", 
       NVL((a.bytes - NVL(f.bytes, 0)) / a.bytes * 100, 0) "% used"
FROM sys.dba_tablespaces d, 
     (select tablespace_name, sum(bytes) bytes 
      from dba_data_files 
      group by tablespace_name) a, 
     (select tablespace_name, sum(bytes) bytes 
      from dba_free_space 
      group by tablespace_name) f 
WHERE d.tablespace_name = a.tablespace_name(+) 
AND d.tablespace_name = f.tablespace_name(+) 
AND NOT (d.extent_management like 'LOCAL' AND d.contents like 'TEMPORARY') 
OREDER BY 2
/

