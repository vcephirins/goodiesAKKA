-- Description : Liste des packages par responsables

-- P1 : nom du responsable (ex : sipad )
\set userName '\'%' :P1 '%\''

select U.login as "Responsable", :packageVersion package,
   date_create as "Creation",
   date_delivery as "Livraison",
   date_deployed as "Deploiement",
   replace(description, E'\n', ' ') as "Description"
from packages P, users U
where upper(login) like upper(:userName)
and   P.id_responsible = U.id_user
and   P.deployed = true
order by 1, package_name, package_version desc, package_patch desc;
