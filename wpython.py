#!/usr/bin/env python
# encoding: utf-8

"""
wpython.py
==========
                                    __   __
              .--.--.--.-----.--.--|  |_|  |--.-----.-----.
              |  |  |  |  _  |  |  |   _|     |  _  |     |
              |________|   __|___  |____|__|__|_____|__|__|
                       |__|  |_____|

With wpython you can launch scripts residing in virtual environments
without the need of activating the venv.

When you want to execute a script in a venv, what do you usually do?
Activate the venv, execute the script, deactivate the venv. But what if
you want to call a venv'ed script in batch mode from another script?

Each venv has its own Python interpreter. When you execute a script in the
venv, this Python interpreter is used to run the script. If you don't
want to activate the venv, then you need to provide the path of this
Python interpreter. Example:

    /path/to/venv/bin/python /path/to/script.py

wpython reduces it to:

    wpython /path/to/script.py

wpython figures out the path of the Python interpreter in the venv
and passes /path/to/script.py to this local interpreter.

Requirements
------------
wpython relies on the excellent unipath library, which provides a sane
way to work with files and directories.
It comes bundled with wpython or you can install it system-wide.

Tested with
-----------
It was tested under Linux with Python 2 and Python 3.

Usage
-----
1) Put wpython.py somewhere in your PATH.
   Tip: I put two symbolic links on it: wpython and wpy.

2) In the root of your venv'ed project directory create a file called ".venv".
   The content of this file should be the path of the directory
   where the virtual env. is created by the commands virtualenv or
   virtualenvwrapper.
   This path can be either absolute or relative.
   You can also rename ".venv", see the VENV_FILE constant in the source below.

virtualenvwrapper example
-------------------------
Say we have our project directory here: `/home/jabba/python/wpython_demo`.
In this folder launch this command:

    mkvirtualenv wpython_demo

It creates the virtual environment here: `/home/jabba/.virtualenvs/wpython_demo.`
Then create the file `/home/jabba/python/wpython_demo/.venv` with this content:

    /home/jabba/.virtualenvs/wpython_demo

Say you have a `demo.py` file in this wpython_demo project. Launch it like this:

    $ cd /home/jabba/python/wpython_demo
    $ wpython demo.py

Notice that we didn't have to activate the virtual environment.

virtualenv example
------------------
Say you put your virtual environment in the root of the project folder
under a subdirectory called "venv". In this case the content of the ".venv"
file can be a relative path:

    $ cat .venv
    venv

You launch a script the same way as explained for virtualenvwrapper.

Extra feature
-------------
With wpython you can also launch scripts that are not in the project's
root folder but deep in a subfolder. You still need just one ".venv" file
in the project's root. If wpython doesn't find the file `.venv` in the folder
of the script to be launched, it will start stepping back to the parent
folders. It will use the first `.venv` file it finds.

Author:
-------
Laszlo Szathmary, alias Jabba Laci, 2014 (jabba.laci@gmail.com)
https://github.com/jabbalaci

ASCII logo made with http://patorjk.com/software/taag
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import shlex
import sys
from subprocess import call

from unipath import Path

VENV_FILE = '.venv'  # rename it if you want
DEBUG = True         # you can also switch debug mode off with the -s option


def my_call(python_path, prg, args):
    """
    Pass the script and its arguments to the Python interpreter in the venv.
    """
    cmd = "{pp} {prg} {args}".format(pp=python_path,
                                     prg=prg,
                                     args=' '.join(args))
    args = shlex.split(cmd)
    call(args)


def find_venv_file(folder):
    """
    Find the .venv file. If necessary, go up to the parent folders.
    """
    venv_file = Path(folder, VENV_FILE)
    while not (venv_file.isfile() or folder == "/"):
        folder = folder.parent
        venv_file = Path(folder, VENV_FILE)
    #
    if venv_file.isfile():
        if DEBUG:
            print("# venv file: {f}".format(f=venv_file), file=sys.stderr)
        return venv_file
    # else
    print("Error: {f} file is missing.".format(f=VENV_FILE), file=sys.stderr)
    sys.exit(1)


def print_usage(help=False):
    print("Usage: wpython  script_in_virtualenvwrapper.py  [arg]...")
    if help:
        print("""
Options:
    -h, --help:        this help
    -s:                silent mode (no debug info)
        """.strip())


def check_args(args):
    """
    Process options passed to wpython.
    """
    global DEBUG

    if args[0] in ("-h", "--help"):
        print_usage(help=True)
        sys.exit(0)

    if args[0] == "-s":
        # silent mode, no debug info
        DEBUG = False
        args = args[1:]

    # Treat all options above. This part below is for the unknown options:
    if len(args) == 0:
        print_usage()
        sys.exit(1)

    if args[0].startswith("-"):
        print("Error: unknown option: {o}".format(o=args[0]), file=sys.stderr)
        sys.exit(1)

    return args


def main():
    """
    Controller.
    """
    args = sys.argv[1:]
    if len(args) == 0:
        print_usage()
        sys.exit(0)

    args = check_args(args)

    prg = args[0]    # script in venv
    args = args[1:]  # arguments of the script in venv

    p = Path(prg).absolute()
    venv_file = find_venv_file(p.parent)

    venv_dir = Path(venv_file.read_file().strip())
    # .venv can also contain a relative path
    if not venv_dir.isabsolute():
        venv_dir = Path(venv_file.parent, venv_dir).norm()

    if not venv_dir.isdir():
        print("Error: {vd} is not a directory.".format(vd=venv_dir),
              file=sys.stderr)
        sys.exit(1)
    #
    python_path = Path(venv_dir, "bin/python")
    if not python_path.isfile():
        print("Error: {pp} is missing.".format(pp=python_path),
              file=sys.stderr)
        sys.exit(1)

    if DEBUG:
        print("# venv dir:  {d}".format(d=venv_dir), file=sys.stderr)

    my_call(python_path, prg, args)

##############################################################################

if __name__ == "__main__":
    main()
