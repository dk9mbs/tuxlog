#!/usr/bin/python3.5

import pexpect
import sys

print("+===================================+")
print("|pwizproxy.py                       |")

python=sys.argv[1]
host=sys.argv[2]
database=sys.argv[3]
username=sys.argv[4]
password=sys.argv[5]
modelfile=sys.argv[6]

print("+-----------------------------------+")
print("|python => "+sys.argv[1])
print("|host => "+sys.argv[2])
print("|database => "+sys.argv[3])
print("|username => "+sys.argv[4])
print("|password => ********")
print("|model => "+sys.argv[6])
print("+===================================+")

cmd='%s -m pwiz -e mysql -u %s -P -H %s %s' % (python,username,host, database) 

print("spawning the command ...")
child = pexpect.spawn(cmd)
print("waiting for Password")
child.expect('Password:')
print("sending password")
child.sendline(password)
print ("waiting for EOF...")
child.expect(pexpect.EOF, timeout=None)
cmd_show_data = child.before.decode('UTF-8')

cmd_output = cmd_show_data.split('\r\n')
found=False
with open(modelfile,'w') as f:
    for line in cmd_output:
        if str(line.replace(" ","")).startswith("database=") and found==False: 
            print ("Database definition found ... replace with DatabaseProxy() ")
            f.write('database = DatabaseProxy()\n')
            found=True
        elif str(line).startswith("from peewee import *"):
            print ("Imports found and replce with playhous")
            f.write(line+'\n')
            f.write('from playhouse.signals import Model as PModel\n')
            f.write('from playhouse.signals import post_save\n')
        elif str(line).startswith("class BaseModel(Model)"):
            print("BaseModel found and replace")
            f.write('class BaseModel(PModel):\n')
        else:
            f.write(line+'\n')       


print("+===================================+")
print("|exit pwizproxy.py                  |")
print("+===================================+")
