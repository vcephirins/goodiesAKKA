-- Description : Liste des outils par annexes tries par nom et version

-- P1 : annexe name (ex : % , cdf , cdf%to)
\set annexeName '\'%' :P1 '%\''

select T.id_tool, :toolVersion tool, A.annexe_name, A.annexe_version as version, A.id_annexe, A.annexe_path path , AT.type_name as type, date_delivery as "livraison"
from tools T, annexes A, tools_annexes TA, annexe_types AT
where upper(A.annexe_name) like upper(:annexeName)
and A.id_annexe = TA.id_annexe
and T.id_tool = TA.id_tool
and AT.id_type = A.id_type
order by 2, 3;
