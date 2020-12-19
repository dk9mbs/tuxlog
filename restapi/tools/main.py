import sys
import tkinter as tk
import time
from threading import Thread

from clientlib import RestApiClient
from rigctl import RigCtl
import logbook
import test


class TuxlogApiClient(RestApiClient):
    def __init__(self, root_url):
        super().__init__(root_url=root_url)

username=sys.argv[1]
password=sys.argv[2]
api_url=sys.argv[3]
#http://localhost:5001/api
client=TuxlogApiClient(api_url)
client.login(username, password)



class App(tk.Frame):
    def __init__(self, master, client):
        if master==None:
            master=self._create_root()
        super().__init__(master)

        self._pubsub_handler=[]
        self.client=client

        self.master.title("tuxlog")
        self.master.geometry("300x50")

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Logbook", command=lambda: self.open_window(logbook) )
        #filemenu.add_command(label="Test", command=lambda: test.init_dialog(self ))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        #button=tk.Button(master=self.master, text="hallo", command=self.test)
        #button.pack()

    def open_window(self, module):
        root=self._create_root(self.master)
        root.protocol("WM_DELETE_WINDOW", lambda: module.close_window(self, root))
        module.open_window(self, root)

    def publish(self, topic, message):
        for handler in self._pubsub_handler:
            if handler['topic']==topic:
                handler['fn'](topic, message, handler['args'])

    def subscribe(self,client_id, topic,fn_handler, args=None):
        self._pubsub_handler.append({"client_id": client_id, "topic":topic, "fn": fn_handler, "args": args})

    def unsubscribe(self,client_id, topic=None):
        for handler in self._pubsub_handler:
            if handler['client_id']==client_id and (topic==None or handler['topic']==topic):
                self._pubsub_handler.remove(handler)

    def _create_root(self, root=None):
        if root==None:
            root=tk.Tk()
        else:
            root=tk.Toplevel(root)

        root.resizable(width = 1, height = 1)
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        return root


def read_rigctl(app, host, port):
    while True:
        result=None
        try:
            rig=RigCtl({"host":"localhost", "port":4532})
            result=rig.get_rig("f")
            app.publish("rigctl.read.frequency",float(result['response']['Frequency'])/1000000 )
        except ConnectionRefusedError as err:
            app.publish("rigctl.error.connection_refused_error", str(err))
            print(err)
        except:
            print(result)
        #    print("Fehler")

        time.sleep(5)

app=App(None, client)


t=Thread(target=read_rigctl, args=(app,"ft817","3502"))
t.daemon=True
t.start()

app.master.mainloop()
print(client.logoff())
