-- Description : Info d'une annexe

-- P1 : identifiant de l'annexe (ex : 10)
\set idAnnexe :P1

select A.annexe_name, A.annexe_version as version, A.id_annexe, A.annexe_path path, AT.type_name as type, D.dir_name as directory, A.date_delivery as "livraison"
from annexes A, annexe_types AT, directories D
where A.id_annexe = :idAnnexe
and AT.id_type = A.id_type
and D.id_dir = AT.id_dir;
