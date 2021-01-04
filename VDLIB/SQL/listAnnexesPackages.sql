-- Description : Liste des packages par annexes tries par nom et version

-- P1 : annexe name (ex : % , doc)
\set annexeName '\'%' :P1 '%\''

select P.id_package, :packageVersion package, A.annexe_name, A.annexe_version as version, A.id_annexe, A.annexe_path path, AT.type_name as type, A.date_delivery as "livraison"
from packages P, annexes A, packages_annexes PA, annexe_types AT
where upper(A.annexe_name) like upper(:annexeName)
and A.id_annexe = PA.id_annexe
and P.id_package = PA.id_package
and AT.id_type = A.id_type
order by 2, 3;
