-- Description : Liste des contacts / packages

-- P1 : nom du contact (ex : % , cdpp )
\set contactName '\'%' :P1 '%\''

select :packageVersion package, :deployedLabel,
   contact_name as "Contact",
   contact_display as "Nom",
   mail as "Mail",
   tel as "Telephone",
   title as "Fonction",
   replace(comment, E'\n', ' ') as "Commentaire"
from packages P, contacts C
where upper(contact_name) like upper(:contactName)
and   C.id_package = P.id_package
order by P.package_name, P.package_version desc, P.package_patch desc, norder

