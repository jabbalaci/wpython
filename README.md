                          __   __
    .--.--.--.-----.--.--|  |_|  |--.-----.-----.
    |  |  |  |  _  |  |  |   _|     |  _  |     |
    |________|   __|___  |____|__|__|_____|__|__|
             |__|  |_____|

wpython.py
==========

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

The name **w**python refers to virtualenv**w**rapper. I use it with
virtualenvwrapper'ed projects but it also works with virtualenv.

Requirements
------------
wpython uses on the excellent unipath library, which provides a sane
way to work with files and directories.
It comes bundled with wpython but you can also install it system-wide.

Tested with
-----------
It was tested under Linux with Python 2 and Python 3.

Usage
-----
1) Put `wpython.py` somewhere in your PATH.
   Tip: I put two symbolic links on it: `wpython` and `wpy`.

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
* Laszlo Szathmary, alias Jabba Laci, 2014 (jabba.laci@gmail.com)
* https://github.com/jabbalaci

ASCII logo made with http://patorjk.com/software/taag
