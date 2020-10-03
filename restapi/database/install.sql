DELETE FROM api_group_permission WHERE solution_id=10001;
DELETE FROM api_user_group WHERE solution_id=10001;
DELETE FROM api_table WHERE solution_id=10001;
DELETE FROM api_session WHERE user_id IN(20000,20001);
DELETE FROM api_user WHERE solution_id=10001;
DELETE FROM api_group WHERE solution_id=10001;
DELETE FROM api_event_handler WHERE solution_id=10001;
DELETE FROM api_solution WHERE id=10001;

INSERT INTO api_solution(id,name) VALUES (10001, 'tuxlog');

INSERT INTO api_user (id,username,password,is_admin,disabled,solution_id) VALUES (20000,'tuxlog','password',0,0,10001);

INSERT INTO api_group(id,groupname,solution_id) VALUES (20000,'tuxlog',10001);

INSERT INTO api_user_group(user_id,group_id,solution_id) VALUES (20000,20000,10001);

INSERT INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id)
    VALUES
    (20000,'log_logs','log_logs','id','Int','yourcall',10001);

INSERT INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20001,'meta_data_exchange_fields','meta_data_exchange_fields','id','Int','external_fieldname',10001);

INSERT INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20002,'log_bands','log_bands','id','Int','name',10001);

INSERT INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20003,'log_dxcc','log_dxcc','id','String','country',10001);

INSERT INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20004,'log_dxcc_prefixes','log_dxcc_prefixes','id','String','id',10001);

INSERT INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20005,'log_logbooks','log_logbooks','id','String','description',10001);


INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20000,-1,-1,-1,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20001,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20002,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20003,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20004,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20005,0,-1,0,0,10001);

/*
Guests
*/

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20000,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20001,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20002,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20003,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20004,0,-1,0,0,10001);

INSERT INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20005,0,-1,0,0,10001);


INSERT INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id) 
    VALUES ('tuxlog_set_band','log_logs','insert','before',100,10001);
INSERT INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id) 
    VALUES ('tuxlog_set_dxcc','log_logs','insert','before',101,10001);

