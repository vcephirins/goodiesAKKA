delete plan_table
/

explain plan for
Select /*+ index (elementary_obs IND_ELEMENTARY_OBS_1) */ ID_SOURCE, ID_TRANSIT 
From elementary_obs 
Where id_htm = ':1' and d_creation between '2006-11-01 00' and '2006-11-01 23'
/

column opid format a10
column op format a50
column info format a12

-- select lpad('  ',2*(level-1))||operation||' '||options||' '||object_name||' '||decode(id, 0, 'Coût = '||position||', Optimizer = '||optimizer) "Plan de recherche"
-- from plan_table
-- start with id = 0 
-- connect by prior id = parent_id
-- /

select * from table ( dbms_xplan.display() )
/

rollback
/

-- Voir script utlxplan.sql (10G)
--create table plan_table (
--STATEMENT_ID                             VARCHAR2(30),
--TIMESTAMP                                DATE,
--REMARKS                                  VARCHAR2(80),
--OPERATION                                VARCHAR2(30),
--OPTIONS                                  VARCHAR2(30),
--OBJECT_NODE                              VARCHAR2(30),
--OBJECT_OWNER                             VARCHAR2(30),
--OBJECT_NAME                              VARCHAR2(30),
--OBJECT_INSTANCE                          NUMBER(38),
--OBJECT_TYPE                              VARCHAR2(30),
--SEARCH_COLUMNS                           NUMBER(38),
--ID                                       NUMBER(38),
--PARENT_ID                                NUMBER(38),
--POSITION                                 NUMBER(38),
--OTHER                                    LONG)
--/

-----------------------------------------------------------------
-- HINTS : syntax => select /*+ hint */     -- Voir application Developper's Guide, Chap 5
-- Pour forcer l'ordre des tables => /*+ ordered */
-- Pour forcer un FULL            => /*+ FULL(table) */
-- pour forcer un index           => /*+ index (table index) */
-- pour forcer un index_asc       => /*+ index_asc (table index) */
-- pour forcer un index_desc      => /*+ index_desc (table index) */
--           /*+ INDEX_DESC(SS11_SB_ISSUE PK_SB_ISSUE)*/
-- pour forcer une jointure par nested loop => /*+ use_nl(table[, table]) */
-- pour forcer une jointure par merge => /*+ use_merge(table) */
-- ramene les lignes avant bufferisation => /*+ first_rows */
-- Ramene toutes les lignes apres bufferisation => /*+ last_rows */

