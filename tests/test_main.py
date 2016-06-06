from pwn import *
import pwn

import pwnup

def test_restoreWrite():
  pwnInstance = pwnup.PwnUp()
  sys.stdout.write = 5
  pwnInstance.restoreWrite()
  assert sys.stdout.write == pwnInstance.oldWrite

def test_restoreInput():
  pwnInstance = pwnup.PwnUp()
  pwn.tube.send = "something else"
  pwnInstance.restoreInput()
  assert pwn.tube.send == pwnInstance.oldSend

def test_writeStub():
  pwnInstance = pwnup.PwnUp()
  pwnInstance.stubWrite()
  print("test")
  pwnInstance.restoreWrite()
  assert pwnInstance.all_io == [(1, "test"), (1, "\n")]

def xtest_inputStub():
  pwnInstance = pwnup.PwnUp()
  oldSend = pwnInstance.oldSend
  oldSendStub = lambda x, y: x
  pwnInstance.oldSend = oldSendStub
  pwnInstance.stubInput()
  pwn.tube.send(5, "things")
  pwnInstance.restoreWrite()
  pwnInstance.oldSend = oldSend
  assert pwnInstance.all_io == [(0, "things")]

