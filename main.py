#!/usr/bin/env python
import sys

try:
  from pwn import *
except:
  print "pwntools must be installed"
  sys.exit(1)

VERSION = "v0.0.1"

# Grab only the last N bytes instead of the exact match for recv's:
LAST_BYTES = 32

# - STUB OUT WRITE & SEND - #
# io_types: { stdin: 0, stdout: 1 }
# ALL_IO contains tuples of (io_type, value)
# -------------------------- #
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
# -------------------------- #
FILENAME = "client.py"

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
# -------------------------- #

def chooseClientType(host, port):
  types = ["ssh", "remote", "local"]
  v = options("Choose a type.", types)
  log.info("You Chose: {}".format(types[v]))
  if types[v] == "remote":
    host = host or raw_input("host > ")
    port = port or raw_input("port > ")
    return "r = remote('{}', {})".format(host, port)
  if types[v] == "local":
    binary = raw_input("binary > ")
    return "r = process('{}')".format(binary)
  if types[v] == "ssh":
    host = host or raw_input("host > ")
    port = port or raw_input("port > ")
    user = raw_input("user > ")
    password = raw_input("password > ")
    cmd = raw_input("cmd > ")
    sshCmd = "sh = ssh(host='{}', user='{}', password='{}', port={})\n".format(
        host, user, password, int(port))
    sshCmd += "r = sh.run('{}')".format(cmd)
    return sshCmd

def saveFile(connection, interaction, host, port):
  client = open(FILENAME, "w")
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

def interact(connection, host, port):
  exec(connection)
  last = -1 if "process" not in connection else -3
  result = ""
  log.info("Press <Ctrl-D> to stop recording ...")
  stubIO()
  r.interactive()
  restoreIO()
  for tup in ALL_IO[1:last]:
    result += "{}\n".format(getIOString(tup))

  return result

def checkArgs():
  host = ""
  port = ""
  if len(sys.argv) > 1:
    if sys.argv[1] in ["-h", "--help"]:
      print "Usage: pwnUp <host> <port>"
      sys.exit(1)
  if len(sys.argv) > 2:
    host = sys.argv[1]
    port = sys.argv[2]
  return host, port

def main():
  host, port = checkArgs()
  log.info("Running PwnUp {}".format(VERSION))
  connection = chooseClientType(host, port)
  interaction = interact(connection, host, port)
  saveFile(connection, interaction, host, port)
  log.info("Client Written to {}".format(FILENAME))

if __name__ == "__main__":
  main()
