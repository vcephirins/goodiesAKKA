set verify off
set linesize 130
set pagesize 4000

ACCEPT node PROMPT 'Data set : '
ACCEPT critere PROMPT 'Critere : '

column "Data Set" format a64
column "Reference" format a64

select C.node_identifier "Data Set", A.node_identifier "Reference"
from t_entity C, ta_data_set_data B, t_entity A
where A.entity_id in (
   select data_object_id 
   from ta_data_set_data 
   where data_set_id in (
      select entity_id 
      from t_entity C
     where node_identifier like upper('%&node%')))
and A.node_identifier like '%&critere%'
and B.data_object_id = A.entity_id
and C.entity_id = B.data_set_id
order by C.node_identifier
;
