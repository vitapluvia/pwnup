#!/usr/bin/env python
import sys

try:
  from pwn import *
except:
  print "pwntools must be installed"
  sys.exit(1)

# Grab only the last 32 bytes instead of the exact match for recv's:
LAST_BYTES = 32

# - STUB OUT WRITE & SEND - #
# io_types: { stdin: 0, stdout: 1 }
# ALL_IO contains tuples of (io_type, value)
OLD_WRITE = sys.stdout.write
OLD_SEND = tube.send
ALL_IO = []
ALL_WRITES = []
ALL_INPUTS = []

def restoreWrite(): sys.stdout.write = OLD_WRITE
def restoreInput(): tube.send = OLD_SEND

def stubWrite():
  def newWrite(v):
    OLD_WRITE(v)
    ALL_IO.append((1, v))
    ALL_WRITES.append(v)

  sys.stdout.write = newWrite

def stubInput():
  def newSend(tube, v):
    OLD_SEND(tube, v)
    ALL_IO.append((0, v))
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

def chooseClientType():
  types = ["ssh", "remote", "local", "shell"]
  v = options("Choose a type.", types)
  log.info("You Chose: {}".format(types[v]))

def saveFile(interaction):
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

def getIOString(tup):
  ioType = tup[0]
  value = tup[1]

  if (ioType == 0):
    return r"  r.send({})".format(repr(value))
  else:
      return r"  print r.recvuntil({})".format(repr(value[-LAST_BYTES:]))

def interact():
  r = remote(HOST, PORT)
  result = ""
  stubIO()
  r.interactive()
  restoreIO()
  for tup in ALL_IO[1:-2]:
    result += "{}\n".format(getIOString(tup))

  return result

def main():
  log.info("Running PwnUp v0.0.1")
  chooseClientType()
  interaction = interact()
  saveFile(interaction)
  log.info("Client Written to {}".format(FILENAME))

if __name__ == "__main__":
  main()
