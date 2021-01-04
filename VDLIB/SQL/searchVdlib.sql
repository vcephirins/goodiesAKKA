-- Description : Recherche d'un mot clef dans la base VDLIB

-- P1 : mot clef a rechercher (ex : xample , AKKA)
\set word '\'%' :P1 '%\''

select :packageVersion Package, description Description
from packages P
where upper(:packageVersion) like upper(:word)
or upper(description) like upper(:word)
order by package_name, package_version desc, package_patch desc;

select :toolVersion Outil, description Description
from tools T
where upper(:toolVersion) like upper(:word)
or upper(description) like upper(:word)
order by tool_name, tool_version desc, tool_patch desc;

select :annexeVersion Annexe, description Description
from annexes A
where upper(:annexeVersion) like upper(:word)
or upper(description) like upper(:word)
order by annexe_name, annexe_version desc;

select contact_display Responsable, contact_name Contact, :packageVersion Package
from contacts C, packages P
where (upper(contact_name) like upper(:word)
or upper(contact_display) like upper(:word))
and P.id_package = C.id_package
order by Responsable, Contact, package_name, package_version desc, package_patch desc;


