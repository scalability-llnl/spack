.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _environments:

============
Environments
============

An environment is used to group together a set of specs for the
purpose of building, rebuilding and deploying in a coherent fashion.
Environments provide a number of advantages over the *à la carte*
approach of building and loading individual Spack modules:

#. Environments separate the steps of (a) choosing what to
   install, (b) concretizing, and (c) installing.  This allows
   Environments to remain stable and repeatable, even if Spack packages
   are upgraded: specs are only re-concretized when the user
   explicitly asks for it.  It is even possible to reliably
   transport environments between different computers running
   different versions of Spack!
#. Environments allow several specs to be built at once; a more robust
   solution than ad-hoc scripts making multiple calls to ``spack
   install``.
#. An Environment that is built as a whole can be loaded as a whole
   into the user environment. An Environment can be built to maintain
   a filesystem view of its packages, and the environment can load
   that view into the user environment at activation time. Spack can
   also generate a script to load all modules related to an
   environment.

Other packaging systems also provide environments that are similar in
some ways to Spack environments; for example, `Conda environments
<https://conda.io/docs/user-guide/tasks/manage-environments.html>`_ or
`Python Virtual Environments
<https://docs.python.org/3/tutorial/venv.html>`_.  Spack environments
provide some distinctive features:

#. A spec installed "in" an environment is no different from the same
   spec installed anywhere else in Spack.  Environments are assembled
   simply by collecting together a set of specs.
#. Spack Environments may contain more than one spec of the same
   package.

Spack uses a "manifest and lock" model similar to `Bundler gemfiles
<https://bundler.io/man/gemfile.5.html>`_ and other package
managers. The user input file is named ``spack.yaml`` and the lock
file is named ``spack.lock``

.. _environments-using:

------------------
Using Environments
------------------

Here we follow a typical use case of creating, concretizing,
installing and loading an environment.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating a named Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An environment is created by:

.. code-block:: console

   $ spack env create myenv

Spack then creates the directory ``var/spack/environments/myenv``.

.. note::

   All named environments are stored in the ``var/spack/environments`` folder.

In the ``var/spack/environments/myenv`` directory, Spack creates the
file ``spack.yaml`` and the hidden directory ``.spack-env``.

Spack stores metadata in the ``.spack-env`` directory. User
interaction will occur through the ``spack.yaml`` file and the Spack
commands that affect it. When the environment is concretized, Spack
will create a file ``spack.lock`` with the concrete information for
the environment.

In addition to being the default location for the view associated with
an Environment, the ``.spack-env`` directory also contains:

  * ``repo/``: A repo consisting of the Spack packages used in this
    environment.  This allows the environment to build the same, in
    theory, even on different versions of Spack with different
    packages!
  * ``logs/``: A directory containing the build logs for the packages
    in this Environment.

Spack Environments can also be created from either a ``spack.yaml``
manifest or a ``spack.lock`` lockfile. To create an Environment from a
``spack.yaml`` manifest:

.. code-block:: console

   $ spack env create myenv spack.yaml

To create an Environment from a ``spack.lock`` lockfile:

.. code-block:: console

   $ spack env create myenv spack.lock

Either of these commands can also take a full path to the
initialization file.

A Spack Environment created from a ``spack.yaml`` manifest is
guaranteed to have the same root specs as the original Environment,
but may concretize differently. A Spack Environment created from a
``spack.lock`` lockfile is guaranteed to have the same concrete specs
as the original Environment. Either may obviously then differ as the
user modifies it.

^^^^^^^^^^^^^^^^^^^^^^^^^
Activating an Environment
^^^^^^^^^^^^^^^^^^^^^^^^^

To activate an environment, use the following command:

.. code-block:: console

   $ spack env activate myenv

By default, the ``spack env activate`` will load the view associated
with the Environment into the user environment. The ``-v,
--with-view`` argument ensures this behavior, and the ``-V,
--without-view`` argument activates the environment without changing
the user environment variables.

The ``-p`` option to the ``spack env activate`` command modifies the
user's prompt to begin with the environment name in brackets.

.. code-block:: console

   $ spack env activate -p myenv
   [myenv] $ ...

To deactivate an environment, use the command:

.. code-block:: console

   $ spack env deactivate

or the shortcut alias

.. code-block:: console

   $ despacktivate

If the environment was activated with its view, deactivating the
environment will remove the view from the user environment.

^^^^^^^^^^^^^^^^^^^^^^
Anonymous Environments
^^^^^^^^^^^^^^^^^^^^^^

Any directory can be treated as an environment if it contains a file
``spack.yaml``. To load an anonymous environment, use:

.. code-block:: console

   $ spack env activate -d /path/to/directory

Anonymous specs can be created in place using the command:

.. code-block:: console

   $ spack env create -d .

In this case Spack simply creates a spack.yaml file in the requested
directory.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Environment Sensitive Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack commands are environment sensitive. For example, the ``find``
command shows only the specs in the active Environment if an
Environment has been activated. Similarly, the ``install`` and
``uninstall`` commands act on the active environment.

.. code-block:: console

  $ spack find
  ==> 0 installed packages

  $ spack install zlib@1.2.11
  ==> Installing zlib-1.2.11-q6cqrdto4iktfg6qyqcc5u4vmfmwb7iv
  ==> No binary for zlib-1.2.11-q6cqrdto4iktfg6qyqcc5u4vmfmwb7iv found: installing from source
  ==> zlib: Executing phase: 'install'
  [+] ~/spack/opt/spack/linux-rhel7-broadwell/gcc-8.1.0/zlib-1.2.11-q6cqrdto4iktfg6qyqcc5u4vmfmwb7iv

  $ spack env activate myenv

  $ spack find
  ==> In environment myenv
  ==> No root specs
  ==> 0 installed packages

  $ spack install zlib@1.2.8
  ==> Installing zlib-1.2.8-yfc7epf57nsfn2gn4notccaiyxha6z7x
  ==> No binary for zlib-1.2.8-yfc7epf57nsfn2gn4notccaiyxha6z7x found: installing from source
  ==> zlib: Executing phase: 'install'
  [+] ~/spack/opt/spack/linux-rhel7-broadwell/gcc-8.1.0/zlib-1.2.8-yfc7epf57nsfn2gn4notccaiyxha6z7x
  ==> Updating view at ~/spack/var/spack/environments/myenv/.spack-env/view

  $ spack find
  ==> In environment myenv
  ==> Root specs
  zlib@1.2.8

  ==> 1 installed package
  -- linux-rhel7-broadwell / gcc@8.1.0 ----------------------------
  zlib@1.2.8

  $ despacktivate

  $ spack find
  ==> 2 installed packages
  -- linux-rhel7-broadwell / gcc@8.1.0 ----------------------------
  zlib@1.2.8  zlib@1.2.11


Note that when we installed the abstract spec ``zlib@1.2.8``, it was
presented as a root of the Environment. All explicitly installed
packages will be listed as roots of the Environment.

All of the Spack commands that act on the list of installed specs are
Environment-sensitive in this way, including ``install``,
``uninstall``, ``activate``, ``deactivate``, ``find``, ``extensions``,
and more. In the :ref:`environment-configuration` section we will discuss
Environment-sensitive commands further.

^^^^^^^^^^^^^^^^^^^^^
Adding Abstract Specs
^^^^^^^^^^^^^^^^^^^^^

An abstract spec is the user-specified spec before Spack has applied
any defaults or dependency information.

Users can add abstract specs to an Environment using the ``spack add``
command. The most important component of an Environment is a list of
abstract specs.

Adding a spec adds to the manifest (the ``spack.yaml`` file), which is
used to define the roots of the Environment, but does not affect the
concrete specs in the lockfile, nor does it install the spec.

The ``spack add`` command is environment aware. It adds to the
currently active environment. All environment aware commands can also
be called using the ``spack -e`` flag to specify the environment.

.. code-block:: console

   $ spack env activate myenv
   $ spack add mpileaks

or

.. code-block:: console

   $ spack -e myenv add python

.. _environments_concretization:

^^^^^^^^^^^^
Concretizing
^^^^^^^^^^^^

Once some user specs have been added to an environment, they can be
concretized. *By default specs are concretized separately*, one after
the other. This mode of operation permits to deploy a full
software stack where multiple configurations of the same package
need to be installed alongside each other. Central installations done
at HPC centers by system administrators or user support groups
are a common case that fits in this behavior.
Environments *can also be configured to concretize all
the root specs in a self-consistent way* to ensure that
each package in the environment comes with a single configuration. This
mode of operation is usually what is required by software developers that
want to deploy their development environment.

Regardless of which mode of operation has been chosen, the following
command will ensure all the root specs are concretized according to the
constraints that are prescribed in the configuration:

.. code-block:: console

   [myenv]$ spack concretize

In the case of specs that are not concretized together, the command
above will concretize only the specs that were added and not yet
concretized. Forcing a re-concretization of all the specs can be done
instead with this command:

.. code-block:: console

   [myenv]$ spack concretize -f

When the ``-f`` flag is not used to reconcretize all specs, Spack
guarantees that already concretized specs are unchanged in the
environment.

The ``concretize`` command does not install any packages. For packages
that have already been installed outside of the environment, the
process of adding the spec and concretizing is identical to installing
the spec assuming it concretizes to the exact spec that was installed
outside of the environment.

The ``spack find`` command can show concretized specs separately from
installed specs using the ``-c`` (``--concretized``) flag.

.. code-block:: console

  [myenv]$ spack add zlib
  [myenv]$ spack concretize
  [myenv]$ spack find -c
  ==> In environment myenv
  ==> Root specs
  zlib

  ==> Concretized roots
  -- linux-rhel7-x86_64 / gcc@4.9.3 -------------------------------
  zlib@1.2.11

  ==> 0 installed packages


.. _installing-environment:

^^^^^^^^^^^^^^^^^^^^^^^^^
Installing an Environment
^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to installing individual specs into an Environment, one
can install the entire Environment at once using the command

.. code-block:: console

   [myenv]$ spack install

If the Environment has been concretized, Spack will install the
concretized specs. Otherwise, ``spack install`` will first concretize
the Environment and then install the concretized specs.

As it installs, ``spack install`` creates symbolic links in the
``logs/`` directory in the Environment, allowing for easy inspection
of build logs related to that environment. The ``spack install``
command also stores a Spack repo containing the ``package.py`` file
used at install time for each package in the ``repos/`` directory in
the Environment.

^^^^^^^
Loading
^^^^^^^

Once an environment has been installed, the following creates a load
script for it:

.. code-block:: console

   $ spack env loads -r

This creates a file called ``loads`` in the environment directory.
Sourcing that file in Bash will make the environment available to the
user; and can be included in ``.bashrc`` files, etc.  The ``loads``
file may also be copied out of the environment, renamed, etc.

----------
spack.yaml
----------

Spack environments can be customized at finer granularity by editing
the ``spack.yaml`` manifest file directly.

.. _environment-configuration:

^^^^^^^^^^^^^^^^^^^^^^^^
Configuring Environments
^^^^^^^^^^^^^^^^^^^^^^^^

A variety of Spack behaviors are changed through Spack configuration
files, covered in more detail in the :ref:`configuration`
section.

Spack Environments provide an additional level of configuration scope
between the custom scope and the user scope discussed in the
configuration documentation.

There are two ways to include configuration information in a Spack Environment:

#. Inline in the ``spack.yaml`` file

#. Included in the ``spack.yaml`` file from another file.

Many Spack commands also affect configuration information in files
automatically. Those commands take a ``--scope`` argument, and the
environment can be specified by ``env:NAME`` (to affect environment
``foo``, set ``--scope env:foo``). These commands will automatically
manipulate configuration inline in the ``spack.yaml`` file.

"""""""""""""""""""""
Inline configurations
"""""""""""""""""""""

Inline Environment-scope configuration is done using the same yaml
format as standard Spack configuration scopes, covered in the
:ref:`configuration` section. Each section is contained under a
top-level yaml object with it's name. For example, a ``spack.yaml``
manifest file containing some package preference configuration (as in
a ``packages.yaml`` file) could contain:

.. code-block:: yaml

   spack:
     ...
     packages:
       all:
         compiler: [intel]
     ...

This configuration sets the default compiler for all packages to
``intel``.

"""""""""""""""""""""""
Included configurations
"""""""""""""""""""""""

Spack environments allow an ``include`` heading in their yaml
schema. This heading pulls in external configuration files and applies
them to the Environment.

.. code-block:: yaml

   spack:
     include:
     - relative/path/to/config.yaml
     - /absolute/path/to/packages.yaml

Environments can include files with either relative or absolute
paths. Inline configurations take precedence over included
configurations, so you don't have to change shared configuration files
to make small changes to an individual Environment. Included configs
listed earlier will have higher precedence, as the included configs are
applied in reverse order.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Manually Editing the Specs List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The list of abstract/root specs in the Environment is maintained in
the ``spack.yaml`` manifest under the heading ``specs``.

.. code-block:: yaml

   spack:
       specs:
         - ncview
         - netcdf
         - nco
         - py-sphinx

Appending to this list in the yaml is identical to using the ``spack
add`` command from the command line. However, there is more power
available from the yaml file.

"""""""""""""""""""
Spec concretization
"""""""""""""""""""

Specs can be concretized separately or together, as already
explained in :ref:`environments_concretization`. The behavior active
under any environment is determined by the ``concretization`` property:

.. code-block:: yaml

   spack:
       specs:
         - ncview
         - netcdf
         - nco
         - py-sphinx
       concretization: together

which can currently take either one of the two allowed values ``together`` or ``separately``
(the default).

.. admonition:: Re-concretization of user specs

   When concretizing specs together the entire set of specs will be
   re-concretized after any addition of new user specs, to ensure that
   the environment remains consistent. When instead the specs are concretized
   separately only the new specs will be re-concretized after any addition.

"""""""""""""
Spec Matrices
"""""""""""""

Entries in the ``specs`` list can be individual abstract specs or a
spec matrix.

A spec matrix is a yaml object containing multiple lists of specs, and
evaluates to the cross-product of those specs. Spec matrices also
contain an ``excludes`` directive, which eliminates certain
combinations from the evaluated result.

The following two Environment manifests are identical:

.. code-block:: yaml

   spack:
     specs:
       - zlib %gcc@7.1.0
       - zlib %gcc@4.9.3
       - libelf %gcc@7.1.0
       - libelf %gcc@4.9.3
       - libdwarf %gcc@7.1.0
       - cmake

   spack:
     specs:
       - matrix:
           - [zlib, libelf, libdwarf]
           - ['%gcc@7.1.0', '%gcc@4.9.3']
         exclude:
           - libdwarf%gcc@4.9.3
       - cmake

Spec matrices can be used to install swaths of software across various
toolchains.

The concretization logic for spec matrices differs slightly from the
rest of Spack. If a variant or dependency constraint from a matrix is
invalid, Spack will reject the constraint and try again without
it. For example, the following two Environment manifests will produce
the same specs:

.. code-block:: yaml

   spack:
     specs:
       - matrix:
           - [zlib, libelf, hdf5+mpi]
           - [^mvapich2@2.2, ^openmpi@3.1.0]

   spack:
     specs:
       - zlib
       - libelf
       - hdf5+mpi ^mvapich2@2.2
       - hdf5+mpi ^openmpi@3.1.0

This allows one to create toolchains out of combinations of
constraints and apply them somewhat indiscriminately to packages,
without regard for the applicability of the constraint.

""""""""""""""""""""
Spec List References
""""""""""""""""""""

The last type of possible entry in the specs list is a reference.

The Spack Environment manifest yaml schema contains an additional
heading ``definitions``. Under definitions is an array of yaml
objects. Each object has one or two fields. The one required field is
a name, and the optional field is a ``when`` clause.

The named field is a spec list. The spec list uses the same syntax as
the ``specs`` entry. Each entry in the spec list can be a spec, a spec
matrix, or a reference to an earlier named list. References are
specified using the ``$`` sigil, and are "splatted" into place
(i.e. the elements of the referent are at the same level as the
elements listed separately). As an example, the following two manifest
files are identical.

.. code-block:: yaml

   spack:
     definitions:
       - first: [libelf, libdwarf]
       - compilers: ['%gcc', '%intel']
       - second:
           - $first
           - matrix:
               - [zlib]
               - [$compilers]
     specs:
       - $second
       - cmake

   spack:
     specs:
       - libelf
       - libdwarf
       - zlib%gcc
       - zlib%intel
       - cmake

.. note::

   Named spec lists in the definitions section may only refer
   to a named list defined above itself. Order matters.

In short files like the example, it may be easier to simply list the
included specs. However for more complicated examples involving many
packages across many toolchains, separately factored lists make
Environments substantially more manageable.

Additionally, the ``-l`` option to the ``spack add`` command allows
one to add to named lists in the definitions section of the manifest
file directly from the command line.

The ``when`` directive can be used to conditionally add specs to a
named list. The ``when`` directive takes a string of Python code
referring to a restricted set of variables, and evaluates to a
boolean. The specs listed are appended to the named list if the
``when`` string evaluates to ``True``. In the following snippet, the
named list ``compilers`` is ``['%gcc', '%clang', '%intel']`` on
``x86_64`` systems and ``['%gcc', '%clang']`` on all other systems.

.. code-block:: yaml

   spack:
     definitions:
       - compilers: ['%gcc', '%clang']
       - when: arch.satisfies('x86_64:')
         compilers: ['%intel']

.. note::

   Any definitions with the same named list with true ``when``
   clauses (or absent ``when`` clauses) will be appended together

The valid variables for a ``when`` clause are:

#. ``platform``. The platform string of the default Spack
   architecture on the system.

#. ``os``. The os string of the default Spack architecture on
   the system.

#. ``target``. The target string of the default Spack
   architecture on the system.

#. ``architecture`` or ``arch``. A Spack spec satisfying the default Spack
   architecture on the system. This supports querying via the ``satisfies``
   method, as shown above.

#. ``arch_str``. The architecture string of the default Spack architecture
   on the system.

#. ``re``. The standard regex module in Python.

#. ``env``. The user environment (usually ``os.environ`` in Python).

#. ``hostname``. The hostname of the system (if ``hostname`` is an
   executable in the user's PATH).

""""""""""""""""""""""""
SpecLists as Constraints
""""""""""""""""""""""""

Dependencies and compilers in Spack can be both packages in an
environment and constraints on other packages. References to SpecLists
allow a shorthand to treat packages in a list as either a compiler or
a dependency using the ``$%`` or ``$^`` syntax respectively.

For example, the following environment has three root packages:
``gcc@8.1.0``, ``mvapich2@2.3.1 %gcc@8.1.0``, and ``hdf5+mpi
%gcc@8.1.0 ^mvapich2@2.3.1``.

.. code-block:: yaml

   spack:
     definitions:
     - compilers: [gcc@8.1.0]
     - mpis: [mvapich2@2.3.1]
     - packages: [hdf5+mpi]

     specs:
     - $compilers
     - matrix:
       - [$mpis]
       - [$%compilers]
     - matrix:
       - [$packages]
       - [$^mpis]
       - [$%compilers]

This allows for a much-needed reduction in redundancy between packages
and constraints.

^^^^^^^^^^^^^^^^^^^^^^^^^
Environment-managed Views
^^^^^^^^^^^^^^^^^^^^^^^^^

Spack Environments can define filesystem views of their software,
which are maintained as packages and can be installed and uninstalled from
the Environment. Filesystem views provide an access point for packages
from the filesystem for users who want to access those packages
directly. For more information on filesystem views, see the section
:ref:`filesystem-views`.

Spack Environment managed views are updated every time the environment
is written out to the lock file ``spack.lock``, so the concrete
environment and the view are always compatible.

"""""""""""""""""""""""""""""
Configuring environment views
"""""""""""""""""""""""""""""

The Spack Environment manifest file has a top-level keyword
``view``. Each entry under that heading is a view descriptor, headed
by a name. The view descriptor contains the root of the view, and
optionally the projections for the view, and ``select`` and
``exclude`` lists for the view. For example, in the following manifest
file snippet we define a view named ``mpis``, rooted at
``/path/to/view`` in which all projections use the package name,
version, and compiler name to determine the path for a given
package. This view selects all packages that depend on MPI, and
excludes those built with the PGI compiler at version 18.5.

.. code-block:: yaml

   spack:
     ...
     view:
       mpis:
         root: /path/to/view
         select: [^mpi]
         exclude: ['%pgi@18.5']
         projections:
           all: {name}/{version}-{compiler.name}

For more information on using view projections, see the section on
:ref:`adding_projections_to_views`. The default for the ``select`` and
``exclude`` values is to select everything and exclude nothing. The
default projection is the default view projection (``{}``).

Any number of views may be defined under the ``view`` heading in a
Spack Environment.

There are two shorthands for environments with a single view. If the
environment at ``/path/to/env`` has a single view, with a root at
``/path/to/env/.spack-env/view``, with default selection and exclusion
and the default projection, we can put ``view: True`` in the
environment manifest. Similarly, if the environment has a view with a
different root, but default selection, exclusion, and projections, the
manifest can say ``view: /path/to/view``. These views are
automatically named ``default``, so that

.. code-block:: yaml

   spack:
     ...
     view: True

is equivalent to

.. code-block:: yaml

   spack:
     ...
     view:
       default:
         root: .spack-env/view

and

.. code-block:: yaml

   spack:
     ...
     view: /path/to/view

is equivalent to

.. code-block:: yaml

   spack:
     ...
     view:
       default:
         root: /path/to/view

By default, Spack environments are configured with ``view: True`` in
the manifest. Environments can be configured without views using
``view: False``. For backwards compatibility reasons, environments
with no ``view`` key are treated the same as ``view: True``.

From the command line, the ``spack env create`` command takes an
argument ``--with-view [PATH]`` that sets the path for a single, default
view. If no path is specified, the default path is used (``view:
True``). The argument ``--without-view`` can be used to create an
environment without any view configured.

The ``spack env view`` command can be used to change the manage views
of an Environment. The subcommand ``spack env view enable`` will add a
view named ``default`` to an environment. It takes an optional
argument to specify the path for the new default view. The subcommand
``spack env view disable`` will remove the view named ``default`` from
an environment if one exists. The subcommand ``spack env view
regenerate`` will regenerate the views for the environment. This will
apply any updates in the environment configuration that have not yet
been applied.

""""""""""""""""""""""""""""
Activating environment views
""""""""""""""""""""""""""""

The ``spack env activate`` command will put the default view for the
environment into the user's path, in addition to activating the
environment for Spack commands. The arguments ``-v,--with-view`` and
``-V,--without-view`` can be used to tune this behavior. The default
behavior is to activate with the environment view if there is one.

The environment variables affected by the ``spack env activate``
command and the paths that are used to update them are determined by
the :ref:`prefix inspections <customize-env-modifications>` defined in
your modules configuration; the defaults are summarized in the following
table.

=================== =========
Variable            Paths
=================== =========
PATH                bin
MANPATH             man, share/man
ACLOCAL_PATH        share/aclocal
LD_LIBRARY_PATH     lib, lib64
LIBRARY_PATH        lib, lib64
CPATH               include
PKG_CONFIG_PATH     lib/pkgconfig, lib64/pkgconfig, share/pkgconfig
CMAKE_PREFIX_PATH   .
=================== =========

Each of these paths are appended to the view root, and added to the
relevant variable if the path exists. For this reason, it is not
recommended to use non-default projections with the default view of an
environment.

The ``spack env deactivate`` command will remove the default view of
the environment from the user's path.
