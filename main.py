#!/usr/bin/env python

try:
  from pwn import *
except:
  import sys
  print "pwntools must be installed"
  sys.exit(1)

FILENAME = "client.py"
HEADER = "#!/usr/bin/env python"
FILE_TEMPLATE = ""
FILE_TEMPLATE += HEADER
FILE_TEMPLATE += """
from pwn import *

def main():
  {}

if __name__ == "__main__":
  main()
"""

def saveFile():
  client = open(FILENAME, "w")
  contents = FILE_TEMPLATE.format("print 'Hello!'")
  client.write(contents)
  client.close()

def main():
  print "Running PwnUp v0.0.1"
  saveFile()
  print "Client Written to {}".format(FILENAME)
  print "Done."

if __name__ == "__main__":
  main()
