select max(n_seq_supervise) from ss10_task_followup
/

select A.n_task_id, A.c_task_status, 
substr(to_char(A.d_event_task, 'DD-MM-YYYY:HH24:MI:SS'), 1,19) D_EVENT_DATE, 
substr(nvl(A.t_oraerr_label, B.t_task_label), 1, 60) LIBELLE
from ss10_task_followup A, ss10_task_def B
where A.n_seq_supervise  = &n_seq_supervise
and B.n_task_id(+) = A.n_task_id
and B.C_SCHEDULER_id(+) = a.c_scheduler_id
order by A.d_event_task,A.c_task_rnk
/

