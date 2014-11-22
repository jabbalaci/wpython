This is the root of a project that you want to put
in a virtual environment using virtualenvwrapper.

Create a virt. env. Here I want to use Python 2:

    mkvirtualenv -p `which python2` virtualenvwrapper_project

Activate the virt. env., install the package listed in `requirements.txt`,
then deactivate the virt. env.

Now, if you try to launch `demo.py` using the system-wide Python interpreter,
you will get an error.

----------

Edit the `.venv` file. In my case its content looks like this:

    /home/jabba/.virtualenvs/virtualenvwrapper_project

Make sure that wpython is in your PATH. Then launch `demo.py` freely,
without activating the virt. env.:

    $ wpython demo.py
    $ wpython demo.py 3 4 5      # passing three parameters
    $ wpython -h                 # help
    $ wpython -s demo.py         # no debug info
    $ wpython                    # prints usage
    $ wpython subfolder/demo.py  # go deep :)

It should work now.
