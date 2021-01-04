
prompt *** ================================================================ ***
prompt ***                       LISTE DES TRANSACTIONS IN-DOUBT            ***
prompt *** ================================================================ ***
select DB_USER, GLOBAL_TRAN_ID, LOCAL_TRAN_ID, STATE
FROM   DBA_2PC_PENDING
order by 1
/

prompt *** ================================================================ ***
prompt ***                       PURGE DES TRANSACTION IN DOUBT             ***
prompt *** ================================================================ ***

accept reponse char format A1 prompt 'Purge automatique des transactions bloqués (O/N) ? : ';

declare
   x varchar2(1);
   cursor cur_ko is 
      select LOCAL_TRAN_ID from DBA_2PC_PENDING order by 1;
begin
   if (upper('&reponse') = 'O') then
      dbms_output.put_line ('*** ================================================================ ***');
      dbms_output.put_line ('***                      PURGE DES TRANSACTIONS BLOQUES                    ***');
      dbms_output.put_line ('*** ================================================================ ***');

      for c in cur_ko loop
         dbms_output.put_line ('>> Purge de la transaction '||c.local_tran_id);
         dbms_transaction.purge_lost_db_entry(c.local_tran_id);
         dbms_output.put_line ('.  Terminé');
      end loop;
   end if;
end;

/

commit;

/
