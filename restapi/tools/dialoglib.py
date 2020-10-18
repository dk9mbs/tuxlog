from tkinter import ttk
from enum import Enum
import tkinter as tk
import json
import xml.etree.ElementTree as ET
import logging

class DataDialogMode(Enum):
    UNDEFINED = 0
    NEW = 1
    EDIT = 2

class DataDialog(tk.Frame):
    def __init__(self, parent,form_xml,client, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._data_mode={"data": DataDialogMode.UNDEFINED}
        self._data_record_id={}
        self._client=client

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

    def get_client(self):
        return self._client

    def get_root(self):
        return self._root

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
                    items=generate_combo_source(self._client,data_table, data_table_filter)
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


def generate_combo_source(client, table_name, filter_xml_string):
    params={"table_name": table_name, "filter":f"{filter_xml_string}" }
    result=client.execute_action('generate_data_combo_source', params, json_out=True)
    if not 'data_source' in result:
        raise NameError(f'Could not find meta data for table: {table_name}')

    return result['data_source']

