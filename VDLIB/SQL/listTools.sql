-- Description : Liste des packages associes aux outils

-- P1 : nom de l'outil (ex: % , list , list%Ref)
\set toolName '\'%' :P1 '%\''

select 
   :toolVersion as "Outil", 
   :packageVersion as "Package", 
   :deployedLabel,
   T.id_tool as "id_tool", 
   P.id_package as "id package", 
   replace(T.description, E'\n', ' ') as "Description"
from tools T, packages P, packages_tools PT
where upper(:toolVersion) like upper(:toolName)
and PT.id_tool = T.id_tool
and P.id_package = PT.id_package
order by 1, 2 ;
