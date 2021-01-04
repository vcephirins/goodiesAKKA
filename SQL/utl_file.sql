/**********************************/
/* TOOL WITCH WRITE THE INTEGRITY */
/*  CONSTRAINTS ON DELTA          */
/**********************************/
DECLARE
  /* Table name from cursor C1 witch is the same         */ 
  /* variable as table_name_ from table USER_CONSTRAINTS */
  c1_table_name  USER_CONSTRAINTS.TABLE_NAME%TYPE;

  /* Constraint name from cursor C2 witch is the same        */ 
  /* variable as constraint_name from table USER_CONSTRAINTS */
  c2_constraint_name  USER_CONSTRAINTS.CONSTRAINT_NAME%TYPE;

  /* File */
  file utl_file.file_type;

  /* Directory location of file */
  location VARCHAR2(100);

  /* File name (including extention) */
  filename VARCHAR2(30);

  /* Open mode of file */
  open_mode VARCHAR2(1);

  /* Text to write in file (same length as a line) */
  buffer VARCHAR2(80);

  /* Cursor on each tables witch have CK constraints */  
  CURSOR C1 IS 
	SELECT DISTINCT TABLE_NAME 
	FROM USER_CONSTRAINTS
        WHERE CONSTRAINT_TYPE='C'
        AND CONSTRAINT_NAME LIKE 'NK%';

  /* Cursor on each constraint of the tables */  
  CURSOR C2 IS 
	SELECT CONSTRAINT_NAME 
	FROM USER_CONSTRAINTS
	WHERE TABLE_NAME=c1_table_name;

BEGIN
    open_mode:='w';
    filename:='toto.txt';
    location:='u001\appli\ss10_dev';
    file:=utl_file.fopen(location,filename,open_mode);
    
  /* Recovery of all table witch have CK constraints */
  OPEN C1;
  /* For each table */
  LOOP
    /* Recovery of the group name */  
    FETCH C1 INTO c1_table_name;
    EXIT WHEN C1%NOTFOUND;
    /* Recovery off all constraints' tables */ 
    /*OPEN C2;*/
    /* For each constraint */
    /*LOOP*/
      /* Recovery of the table name */
      /*FETCH C2 INTO c2_constraint_name;
      EXIT WHEN C2%NOTFOUND;*/ 
      buffer:=c1_table_name;
      utl_file.put_line(file,buffer);
    /*END LOOP;
    CLOSE C2;*/
  END LOOP;
  CLOSE C1;
  utl_file.fclose(file);
--EXCEPTION
--  WHEN utl_file.invalid_path THEN null;
END;
/

