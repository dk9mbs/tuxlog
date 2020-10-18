from dialoglib import DataDialog
from clientlib import RestApiClient
import logbook

client=RestApiClient("http://localhost:5001/api")
client.login("tuxlog", "password")

root=DataDialog.create_root()
logbook.init_dialog(client, root)


root.mainloop()
print(client.logoff())
