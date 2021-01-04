select sid, serial#, process, substr(username, 1, 15) username, 
   decode(taddr, NULL, '', 'Oui ') en_cours, substr(machine, 1, 30) machine, 
   substr(program, 1, 30) program, substr(module, 1, 20) module
from v$session
order by username desc, en_cours;

