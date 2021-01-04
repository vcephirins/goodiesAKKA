set linesize 400

select type||' '||name||' line '||line||':'||position||CHR(10)||text as ERRORS from all_errors;

