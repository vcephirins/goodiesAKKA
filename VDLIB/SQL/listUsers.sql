-- Description : Liste des utilisateurs declares

\set adminLabel 'case when admin = true then \'Admin\' else \'-\' end as admin'

select id_user, login, password, mail, :adminLabel
from users
order by 2 ;
