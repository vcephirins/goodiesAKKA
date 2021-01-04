-- Description : Invalide un package

-- P1 : Nom du package avec la version (ex : cef-to-cdf_v1_0_0)
\set packageName '\'' :P1 '\''

update packages set deployed = false, validated = false
where :packageVersion = :packageName;
