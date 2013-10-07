===================
python-tuskarclient
===================

python-tuskarclient is a Python client and a command-line interface
for `Tuskar <https://github.com/openstack/tuskar>`_.


Getting Started
===============

Clone the repo::

    $ git clone https://github.com/openstack/python-tuskarclient.git

Then, use ``tox`` to set up a virtual environment and run tests::

    $ cd python-tuskarclient
    $ tox

When this is done, activate your virtual environment::

    $ source .tox/py27/bin/activate

Finally, use this script to build the wrapper script in your virtual
environment for the CLI tools::

    $ python setup.py develop


Use from Python
===============

For using ``python-tuskarclient`` within a Python application, `this
wiki page <https://github.com/tuskar/python-tuskarclient/wiki/Usage>`_
provides the most complete documentation.

Use from the CLI
================

On the command line, ``python-tuskarclient`` implements the ``tuskar``
command.

First, be sure to run all of the steps in the Getting Started section,
above, and that you have not deactivated your virtual environment.

Then, export these two environment variables, customizing them if
necessary::

    $ export OS_AUTH_TOKEN=nopass
    $ export TUSKAR_URL=http://localhost:8585/

(Note that 'nopass' is the correct value in a default setup with no
authentication.)

Now you may interact with Tuskar by using the ``tuskar``
command. ``tuskar --help`` with list full usage details. You can use
``tuskar rack-list`` as an example.
