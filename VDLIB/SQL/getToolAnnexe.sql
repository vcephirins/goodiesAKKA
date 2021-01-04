-- Description : Info d'un tool et de son annexe

-- P1 : tool name (ex : WHISPER_v3_1_0)
\set toolName '\'' :P1 '\''
-- P2 : annexe name (ex : WHISPER_v3_1.val.tar.gz)
\set annexeName '\'' :P2 '\''

select T.id_tool, :toolVersion tool, A.annexe_name, A.annexe_version as version, A.id_annexe, A.annexe_path path, D.dir_name as directory, A.date_delivery as "livraison"
from tools T, annexes A, tools_annexes TA, annexe_types AT, directories D
where :toolVersion = :toolName
and A.annexe_name = :annexeName
and A.id_annexe = TA.id_annexe
and T.id_tool = TA.id_tool
and AT.id_type = A.id_type
and D.id_dir = AT.id_dir
order by 2, 3;
