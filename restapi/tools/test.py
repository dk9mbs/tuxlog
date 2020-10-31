from tkinter import ttk
from enum import Enum
import tkinter as tk
import json
import xml.etree.ElementTree as ET
import logging

from dialoglib import DataDialog, DataDialogMode

def init_dialog(app):
    root=tk.Toplevel(app.master)
    f=open('log.dialog.xml','r')
    form_xml=f.read()
    xml=ET.fromstring(form_xml)
    f.close()

    ui=DataDialog(root,xml,app.client)
    #ui.register_callback("search","leftclick", on_search_click)
    #ui.register_callback("yourcall", "focusout", on_yourcall_change)
    #ui.register_callback("btn_save", "leftclick", on_save_click)
    #ui.register_callback("btn_new","leftclick", on_new_click)
    #ui.register_callback("btn_delete","leftclick", on_delete_click)
    #ui.register_callback("treev","itemselect",on_item_click)

    ui.bind("data", {"yourcall": "dk9mbs"})

    menu = tk.Menu(ui.get_root())
    ui.get_root().config(menu=menu)
    filemenu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=lambda: generic_item_event('NewFile') )
    filemenu.add_command(label="Open...", command=lambda: generic_item_event(''))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=ui.get_root().quit)
    helpmenu = tk.Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=lambda: generic_item_event('About'))

