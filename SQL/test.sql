/*
DATA_STORAGE_OBJECT_ID                                NOT NULL NUMBER
 DATA_STORAGE_OBJECT_STRING_ID                         NOT NULL VARCHAR2(64)
 FILE_SIZE                                             NOT NULL NUMBER
 ARCHIVE_NAME                                                   VARCHAR2(256)
 ARCHIVE_OBJECT_NAME                                            VARCHAR2(256)
 ARCHIVE_PATH                                                   VARCHAR2(512)
 ON_LINE_OBJECT_NAME                                            VARCHAR2(256)
 ON_LINE_PATH                                                   VARCHAR2(512)
*/

select * from t_data_storage_object
where ARCHIVE_PATH like '%WHISPER/CAA%'
/* and ARCHIVE_OBJECT_NAME like '%_V01%'; */
;
