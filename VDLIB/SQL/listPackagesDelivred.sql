-- Description : Liste des packages livres a la VDLIB depuis une date donnee

-- P1 : Date  (ex : % , 2015-01-01)
--\set fromDate  case ':P1' when '%' then '2001-01-01' else ':P1' end
\set fromDate  '\'' :P1 '\''

select :packageVersion as "Nom du package", 
   date_create as "Creation",
   date_delivery as "Livraison", 
   date_deployed as "Deploiement",
   case when date_deleted is not null then date_deleted else date_deployed end as "M.A.J",
   date_deleted as "Suppr.",
   :validatedLabel, :deployedLabel,
   replace(reason, E'\n', ' ') as Raison
from packages 
where date_delivery >= :fromDate
or    date_deployed >= :fromDate
or    date_deleted >= :fromDate
order by 5;
