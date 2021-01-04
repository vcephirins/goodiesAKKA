-- Description : Liste des packages non valides

select id_package, :deployedLabel, :packageVersion package, date_delivery as livraison 
from packages P
where validated = false
order by package_name, 2 desc, 1;
