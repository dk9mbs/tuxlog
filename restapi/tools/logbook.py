from tkinter import ttk
import tkinter as tk
import json
import xml.etree.ElementTree as ET

from clientlib import RestApiClient

client=RestApiClient("http://10.8.1.1:5001/api")
client.login("tuxlog", "password")

class Ui(tk.Frame):
    def __init__(self, parent,form_xml, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._root=parent
        self._callbacks=[]
        self._control_dict={}

        self._total_rows=0
        self._total_columns=0

        self.__read_form_xml(form_xml)

        self.grid(row=0, column=0, sticky=("N","S","E","W"))

        #for y in range(self._total_rows):
        #    tk.Grid.rowconfigure(self, y, weight=1)

        for x in range(self._total_columns):
            tk.Grid.columnconfigure(self, x, weight=1)

    def register_callback(self, control_name, event_name, fn):
        callback={"fn":fn, "control_name":control_name, "event_name":event_name}
        self._callbacks.append(callback)

    def _fire_external_event(self, event, control_name, event_name):
        for callback in self._callbacks:
            if callback['control_name']==control_name and callback['event_name']==event_name:
                callback['fn'](event, control_name, event_name)

    def __read_form_xml(self, tree):
        c=0
        for row in tree.find('rows').findall('row'):
            for column in row.find('columns').findall('column'):
                c+=2

                colspan=0
                id=column.attrib['id']
                type=column.attrib['type']
                databind=""

                if 'databind' in column.attrib:
                    databind=column.attrib['databind']

                label=None
                if 'label' in column.attrib:
                    col=c-1
                    colspan=1
                    label=tk.Label(self,name=f"lab_{id}", text=f"{column.attrib['label']}" , height=1, bg="gray")
                    label.extra = f"lab_{id}"
                    self.add_control(label, row=self._total_rows,column=c-2,colspan=colspan, name=f"lab_{id}")
                else:
                    col=c-2
                    colspan=2

                control=tk.Entry(self,name=id)
                control.bind("<Button-1>", lambda event: self.__generic_event_handler(event, "on_leftclick"))
                control.bind("<Button-2>", lambda event: self.__generic_event_handler(event, "on_middleclick"))
                control.bind("<Button-3>", lambda event: self.__generic_event_handler(event, "on_rightclick"))
                self.add_control(control, row=self._total_rows,column=col,colspan=colspan, name=id, databind=databind)

            if 'weight' in row.attrib:
                tk.Grid.rowconfigure(self,self._total_rows,weight=1)
            self._total_rows+=1

            if c>self._total_columns:
                self._total_columns=c
            c=0

    def __generic_event_handler(self,event, event_name):
        self._fire_external_event(event, event.widget.extra, event_name)

    @staticmethod
    def create_root():
        root=tk.Tk()
        root.resizable(width = 1, height = 1)
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        return root

    def add_control(self, control, row=0, column=0, colspan=1, name="", databind=""):
        control.extra=name
        control.databind=databind
        sticky='nswe'
        if isinstance(control, tk.Label):
            sticky='nswe'

        control.grid(row=row, column=column, sticky=sticky, columnspan=colspan, padx=1, pady=1)
        self._control_dict[name]={"control": control}

    def get_control(self, control_name):
        if control_name in self._control_dict:
            return self._control_dict[control_name]['control']

        raise NameError(f'Control not found: {control_name}')

form_xml=f"""
<formxml>
    <rows>
        <row>
            <columns>
                <column id="search_yourcall" type="Input" label="Callsign"/>
                <column id="search_locator" type="Input" label="Locator" />
                <column id="search_logbook_id" type="Input" label="Logbook"/>
            </columns>
        </row>
        <row>
            <columns>
                <column id="search" type="Button"/>
            </columns>
        </row>
        <row weight="1">
            <columns>
            </columns>
        </row>
        <row>
            <columns>
                <column id="yourcall" type="Input" label="Callsign" databind="yourcall"/>
                <column id="locator" type="Input" label="Locator" databind="locator"/>
                <column id="logbook_id" type="Input" label="Logbook" databind="logbook_id"/>
            </columns>
        </row>
    </rows>
</formxml>
"""

def load_log_list(**kwargs):
    where=[]
    if 'yourcall' in kwargs:
        value=kwargs['yourcall']
        if value != "" and value != None:
            where.append(f"""<condition field="yourcall" value="{value}" operator="like"/>""" )
    if 'locator' in kwargs:
        value=kwargs['locator']
        if value != "" and value != None:
            where.append(f"""<condition field="locator" value="{value}" operator="like"/>""" )

    filter=''.join(where)
    if filter != "":
        filter=f"<filter>{filter}</filter>"

    fetch=f"""
    <restapi type="select">
        <table name="log_logs" alias="l"/>
        <select>
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

    return logs

def on_search_click(event, control_name, event_name):
    for item in ui.get_control("treev").get_children():
        ui.get_control("treev").delete(item)

    logs=load_log_list(yourcall=ui.get_control("search_yourcall").get(), locator=ui.get_control("search_locator").get() )
    for log in logs:
        treev.insert("", 'end', text ="Hallo",values =(log['yourcall'], 
            log['logdate_utc'], log['start_utc'],log['end_utc'], log['logbook_id'],log['mode_id'],log['adif_name'],log['frequency'],
            log['continent'],log['country']))


xml=ET.fromstring(form_xml)
ui=Ui(Ui.create_root(),xml)
ui.register_callback("search","on_leftclick", on_search_click)

treev = ttk.Treeview(ui, selectmode ='browse')
ui.add_control(treev,row=2,column=0, colspan=6, name="treev")

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

logs=load_log_list()
for log in logs:
    treev.insert("", 'end', text ="Hallo",values =(log['yourcall'], 
        log['logdate_utc'], log['start_utc'],log['end_utc'], log['logbook_id'],log['mode_id'],log['adif_name'],log['frequency'],
        log['continent'],log['country']))


ui._root.mainloop()
print(client.logoff())
