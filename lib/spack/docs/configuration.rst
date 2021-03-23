.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _configuration:

===================
Configuration Files
===================

Spack has many configuration files.  Here is a quick list of them, in
case you want to skip directly to specific docs:

* :ref:`compilers.yaml <compiler-config>`
* :ref:`config.yaml <config-yaml>`
* :ref:`mirrors.yaml <mirrors>`
* :ref:`modules.yaml <modules>`
* :ref:`packages.yaml <build-settings>`
* :ref:`repos.yaml <repositories>`

-----------
YAML Format
-----------

Spack configuration files are written in YAML.  We chose YAML because
it's human readable, but also versatile in that it supports dictionaries,
lists, and nested sections. For more details on the format, see `yaml.org
<http://yaml.org>`_ and `libyaml <http://pyyaml.org/wiki/LibYAML>`_.
Here is an example ``config.yaml`` file:

.. code-block:: yaml

   config:
     install_tree: $spack/opt/spack
     module_roots:
       lmod: $spack/share/spack/lmod
     build_stage:
       - $tempdir/$user/spack-stage
       - ~/.spack/stage

Each Spack configuration file is nested under a top-level section
corresponding to its name. So, ``config.yaml`` starts with ``config:``,
``mirrors.yaml`` starts with ``mirrors:``, etc.

.. _configuration-scopes:

--------------------
Configuration Scopes
--------------------

Spack pulls configuration data from files in several directories. There
are six configuration scopes. From lowest to highest:

#. **defaults**: Stored in ``$(prefix)/etc/spack/defaults/``. These are
   the "factory" settings. Users should generally not modify the settings
   here, but should override them in other configuration scopes. The
   defaults here will change from version to version of Spack.

#. **system**: Stored in ``/etc/spack/``. These are settings for this
   machine, or for all machines on which this file system is
   mounted. The site scope can be used for settings idiosyncratic to a
   particular machine, such as the locations of compilers or external
   packages. These settings are presumably controlled by someone with
   root access on the machine. They override the defaults scope.

#. **site**: Stored in ``$(prefix)/etc/spack/``. Settings here affect
   only *this instance* of Spack, and they override the defaults and system
   scopes.  The site scope can can be used for per-project settings (one
   Spack instance per project) or for site-wide settings on a multi-user
   machine (e.g., for a common Spack instance).

#. **user**: Stored in the home directory: ``~/.spack/``. These settings
   affect all instances of Spack and take higher precedence than site,
   system, or defaults scopes.

#. **custom**: Stored in a custom directory specified by ``--config-scope``.
   If multiple scopes are listed on the command line, they are ordered
   from lowest to highest precedence.

#. **environment**: When using Spack :ref:`environments`, Spack reads
   additional configuration from the environment file. See
   :ref:`environment-configuration` for further details on these
   scopes. Environment scopes can be referenced from the command line
   as ``env:name`` (to reference environment ``foo``, use
   ``env:foo``).

#. **command line**: Build settings specified on the command line take
   precedence over all other scopes.

Each configuration directory may contain several configuration files,
such as ``config.yaml``, ``compilers.yaml``, or ``mirrors.yaml``.  When
configurations conflict, settings from higher-precedence scopes override
lower-precedence settings.

Commands that modify scopes (e.g., ``spack compilers``, ``spack repo``,
etc.) take a ``--scope=<name>`` parameter that you can use to control
which scope is modified.  By default, they modify the highest-precedence
scope.

.. _custom-scopes:

^^^^^^^^^^^^^
Custom scopes
^^^^^^^^^^^^^

In addition to the ``defaults``, ``system``, ``site``, and ``user``
scopes, you may add configuration scopes directly on the command
line with the ``--config-scope`` argument, or ``-C`` for short.

For example, the following adds two configuration scopes, named
``scopea`` and ``scopeb``, to a ``spack spec`` command:

.. code-block:: console

   $ spack -C ~/myscopes/scopea -C ~/myscopes/scopeb spec ncurses

Custom scopes come *after* the ``spack`` command and *before* the
subcommand, and they specify a single path to a directory full of
configuration files. You can add the same configuration files to that
directory that you can add to any other scope (``config.yaml``,
``packages.yaml``, etc.).

If multiple scopes are provided:

#. Each must be preceded with the ``--config-scope`` or ``-C`` flag.
#. They must be ordered from lowest to highest precedence.

"""""""""""""""""""""""""""""""""""""""""""
Example: scopes for release and development
"""""""""""""""""""""""""""""""""""""""""""

Suppose that you need to support simultaneous building of release and
development versions of ``mypackage``, where ``mypackage`` -> ``A`` -> ``B``.
You could create The following files:

.. code-block:: yaml
   :caption: ~/myscopes/release/packages.yaml

   packages:
       mypackage:
           version: [1.7]
       A:
           version: [2.3]
       B:
           version: [0.8]

.. code-block:: yaml
   :caption: ~/myscopes/develop/packages.yaml

   packages:
       mypackage:
           version: [develop]
       A:
           version: [develop]
       B:
           version: [develop]

You can switch between ``release`` and ``develop`` configurations using
configuration arguments.  You would type ``spack -C ~/myscopes/release``
when you want to build the designated release versions of ``mypackage``,
``A``, and ``B``, and you would type ``spack -C ~/myscopes/develop`` when
you want to build all of these packages at the ``develop`` version.

"""""""""""""""""""""""""""""""
Example: swapping MPI providers
"""""""""""""""""""""""""""""""

Suppose that you need to build two software packages, ``packagea`` and
``packageb``. ``packagea`` is Python 2-based and ``packageb`` is Python
3-based. ``packagea`` only builds with OpenMPI and ``packageb`` only builds
with MPICH. You can create different configuration scopes for use with
``packagea`` and ``packageb``:

.. code-block:: yaml
   :caption: ~/myscopes/packgea/packages.yaml

   packages:
       python:
           version: [2.7.11]
       all:
           providers:
               mpi: [openmpi]

.. code-block:: yaml
   :caption: ~/myscopes/packageb/packages.yaml

   packages:
       python:
           version: [3.5.2]
       all:
           providers:
               mpi: [mpich]


.. _platform-scopes:

------------------------
Platform-specific Scopes
------------------------

For each scope above (excluding environment scopes), there can also be
platform-specific settings.  For example, on most platforms, GCC is
the preferred compiler.  However, on macOS (darwin), Clang often works
for more packages, and is set as the default compiler. This
configuration is set in
``$(prefix)/etc/spack/defaults/darwin/packages.yaml``. It will take
precedence over settings in the ``defaults`` scope, but can still be
overridden by settings in ``system``, ``system/darwin``, ``site``,
``site/darwin``, ``user``, ``user/darwin``, ``custom``, or
``custom/darwin``. So, the full scope precedence is:

#. ``defaults``
#. ``defaults/<platform>``
#. ``system``
#. ``system/<platform>``
#. ``site``
#. ``site/<platform>``
#. ``user``
#. ``user/<platform>``
#. ``custom``
#. ``custom/<platform>``

You can get the name to use for ``<platform>`` by running ``spack arch
--platform``. The system config scope has a ``<platform>`` section for
sites at which ``/etc`` is mounted on multiple heterogeneous machines.

----------------
Scope Precedence
----------------

When spack queries for configuration parameters, it searches in
higher-precedence scopes first. So, settings in a higher-precedence file
can override those with the same key in a lower-precedence one. For
list-valued settings, Spack *prepends* higher-precedence settings to
lower-precedence settings. Completely ignoring higher-level configuration
options is supported with the ``::`` notation for keys (see
:ref:`config-overrides` below).

^^^^^^^^^^^
Simple keys
^^^^^^^^^^^

Let's look at an example of overriding a single key in a Spack file. If
your configurations look like this:

.. code-block:: yaml
   :caption: $(prefix)/etc/spack/defaults/config.yaml

   config:
     install_tree: $spack/opt/spack
     module_roots:
       lmod: $spack/share/spack/lmod
     build_stage:
       - $tempdir/$user/spack-stage
       - ~/.spack/stage


.. code-block:: yaml
   :caption: ~/.spack/config.yaml

   config:
     install_tree: /some/other/directory


Spack will only override ``install_tree`` in the ``config`` section, and
will take the site preferences for other settings. You can see the
final, combined configuration with the ``spack config get <configtype>``
command:

.. code-block:: console
   :emphasize-lines: 3

   $ spack config get config
   config:
     install_tree: /some/other/directory
     module_roots:
       lmod: $spack/share/spack/lmod
     build_stage:
       - $tempdir/$user/spack-stage
       - ~/.spack/stage


.. _config-overrides:

^^^^^^^^^^^^^^^^^^^^^^^^^^
Overriding entire sections
^^^^^^^^^^^^^^^^^^^^^^^^^^

Above, the user ``config.yaml`` only overrides specific settings in the
default ``config.yaml``. Sometimes, it is useful to *completely*
override lower-precedence settings. To do this, you can use *two* colons
at the end of a key in a configuration file. For example:

.. code-block:: yaml
   :emphasize-lines: 1
   :caption: ~/.spack/config.yaml

   config::
     install_tree: /some/other/directory

Spack will ignore all lower-precedence configuration under the
``config::`` section:

.. code-block:: console

   $ spack config get config
   config:
     install_tree: /some/other/directory


^^^^^^^^^^^^^^^^^^^^
List-valued settings
^^^^^^^^^^^^^^^^^^^^

Let's revisit the ``config.yaml`` example one more time. The
``build_stage`` setting's value is an ordered list of directories:

.. code-block:: yaml
   :caption: $(prefix)/etc/spack/defaults/config.yaml

   build_stage:
     - $tempdir/$user/spack-stage
     - ~/.spack/stage


Suppose the user configuration adds its *own* list of ``build_stage``
paths:

.. code-block:: yaml
   :caption: ~/.spack/config.yaml

   build_stage:
     - /lustre-scratch/$user/spack
     - ~/mystage


Spack will first look at the paths in the defaults ``config.yaml``, then the
paths in the user's ``~/.spack/config.yaml``. The list in the
higher-precedence scope is *prepended* to the defaults. ``spack config
get config`` shows the result:

.. code-block:: console
   :emphasize-lines: 7-10

   $ spack config get config
   config:
     install_tree: /some/other/directory
     module_roots:
       lmod: $spack/share/spack/lmod
     build_stage:
       - /lustre-scratch/$user/spack
       - ~/mystage
       - $tempdir/$user/spack-stage
       - ~/.spack/stage


As in :ref:`config-overrides`, the higher-precedence scope can
*completely* override the lower-precedence scope using ``::``. So if the
user config looked like this:

.. code-block:: yaml
   :emphasize-lines: 1
   :caption: ~/.spack/config.yaml

   build_stage::
     - /lustre-scratch/$user/spack
     - ~/mystage


The merged configuration would look like this:

.. code-block:: console
   :emphasize-lines: 7-8

   $ spack config get config
   config:
     install_tree: /some/other/directory
     module_roots:
       lmod: $spack/share/spack/lmod
     build_stage:
       - /lustre-scratch/$user/spack
       - ~/mystage


.. _config-file-variables:

---------------------
Config File Variables
---------------------

Spack understands several variables which can be used in config file
paths wherever they appear. There are three sets of these variables:
Spack-specific variables, environment variables, and user path
variables. Spack-specific variables and environment variables are both
indicated by prefixing the variable name with ``$``. User path variables
are indicated at the start of the path with ``~`` or ``~user``.

^^^^^^^^^^^^^^^^^^^^^^^^
Spack-specific variables
^^^^^^^^^^^^^^^^^^^^^^^^

Spack understands several special variables. These are:

* ``$spack``: path to the prefix of this Spack installation
* ``$tempdir``: default system temporary directory (as specified in
  Python's `tempfile.tempdir
  <https://docs.python.org/2/library/tempfile.html#tempfile.tempdir>`_
  variable.
* ``$user``: name of the current user

Note that, as with shell variables, you can write these as ``$varname``
or with braces to distinguish the variable from surrounding characters:
``${varname}``. Their names are also case insensitive, meaning that
``$SPACK`` works just as well as ``$spack``. These special variables are
substituted first, so any environment variables with the same name will
not be used.

^^^^^^^^^^^^^^^^^^^^^
Environment variables
^^^^^^^^^^^^^^^^^^^^^

After Spack-specific variables are evaluated, environment variables are
expanded. These are formatted like Spack-specific variables, e.g.,
``${varname}``. You can use this to insert environment variables in your
Spack configuration.

^^^^^^^^^^^^^^^^^^^^^
User home directories
^^^^^^^^^^^^^^^^^^^^^

Spack performs Unix-style tilde expansion on paths in configuration
files. This means that tilde (``~``) will expand to the current user's
home directory, and ``~user`` will expand to a specified user's home
directory. The ``~`` must appear at the beginning of the path, or Spack
will not expand it.

.. _configuration_environment_variables:

-------------------------
Environment Modifications
-------------------------

Spack allows to prescribe custom environment modifications in a few places
within its configuration files. Every time these modifications are allowed
they are specified as a dictionary, like in the following example:

.. code-block:: yaml

   environment:
     set:
       LICENSE_FILE: '/path/to/license'
     unset:
     - CPATH
     - LIBRARY_PATH
     append_path:
       PATH: '/new/bin/dir'

The possible actions that are permitted are ``set``, ``unset``, ``append_path``,
``prepend_path`` and finally ``remove_path``. They all require a dictionary
of variable names mapped to the values used for the modification.
The only exception is ``unset`` that requires just a list of variable names.
No particular order is ensured on the execution of each of these modifications.

----------------------------
Seeing Spack's Configuration
----------------------------

With so many scopes overriding each other, it can sometimes be difficult
to understand what Spack's final configuration looks like.

Spack provides two useful ways to view the final "merged" version of any
configuration file: ``spack config get`` and ``spack config blame``.

.. _cmd-spack-config-get:

^^^^^^^^^^^^^^^^^^^^
``spack config get``
^^^^^^^^^^^^^^^^^^^^

``spack config get`` shows a fully merged configuration file, taking into
account all scopes. For example, to see the fully merged
``config.yaml``, you can type:

.. code-block:: console

   $ spack config get config
   config:
     debug: false
     checksum: true
     verify_ssl: true
     dirty: false
     build_jobs: 8
     install_tree: $spack/opt/spack
     template_dirs:
     - $spack/templates
     directory_layout: {architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}
     module_roots:
       tcl: $spack/share/spack/modules
       lmod: $spack/share/spack/lmod
     build_stage:
     - $tempdir/$user/spack-stage
     - ~/.spack/stage
     - $spack/var/spack/stage
     source_cache: $spack/var/spack/cache
     misc_cache: ~/.spack/cache
     locks: true

Likewise, this will show the fully merged ``packages.yaml``:

.. code-block:: console

   $ spack config get packages

You can use this in conjunction with the ``-C`` / ``--config-scope`` argument to
see how your scope will affect Spack's configuration:

.. code-block:: console

   $ spack -C /path/to/my/scope config get packages


.. _cmd-spack-config-blame:

^^^^^^^^^^^^^^^^^^^^^^
``spack config blame``
^^^^^^^^^^^^^^^^^^^^^^

``spack config blame`` functions much like ``spack config get``, but it
shows exactly which configuration file each preference came from. If you
do not know why Spack is behaving a certain way, this can help you track
down the problem:

.. code-block:: console

   $ spack --insecure -C ./my-scope -C ./my-scope-2 config blame config
   ==> Warning: You asked for --insecure. Will NOT check SSL certificates.
   ---                                                   config:
   _builtin                                                debug: False
   /home/myuser/spack/etc/spack/defaults/config.yaml:72    checksum: True
   command_line                                            verify_ssl: False
   ./my-scope-2/config.yaml:2                              dirty: False
   _builtin                                                build_jobs: 8
   ./my-scope/config.yaml:2                                install_tree: /path/to/some/tree
   /home/myuser/spack/etc/spack/defaults/config.yaml:23    template_dirs:
   /home/myuser/spack/etc/spack/defaults/config.yaml:24    - $spack/templates
   /home/myuser/spack/etc/spack/defaults/config.yaml:28    directory_layout: {architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}
   /home/myuser/spack/etc/spack/defaults/config.yaml:32    module_roots:
   /home/myuser/spack/etc/spack/defaults/config.yaml:33      tcl: $spack/share/spack/modules
   /home/myuser/spack/etc/spack/defaults/config.yaml:34      lmod: $spack/share/spack/lmod
   /home/myuser/spack/etc/spack/defaults/config.yaml:49    build_stage:
   /home/myuser/spack/etc/spack/defaults/config.yaml:50    - $tempdir/$user/spack-stage
   /home/myuser/spack/etc/spack/defaults/config.yaml:51    - ~/.spack/stage
   /home/myuser/spack/etc/spack/defaults/config.yaml:52    - $spack/var/spack/stage
   /home/myuser/spack/etc/spack/defaults/config.yaml:57    source_cache: $spack/var/spack/cache
   /home/myuser/spack/etc/spack/defaults/config.yaml:62    misc_cache: ~/.spack/cache
   /home/myuser/spack/etc/spack/defaults/config.yaml:86    locks: True

You can see above that the ``build_jobs`` and ``debug`` settings are
built in and are not overridden by a configuration file. The
``verify_ssl`` setting comes from the ``--insceure`` option on the
command line. ``dirty`` and ``install_tree`` come from the custom
scopes ``./my-scope`` and ``./my-scope-2``, and all other configuration
options come from the default configuration files that ship with Spack.
