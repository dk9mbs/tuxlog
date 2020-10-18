from tkinter import ttk
from enum import Enum
import tkinter as tk
import json
import xml.etree.ElementTree as ET
import logging

from dialoglib import DataDialog, DataDialogMode

def load_log_list(client,dialog_deprectated, treev, **kwargs):
    for item in treev.get_children():
        treev.delete(item)

    where=[]
    if 'yourcall' in kwargs:
        value=kwargs['yourcall']
        if value != "" and value != None:
            where.append(f"""<condition field="yourcall" value="{value}" operator="like"/>""" )
    if 'locator' in kwargs:
        value=kwargs['locator']
        if value != "" and value != None:
            where.append(f"""<condition field="locator" value="{value}" operator="like"/>""" )
    if 'logbook_id' in kwargs:
        value=kwargs['logbook_id']
        if value != "" and value != None:
            where.append(f"""<condition field="logbook_id" value="{value}" operator="="/>""" )


    filter=''.join(where)
    if filter != "":
        filter=f"<filter>{filter}</filter>"

    fetch=f"""
    <restapi type="select">
        <table name="log_logs" alias="l"/>
        <select>
            <field name="id" table_alias="l"/>
            <field name="yourcall"/>
            <field name="logdate_utc"/>
            <field name="start_utc"/>
            <field name="end_utc"/>
            <field name="logbook_id"/>
            <field name="mode_id"/>
            <field name="frequency"/>
            <field name="adif_name" table_alias="b"/>
            <field name="country" table_alias="d"/>
            <field name="continent" table_alias="d"/>
            <field name="cq_zone" table_alias="d"/>
            <field name="itu_zone" table_alias="d"/>
        </select>
        <joins>
            <join table="log_bands" alias="b" type="left" condition="l.band_id=b.id"/>
            <join table="log_dxcc" alias="d" type="left" condition="l.dxcc=d.id"/>
        </joins>
        <orderby>
            <field name="logdate_utc" sort="DESC"/>
            <field name="start_utc" sort="DESC"/>
        </orderby>
        {filter}
    </restapi>
    """

    logs=json.loads(client.read_multible("log_logs", fetch))

    for log in logs:
        treev.insert('', 'end',iid=log['id'], text ="Hallo",values =(log['yourcall'], 
            log['logdate_utc'], log['start_utc'],log['end_utc'], log['logbook_id'],log['mode_id'],log['adif_name'],log['frequency'],
            log['continent'],log['country']))

    return logs

def on_search_click(event,dialog, control_name, event_name):

    logs=load_log_list(dialog.get_client(),dialog, dialog.get_control("treev")['control'], yourcall=dialog.get_control("search_yourcall")['control'].get(),
        locator=dialog.get_control("search_locator")['control'].get(), logbook_id=dialog.get_control("search_logbook_id")['control'].get() )

def on_yourcall_change(event,dialog, control_name, event_name):
    call=dialog.get_control(control_name)['control'].get()
    result=dialog.get_client().execute_action("tuxlog_get_dxcc_info",{"call":call},json_out=True)
    dialog.bind("data", {"cq":result['cq_zone'],"itu":result['itu_zone'],"dxcc": result['dxcc'],"yourcall":call.upper()})

def on_save_click(event,dialog,control_name, event_name):
    result=dialog.get_bind_data("data")
    print(result)
    if dialog.get_dialog_mode("data")==DataDialogMode.NEW:
        print(dialog.get_client().create("log_logs", result))
    elif dialog.get_dialog_mode("data")==DataDialogMode.EDIT:
        print(dialog.get_client().update("log_logs",dialog.get_dialog_record_id("data"), result))

    logs=load_log_list(dialog.get_client(), dialog,dialog.get_control("treev")['control'], yourcall=dialog.get_control("search_yourcall")['control'].get(),
        locator=dialog.get_control("search_locator")['control'].get(), logbook_id=dialog.get_control("search_logbook_id")['control'].get() )

    dialog.reset("data")
    dialog.set_dialog_record_id(None, "data")

def on_delete_click(event,dialog,control_name,event_name):
    id=dialog.get_dialog_record_id("data")
    print(dialog.get_client().delete("log_logs",id))
    dialog.set_dialog_record_id(None,"data")
    load_log_list(dialog.get_client(), dialog, dialog.get_control("treev")['control'])


def on_new_click(event,dialog, control_name,event_name):
    dialog.reset("data")
    dialog.set_dialog_record_id(None, "data")

def on_item_click(event,dialog,control_name,event_name):
    id=dialog.get_control(control_name)['control'].focus()
    result=dialog.get_client().read("log_logs", id, json_out=True)
    dialog.bind("data", result)
    dialog.set_dialog_record_id(id, "data")


def generic_item_event(dialog, item, item_id=None):
    import test

    test.init_dialog(dialog.get_client(), dialog.create_root())
    print(item)


def init_dialog(client,root):
    f=open('log.dialog.xml','r')
    form_xml=f.read()
    xml=ET.fromstring(form_xml)
    f.close()

    ui=DataDialog(root,xml,client)
    ui.register_callback("search","leftclick", on_search_click)
    ui.register_callback("yourcall", "focusout", on_yourcall_change)
    ui.register_callback("btn_save", "leftclick", on_save_click)
    ui.register_callback("btn_new","leftclick", on_new_click)
    ui.register_callback("btn_delete","leftclick", on_delete_click)
    ui.register_callback("treev","itemselect",on_item_click)

    treev = ttk.Treeview(ui, selectmode ='browse')
    ui.add_control(treev,row=2,column=0, colspan=12, name="treev")

    verscrlbar = ttk.Scrollbar(ui,
                           orient ="vertical",
                           command = treev.yview)

    verscrlbar.grid(sticky=('w','n','s') ,row=2, column=ui._total_columns)
    treev.configure(xscrollcommand = verscrlbar.set)
    treev["columns"] = ("1", "2", "3","4","5","6","7","8","9","10")
    treev['show'] = 'headings'

    treev.column("1", width = 90, anchor ='sw')
    treev.column("2", width = 90, anchor ='se')
    treev.column("3", width = 90, anchor ='se')
    treev.column("4", width = 90, anchor ='se')
    treev.column("5", width = 90, anchor ='se')
    treev.column("6", width = 90, anchor ='se')
    treev.column("7", width = 90, anchor ='se')
    treev.column("8", width = 90, anchor ='se')
    treev.column("9", width = 90, anchor ='se')

    treev.heading("1", text ="Yourcall")
    treev.heading("2", text ="Date")
    treev.heading("3", text ="Start (UTC)")
    treev.heading("4", text ="End (UTC)")
    treev.heading("5", text ="Station")
    treev.heading("6", text ="Mode")
    treev.heading("7", text ="Band")
    treev.heading("8", text ="Frequency")
    treev.heading("9", text ="Continent")
    treev.heading("10", text ="Country")

    logs=load_log_list(client,ui,treev)

    ui.bind("data", {"yourcall": "dk9mbs"})


