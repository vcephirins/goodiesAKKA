-- Description : Mie a jour de la date de livraison de l'annexe

-- P1 : id de l'annexe (ex : 10)
\set idAnnexe :P1 
-- P2 : Chemin d'acces a l'annexe
\set annexePath '\'' :P2 '\''

-- Le path est mis a jour dans le cas d'une nouvel version de package ou d'outil
update annexes set date_delivery = now(), annexe_path = :annexePath
where id_annexe = :idAnnexe;
