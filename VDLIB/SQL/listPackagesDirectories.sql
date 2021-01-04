-- Description : Liste des repertoires d'un package

-- P1 : Nom du package avec la version (ex : cef-to-cdf_v1_0_0)
\set packageName '\'%' :P1 '%\''

select P.id_package, :packageVersion package, D.dir_name directory
from packages P, packages_directories PD, directories D
where upper(:packageVersion) like upper(:packageName)
and PD.id_package = P.id_package
and D.id_dir = PD.id_dir
order by 2, 3;
