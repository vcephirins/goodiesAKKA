-- Description : Liste des packages avec les contacts tries par nom et version

-- P1 : nom du package (ex : % , outil , out%spot)
\set packageName '\'%' :P1 '%\''

select :packageVersion package, :deployedLabel,
   contact_name as "Contact",
   contact_display as "Nom",
   mail as "Mail",
   tel as "Telephone",
   title as "Fonction",
   replace(comment, E'\n', ' ') as "Commentaire"
from packages P left join contacts C using (id_package)
where upper(:packageVersion) like upper(:packageName)
order by package_name, package_version desc, package_patch desc, norder;
