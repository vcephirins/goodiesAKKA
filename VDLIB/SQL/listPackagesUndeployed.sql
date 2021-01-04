-- Description : Liste des packages non valides

select id_package, :validatedLabel, 
   date_create as "Creation",
   date_delivery as "Livraison",
   date_deployed as "Deploiement",
   date_deleted as "Suppr.",
   :packageVersion as "Nom du package"
from packages P
where deployed = false
order by package_name, 2 desc;
