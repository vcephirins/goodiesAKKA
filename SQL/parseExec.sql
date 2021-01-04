set verify off
set linesize 500
set pagesize 0

ACCEPT text PROMPT 'search : '

-- spool parseExec

PROMPT    ___NB_EXEC NB_FETCHES     NB_ROWS

PROMPT    ____TEXT
PROMPT    --------

SELECT 
--  PARSE_EXEC
  vs.executions NB_EXEC,
  vs.FETCHES NB_FETCHES,
  rows_processed NB_ROWS ,
--    vs.first_load_time first_load_time,
--  vs.command_type  ,
--  OPTIMIZER_MODE  ,
  vs.sql_text TEXT
FROM 
  v$sqlarea vs
WHERE 
  (parsing_user_id != 0)
  and (executions >= 1)
  and (parsing_user_id = userenv('SCHEMAID'))
  and (InStr(Upper(sql_text), upper('&text'))>0)
  and (sql_text not like 'SELECT --  PARSE_EXEC%'
    and sql_text not like 'EXPLAIN %')
order by   buffer_gets/executions desc
/

-- spool off

start init

-- !more parseExec.lst
