from tkinter import ttk
from enum import Enum
import tkinter as tk
import json
import xml.etree.ElementTree as ET
import logging

from clientlib import RestApiClient

client=RestApiClient("http://localhost:5001/api")
client.login("tuxlog", "password")

class DataDialogMode(Enum):
    UNDEFINED = 0
    NEW = 1
    EDIT = 2

class DataDialog(tk.Frame):
    def __init__(self, parent,form_xml, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._data_mode={"data": DataDialogMode.UNDEFINED}
        self._data_record_id={}

        self._root=parent
        self._callbacks=[]
        self._controls=[]
        self._datasource={}

        self._total_rows=0
        self._total_columns=0

        self.__read_form_xml(form_xml)

        self.grid(row=0, column=0, sticky=("N","S","E","W"))

        #for y in range(self._total_rows):
        #    tk.Grid.rowconfigure(self, y, weight=1)

        for x in range(self._total_columns):
            tk.Grid.columnconfigure(self, x, weight=1)

    def register_callback(self, control_name, message, fn):
        callback={"fn":fn, "control_name":control_name, "message":message}
        self._callbacks.append(callback)

    def _fire_external_event(self, event, control_name, message):
        for callback in self._callbacks:
            if callback['control_name']==control_name and callback['message']==message:
                logging.info(f"Fire event with message: {message}")
                callback['fn'](event,self, control_name, message)

    def __read_form_xml(self, tree):
        c=0
        for row in tree.find('rows').findall('row'):
            for column in row.find('columns').findall('column'):
                #c+=2

                colspan=0
                id=column.attrib['id']
                type=column.attrib['type']
                data_bind=""
                data_src=""
                data_table=""
                text=""
                data_table_filter=""
                default_value=""

                if 'text' in column.attrib:
                    text=column.attrib['text']

                if 'data_bind' in column.attrib:
                    data_bind=column.attrib['data_bind']

                if 'data_src' in column.attrib:
                    data_src=column.attrib['data_src']

                if 'data_table' in column.attrib:
                    data_table=column.attrib['data_table']

                if 'default' in column.attrib:
                    default_value=column.attrib['default']

                if column.find('filter'):
                    data_table_filter=ET.tostring(column.find('filter'))

                label=None
                if 'label' in column.attrib:
                    c+=2
                    col=c-1
                    colspan=1
                    textvar=tk.StringVar()
                    textvar.set(f"{column.attrib['label']}")
                    label=tk.Label(self,name=f"lab_{id}", textvariable=textvar , height=1, bg="gray")
                    label.extra = f"lab_{id}"
                    self.add_control(label, row=self._total_rows,column=c-2,colspan=colspan, name=f"lab_{id}", textvar=textvar)
                else:
                    c+=1
                    col=c-1
                    colspan=1

                textvar=tk.StringVar()
                textvar.set(text)
                if type.upper()=='INPUT':
                    control=DialogInput(self,name=id, textvariable=textvar)
                elif type.upper() == 'CHECKBOX':
                    textvar=tk.IntVar()
                    default_value=0
                    control=tk.Checkbutton(self,name=id,variable=textvar)
                elif type.upper() == 'BUTTON':
                    control=DialogButton(self,name=id,textvariable=textvar)
                elif type.upper() == 'COMBOBOX':
                    items=generate_combo_source(data_table, data_table_filter)
                    control=DialogCombobox(self, name=id, textvariable=textvar, values=items)
                else:
                    control=tk.Label(self,name=id, textvariable=textvar)

                self.add_control(control, row=self._total_rows,column=col,colspan=colspan, name=id,data_src=data_src,
                    data_bind=data_bind, textvar=textvar, default_value=default_value)

            if 'weight' in row.attrib:
                tk.Grid.rowconfigure(self,self._total_rows,weight=1)
            self._total_rows+=1

            if c>self._total_columns:
                self._total_columns=c
            c=0

    def __generic_event_handler(self,event, message):
        self._fire_external_event(event,event.widget.extra, message)

    @staticmethod
    def create_root():
        root=tk.Tk()
        root.resizable(width = 1, height = 1)
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        return root

    def add_control(self, control, row=0, column=0, colspan=1, name="", data_src="", data_bind="", textvar=None, default_value=""):
        control.bind("<Button-1>", lambda event: self.__generic_event_handler(event, "leftclick"))
        control.bind("<Button-2>", lambda event: self.__generic_event_handler(event, "middleclick"))
        control.bind("<Button-3>", lambda event: self.__generic_event_handler(event, "rightclick"))
        control.bind("<FocusIn>", lambda event: self.__generic_event_handler(event, "focusin"))
        control.bind("<FocusOut>", lambda event: self.__generic_event_handler(event, "focusout"))
        control.bind("<<TreeviewSelect>>", lambda event: self.__generic_event_handler(event, "itemselect"))

        control.extra=name
        sticky='nswe'
        if isinstance(control, tk.Label):
            sticky='nswe'

        control.grid(row=row, column=column, sticky=sticky, columnspan=colspan, padx=1, pady=1)
        self._controls.append({"control": control,
            "data_bind": data_bind, "data_src": data_src, "id":name, "name": name, "textvar": textvar, "default_value": default_value})

    def get_control(self, control_name):
        for control in self._controls:
            if control['name']==control_name:
                return control

        raise NameError(f'Control not found: {control_name}')

    def get_control_by_data_bind(self, data_src, data_bind):
        result=[]
        for control in self._controls:
            if control['data_bind']==data_bind and control['data_src']==data_src:
                result.append(control)

        return result

    def bind(self, data_src, data):
        self._datasource[data_src]=data
        for k,v in data.items():
            controls=self.get_control_by_data_bind(data_src, k)
            if v==None: v=''
            for control in controls:
                if isinstance(control['control'], DialogCombobox):
                    control['control'].set(v)
                else:
                    if control['textvar'] != None:
                        control['textvar'].set(v)

    def get_bind_data(self, data_src):
        result={}

        for control in self._controls:
            value=None
            if control['data_src']==data_src:
                if isinstance(control['control'],DialogCombobox):
                    value=control['control'].get()
                else:
                    if not control['textvar']==None:
                        value=control['textvar'].get()

                if value=="":
                    value=None

                result[control['data_bind']]=value
        return result

    def reset(self, data_src):
        for control in self._controls:
            if control['data_src']==data_src:
                control['textvar'].set(control['default_value'])

    def get_dialog_mode(self, data_src="data"):
        return self._data_mode[data_src]

    def set_dialog_record_id(self, id, data_src="data"):
        self._data_record_id[data_src]=id
        if id == None:
            self._data_mode[data_src]=DataDialogMode.NEW
        else:
            self._data_mode[data_src]=DataDialogMode.EDIT

    def get_dialog_record_id(self,data_src="data"):
        return self._data_record_id[data_src]

class DialogInput(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)

class DialogButton(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)

class DialogCombobox(ttk.Combobox):
    def __init__(self, parent, *args, **options):
        self.dict = {}
        self.dict_keys = {}

        if 'values' in options:
            keys=[]
            for item in options['values']:
                keys.append(item['name'])
                self.dict_keys[item['id']]=item['name']
                self.dict[item['name']]=item['id']

            options['values']=keys

        ttk.Combobox.__init__(self,parent,*args, **options)

        self.bind('<<ComboboxSelected>>', self.on_select)

    def on_select(self, event):
        #print(self.get())
        pass

    def get(self):
        if ttk.Combobox.get(self)=='':
            return ''

        return self.dict[ttk.Combobox.get(self)]

    def set(self,value):
        for k,v in self.dict_keys.items():
            if k.lower()==str(value).lower():
                #v=self.dict_keys[value.lower()]
                ttk.Combobox.set(self, v)


def generate_combo_source(table_name, filter_xml_string):
    params={"table_name": table_name, "filter":f"{filter_xml_string}" }
    result=client.execute_action('generate_data_combo_source', params, json_out=True)
    if not 'data_source' in result:
        raise NameError(f'Could not find meta data for table: {table_name}')

    return result['data_source']

form_xml=f"""
<formxml>
    <rows>
        <row>
            <columns>
                <column id="search_yourcall" data_src="search" data_bind="yourcall" type="Input" label="Callsign"/>
                <column id="search_locator" data_src="search" data_binf="locator" type="Input" label="Locator" />
                <column id="search_logbook_id" data_table="log_logbooks" data_src="search" data_bind="logbook_id" type="Combobox" label="Logbook">
                    <filter>
                        <condition field="id" operator="neq" value="*"/>
                    </filter>
                </column>
                <column id="search" type="Button" text="Search"/>
            </columns>
        </row>

        <row>
            <columns>
            </columns>
        </row>

        <row weight="1">
            <columns>
            </columns>
        </row>

        <row>
            <columns>
                <column id="logbook_id" data_table="log_logbooks" data_src="data" data_bind="logbook_id" type="Combobox" label="Logbook">
                    <filter>
                        <condition field="id" operator="neq" value="*"/>
                    </filter>
                </column>

                <column id="mode_id" data_table="log_modes" data_src="data" data_bind="mode_id" type="Combobox" label="Mode">
                </column>

                <column id="rig_id" data_table="log_rigs" data_src="data" data_bind="rig_id" type="Combobox" label="Rig">
                </column>
            </columns>
        </row>


        <row>
            <columns>
                <column id="frequency" type="Input" label="QRG" data_src="data" data_bind="frequency"/>
                <column id="power" type="Input" label="Power" data_src="data" data_bind="power"/>
                <column id="logdate_utc" type="Input" label="Date (UTC)" data_src="data" data_bind="logdate_utc"/>
                <column id="start_utc" type="Input" label="Time" data_src="data" data_bind="start_utc"/>
            </columns>
        </row>

        <row>
            <columns>
                <column id="yourcall" type="Input" label="Callsign" data_src="data" data_bind="yourcall"/>
                <column id="viacall" type="Input" label="Via" data_src="data" data_bind="viacall"/>
                <column id="rxrst" type="Input" label="Rx rst" data_src="data" data_bind="rxrst"/>
                <column id="txrst" type="Input" label="Tx rst" data_src="data" data_bind="txrst"/>
            </columns>
        </row>
        <row>
            <columns>
                <column id="name" type="Input" label="Name" data_src="data" data_bind="name"/>
                <column id="qth" type="Input" label="QTH" data_src="data" data_bind="qth"/>
                <column id="locator" type="Input" label="Locator" data_src="data" data_bind="locator"/>
                <column id="country" type="Input" label="Country" data_src="data" data_bind="country"/>
            </columns>
        </row>

        <row>
            <columns>
                <column id="qsl_shipmentmode" type="Combobox" label="QSL" data_table="log_qslshipmentmodes" data_src="data" data_bind="qsl_shipmentmode"/>
                <column id="comment" type="Input" label="Comment" data_src="data" data_bind="comment"/>
                <column id="qslrecv" type="Checkbox" label="QSL in" data_src="data" data_bind="qslrecv"/>
                <column id="qslsend" type="Checkbox" label="QSL out" data_src="data" data_bind="qslsend"/>
            </columns>
        </row>

        <row>
            <columns>
                <column id="dxcc" type="Input" label="dxcc" data_src="data" data_bind="dxcc"/>
                <column id="cq" type="Input" label="cq zone" data_src="data" data_bind="cq"/>
                <column id="itu" type="Input" label="itu zone" data_src="data" data_bind="itu"/>
                <column id="dok" type="Input" label="DOK (DL only)" data_src="data" data_bind="dok"/>
            </columns>
        </row>

        <row>
            <columns>
                <column id="btn_new" type="Button" text="New"/>
                <column id="btn_save" type="Button" text="Save"/>
                <column id="btn_delete" type="Button" text="Delete"/>
                <column id="btn_default" type="Button" text="Default"/>
            </columns>
        </row>

    </rows>
</formxml>
"""

def load_log_list(treev, **kwargs):
    for item in treev.get_children():
        ui.get_control("treev")['control'].delete(item)

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

    logs=load_log_list(treev, yourcall=ui.get_control("search_yourcall")['control'].get(),
        locator=ui.get_control("search_locator")['control'].get(), logbook_id=ui.get_control("search_logbook_id")['control'].get() )

def on_yourcall_change(event,dialog, control_name, event_name):
    call=ui.get_control(control_name)['control'].get()
    result=client.execute_action("tuxlog_get_dxcc_info",{"call":call},json_out=True)
    ui.bind("data", {"cq":result['cq_zone'],"itu":result['itu_zone'],"dxcc": result['dxcc'],"yourcall":call.upper()})

def on_save_click(event,dialog,control_name, event_name):
    result=ui.get_bind_data("data")
    print(result)
    if ui.get_dialog_mode("data")==DataDialogMode.NEW:
        print(client.create("log_logs", result))
    elif ui.get_dialog_mode("data")==DataDialogMode.EDIT:
        print(client.update("log_logs",ui.get_dialog_record_id("data"), result))

    load_log_list(ui.get_control("treev")['control'])
    ui.reset("data")
    ui.set_dialog_record_id(None, "data")

def on_delete_click(event,dialog,control_name,event_name):
    id=dialog.get_dialog_record_id("data")
    print(client.delete("log_logs",id))
    dialog.set_dialog_record_id(None,"data")
    load_log_list(ui.get_control("treev")['control'])


def on_new_click(event, control_name,event_name):
    ui.reset("data")
    ui.set_dialog_record_id(None, "data")

def on_item_click(event,dialog,control_name,event_name):
    id=ui.get_control(control_name)['control'].focus()
    result=client.read("log_logs", id, json_out=True)
    ui.bind("data", result)
    ui.set_dialog_record_id(id, "data")

xml=ET.fromstring(form_xml)
ui=DataDialog(DataDialog.create_root(),xml)
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

logs=load_log_list(treev)


ui.bind("data", {"yourcall": "dk9mbs"})

ui._root.mainloop()
print(client.logoff())
