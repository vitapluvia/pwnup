#!/usr/bin/env python
from builtins import input
from io import open
import sys
import pwn

VERSION = "v0.0.1"

# Grab only the last N bytes instead of the exact match for recv's:
LAST_BYTES = 32

# - STUB OUT WRITE & SEND - #
# -------------------------- #
EOF_STR_READ = "Got EOF while reading in interactive"
EOF_STR_SEND = "Got EOF while sending in interactive"
EXIT_CODE_NOTE = " stopped with exit code "
CLOSED_SSH = " Closed SSH channel with "
INTERRUPT = "] Interrupted\n"

# - FILE CONSTANTS - #
# ------------------ #
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

class PwnUp():
  def __init__(self):
    # io_types: { stdin: 0, stdout: 1 }
    # self.all_io contains tuples of (io_type, value)
    self.all_io = []
    self.oldWrite = sys.stdout.write
    self.oldSend = pwn.tube.send
    self.filename = "client.py"

  def restoreWrite(self): sys.stdout.write = self.oldWrite
  def restoreInput(self): pwn.tube.send = self.oldSend

  def stubWrite(self):
    def newWrite(v):
      self.oldWrite(v)
      if EOF_STR_READ not in v \
        and EOF_STR_SEND not in v \
        and INTERRUPT not in v \
        and CLOSED_SSH not in v \
        and EXIT_CODE_NOTE not in v:
        self.all_io.append((1, v))

    sys.stdout.write = newWrite

  def stubInput(self):
    def newSend(tube, v):
      self.oldSend(tube, v)
      self.all_io.append((0, v))

    pwn.tube.send = newSend

  def chooseClientType(self, host, port):
    types = ["ssh", "remote", "local"]
    v = options("Choose a type.", types)
    log.info("You Chose: {}".format(types[v]))
    if types[v] == "remote":
      host = host or input("host > ")
      port = port or input("port > ")
      return "r = remote('{}', {})".format(host, port)
    if types[v] == "local":
      binary = input("binary > ")
      return "r = process('{}')".format(binary)
    if types[v] == "ssh":
      host = host or input("host > ")
      port = port or input("port > ")
      user = input("user > ")
      password = input("password > ")
      cmd = input("cmd > ")
      sshCmd = "sh = ssh(host='{}', user='{}', password='{}', port={})\n".format(
          host, user, password, int(port))
      sshCmd += "r = sh.run('{}')".format(cmd)
      return sshCmd

  def saveFile(self, connection, interaction):
    client = open(self.filename, "w", encoding="utf-8")
    contents = unicode(FILE_TEMPLATE.format(connection, interaction))
    client.write(contents)
    client.close()

  def stubIO(self):
    self.stubWrite()
    self.stubInput()

  def restoreIO(self):
    self.restoreInput()
    self.restoreWrite()

  def getIOString(self, tup):
    ioType = tup[0]
    value = tup[1]

    if (ioType == 0):
      return r"  r.send({})".format(repr(value))
    else:
      return r"  print(r.recvuntil({}))".format(repr(value[-LAST_BYTES:]))

  def interact(self, connection):
    exec(connection)
    result = ""
    log.info("Press <Ctrl-D> to stop recording ...")
    self.stubIO()
    r.interactive()
    self.restoreIO()
    for tup in self.all_io[1:]:
      result += "{}\n".format(self.getIOString(tup))

    return result

  def checkArgs(self):
    host = ""
    port = ""
    if len(sys.argv) > 1:
      if sys.argv[1] in ["-h", "--help"]:
        print("Usage: pwnUp <host> <port>")
        sys.exit(1)
    if len(sys.argv) > 2:
      host = sys.argv[1]
      port = sys.argv[2]
    return host, port

  def run(self):
    host, port = self.checkArgs()
    log.info("Running PwnUp {}".format(VERSION))
    connection = self.chooseClientType(host, port)
    interaction = self.interact(connection)
    self.saveFile(connection, interaction)
    log.info("Client Written to {}".format(self.filename))


if __name__ == "__main__":
  try:
    from pwn import *
  except:
    print("pwntools must be installed")
    sys.exit(1)

  PwnUp().run()

