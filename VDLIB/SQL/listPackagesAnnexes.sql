-- Description : Liste des annexes par packages triees par nom et version

-- P1 : package name (ex : % , invent , invent%v1_0_2)
\set packageName '\'%' :P1 '%\''

select P.id_package, :packageVersion package, A.annexe_name, A.annexe_version as version, A.id_annexe, A.annexe_path path, T.type_name as type, A.date_delivery as "livraison"
from packages P, annexes A, packages_annexes PA, annexe_types T
where upper(:packageVersion) like upper(:packageName)
and A.id_annexe = PA.id_annexe
and P.id_package = PA.id_package
and T.id_type = A.id_type
order by 2, 3;
