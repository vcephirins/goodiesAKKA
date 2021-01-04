set verify off
set linesize 80
set pagesize 4000

ACCEPT node PROMPT 'Data set : '
ACCEPT critere PROMPT 'Critere : '

column "Data Set" format a64
column "Nombre de ref." format 99999

select C.node_identifier "Data Set", count(A.node_identifier) "Nombre de ref."
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
group by C.node_identifier
;

column "Nombre de Data Set" format 99999
column "Total de ref." format 9999999

select count(C.node_identifier) "Nombre de Data Set", 
       sum(count(A.node_identifier)) "Total de ref."
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
group by C.node_identifier
;

