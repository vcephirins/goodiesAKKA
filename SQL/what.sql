set pagesize 50
set linesize 80
col v$session.username format A20
col v$sql.sql_text heading REQUEST newline
select v$session.sid, v$session.osuser, v$session.username, v$sqlarea.sql_text
 from v$session, v$sqlarea
 where v$sqlarea.address = v$session.sql_address and
       v$sqlarea.hash_value = v$session.sql_hash_value and
       v$session.username is not null
 order by v$session.sid;
