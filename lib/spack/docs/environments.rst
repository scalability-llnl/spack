.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _environments:

=====================================
Environments (spack.yaml, spack.lock)
=====================================

An environment is used to group a set of specs intended for some purpose
to be built, rebuilt, and deployed in a coherent fashion. Environments
define aspects of the installation of the software, such as:

#. *which* specs to install;
#. *how* those specs are configured; and
#. *where* the concretized software will be installed.

Aggregating this information into an environment for processing has advantages
over the *à la carte* approach of building and loading individual Spack modules.

With environments, you concretize, install, or load (activate) all of the
specs with a single command. Concretization fully configures the specs
and dependencies of the environment in preparation for installing the
software. This is a more robust solution than ad-hoc installation scripts.
And you can share an environment or even re-use it on a different computer.

Environment definitions, especially *how* specs are configured, allow the
software to remain stable and repeatable even when Spack packages are upgraded. Changes are only picked up when the environment is explicitly re-concretized.

Defining *where* specs are installed supports a filesystem view of the
environment. Yet Spack maintains a single installation of the software that
can be re-used across multiple environments.

Activating an environment determines *when* all of the associated (and
installed) specs are loaded so limits the software loaded to those specs
actually needed by the environment. Spack can even generate a script to
load all modules related to an environment.

Other packaging systems also provide environments that are similar in
some ways to Spack environments; for example, `Conda environments
<https://conda.io/docs/user-guide/tasks/manage-environments.html>`_ or
`Python Virtual Environments
<https://docs.python.org/3/tutorial/venv.html>`_.  Spack environments
provide some distinctive features though:

#. A spec installed "in" an environment is no different from the same
   spec installed anywhere else in Spack.
#. Spack environments may contain more than one spec of the same
   package.

Spack uses a "manifest and lock" model similar to `Bundler gemfiles
<https://bundler.io/man/gemfile.5.html>`_ and other package managers.
The environment's user input file (or manifest), is named ``spack.yaml``.
The lock file, which contains the fully configured and concretized specs,
is named ``spack.lock``.

.. _environments-using:

------------------
Using Environments
------------------

Here we follow a typical use case of creating, concretizing,
installing and loading an environment.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating a managed Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An environment is created by:

.. code-block:: console

   $ spack env create myenv

The directory ``$SPACK_ROOT/var/spack/environments/myenv`` is created
to manage the environment.

.. note::

   All managed environments by default are stored in the
   ``$SPACK_ROOT/var/spack/environments`` folder. This location can be changed
   by setting the ``environments_root`` variable in ``config.yaml``.

Spack creates the file ``spack.yaml``, hidden directory ``.spack-env``, and
``spack.lock`` file under ``$SPACK_ROOT/var/spack/environments/myenv``. User
interaction occurs through the ``spack.yaml`` file and the Spack commands
that affect it. Metadata and, by default, the view are stored in the
``.spack-env`` directory. When the environment is concretized, Spack creates
the ``spack.lock`` file with the fully configured specs and dependencies for
the environment.

The ``.spack-env`` subdirectory also contains:

  * ``repo/``: A subdirectory acting as the repo consisting of the Spack
    packages used in the environment. It allows the environment to build
    the same, in theory, even on different versions of Spack with different
    packages!
  * ``logs/``: A subdirectory containing the build logs for the packages
    in this environment.

Spack Environments can also be created from either the user input, or
manifest, file or the lockfile. Create an environment from a manifest using:

.. code-block:: console

   $ spack env create myenv spack.yaml

The resulting environment is guaranteed to have the same root specs as
the original but may concretize differently in the presence of different
explicit or default configuration settings (e.g., a different version of
Spack or for a different user account).

Create an environment from a ``spack.lock`` file using:

.. code-block:: console

   $ spack env create myenv spack.lock

The resulting environment, when on the same or a compatible machine, is
guaranteed to initially have the same concrete specs as the original.

.. note::

   Environment creation also accepts a full path to the file.

   If the path is not under the ``$SPACK_ROOT/var/spack/environments``
   directory then the source is referred to as an
   :ref:`independent environment <independent_environments>`.

^^^^^^^^^^^^^^^^^^^^^^^^^
Activating an Environment
^^^^^^^^^^^^^^^^^^^^^^^^^

To activate an environment, use the following command:

.. code-block:: console

   $ spack env activate myenv

By default, the ``spack env activate`` will load the view associated
with the environment into the user environment. The ``-v,
--with-view`` argument ensures this behavior, and the ``-V,
--without-view`` argument activates the environment without changing
the user environment variables.

The ``-p`` option to the ``spack env activate`` command modifies the
user's prompt to begin with the environment name in brackets.

.. code-block:: console

   $ spack env activate -p myenv
   [myenv] $ ...

The ``activate`` command can also be used to create a new environment, if it is
not already defined, by adding the ``--create`` flag. Managed and independent
environments can both be created using the same flags that `spack env create`
accepts.  If an environment already exists then spack will simply activate it
and ignore the create-specific flags.

.. code-block:: console
   
   $ spack env activate --create -p myenv
   # ...
   # [creates if myenv does not exist yet]
   # ...
   [myenv] $ ...

To deactivate an environment, use the command:

.. code-block:: console

   $ spack env deactivate

or the shortcut alias

.. code-block:: console

   $ despacktivate

If the environment was activated with its view, deactivating the
environment will remove the view from the user environment.

.. _independent_environments:

^^^^^^^^^^^^^^^^^^^^^^^^
Independent Environments
^^^^^^^^^^^^^^^^^^^^^^^^

Independent environments can be located in any directory outside of Spack.

.. note::

   When uninstalling packages, Spack asks the user to confirm the removal of packages
   that are still used in a managed environment. This is not the case for independent
   environments.

To create an independent environment, use one of the following commands:

.. code-block:: console

   $ spack env create --dir my_env
   $ spack env create ./my_env

As a shorthand, you can also create an independent environment upon activation if it does not
already exist:

.. code-block:: console

   $ spack env activate --create ./my_env

For convenience, Spack can also place an independent environment in a temporary directory for you:

.. code-block:: console

   $ spack env activate --temp


^^^^^^^^^^^^^^^^^^^^^^^^^^
Environment-Aware Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack commands are environment-aware. For example, the ``find``
command shows only the specs in the active environment if an
environment has been activated. Otherwise it shows all specs in
the Spack instance. The same rule applies to the ``install`` and
``uninstall`` commands.

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
presented as a root of the environment. All explicitly installed
packages will be listed as roots of the environment.

All of the Spack commands that act on the list of installed specs are
environment-aware in this way, including ``install``,
``uninstall``, ``find``, ``extensions``, etcetera. In the
:ref:`environment-configuration` section we will discuss
environment-aware commands further.

^^^^^^^^^^^^^^^^^^^^^
Adding Abstract Specs
^^^^^^^^^^^^^^^^^^^^^

An abstract spec is the user-specified spec before Spack applies
defaults or dependency information.

Users can add abstract specs to an environment using the ``spack add``
command. The most important component of an environment is a list of
abstract specs.

Adding a spec adds it as a root spec of the environment in the user
input file (``spack.yaml``). It does not affect the concrete specs
in the lock file (``spack.lock``) and it does not install the spec.

The ``spack add`` command is environment-aware. It adds the spec to the
currently active environment. An error is generated if there isn't an
active environment. All environment-aware commands can also
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

Once user specs have been added to an environment, they can be concretized.
There are three different modes of operation to concretize an environment,
explained in detail in :ref:`environments_concretization_config`.
Regardless of which mode of operation is chosen, the following
command will ensure all of the root specs are concretized according to the
constraints that are prescribed in the configuration:

.. code-block:: console

   [myenv]$ spack concretize

In the case of specs that are not concretized together, the command
above will concretize only the specs that were added and not yet
concretized. Forcing a re-concretization of all of the specs can be done
by adding the ``-f`` option:

.. code-block:: console

   [myenv]$ spack concretize -f

Without the option, Spack guarantees that already concretized specs are
unchanged in the environment.

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

In addition to adding individual specs to an environment, one
can install the entire environment at once using the command

.. code-block:: console

   [myenv]$ spack install

If the environment has been concretized, Spack will install the
concretized specs. Otherwise, ``spack install`` will concretize
the environment before installing the concretized specs.

.. note::

   Every ``spack install`` process builds one package at a time with multiple build
   jobs, controlled by the ``-j`` flag and the ``config:build_jobs`` option
   (see :ref:`build-jobs`). To speed up environment builds further, independent
   packages can be installed in parallel by launching more Spack instances. For
   example, the following will build at most four packages in parallel using
   three background jobs:

   .. code-block:: console

      [myenv]$ spack install & spack install & spack install & spack install

   Another option is to generate a ``Makefile`` and run ``make -j<N>`` to control
   the number of parallel install processes. See :ref:`env-generate-depfile`
   for details.


As it installs, ``spack install`` creates symbolic links in the
``logs/`` directory in the environment, allowing for easy inspection
of build logs related to that environment. The ``spack install``
command also stores a Spack repo containing the ``package.py`` file
used at install time for each package in the ``repos/`` directory in
the environment.

The ``--no-add`` option can be used in a concrete environment to tell
spack to install specs already present in the environment but not to
add any new root specs to the environment.  For root specs provided
to ``spack install`` on the command line, ``--no-add`` is the default,
while for dependency specs, it is optional.  In other
words, if there is an unambiguous match in the active concrete environment
for a root spec provided to ``spack install`` on the command line, spack
does not require you to specify the ``--no-add`` option to prevent the spec
from being added again.  At the same time, a spec that already exists in the
environment, but only as a dependency, will be added to the environment as a
root spec without the ``--no-add`` option.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Developing Packages in a Spack Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``spack develop`` command allows one to develop Spack packages in
an environment. It requires a spec containing a concrete version, and
will configure Spack to install the package from local source. 
If a version is not provided from the command line interface then spack 
will automatically pick the highest version the package has defined.
This means any infinity versions (``develop``, ``main``, ``stable``) will be
preferred in this selection process.
By default, ``spack develop`` will also clone the package to a subdirectory in the
environment for the local source. This package will have a special variant ``dev_path``
set, and Spack will ensure the package and its dependents are rebuilt
any time the environment is installed if the package's local source
code has been modified. Spack's native implementation to check for modifications
is to check if ``mtime`` is newer than the installation.
A custom check can be created by overriding the ``detect_dev_src_change`` method 
in your package class. This is particularly useful for projects using custom spack repo's 
to drive development and want to optimize performance. 

Spack ensures that all instances of a
developed package in the environment are concretized to match the
version (and other constraints) passed as the spec argument to the
``spack develop`` command.

For packages with ``git`` attributes, git branches, tags, and commits can
also be used as valid concrete versions (see :ref:`version-specifier`).
This means that for a package ``foo``, ``spack develop foo@git.main`` will clone
the ``main`` branch of the package, and ``spack install`` will install from
that git clone if ``foo`` is in the environment.
Further development on ``foo`` can be tested by re-installing the environment,
and eventually committed and pushed to the upstream git repo.

If the package being developed supports out-of-source builds then users can use the
``--build_directory`` flag to control the location and name of the build directory. 
This is a shortcut to set the ``package_attributes:build_directory`` in the
``packages`` configuration (see :ref:`assigning-package-attributes`).
The supplied location will become the build-directory for that package in all future builds.

.. warning::
   Potential pitfalls of setting the build directory
    Spack does not check for out-of-source build compatibility with the packages and
    so the onerous of making sure the package supports out-of-source builds is on
    the user.
    For example, most ``autotool`` and ``makefile`` packages do not support out-of-source builds
    while all ``CMake`` packages do.
    Understanding these nuances are on the software developers and we strongly encourage
    developers to only redirect the build directory if they understand their package's
    build-system.

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


.. _environment_include_concrete:

------------------------------
Included Concrete Environments
------------------------------

Spack environments can create an environment based off of information in already
established environments. You can think of it as a combination of existing
environments. It will gather information from the existing environment's
``spack.lock`` and use that during the creation of this included concrete
environment. When an included concrete environment is created it will generate
a ``spack.lock`` file for the newly created environment.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating included environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To create a combined concrete environment, you must have at least one existing
concrete environment. You will use the command ``spack env create`` with the
argument ``--include-concrete`` followed by the name or path of the environment
you'd like to include. Here is an example of how to create a combined environment
from the command line.

.. code-block:: console

   $ spack env create myenv
   $ spack -e myenv add python
   $ spack -e myenv concretize
   $ spack env create --include-concrete myenv included_env


You can also include an environment directly in the ``spack.yaml`` file. It
involves adding the ``include_concrete`` heading in the yaml followed by the
absolute path to the independent environments.

.. code-block:: yaml

   spack:
     specs: []
     concretizer:
         unify: true
     include_concrete:
     - /absolute/path/to/environment1
     - /absolute/path/to/environment2


Once the ``spack.yaml`` has been updated you must concretize the environment to
get the concrete specs from the included environments.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Updating an included environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If changes were made to the base environment and you want that reflected in the
included environment you will need to reconcretize both the base environment and the
included environment for the change to be implemented. For example:

.. code-block:: console

   $ spack env create myenv
   $ spack -e myenv add python
   $ spack -e myenv concretize
   $ spack env create --include-concrete myenv included_env


   $ spack -e myenv find
   ==> In environment myenv
   ==> Root specs
   python

   ==> 0 installed packages


   $ spack -e included_env find
   ==> In environment included_env
   ==> No root specs
   ==> Included specs
   python

   ==> 0 installed packages

Here we see that ``included_env`` has access to the python package through
the ``myenv`` environment. But if we were to add another spec to ``myenv``,
``included_env`` will not be able to access the new information.

.. code-block:: console

   $ spack -e myenv add perl
   $ spack -e myenv concretize
   $ spack -e myenv find
   ==> In environment myenv
   ==> Root specs
   perl  python

   ==> 0 installed packages


   $ spack -e included_env find
   ==> In environment included_env
   ==> No root specs
   ==> Included specs
   python

   ==> 0 installed packages

It isn't until you run the ``spack concretize`` command that the combined
environment will get the updated information from the reconcretized base environmennt.

.. code-block:: console

   $ spack -e included_env concretize
   $ spack -e included_env find
   ==> In environment included_env
   ==> No root specs
   ==> Included specs
   perl  python

   ==> 0 installed packages

.. _environment-configuration:

------------------------
Configuring Environments
------------------------

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

^^^^^^^^^^^^^^^^^^^^^
Inline configurations
^^^^^^^^^^^^^^^^^^^^^

Inline environment-scope configuration is done using the same yaml
format as standard Spack configuration scopes, covered in the
:ref:`configuration` section. Each section is contained under a
top-level yaml object with it's name. For example, a ``spack.yaml``
manifest file containing some package preference configuration (as in
a ``packages.yaml`` file) could contain:

.. code-block:: yaml

   spack:
     # ...
     packages:
       all:
         compiler: [intel]
     # ...

This configuration sets the default compiler for all packages to
``intel``.

^^^^^^^^^^^^^^^^^^^^^^^
Included configurations
^^^^^^^^^^^^^^^^^^^^^^^

Spack environments allow an ``include`` heading in their yaml
schema. This heading pulls in external configuration files and applies
them to the environment.

.. code-block:: yaml

   spack:
     include:
     - relative/path/to/config.yaml
     - https://github.com/path/to/raw/config/compilers.yaml
     - /absolute/path/to/packages.yaml

Environments can include files or URLs. File paths can be relative or
absolute. URLs include the path to the text for individual files or
can be the path to a directory containing configuration files.
Spack supports ``file``, ``http``, ``https`` and ``ftp`` protocols (or
schemes). Spack-specific, environment and user path variables may be
used in these paths. See :ref:`config-file-variables` for more information.

^^^^^^^^^^^^^^^^^^^^^^^^
Configuration precedence
^^^^^^^^^^^^^^^^^^^^^^^^

Inline configurations take precedence over included configurations, so
you don't have to change shared configuration files to make small changes
to an individual environment. Included configurations listed earlier will
have higher precedence, as the included configs are applied in reverse order.

-------------------------------
Manually Editing the Specs List
-------------------------------

The list of abstract/root specs in the environment is maintained in
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

.. _environments_concretization_config:

^^^^^^^^^^^^^^^^^^^
Spec concretization
^^^^^^^^^^^^^^^^^^^
An environment can be concretized in three different modes and the behavior active under
any environment is determined by the ``concretizer:unify`` configuration option.

The *default* mode is to unify all specs:

.. code-block:: yaml

   spack:
       specs:
         - hdf5+mpi
         - zlib@1.2.8
       concretizer:
         unify: true

This means that any package in the environment corresponds to a single concrete spec. In
the above example, when ``hdf5`` depends down the line of ``zlib``, it is required to
take ``zlib@1.2.8`` instead of a newer version. This mode of concretization is
particularly useful when environment views are used: if every package occurs in
only one flavor, it is usually possible to merge all install directories into a view.

A downside of unified concretization is that it can be overly strict. For example, a
concretization error would happen when both ``hdf5+mpi`` and ``hdf5~mpi`` are specified
in an environment.

The second mode is to *unify when possible*: this makes concretization of root specs
more independendent. Instead of requiring reuse of dependencies across different root
specs, it is only maximized:

.. code-block:: yaml

   spack:
       specs:
         - hdf5~mpi
         - hdf5+mpi
         - zlib@1.2.8
       concretizer:
         unify: when_possible

This means that both ``hdf5`` installations will use ``zlib@1.2.8`` as a dependency even
if newer versions of that library are available.

The third mode of operation is to concretize root specs entirely independently by
disabling unified concretization:

.. code-block:: yaml

   spack:
       specs:
         - hdf5~mpi
         - hdf5+mpi
         - zlib@1.2.8
       concretizer:
         unify: false

In this example ``hdf5`` is concretized separately, and does not consider ``zlib@1.2.8``
as a constraint or preference. Instead, it will take the latest possible version.

The last two concretization options are typically useful for system administrators and
user support groups providing a large software stack for their HPC center.

.. note::

   The ``concretizer:unify`` config option was introduced in Spack 0.18 to
   replace the ``concretization`` property. For reference,
   ``concretization: together`` is replaced by ``concretizer:unify:true``,
   and ``concretization: separately`` is replaced by ``concretizer:unify:false``.

.. admonition:: Re-concretization of user specs

   The ``spack concretize`` command without additional arguments will *not* change any
   previously concretized specs. This may prevent it from finding a solution when using
   ``unify: true``, and it may prevent it from finding a minimal solution when using
   ``unify: when_possible``. You can force Spack to ignore the existing concrete environment
   with ``spack concretize -f``.

^^^^^^^^^^^^^
Spec Matrices
^^^^^^^^^^^^^

Entries in the ``specs`` list can be individual abstract specs or a
spec matrix.

A spec matrix is a yaml object containing multiple lists of specs, and
evaluates to the cross-product of those specs. Spec matrices also
contain an ``excludes`` directive, which eliminates certain
combinations from the evaluated result.

The following two environment manifests are identical:

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

^^^^^^^^^^^^^^^^^^^^
Spec List References
^^^^^^^^^^^^^^^^^^^^

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
environments substantially more manageable.

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
       - when: arch.satisfies('target=x86_64:')
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

^^^^^^^^^^^^^^^^^^^^^^^^
SpecLists as Constraints
^^^^^^^^^^^^^^^^^^^^^^^^

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


-----------------
Environment Views
-----------------

Spack Environments can have an associated filesystem view, which is a directory
with a more traditional structure ``<view>/bin``, ``<view>/lib``, ``<view>/include``
in which all files of the installed packages are linked.

By default a view is created for each environment, thanks to the ``view: true``
option in the ``spack.yaml`` manifest file:

.. code-block:: yaml

   spack:
     specs: [perl, python]
     view: true

The view is created in a hidden directory ``.spack-env/view`` relative to the environment.
If you've used ``spack env activate``, you may have already interacted with this view. Spack
prepends its ``<view>/bin`` dir to ``PATH`` when the environment is activated, so that
you can directly run executables from all installed packages in the environment.

Views are highly customizable: you can control where they are put, modify their structure,
include and exclude specs, change how files are linked, and you can even generate multiple
views for a single environment.

.. _configuring_environment_views:

^^^^^^^^^^^^^^^^^^^^^^^^^^
Minimal view configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

The minimal configuration

.. code-block:: yaml

   spack:
     # ...
     view: true

lets Spack generate a single view with default settings under the
``.spack-env/view`` directory of the environment.

Another short way to configure a view is to specify just where to put it:

.. code-block:: yaml

   spack:
     # ...
     view: /path/to/view

Views can also be disabled by setting ``view: false``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Advanced view configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

One or more **view descriptors** can be defined under ``view``, keyed by a name.
The example from the previous section with ``view: /path/to/view`` is equivalent
to defining a view descriptor named ``default`` with a ``root`` attribute:

.. code-block:: yaml

   spack:
     # ...
     view:
       default:  # name of the view
         root: /path/to/view  # view descriptor attribute

The ``default`` view descriptor name is special: when you ``spack env activate`` your
environment, this view will be used to update (among other things) your ``PATH``
variable.

View descriptors must contain the root of the view, and optionally projections,
``select`` and ``exclude`` lists and link information via ``link`` and
``link_type``.

As a more advanced example, in the following manifest
file snippet we define a view named ``mpis``, rooted at
``/path/to/view`` in which all projections use the package name,
version, and compiler name to determine the path for a given
package. This view selects all packages that depend on MPI, and
excludes those built with the GCC compiler at version 18.5.
The root specs with their (transitive) link and run type dependencies
will be put in the view due to the  ``link: all`` option,
and the files in the view will be symlinks to the spack install
directories.

.. code-block:: yaml

   spack:
     # ...
     view:
       mpis:
         root: /path/to/view
         select: [^mpi]
         exclude: ['%gcc@18.5']
         projections:
           all: '{name}/{version}-{compiler.name}'
         link: all
         link_type: symlink

The default for the ``select`` and
``exclude`` values is to select everything and exclude nothing. The
default projection is the default view projection (``{}``). The ``link``
attribute allows the following values:

#. ``link: all`` include root specs with their transitive run and link type
   dependencies (default);
#. ``link: run`` include root specs with their transitive run type dependencies;
#. ``link: roots`` include root specs without their dependencies.

The ``link_type`` defaults to ``symlink`` but can also take the value
of ``hardlink`` or ``copy``.

.. tip::

   The option ``link: run`` can be used to create small environment views for
   Python packages. Python will be able to import packages *inside* of the view even
   when the environment is not activated, and linked libraries will be located
   *outside* of the view thanks to rpaths.

From the command line, the ``spack env create`` command takes an
argument ``--with-view [PATH]`` that sets the path for a single, default
view. If no path is specified, the default path is used (``view:
true``). The argument ``--without-view`` can be used to create an
environment without any view configured.

The ``spack env view`` command can be used to change the manage views
of an environment. The subcommand ``spack env view enable`` will add a
view named ``default`` to an environment. It takes an optional
argument to specify the path for the new default view. The subcommand
``spack env view disable`` will remove the view named ``default`` from
an environment if one exists. The subcommand ``spack env view
regenerate`` will regenerate the views for the environment. This will
apply any updates in the environment configuration that have not yet
been applied.

.. _view_projections:

""""""""""""""""
View Projections
""""""""""""""""
The default projection into a view is to link every package into the
root of the view. The projections attribute is a mapping of partial specs to
spec format strings, defined by the :meth:`~spack.spec.Spec.format`
function, as shown in the example below:

.. code-block:: yaml

   projections:
     zlib: "{name}-{version}"
     ^mpi: "{name}-{version}/{^mpi.name}-{^mpi.version}-{compiler.name}-{compiler.version}"
     all: "{name}-{version}/{compiler.name}-{compiler.version}"

Projections also permit environment and spack configuration variable
expansions as shown below:

.. code-block:: yaml

   projections:
     all: "{name}-{version}/{compiler.name}-{compiler.version}/$date/$SYSTEM_ENV_VARIBLE"

where ``$date`` is the spack configuration variable that will expand with the ``YYYY-MM-DD``
format and ``$SYSTEM_ENV_VARIABLE`` is an environment variable defined in the shell.

The entries in the projections configuration file must all be either
specs or the keyword ``all``. For each spec, the projection used will
be the first non-``all`` entry that the spec satisfies, or ``all`` if
there is an entry for ``all`` and no other entry is satisfied by the
spec. Where the keyword ``all`` appears in the file does not
matter.

Given the example above, the spec ``zlib@1.2.8``
will be linked into ``/my/view/zlib-1.2.8/``, the spec
``hdf5@1.8.10+mpi %gcc@4.9.3 ^mvapich2@2.2`` will be linked into
``/my/view/hdf5-1.8.10/mvapich2-2.2-gcc-4.9.3``, and the spec
``hdf5@1.8.10~mpi %gcc@4.9.3`` will be linked into
``/my/view/hdf5-1.8.10/gcc-4.9.3``.

If the keyword ``all`` does not appear in the projections
configuration file, any spec that does not satisfy any entry in the
file will be linked into the root of the view as in a single-prefix
view. Any entries that appear below the keyword ``all`` in the
projections configuration file will not be used, as all specs will use
the projection under ``all`` before reaching those entries.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Activating environment views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``spack env activate <env>`` has two effects:

1. It activates the environment so that further Spack commands such
   as ``spack install`` will run in the context of the environment.
2. It activates the view so that environment variables such as
   ``PATH`` are updated to include the view.

Without further arguments, the ``default`` view of the environment is
activated. If a view with a different name has to be activated,
``spack env activate --with-view <name> <env>`` can be
used instead. You can also activate the environment without modifying
further environment variables using ``--without-view``.

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
PKG_CONFIG_PATH     lib/pkgconfig, lib64/pkgconfig, share/pkgconfig
CMAKE_PREFIX_PATH   .
=================== =========

Each of these paths are appended to the view root, and added to the
relevant variable if the path exists. For this reason, it is not
recommended to use non-default projections with the default view of an
environment.

The ``spack env deactivate`` command will remove the active view of
the Spack environment from the user's environment variables.


.. _env-generate-depfile:


------------------------------------------
Generating Depfiles from Environments
------------------------------------------

Spack can generate ``Makefile``\s to make it easier to build multiple
packages in an environment in parallel. Generated ``Makefile``\s expose
targets that can be included in existing ``Makefile``\s, to allow
other targets to depend on the environment installation.

A typical workflow is as follows:

.. code-block:: console

   spack env create -d .
   spack -e . add perl
   spack -e . concretize
   spack -e . env depfile -o Makefile
   make -j64

This generates a ``Makefile`` from a concretized environment in the
current working directory, and ``make -j64`` installs the environment,
exploiting parallelism across packages as much as possible. Spack
respects the Make jobserver and forwards it to the build environment
of packages, meaning that a single ``-j`` flag is enough to control the
load, even when packages are built in parallel.

By default the following phony convenience targets are available:

- ``make all``: installs the environment (default target);
- ``make clean``: cleans files used by make, but does not uninstall packages.

.. tip::

   GNU Make version 4.3 and above have great support for output synchronization
   through the ``-O`` and ``--output-sync`` flags, which ensure that output is
   printed orderly per package install. To get synchronized output with colors,
   use ``make -j<N> SPACK_COLOR=always --output-sync=recurse``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specifying dependencies on generated ``make`` targets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An interesting question is how to include generated ``Makefile``\s in your own
``Makefile``\s. This comes up when you want to install an environment that provides
executables required in a command for a make target of your own.

The example below shows how to accomplish this: the ``env`` target specifies
the generated ``spack/env`` target as a prerequisite, meaning that the environment
gets installed and is available for use in the ``env`` target.

.. code:: Makefile

   SPACK ?= spack

   .PHONY: all clean env

   all: env

   spack.lock: spack.yaml
   	$(SPACK) -e . concretize -f

   env.mk: spack.lock
   	$(SPACK) -e . env depfile -o $@ --make-prefix spack

   env: spack/env
   	$(info environment installed!)

   clean:
   	rm -rf spack.lock env.mk spack/

   ifeq (,$(filter clean,$(MAKECMDGOALS)))
   include env.mk
   endif

This works as follows: when ``make`` is invoked, it first "remakes" the missing
include ``env.mk`` as there is a target for it. This triggers concretization of
the environment and makes spack output ``env.mk``. At that point the
generated target ``spack/env`` becomes available through ``include env.mk``.

As it is typically undesirable to remake ``env.mk`` as part of ``make clean``,
the include is conditional.

.. note::

   When including generated ``Makefile``\s, it is important to use
   the ``--make-prefix`` flag and use the non-phony target
   ``<prefix>/env`` as prerequisite, instead of the phony target
   ``<prefix>/all``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Building a subset of the environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated ``Makefile``\s contain install targets for each spec, identified
by ``<name>-<version>-<hash>``. This allows you to install only a subset of the
packages in the environment. When packages are unique in the environment, it's
enough to know the name and let tab-completion fill out the version and hash.

The following phony targets are available: ``install/<spec>`` to install the
spec with its dependencies, and ``install-deps/<spec>`` to *only* install
its dependencies. This can be useful when certain flags should only apply to
dependencies. Below we show a use case where a spec is installed with verbose
output (``spack install --verbose``) while its dependencies are installed silently:

.. code-block:: console

   $ spack env depfile -o Makefile

   # Install dependencies in parallel, only show a log on error.
   $ make -j16 install-deps/python-3.11.0-<hash> SPACK_INSTALL_FLAGS=--show-log-on-error

   # Install the root spec with verbose output.
   $ make -j16 install/python-3.11.0-<hash> SPACK_INSTALL_FLAGS=--verbose

^^^^^^^^^^^^^^^^^^^^^^^^^
Adding post-install hooks
^^^^^^^^^^^^^^^^^^^^^^^^^

Another advanced use-case of generated ``Makefile``\s is running a post-install
command for each package. These "hooks" could be anything from printing a
post-install message, running tests, or pushing just-built binaries to a buildcache.

This can be accomplished through the generated ``[<prefix>/]SPACK_PACKAGE_IDS``
variable. Assuming we have an active and concrete environment, we generate the
associated ``Makefile`` with a prefix ``example``:

.. code-block:: console

   $ spack env depfile -o env.mk --make-prefix example

And we now include it in a different ``Makefile``, in which we create a target
``example/push/%`` with ``%`` referring to a package identifier. This target
depends on the particular package installation. In this target we automatically
have the target-specific ``HASH`` and ``SPEC`` variables at our disposal. They
are respectively the spec hash (excluding leading ``/``), and a human-readable spec.
Finally, we have an entrypoint target ``push`` that will update the buildcache
index once every package is pushed. Note how this target uses the generated
``example/SPACK_PACKAGE_IDS`` variable to define its prerequisites.

.. code:: Makefile

   SPACK ?= spack
   BUILDCACHE_DIR = $(CURDIR)/tarballs

   .PHONY: all

   all: push

   include env.mk

   example/push/%: example/install/%
   	@mkdir -p $(dir $@)
   	$(info About to push $(SPEC) to a buildcache)
   	$(SPACK) -e . buildcache push --only=package $(BUILDCACHE_DIR) /$(HASH)
   	@touch $@

   push: $(addprefix example/push/,$(example/SPACK_PACKAGE_IDS))
   	$(info Updating the buildcache index)
   	$(SPACK) -e . buildcache update-index $(BUILDCACHE_DIR)
   	$(info Done!)
   	@touch $@
