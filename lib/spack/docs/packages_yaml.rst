.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)


.. _packages-config:

================================
Package Settings (packages.yaml)
================================

Spack allows you to customize how your software is built through the
``packages.yaml`` file.  Using it, you can make Spack prefer particular
implementations of virtual dependencies (e.g., MPI or BLAS/LAPACK),
or you can make it prefer to build with particular compilers.  You can
also tell Spack to use *external* software installations already
present on your system.

At a high level, the ``packages.yaml`` file is structured like this:

.. code-block:: yaml

   packages:
     package1:
       # settings for package1
     package2:
       # settings for package2
     # ...
     all:
       # settings that apply to all packages.

So you can either set build preferences specifically for *one* package,
or you can specify that certain settings should apply to *all* packages.
The types of settings you can customize are described in detail below.

Spack's build defaults are in the default
``etc/spack/defaults/packages.yaml`` file.  You can override them in
``~/.spack/packages.yaml`` or ``etc/spack/packages.yaml``. For more
details on how this works, see :ref:`configuration-scopes`.

.. _sec-external-packages:

-----------------
External Packages
-----------------

Spack can be configured to use externally-installed
packages rather than building its own packages. This may be desirable
if machines ship with system packages, such as a customized MPI
that should be used instead of Spack building its own MPI.

External packages are configured through the ``packages.yaml`` file.
Here's an example of an external configuration:

.. code-block:: yaml

   packages:
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel

This example lists three installations of OpenMPI, one built with GCC,
one built with GCC and debug information, and another built with Intel.
If Spack is asked to build a package that uses one of these MPIs as a
dependency, it will use the pre-installed OpenMPI in
the given directory. Note that the specified path is the top-level
install prefix, not the ``bin`` subdirectory.

``packages.yaml`` can also be used to specify modules to load instead
of the installation prefixes.  The following example says that module
``CMake/3.7.2`` provides cmake version 3.7.2.

.. code-block:: yaml

   cmake:
     externals:
     - spec: cmake@3.7.2
       modules:
       - CMake/3.7.2

Each ``packages.yaml`` begins with a ``packages:`` attribute, followed
by a list of package names.  To specify externals, add an ``externals:``
attribute under the package name, which lists externals.
Each external should specify a ``spec:`` string that should be as
well-defined as reasonably possible.  If a
package lacks a spec component, such as missing a compiler or
package version, then Spack will guess the missing component based
on its most-favored packages, and it may guess incorrectly.

Each package version and compiler listed in an external should
have entries in Spack's packages and compiler configuration, even
though the package and compiler may not ever be built.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Extra attributes for external packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes external packages require additional attributes to be used
effectively. This information can be defined on a per-package basis
and stored in the ``extra_attributes`` section of the external package
configuration. In addition to per-package information, this section
can be used to define environment modifications to be performed
whenever the package is used. For example, if an external package is
built without ``rpath`` support, it may require ``LD_LIBRARY_PATH``
settings to find its dependencies. This could be configured as
follows:

.. code-block:: yaml

   packages:
     mpich:
       externals:
       - spec: mpich@3.3 %clang@12.0.0 +hwloc
         prefix: /path/to/mpich
         extra_attributes:
           environment:
             prepend_path:
               LD_LIBRARY_PATH: /path/to/hwloc/lib64

See :ref:`configuration_environment_variables` for more information on
how to configure environment modifications in Spack config files.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Prevent packages from being built from sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adding an external spec in ``packages.yaml`` allows Spack to use an external location,
but it does not prevent Spack from building packages from sources. In the above example,
Spack might choose for many valid reasons to start building and linking with the
latest version of OpenMPI rather than continue using the pre-installed OpenMPI versions.

To prevent this, the ``packages.yaml`` configuration also allows packages
to be flagged as non-buildable.  The previous example could be modified to
be:

.. code-block:: yaml

   packages:
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel
       buildable: False

The addition of the ``buildable`` flag tells Spack that it should never build
its own version of OpenMPI from sources, and it will instead always rely on a pre-built
OpenMPI.

.. note::

   If ``concretizer:reuse`` is on (see :ref:`concretizer-options` for more information on that flag)
   pre-built specs include specs already available from a local store, an upstream store, a registered
   buildcache or specs marked as externals in ``packages.yaml``. If ``concretizer:reuse`` is off, only
   external specs in ``packages.yaml`` are included in the list of pre-built specs.

If an external module is specified as not buildable, then Spack will load the
external module into the build environment which can be used for linking.

The ``buildable`` does not need to be paired with external packages.
It could also be used alone to forbid packages that may be
buggy or otherwise undesirable.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Non-buildable virtual packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Virtual packages in Spack can also be specified as not buildable, and
external implementations can be provided. In the example above,
OpenMPI is configured as not buildable, but Spack will often prefer
other MPI implementations over the externally available OpenMPI. Spack
can be configured with every MPI provider not buildable individually,
but more conveniently:

.. code-block:: yaml

   packages:
     mpi:
       buildable: False
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel

Spack can then use any of the listed external implementations of MPI
to satisfy a dependency, and will choose depending on the compiler and
architecture.

In cases where the concretizer is configured to reuse specs, and other ``mpi`` providers
(available via stores or buildcaches) are not wanted, Spack can be configured to require
specs matching only the available externals:

.. code-block:: yaml

   packages:
     mpi:
       buildable: False
       require:
       - one_of: [
           "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64",
           "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug",
           "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         ]
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel

This configuration prevents any spec using MPI and originating from stores or buildcaches to be reused,
unless it matches the requirements under ``packages:mpi:require``. For more information on requirements see
:ref:`package-requirements`.

.. _cmd-spack-external-find:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Automatically Find External Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can run the :ref:`spack external find <spack-external-find>` command
to search for system-provided packages and add them to ``packages.yaml``.
After running this command your ``packages.yaml`` may include new entries:

.. code-block:: yaml

   packages:
     cmake:
       externals:
       - spec: cmake@3.17.2
         prefix: /usr

Generally this is useful for detecting a small set of commonly-used packages;
for now this is generally limited to finding build-only dependencies.
Specific limitations include:

* Packages are not discoverable by default: For a package to be
  discoverable with ``spack external find``, it needs to add special
  logic. See :ref:`here <make-package-findable>` for more details.
* The logic does not search through module files, it can only detect
  packages with executables defined in ``PATH``; you can help Spack locate
  externals which use module files by loading any associated modules for
  packages that you want Spack to know about before running
  ``spack external find``.
* Spack does not overwrite existing entries in the package configuration:
  If there is an external defined for a spec at any configuration scope,
  then Spack will not add a new external entry (``spack config blame packages``
  can help locate all external entries).

.. _package-requirements:

--------------------
Package Requirements
--------------------

Spack can be configured to always use certain compilers, package
versions, and variants during concretization through package
requirements.

Package requirements are useful when you find yourself repeatedly
specifying the same constraints on the command line, and wish that
Spack respects these constraints whether you mention them explicitly
or not. Another use case is specifying constraints that should apply
to all root specs in an environment, without having to repeat the
constraint everywhere.

Apart from that, requirements config is more flexible than constraints
on the command line, because it can specify constraints on packages
*when they occur* as a dependency. In contrast, on the command line it
is not possible to specify constraints on dependencies while also keeping
those dependencies optional.

.. seealso::

   FAQ: :ref:`Why does Spack pick particular versions and variants? <faq-concretizer-precedence>`


^^^^^^^^^^^^^^^^^^^
Requirements syntax
^^^^^^^^^^^^^^^^^^^

The package requirements configuration is specified in ``packages.yaml``,
keyed by package name and expressed using the Spec syntax. In the simplest
case you can specify attributes that you always want the package to have
by providing a single spec string to ``require``:

.. code-block:: yaml

   packages:
     libfabric:
       require: "@1.13.2"

In the above example, ``libfabric`` will always build with version 1.13.2. If you
need to compose multiple configuration scopes ``require`` accepts a list of
strings:

.. code-block:: yaml

   packages:
     libfabric:
       require:
       - "@1.13.2"
       - "%gcc"

In this case ``libfabric`` will always build with version 1.13.2 **and** using GCC
as a compiler.

For more complex use cases, require accepts also a list of objects. These objects
must have either a ``any_of`` or a ``one_of`` field, containing a list of spec strings,
and they can optionally have a ``when`` and a ``message`` attribute:

.. code-block:: yaml

   packages:
     openmpi:
       require:
       - any_of: ["@4.1.5", "%gcc"]
         message: "in this example only 4.1.5 can build with other compilers"

``any_of`` is a list of specs. One of those specs must be satisfied
and it is also allowed for the concretized spec to match more than one.
In the above example, that means you could build ``openmpi@4.1.5%gcc``,
``openmpi@4.1.5%clang`` or ``openmpi@3.9%gcc``, but
not ``openmpi@3.9%clang``.

If a custom message is provided, and the requirement is not satisfiable,
Spack will print the custom error message:

.. code-block:: console

   $ spack spec openmpi@3.9%clang
   ==> Error: in this example only 4.1.5 can build with other compilers

We could express a similar requirement using the ``when`` attribute:

.. code-block:: yaml

   packages:
     openmpi:
       require:
       - any_of: ["%gcc"]
         when: "@:4.1.4"
         message: "in this example only 4.1.5 can build with other compilers"

In the example above, if the version turns out to be 4.1.4 or less, we require the compiler to be GCC.
For readability, Spack also allows a ``spec`` key accepting a string when there is only a single
constraint:

.. code-block:: yaml

   packages:
     openmpi:
       require:
       - spec: "%gcc"
         when: "@:4.1.4"
         message: "in this example only 4.1.5 can build with other compilers"

This code snippet and the one before it are semantically equivalent.

Finally, instead of ``any_of`` you can use ``one_of`` which also takes a list of specs. The final
concretized spec must match one and only one of them:

.. code-block:: yaml

   packages:
     mpich:
       require:
       - one_of: ["+cuda", "+rocm"]

In the example above, that means you could build ``mpich+cuda`` or ``mpich+rocm`` but not ``mpich+cuda+rocm``.

.. note::

   For ``any_of`` and ``one_of``, the order of specs indicates a
   preference: items that appear earlier in the list are preferred
   (note that these preferences can be ignored in favor of others).

.. note::

   When using a conditional requirement, Spack is allowed to actively avoid the triggering
   condition (the ``when=...`` spec) if that leads to a concrete spec with better scores in
   the optimization criteria. To check the current optimization criteria and their
   priorities you can run ``spack solve zlib``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setting default requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also set default requirements for all packages under ``all``
like this:

.. code-block:: yaml

   packages:
     all:
       require: '%clang'

which means every spec will be required to use ``clang`` as a compiler.

Requirements on variants for all packages are possible too, but note that they
are only enforced for those packages that define these variants, otherwise they
are disregarded. For example:

.. code-block:: yaml

   packages:
     all:
       require:
       - "+shared"
       - "+cuda"

will just enforce ``+shared`` on ``zlib``, which has a boolean ``shared`` variant but
no ``cuda`` variant.

Constraints in a single spec literal are always considered as a whole, so in a case like:

.. code-block:: yaml

   packages:
     all:
       require: "+shared +cuda"

the default requirement will be enforced only if a package has both a ``cuda`` and
a ``shared`` variant, and will never be partially enforced.

Finally, ``all`` represents a *default set of requirements* -
if there are specific package requirements, then the default requirements
under ``all`` are disregarded. For example, with a configuration like this:

.. code-block:: yaml

   packages:
     all:
       require:
       - 'build_type=Debug'
       - '%clang'
     cmake:
       require:
       - 'build_type=Debug'
       - '%gcc'

Spack requires ``cmake`` to use ``gcc`` and all other nodes (including ``cmake``
dependencies) to use ``clang``. If enforcing ``build_type=Debug`` is needed also
on ``cmake``, it must be repeated in the specific ``cmake`` requirements.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setting requirements on virtual specs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A requirement on a virtual spec applies whenever that virtual is present in the DAG.
This can be useful for fixing which virtual provider you want to use:

.. code-block:: yaml

   packages:
     mpi:
       require: 'mvapich2 %gcc'

With the configuration above the only allowed ``mpi`` provider is ``mvapich2 %gcc``.

Requirements on the virtual spec and on the specific provider are both applied, if
present. For instance with a configuration like:

.. code-block:: yaml

   packages:
     mpi:
       require: 'mvapich2 %gcc'
     mvapich2:
       require: '~cuda'

you will use ``mvapich2~cuda %gcc`` as an ``mpi`` provider.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Conflicts and strong preferences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the semantic of requirements is too strong, you can also express "strong preferences" and "conflicts"
from configuration files:

.. code-block:: yaml

   packages:
     all:
       prefer:
       - '%clang'
       conflict:
       - '+shared'

The ``prefer`` and ``conflict`` sections can be used whenever a ``require`` section is allowed.
The argument is always a list of constraints, and each constraint can be either a simple string,
or a more complex object:

.. code-block:: yaml

   packages:
     all:
       conflict:
       - spec: '%clang'
         when: 'target=x86_64_v3'
         message: 'reason why clang cannot be used'

The ``spec`` attribute is mandatory, while both ``when`` and ``message`` are optional.

.. note::

   Requirements allow for expressing both "strong preferences" and "conflicts".
   The syntax for doing so, though, may not be immediately clear. For
   instance, if we want to prevent any package from using ``%clang``, we can set:

   .. code-block:: yaml

      packages:
        all:
          require:
          - one_of: ['%clang', '@:']

   Since only one of the requirements must hold, and ``@:`` is always true, the rule above is
   equivalent to a conflict. For "strong preferences" we need to substitute the ``one_of`` policy
   with ``any_of``.



.. _package-preferences:

-------------------
Package Preferences
-------------------

In some cases package requirements can be too strong, and package
preferences are the better option. Package preferences do not impose
constraints on packages for particular versions or variants values,
they rather only set defaults. The concretizer is free to change
them if it must, due to other constraints, and also prefers reusing
installed packages over building new ones that are a better match for
preferences.

.. seealso::

   FAQ: :ref:`Why does Spack pick particular versions and variants? <faq-concretizer-precedence>`


Most package preferences (``compilers``, ``target`` and ``providers``)
can only be set globally under the ``all`` section of ``packages.yaml``:

.. code-block:: yaml

   packages:
     all:
       compiler: [gcc@12.2.0, clang@12:, oneapi@2023:]
       target: [x86_64_v3]
       providers:
         mpi: [mvapich2, mpich, openmpi]

These preferences override Spack's default and effectively reorder priorities
when looking for the best compiler, target or virtual package provider. Each
preference takes an ordered list of spec constraints, with earlier entries in
the list being preferred over later entries.

In the example above all packages prefer to be compiled with ``gcc@12.2.0``,
to target the ``x86_64_v3`` microarchitecture and to use ``mvapich2`` if they
depend on ``mpi``.

The ``variants`` and ``version`` preferences can be set under
package specific sections of the ``packages.yaml`` file:

.. code-block:: yaml

   packages:
     opencv:
       variants: +debug
     gperftools:
       version: [2.2, 2.4, 2.3]

In this case, the preference for ``opencv`` is to build with debug options, while
``gperftools`` prefers version 2.2 over 2.4.

Any preference can be overwritten on the command line if explicitly requested.

Preferences cannot overcome explicit constraints, as they only set a preferred
ordering among homogeneous attribute values. Going back to the example, if
``gperftools@2.3:`` was requested, then Spack will install version 2.4
since the most preferred version 2.2 is prohibited by the version constraint.

.. _package_permissions:

-------------------
Package Permissions
-------------------

Spack can be configured to assign permissions to the files installed
by a package.

In the ``packages.yaml`` file under ``permissions``, the attributes
``read``, ``write``, and ``group`` control the package
permissions. These attributes can be set per-package, or for all
packages under ``all``. If permissions are set under ``all`` and for a
specific package, the package-specific settings take precedence.

The ``read`` and ``write`` attributes take one of ``user``, ``group``,
and ``world``.

.. code-block:: yaml

  packages:
    all:
      permissions:
        write: group
        group: spack
    my_app:
      permissions:
        read: group
        group: my_team

The permissions settings describe the broadest level of access to
installations of the specified packages. The execute permissions of
the file are set to the same level as read permissions for those files
that are executable. The default setting for ``read`` is ``world``,
and for ``write`` is ``user``. In the example above, installations of
``my_app`` will be installed with user and group permissions but no
world permissions, and owned by the group ``my_team``. All other
packages will be installed with user and group write privileges, and
world read privileges. Those packages will be owned by the group
``spack``.

The ``group`` attribute assigns a Unix-style group to a package. All
files installed by the package will be owned by the assigned group,
and the sticky group bit will be set on the install prefix and all
directories inside the install prefix. This will ensure that even
manually placed files within the install prefix are owned by the
assigned group. If no group is assigned, Spack will allow the OS
default behavior to go as expected.

.. _assigning-package-attributes:

----------------------------
Assigning Package Attributes
----------------------------

You can assign class-level attributes in the configuration:

.. code-block:: yaml

  packages:
    mpileaks:
      package_attributes:
        # Override existing attributes
        url: http://www.somewhereelse.com/mpileaks-1.0.tar.gz
        # ... or add new ones
        x: 1

Attributes set this way will be accessible to any method executed
in the package.py file (e.g. the ``install()`` method). Values for these
attributes may be any value parseable by yaml.

These can only be applied to specific packages, not "all" or
virtual packages.
