# pwnup

[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

### Installation:

```
pip install pwntools
```

```
pip install pwnup
```

### Description:

pwnup is a quick scaffolding tool to help generate pwntools-based clients.

It records your stdio when connecting to a local, remote or ssh server during a pwntools interactive session.  After recording it will dump a `client.py` file.

This could be thought of as the `autoexpect` for pwntools.

### Requirements:
- [Python](https://www.python.org/)
- [pwntools](https://github.com/Gallopsled/pwntools) or [binjitsu](https://github.com/binjitsu/binjitsu)

### Usage:

- Simply run `pwnup` optionally pass host & port if working with remote server.
- Press `ctrl-d` or `ctrl-c` after recording interactive session.
- Once finished, it will drop a `client.py` file in the current directory.
