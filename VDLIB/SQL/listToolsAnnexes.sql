-- Description : Liste des annexes par outils triees par nom et version

-- P1 : tool name (ex : % , invent , invent%v1_0_2)
\set toolName '\'%' :P1 '%\''

select T.id_tool, :toolVersion tool, A.annexe_name, A.annexe_version as version, A.id_annexe, A.annexe_path path, AT.type_name as type, A.date_delivery as "livraison"
from tools T, annexes A, tools_annexes TA, annexe_types AT
where upper(:toolVersion) like upper(:toolName)
and A.id_annexe = TA.id_annexe
and T.id_tool = TA.id_tool
and AT.id_type = A.id_type
order by 2, 3;
