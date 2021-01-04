-- Description : Liste des outils associes aux packages

-- P1 : nom du package (ex : % , outil , out%spot)
\set packageName '\'%' :P1 '%\''

select :packageVersion as "Package", :toolVersion as "Outil", T.id_tool as "Id tool"
from tools T, packages P, packages_tools PT
where upper(:packageVersion) like upper(:packageName)
and PT.id_tool = T.id_tool
and P.id_package = PT.id_package
order by 1, 2 ;
