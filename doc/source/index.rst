Python bindings to the OpenStack Tuskar API
===========================================

This is a client for OpenStack Tuskar API. There's a Python API
(the :mod:`tuskarclient` module), and a command-line script
(installed as :program:`tuskar`).

Python API
==========

You can use the API like so::

  >>> from tuskarclient.client import Client
  >>> tuskar = Client('1', endpoint=tuskar_url)

Reference
---------

.. toctree::
    :maxdepth: 1

    ref/index
    ref/v1/index
    ref/v2/index

Command-line Tool
=================

.. toctree::
    :maxdepth: 1

    cli/v2/index

Man Pages
=========

.. toctree::
    :maxdepth: 1

    man/tuskar

Contributing
============

Code is hosted `on OpenStack git`_. Submit bugs to the Tuskar project on
`Launchpad`_. Submit code to the openstack/python-tuskarclient project
using `Gerrit`_.

.. _on OpenStack git: http://git.openstack.org/cgit/openstack/python-tuskarclient
.. _Launchpad: https://launchpad.net/python-tuskarclient
.. _Gerrit: http://docs.openstack.org/infra/manual/developers.html#development-workflow
