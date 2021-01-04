set verify off
set linesize 200
set maxdata  60000
set arraysize 30

ACCEPT table PROMPT '   Table = '

SELECT A.num_rows, A.blocks, A.empty_blocks,
       A.avg_space, A.chain_cnt, A.avg_row_len
FROM   DBA_TABLES A
WHERE  A.TABLE_NAME = UPPER('&table')

/

SELECT B.BYTES/1024 "Ko",
       C.INITIAL_EXTENT/1024 "IE",
       C.NEXT_EXTENT/1024 "NE",
       C.PCT_INCREASE,
       C.PCT_FREE,
       C.PCT_USED,
       B.EXTENTS
FROM   DBA_TABLES C, DBA_SEGMENTS B
WHERE  C.TABLE_NAME = B.SEGMENT_NAME
AND    C.TABLE_NAME = UPPER('&table')

/

SELECT SUBSTR(C.INDEX_NAME, 1, 15) INDEXE,
       SUBSTR(C.TABLESPACE_NAME, 1, 8) TABLESPC,
       C.INITIAL_EXTENT/1024 "IE",
       C.NEXT_EXTENT/1024 "NE",
       SUBSTR(C.PCT_INCREASE, 1, 5) INCR ,
       C.PCT_FREE,
       B.EXTENTS
FROM   DBA_INDEXES C, DBA_SEGMENTS B
WHERE  C.TABLE_NAME = UPPER('&table')
AND    B.SEGMENT_NAME = C.INDEX_NAME

/

