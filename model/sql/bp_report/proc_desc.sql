SELECT ROUTINE_COMMENT as href_name FROM information_schema.routines
WHERE routine_schema = 'kino' and ROUTINE_NAME = '$proc';