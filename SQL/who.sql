set linesize 100
set pagesize 50
col username format A20
col machine format A20
select sid, username, osuser, process, machine,
    lpad(to_char(logon_time, 'DD-MON-YY HH:MM:SS'), 20)  "Logon time"
  from v$session where username is not null
  order by sid;
