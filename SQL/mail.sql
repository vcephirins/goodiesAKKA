select a.C_REQUEST_NO NUM, a.c_mail_id ID, 
       SUBSTR(B.C_STATUS_LIB, 1, 30) STATUS,
       b.c_status_delay DELAY,
       TO_CHAR(a.D_REQUEST, 'DDMMYYYY HH24:MI:SS') D_REQUEST,
       TO_CHAR(a.d_status, 'DDMMYYYY HH24:MI:SS') D_STATUS
from ss10_em_mail_request A, ss10_em_mail_status B
where a.D_REQUEST > (sysdate - 1)
and   a.c_mail_status = b.c_mail_status
order by a.C_REQUEST_NO
/
