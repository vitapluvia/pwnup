![PWNUP](./pwnup.png)

# pwnup

[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

### Installation:

`pip install pwnup`

### Usage:

- Run `pwnup` (optionally pass host & port if working with a remote server.)
- Select type of client
- After finished interacting, press `ctrl-d`/`ctrl-c` to end the session.
- It will drop a `client.py` file in the current directory.

### Description:

pwnup is a quick scaffolding tool to help generate pwntools-based clients.

It records your stdio when connecting to a local, remote or ssh server during a pwntools interactive session.  After recording it will dump a `client.py` file.

This could be thought of as the `autoexpect` for pwntools.

### Requirements:
- [Python](https://www.python.org/)
- [pwntools](https://github.com/Gallopsled/pwntools) or [binjitsu](https://github.com/binjitsu/binjitsu)
