Roles commands with version 2 API
=================================


Retrieving Possible Roles
-------------------------

*tuskar role-list [-h]*

Usage example:

::

    tuskar role-list

This will show table of all Roles:

Example:

::

    +--------------------------------------+------------+---------+------------------------------------------------------------------------------+
    | uuid                                 | name       | version | description                                                                  |
    +--------------------------------------+------------+---------+------------------------------------------------------------------------------+
    | b7b1583c-5c80-481f-a25b-708ed4a39734 | compute    | 1       | OpenStack hypervisor node. Can be wrapped in a ResourceGroup for scaling.    |
    | df9edfac-e009-4df1-ac7f-8931d37f4be6 | controller | 1       | OpenStack control plane node. Can be wrapped in a ResourceGroup for scaling. |
    +--------------------------------------+------------+---------+------------------------------------------------------------------------------+
