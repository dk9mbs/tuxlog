DELETE FROM api_process_log WHERE event_handler_id IN (SELECT id FROM api_event_handler WHERE solution_id=10001);

DELETE FROM api_group_permission WHERE solution_id=10001;
DELETE FROM api_user_group WHERE solution_id=10001;
#DELETE FROM api_table WHERE solution_id=10001;
DELETE FROM api_session WHERE user_id IN(20000,20001);
DELETE FROM api_user WHERE solution_id=10001;
DELETE FROM api_group WHERE solution_id=10001;
DELETE FROM api_event_handler WHERE solution_id=10001;
#DELETE FROM api_solution WHERE id=10001;
DELETE FROM api_ui_app_nav_item WHERE solution_id=10001;
DELETE FROM api_ui_app WHERE solution_id=10001;
DELETE FROM api_table_view  WHERE solution_id=10001;

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

/* log_logs */
/* api_event_handler */
call api_proc_create_table_field_instance(20000,100, 'id','ID','int',14,'{"disabled": true}', @out_value);
call api_proc_create_table_field_instance(20000,150, 'logdate_utc','Datum (UTC)','date',3,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,200, 'logbook_id','Mein Rufzeichen','int',2,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,250, 'yourcall','Rufzeichen (DX)','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,300, 'mode_id','Mode','int',2,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,400, 'rig_id','Gerät','int',2,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,500, 'power','Leistung','decimal',14,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,600, 'frequency','QRG','int',14,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,700, 'band_id','Band','int',2,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,900, 'start_utc','Start (UTC)','time',4,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1100, 'viacall','Via','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1200, 'name','Name','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1210, 'dok', 'DOK','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1300, 'locator','Locator','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1400, 'qth','QTH','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1405, 'country', 'Land','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1410, 'txrst','RST (gesendet)','int',14,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1420, 'rxrst','RST (empfangen)','int',14,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1500, 'comment','Kommentar','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1510, 'qsl_shipmentmode', 'QSL Versand','string',2,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1550, 'end_utc','Ende (UTC)','time',4,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1800, 'qslrecv','QSL empfangen','int',19,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,1900, 'qslsend','QSL gesendet','int',19,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,2300, 'lognr','Log Nummer','int',14,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,2400, 'itu_prefix','ITU Prefix','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,2500, 'dxcc','DXCC','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,2600, 'cq','CQ','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,2700, 'itu', 'ITU','tring',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3100, 'web', 'WWW','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3200, 'email', 'E-Mail','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3300, 'distance', 'Distance','decimal',14,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3400, 'source', 'Herkunft','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3410, 'mytestnr','mytestnr','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3420, 'yourtestnr','yourtestnr','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3500, 'rxexchange1', 'RX Exchange 1','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3600, 'txexchange1', 'TX Exchange 1','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3700, 'rxexchange2', 'RX Exchange 2','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3800, 'txexchange2', 'TX Exchange 2','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(20000,3900, 'entity', 'Entity','string',1,'{"disabled": false}', @out_value);



/*
call api_proc_create_table_field_instance(9,300, 'publisher','Publisher','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,400, 'event','Ereignis','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,500, 'type','Typ','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,600, 'sorting','Reihenfolge','int',14,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,700, 'solution_id','Lösung','int',2,'{"disabled": false}', @out_value);
UPDATE api_table_field SET referenced_table_name='api_solution', referenced_table_id=25, referenced_field_name='id', is_lookup=-1 WHERE id=@out_value;
call api_proc_create_table_field_instance(9,800, 'run_async','Asynchron','int',19,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,900, 'run_queue','Queue','int',19,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,1000, 'is_enabled','Aktiv','int',19,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,1100, 'config','Configuration','string',1,'{"disabled": false}', @out_value);
call api_proc_create_table_field_instance(9,1100, 'inline_code','Inline Code','string',101,'{"disabled": false, "mode":"ace/mode/python"}', @out_value);
*/

/* App */
INSERT IGNORE INTO api_ui_app (id, name,description,home_url,solution_id)
VALUES (
10001001,'tuxlog','tuxlog','/ui/v1.0/data/view/log_logs/default?app_id=10001001',10001);
INSERT IGNORE INTO api_ui_app_nav_item(id, app_id,name,url,type_id,solution_id) VALUES (10001001,10001001,'Meine Geräte','/ui/v1.0/data/view/log_rigs/default',1,10001);
INSERT IGNORE INTO api_ui_app_nav_item(id, app_id,name,url,type_id,solution_id) VALUES (10001002,10001001,'Meine Rufzeichen','/ui/v1.0/data/view/log_logbooks/default',1,10001);
INSERT IGNORE INTO api_ui_app_nav_item(id, app_id,name,url,type_id,solution_id) VALUES (10001003,10001001,'Bänder','/ui/v1.0/data/view/log_bands/default',1,10001);
INSERT IGNORE INTO api_ui_app_nav_item(id, app_id,name,url,type_id,solution_id) VALUES (10001004,10001001,'Modes','/ui/v1.0/data/view/log_modes/default',1,10001);
INSERT IGNORE INTO api_ui_app_nav_item(id, app_id,name,url,type_id,solution_id) VALUES (10001005,10001001,'Datenmapping','/ui/v1.0/data/view/log_data_exchange_fields/default',1,10001);


/* Views */
INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml, columns) VALUES (
100010001,'LISTVIEW','default',20000,'id',10001,'<restapi type="select">
    <table name="log_logs" alias="l"/>
    <orderby>
        <field name="logdate_utc" alias="l" sort="DESC"/>
        <field name="start_utc" alias="l" sort="DESC"/>
    </orderby>
</restapi>',
'{"id": {},"yourcall": {},"locator": {}, "txrst":{},"rxrst": {},  "__mode_id@name": {},"__band_id@name": {},"__rig_id@name": {}, "logdate_utc": {}, "start_utc": {}, "end_utc":{} }');

INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml, columns) VALUES (
100010002,'LISTVIEW','default',20006,'id',10001,'<restapi type="select">
    <table name="log_rigs" alias="r"/>
    <orderby>
        <field name="id" alias="r" sort="ASC"/>
    </orderby>
</restapi>',
'{"id": {},"description": {},"hamlib_id": {},"remote_host": {}, "remote_port": {} }');

INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml, columns) VALUES (
100010003,'LISTVIEW','default',20005,'id',10001,'<restapi type="select">
    <table name="log_logbooks" alias="l"/>
    <orderby>
        <field name="id" alias="l" sort="ASC"/>
    </orderby>
</restapi>',
'{"id": {},"description": {},"mycall": {},"description": {} }');

INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml, columns) VALUES (
100010004,'LISTVIEW','default',20002,'id',10001,'<restapi type="select">
    <table name="log_bands" alias="b"/>
    <orderby>
        <field name="id" alias="b" sort="ASC"/>
    </orderby>
</restapi>',
'{"id": {},"name": {},"adif_name": {},"frequency_min": {}, "frequency_max":{}, "frequency_unit":{} }');

INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml, columns) VALUES (
100010005,'LISTVIEW','default',20007,'id',10001,'<restapi type="select">
    <table name="log_modes" alias="m"/>
    <orderby>
        <field name="description" alias="m" sort="ASC"/>
    </orderby>
</restapi>',
'{"id": {},"description": {},"parent": {} }');

INSERT IGNORE INTO api_table_view (id,type_id,name,table_id,id_field_name,solution_id,fetch_xml, columns) VALUES (
100010006,'LISTVIEW','default',20001,'id',10001,'<restapi type="select">
    <table name="log_data_exchange_fields" alias="e"/>
    <orderby>
        <field name="converter_id" alias="e" sort="ASC"/>
        <field name="external_fieldname" alias="e" sort="ASC"/>
    </orderby>
</restapi>',
'{"id": {},"converter_id": {},"external_fieldname": {},"internal_fieldname": {}, "internal_datatype":{} }');



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
