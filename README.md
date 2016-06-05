# PwnUp

### Description:
PwnUp is a quick scaffolding tool to help generate pwntools-based clients.

It records your stdio when connecting to a local, remote or ssh server during a pwntools interactive session.  After recording it will dump a `client.py` file.

This could be thought of as the `autoexpect` for pwntools.

### Requirements:
- [Python](https://www.python.org/)
- [PwnTools](https://github.com/Gallopsled/pwntools) or [Binjitsu](https://github.com/binjitsu/binjitsu)

### Usage:
- Simply run `./main.py` after cloning.  Optionally pass host & port if working with remote server.
- Press `ctrl-d` or `ctrl-c` after recording is finished to dump a `client.py` file in the current directory.

