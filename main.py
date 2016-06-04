#!/usr/bin/env python

try:
  from pwn import *
except:
  import sys
  print "pwntools must be installed"
  sys.exit(1)

HOST = "google.com"
PORT =  80

FILENAME = "client.py"
CLIENT_TYPE = "remote"
HEADER = "#!/usr/bin/env python"
FILE_TEMPLATE = ""
FILE_TEMPLATE += HEADER
FILE_TEMPLATE += """
from pwn import *

{}

def main():
{} 
if __name__ == "__main__":
  main()
"""

interaction = r"""
  r.sendline('GET / HTTP/1.1\n\n')
  print r.recvline()
""".lstrip('\n')

def chooseClientType():
  types = ["ssh", "remote", "local", "shell"]
  v = options("Choose a type.", types)
  print "You chose: {}".format(types[v])

def saveFile():
  client = open(FILENAME, "w")
  connection = "r = remote('{}', {})".format(HOST, PORT)
  contents = FILE_TEMPLATE.format(connection, interaction)
  client.write(contents)
  client.close()

def main():
  print "Running PwnUp v0.0.1"
  chooseClientType()
  saveFile()
  print "Client Written to {}".format(FILENAME)
  print "Done."

if __name__ == "__main__":
  main()
