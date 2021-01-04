
col g_user      format a10
col what        format a25
col interval    format a25
set serverout on

prompt *** ================================================================ ***
prompt ***                       LISTE DES JOBS BLOQUES                     ***
prompt *** ================================================================ ***
select 
JOB, 
LOG_USER               ,
WHAT                   ,
INTERVAL               ,
LAST_DATE              ,
LAST_SEC               ,
NEXT_DATE              ,
NEXT_SEC               ,
TOTAL_TIME             ,
BROKEN                 ,
FAILURES               
from dba_jobs
where broken = 'Y'
order by 1
/

-- *** ================================================================ ***
-- ***                      RELANCE DES JOBS BLOQUES                    ***
-- *** ================================================================ ***

accept reponse char format A1 prompt 'Relance automatique des Jobs bloqués (O/N) ? : ';

declare
   x varchar2(1);
   cursor cur_ko is 
      select JOB from dba_jobs where broken = 'Y' order by 1;
begin
   if (upper('&reponse') = 'O') then
      dbms_output.put_line ('*** ================================================================ ***');
      dbms_output.put_line ('***                      RELANCE DES JOBS BLOQUES                    ***');
      dbms_output.put_line ('*** ================================================================ ***');

      for c in cur_ko loop
         dbms_output.put_line ('>> Relance et exécution du job '||c.job);
         dbms_job.broken(c.job, FALSE, sysdate+1/(24*12));
         dbms_output.put_line ('.  Terminé');
      end loop;
   end if;
end;
/

commit;

/
