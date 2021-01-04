set verify off
set linesize 200
set maxdata  60000
set arraysize 30

ACCEPT table PROMPT '   Table = '

SELECT C.INDEX_NAME,
       C.STATUS,
       SUBSTR(C.TABLESPACE_NAME, 1, 8) TABLESPC,
       C.INITIAL_EXTENT/1024 "IE",
       C.NEXT_EXTENT/1024 "NE",
       C.PCT_INCREASE,
       C.PCT_FREE
FROM   DBA_INDEXES C
WHERE    C.TABLE_NAME = UPPER('&table')

/


