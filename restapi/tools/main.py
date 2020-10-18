import tkinter as tk

from clientlib import RestApiClient
import logbook
import test


class TuxlogApiClient(RestApiClient):
    def __init__(self, root_url):
        super().__init__(root_url=root_url)

client=TuxlogApiClient("http://localhost:5001/api")
client.login("tuxlog", "password")


def create_root(root=None):
    if root==None:
        root=tk.Tk()
    else:
        root=tk.Toplevel(root)

    root.resizable(width = 1, height = 1)
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    return root


root=create_root()
root.title("tuxlog starter")
root.geometry("300x50")

menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Logbook", command=lambda: logbook.init_dialog(client, create_root(root) ))
filemenu.add_command(label="Test", command=lambda: test.init_dialog(client, create_root(root) ))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)



root.mainloop()
print(client.logoff())
