-- select * from task limit 5

-- select * from task_option limit 5

-- select * from task left join task_option on task.task_id = task_option.task_id limit 10
-- select * from task limit 10

BEGIN
    CREATE TABLE test.bbbb_bk AS SELECT * FROM test.bbbb;
    BEGIN TRANSACTION;
    DELETE FROM test.bbbb WHERE True;
--    INSERT INTO ds_test.table1 (SELECT * FROM ds_test.table1_bk WHERE x = 1);
    INSERT INTO test.bbbb (SELECT * FROM test.bbbb_tmp WHERE x = 1);
    COMMIT TRANSACTION;
    DROP TABLE test.bbbb_bk;
EXCEPTION WHEN ERROR THEN
    ROLLBACK TRANSACTION;
    DROP TABLE test.bbbb_bk;
END;
