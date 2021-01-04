-- Description : Mise a jour du statut valide et deploye d'un package

-- P1 : Nom du package avec la version (ex : cef-to-cdf_v1_0_0)
-- P2 : Date de livraison (ex : 2015-05-22)
\set packageName '\'' :P1 '\''
\set dateDelivery '\'' :P2 '\''

update packages 
set validated = true, deployed = true, 
    date_delivery = :dateDelivery,
    date_deployed = now()
where :packageVersion = :packageName;
