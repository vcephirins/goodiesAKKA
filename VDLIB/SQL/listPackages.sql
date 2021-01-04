-- Description : Liste des packages tries par nom et version

-- P1 : nom du package (ex : % , outil , out%spot)
\set packageName '\'%' :P1 '%\''

select P.id_package, :packageVersion package, :deployedLabel, :validatedLabel,
   date_create as "Creation",
   date_delivery as "Livraison",
   date_deployed as "Deploiement",
   date_deleted as "Suppr.",
   replace(reason, E'\n', ' ') as "raison",
   replace(description, E'\n', ' ') as "Description"
from packages P
where upper(:packageVersion) like upper(:packageName)
order by package_name, package_version desc, package_patch desc;
