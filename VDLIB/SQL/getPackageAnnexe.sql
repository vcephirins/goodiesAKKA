-- Description : Info d'un package et de son annexe

-- P1 : package name (ex : WHISPER_v3_1_0)
\set packageName '\'' :P1 '\''
-- P2 : annexe name (ex : WHISPER_v3_1.val.tar.gz)
\set annexeName '\'' :P2 '\''

select P.id_package, :packageVersion package, A.annexe_name, A.annexe_version as version, A.id_annexe, A.annexe_path path, D.dir_name as directory, A.date_delivery as "livraison"
from packages P, annexes A, packages_annexes PA, annexe_types AT, directories D
where :packageVersion = :packageName
and A.annexe_name = :annexeName
and A.id_annexe = PA.id_annexe
and P.id_package = PA.id_package
and AT.id_type = A.id_type
and D.id_dir = AT.id_dir
order by 2, 3;
