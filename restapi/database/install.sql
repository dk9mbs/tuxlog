DELETE FROM api_process_log WHERE event_handler_id IN (SELECT id FROM api_event_handler WHERE solution_id=10001);

DELETE FROM api_group_permission WHERE solution_id=10001;
DELETE FROM api_user_group WHERE solution_id=10001;
#DELETE FROM api_table WHERE solution_id=10001;
DELETE FROM api_session WHERE user_id IN(20000,20001);
DELETE FROM api_user WHERE solution_id=10001;
DELETE FROM api_group WHERE solution_id=10001;
DELETE FROM api_event_handler WHERE solution_id=10001;
#DELETE FROM api_solution WHERE id=10001;

INSERT IGNORE INTO api_solution(id,name) VALUES (10001, 'tuxlog');

INSERT IGNORE INTO api_user (id,username,password,is_admin,disabled,solution_id) VALUES (20000,'tuxlog','password',0,0,10001);

INSERT IGNORE INTO api_group(id,groupname,solution_id) VALUES (20000,'tuxlog',10001);

INSERT IGNORE INTO api_user_group(user_id,group_id,solution_id) VALUES (20000,20000,10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,enable_audit_log,solution_id)
    VALUES
    (20000,'log_logs','log_logs','id','int','yourcall',-1,10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20001,'log_data_exchange_fields','meta_data_exchange_fields','id','int','external_fieldname',10001);

UPDATE api_table SET alias='log_data_exchange_fields' where id=20001 AND alias like 'meta%';

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20002,'log_bands','log_bands','id','int','name',10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20003,'log_dxcc','log_dxcc','id','String','country',10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20004,'log_dxcc_prefixes','log_dxcc_prefixes','id','String','id',10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20005,'log_logbooks','log_logbooks','id','String','description',10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20006,'log_rigs','log_rigs','id','String','description',10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20007,'log_modes','log_modes','id','String','description',10001);

INSERT IGNORE INTO api_table(id,alias,table_name,id_field_name,id_field_type,desc_field_name,solution_id) 
    VALUES
    (20008,'log_qslshipmentmodes','log_qslshipmentmodes','id','String','description',10001);


INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20000,-1,-1,-1,-1,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20001,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20002,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20003,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20004,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20006,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20007,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (20000,20008,0,-1,0,0,10001);

/*
Guests
*/

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20000,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20001,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20002,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20003,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20004,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20006,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20007,0,-1,0,0,10001);

INSERT IGNORE INTO api_group_permission (group_id,table_id,mode_create,mode_read,mode_update,mode_delete,solution_id)
    VALUES
    (100,20008,0,-1,0,0,10001);


INSERT IGNORE INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id)
    VALUES ('tuxlog_set_band','log_logs','insert','before',100,10001);
INSERT IGNORE INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id)
    VALUES ('tuxlog_set_dxcc','log_logs','insert','before',101,10001);
INSERT IGNORE INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id)
    VALUES ('tuxlog_combo_sources','generate_data_combo_source','execute','before',100,10001);
INSERT IGNORE INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id)
    VALUES ('tuxlog_action_dxcc','tuxlog_get_dxcc_info','execute','before',100,10001);
INSERT IGNORE INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id)
    VALUES ('tuxlog_app_start','$app_start','execute','before',100,10001);
INSERT IGNORE INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id,run_async)
    VALUES ('tuxlog_plugin_import-cty','textfileimport_cty','post','before',100,10001,-1);
INSERT IGNORE INTO api_event_handler (plugin_module_name,publisher,event,type,sorting,solution_id,run_async)
    VALUES ('tuxlog_plugin_import-adif','textfileimport_adif','post','before',100,10001,0);


/* portal */
INSERT IGNORE INTO api_portal(id,name,solution_id) VALUES ('tuxlog', 'tuxlog',10001);
UPDATE api_portal SET template='<!DOCTYPE HTML5>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="language" content="deutsch, de" />
<meta name="robots" content="index, follow" />
<meta name="author" content="dk9mbs.de" />
<meta http-equiv="expires" content="5" />
<meta name="Keywords" content="" >
<meta name="Description" content="" >
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>tuxlog</title>

<!-- Start Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztc$
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.min.js" integrity="sha384-Atwg2Pkwv9vp0ygtn1JAojH0nYbwNJLPhwyoVbhoPwBhjQPR5VtM2+x$
<!-- End Bootstrap -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>
<body>
    <div id="content">
    {{ content }}
    </div>
</body>
</html>' WHERE id='tuxlog';


INSERT IGNORE INTO api_portal_content(portal_id, name, title, type_id, is_active, solution_id) VALUES (
'tuxlog', 'tuxlog-fileimport', 'tuxlog Datei Import', 1, -1, 10001);

UPDATE api_portal_content SET content='<h1>Datei-Import</h1>

<h2>CTY.DAT</h2>
<form method="POST" action="/api/v1.0/tuxlog/cty" enctype = "multipart/form-data">
<table>
<tr><td>cty.dat Datei</td><td><input type="file" id="file" name="file"/></td></tr>
<tr><td>Absenden</td><td><input type="submit" value="Upload"/></td></tr>
</table>
</form>

<h2>ADIF Files</h2>
<form method="POST" action="/api/v1.0/tuxlog/adif" enctype = "multipart/form-data">
<table>
<tr><td>cty.dat Datei</td><td><input type="file" id="file" name="file"/></td></tr>
<tr><td>Absenden</td><td><input type="submit" value="Upload"/></td></tr>
</table>
</form>
' WHERE name='tuxlog-fileimport' AND solution_id=10001;
