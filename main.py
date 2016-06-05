#!/usr/bin/env python
import sys

try:
  from pwn import *
except:
  print "pwntools must be installed"
  sys.exit(1)

##### STUB OUT WRITE & SEND #####
OLD_WRITE = sys.stdout.write
OLD_SEND = tube.send
ALL_WRITES = []
ALL_INPUTS = []

def restoreWrite(): sys.stdout.write = OLD_WRITE
def restoreInput(): tube.send = OLD_SEND

def stubWrite():
  def newWrite(v):
    OLD_WRITE(v)
    ALL_WRITES.append(v)

  sys.stdout.write = newWrite

def stubInput():
  def newSend(tube, v):
    OLD_SEND(tube, v)
    ALL_INPUTS.append(v)

  tube.send = newSend
##############################

FILENAME = "client.py"
CLIENT_TYPE = "remote"
HOST = "google.com"
PORT =  80

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
  log.info("You Chose: {}".format(types[v]))

def saveFile():
  client = open(FILENAME, "w")
  connection = "r = remote('{}', {})".format(HOST, PORT)
  contents = FILE_TEMPLATE.format(connection, interaction)
  client.write(contents)
  client.close()

def stubIO():
  stubWrite()
  stubInput()

def restoreIO():
  restoreInput()
  restoreWrite()

def interact():
  r = remote(HOST, PORT)
  stubIO()
  r.interactive()
  restoreIO()
  print ALL_INPUTS
  print ALL_WRITES[1:]


def main():
  log.info("Running PwnUp v0.0.1")
  chooseClientType()
  interact()
  saveFile()
  log.info("Client Written to {}".format(FILENAME))

if __name__ == "__main__":
  main()
