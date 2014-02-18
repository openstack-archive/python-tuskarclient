======
Tuskar
======

.. program:: tuskar

SYNOPSIS
========

  `tuskar` [options] <command> [command-options]

  `tuskar help`

  `tuskar help` <command>


DESCRIPTION
===========

`tuskar` is a command line client for controlling OpenStack Tuskar.

Before the `tuskar` command is issued, ensure the environment contains
the necessary variables so that the CLI can pass user credentials to
the server.
See `Getting Credentials for a CLI`  section of `OpenStack CLI Guide`
for more info.


OPTIONS
=======

To get a list of available commands and options run::

    tuskar help

To get usage and options of a command run::

    tuskar help <command>


EXAMPLES
========

Get information about stack-create command::

    tuskar help stack-create

List available stacks::

    tuskar stack-list

List available resources in a stack::

    tuskar resource-list <stack name>

Create a stack::

    tuskar stack-create mystack -f some-template.yaml -P "KeyName=mine"

View stack information::

    tuskar stack-show mystack

List events::

    tuskar event-list mystack

Delete a stack::

    tuskar stack-delete mystack

Abandon a stack::

    tuskar stack-abandon mystack

BUGS
====

Tuskar client is hosted in Launchpad so you can view current bugs at
https://bugs.launchpad.net/python-tuskarclient/.
