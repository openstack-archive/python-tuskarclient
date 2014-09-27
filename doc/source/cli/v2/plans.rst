Plans commands with version 2 API
=================================

List All Plans
--------------
*tuskar plan-list [-h]*

Usage example:

::

    tuskar plan-list

This will show table of all Plans.

Example:

::

 +--------------------------------------+-------------+---------------------------+---------------------+
 | uuid                                 | name        | description               | roles               |
 +--------------------------------------+-------------+---------------------------+---------------------+
 | 53268a27-afc8-4b21-839f-90227dd7a001 | dev-cloud-3 | Development testing cloud | controller, compute |
 +--------------------------------------+-------------+---------------------------+---------------------+
 | a117fa66-1445-44c7-8ad1-7663d2607aca | test1       | None                      |                     |
 +--------------------------------------+-------------+---------------------------+---------------------+
 | c367b394-7179-4c44-85ed-bf84baaf9fee | dev-cloud-2 | Development testing cloud |                     |
 +--------------------------------------+-------------+---------------------------+---------------------+

Field 'roles' contains list of names of Roles assigned to the Plan.

Retrieve a Single Plan
----------------------
*tuskar plan-show [-h] <PLAN>*

Usage example:

::

    tuskar plan-show c367b394-7179-4c44-85ed-bf84baaf9fee

This command will show table with properties of the Plan and their values.

Example:

::

        +-------------+------------------------------------------------------------------------------------------+
        | Property    | Value                                                                                    |
        +-------------+------------------------------------------------------------------------------------------+
        | created_at  | 2014-09-26T13:36:28.804272                                                               |
        | description | Development testing cloud                                                                |
        | name        | dev-cloud-2                                                                              |
        | parameters  | ...                                                                                      |
        | roles       | description=OpenStack hypervisor node. Can be wrapped in a ResourceGroup for scaling.    |
        |             | name=compute                                                                             |
        |             | uuid=b7b1583c-5c80-481f-a25b-708ed4a39734                                                |
        |             | version=1                                                                                |
        |             |                                                                                          |
        |             | description=OpenStack control plane node. Can be wrapped in a ResourceGroup for scaling. |
        |             | name=controller                                                                          |
        |             | uuid=df9edfac-e009-4df1-ac7f-8931d37f4be6                                                |
        |             | version=1                                                                                |
        | updated_at  | None                                                                                     |
        | uuid        | c367b394-7179-4c44-85ed-bf84baaf9fee                                                     |
        +-------------+------------------------------------------------------------------------------------------+

Note: Parameters are displayed similarly as Roles, ie. set of properties with values. Each Parameter/Role separated by empty line from previous.

Create a New Plan
-----------------
*tuskar plan-create [-h] [-d <DESCRIPTION>] name*

Usage example:

::

    tuskar plan-create -d 'Description of new plan' new-plan-name

Output will be the same as for showing detail of a Plan.
Note that parameters and roles are not set for newly created Plan.

::

     +-------------+--------------------------------------+
     | Property    | Value                                |
     +-------------+--------------------------------------+
     | created_at  | 2014-09-27T00:10:33.958239           |
     | description | Description of new plan              |
     | name        | new-plan-name                        |
     | parameters  |                                      |
     | roles       |                                      |
     | updated_at  | None                                 |
     | uuid        | 839fcbbf-7aa0-4801-8ccb-d020da654dd6 |
     +-------------+--------------------------------------+

Delete an Existing Plan
-----------------------
*tuskar plan-delete [-h] <PLAN>*

Usage example:

::

    tuskar plan-delete 839fcbbf-7aa0-4801-8ccb-d020da654dd6

When successfully deleted, you will get message like this:

::

  Deleted Plan "new-plan-name".

Adding a Role to a Plan
-----------------------
*tuskar plan-add-role [-h] -r <ROLE UUID> plan_uuid*

Usage example:

::

    tuskar plan-add-role -r df9edfac-e009-4df1-ac7f-8931d37f4be6 c367b394-7179-4c44-85ed-bf84baaf9fee

This will assign Role specified by UUID to Plan.
Output of this command is the same as for plan-show.

Removing a Role from a Plan
---------------------------
*tuskar plan-remove-role [-h] -r <ROLE UUID> plan_uuid*

Usage example:

::

    tuskar plan-remove-role -r df9edfac-e009-4df1-ac7f-8931d37f4be6 c367b394-7179-4c44-85ed-bf84baaf9fee

This will unassign Role from a Plan. This will not delete the Role from Tuskar.
Output of this command is the same as for plan-show.

Changing a Plan’s Configuration Values
--------------------------------------
*tuskar plan-patch [-h] [-A <KEY1=VALUE1>] plan_uuid*

Usage example:

::

    tuskar plan-patch -A compute-1::CeilometerPassword=secret-password -A compute-1::CeilometerMeteringSecret=secret-secret 53268a27-afc8-4b21-839f-90227dd7a001

This command accepts multiple name=value pairs for parameters to be updated.
Above example will look for parameter named 'compute-1::CeilometerPassword' and update its value to 'secret-password'
and will do similar update for 'compute-1::CeilometerMeteringSecret' parameter.

This command can be used only for updating existing parameters. It is not possible to create new parameter this way.

Retrieve a Plan’s Template Files
--------------------------------
*tuskar plan-templates [-h] -O <OUTPUT DIR> plan_uuid*

Usage example:

::

    tuskar plan-templates -O templates 53268a27-afc8-4b21-839f-90227dd7a001

This command will retrieve contents of templates of the Plan and save them as files into specified directory.
-O/--output-dir is mandatory and application will create it if it does not exist.
Output is list of files with templates.

::

  Following templates has been written:
  templates/plan.yaml
  templates/environment.yaml
  templates/provider-controller-1.yaml
  templates/provider-compute-1.yaml
