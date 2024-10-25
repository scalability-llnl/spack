.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _sconspackage:

-----
SCons
-----

SCons is a general-purpose build system that does not rely on
Makefiles to build software. SCons is written in Python, and handles
all building and linking itself.

As far as build systems go, SCons is very non-uniform. It provides a
common framework for developers to write build scripts, but the build
scripts themselves can vary drastically. Some developers add subcommands
like:

.. code-block:: console

   $ scons clean
   $ scons build
   $ scons test
   $ scons install


Others don't add any subcommands. Some have configuration options that
can be specified through variables on the command line. Others don't.

^^^^^^
Phases
^^^^^^

As previously mentioned, SCons allows developers to add subcommands like
``build`` and ``install``, but by default, installation usually looks like:

.. code-block:: console

   $ scons
   $ scons install


To facilitate this, the ``SConsBuilder`` and ``SconsPackage`` base classes provide the
following phases:

#. ``build`` - build the package
#. ``install`` - install the package

Package developers often add unit tests that can be invoked with
``scons test`` or ``scons check``. Spack provides a ``build_test`` method
to handle this. Since we don't know which one the package developer
chose, the ``build_test`` method does nothing by default, but can be easily
overridden like so:

.. code-block:: python

   def build_test(self):
       scons("check")


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

SCons packages can be identified by their ``SConstruct`` files. These
files handle everything from setting up subcommands and command-line
options to linking and compiling.

One thing to look for is the ``EnsureSConsVersion`` function:

.. code-block:: none

   EnsureSConsVersion(2, 3, 0)


This means that SCons 2.3.0 is the earliest release that will work.
You should specify this in a ``depends_on`` statement.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

At the bare minimum, packages that use the SCons build system need a
``scons`` dependency. Since this is always the case, the ``SConsPackage``
base class already contains:

.. code-block:: python

   depends_on("scons", type="build")


If you want to specify a particular version requirement, you can override
this in your package:

.. code-block:: python

   depends_on("scons@2.3.0:", type="build")


^^^^^^^^^^^^^^^^^^^^^^^^^
Finding available options
^^^^^^^^^^^^^^^^^^^^^^^^^

The first place to start when looking for a list of valid options to
build a package is ``scons --help``. Some packages like
`kahip <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/kahip/package.py>`_
don't bother overwriting the default SCons help message, so this isn't
very useful, but other packages like
`serf <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/serf/package.py>`_
print a list of valid command-line variables:

.. code-block:: console

   $ scons --help
   scons: Reading SConscript files ...
   Checking for GNU-compatible C compiler...yes
   scons: done reading SConscript files.

   PREFIX: Directory to install under ( /path/to/PREFIX )
       default: /usr/local
       actual: /usr/local

   LIBDIR: Directory to install architecture dependent libraries under ( /path/to/LIBDIR )
       default: $PREFIX/lib
       actual: /usr/local/lib

   APR: Path to apr-1-config, or to APR's install area ( /path/to/APR )
       default: /usr
       actual: /usr

   APU: Path to apu-1-config, or to APR's install area ( /path/to/APU )
       default: /usr
       actual: /usr

   OPENSSL: Path to OpenSSL's install area ( /path/to/OPENSSL )
       default: /usr
       actual: /usr

   ZLIB: Path to zlib's install area ( /path/to/ZLIB )
       default: /usr
       actual: /usr

   GSSAPI: Path to GSSAPI's install area ( /path/to/GSSAPI )
       default: None
       actual: None

   DEBUG: Enable debugging info and strict compile warnings (yes|no)
       default: False
       actual: False

   APR_STATIC: Enable using a static compiled APR (yes|no)
       default: False
       actual: False

   CC: Command name or path of the C compiler
       default: None
       actual: gcc

   CFLAGS: Extra flags for the C compiler (space-separated)
       default: None
       actual:

   LIBS: Extra libraries passed to the linker, e.g. "-l<library1> -l<library2>" (space separated)
       default: None
       actual: None

   LINKFLAGS: Extra flags for the linker (space-separated)
       default: None
       actual:

   CPPFLAGS: Extra flags for the C preprocessor (space separated)
       default: None
       actual: None

   Use scons -H for help about command-line options.


More advanced packages like
`cantera <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/cantera/package.py>`_
use ``scons --help`` to print a list of subcommands:

.. code-block:: console

   $ scons --help
   scons: Reading SConscript files ...

   SCons build script for Cantera

   Basic usage:
       'scons help' - print a description of user-specifiable options.

       'scons build' - Compile Cantera and the language interfaces using
                       default options.

       'scons clean' - Delete files created while building Cantera.

       '[sudo] scons install' - Install Cantera.

       '[sudo] scons uninstall' - Uninstall Cantera.

       'scons test' - Run all tests which did not previously pass or for which the
                      results may have changed.

       'scons test-reset' - Reset the passing status of all tests.

       'scons test-clean' - Delete files created while running the tests.

       'scons test-help' - List available tests.

       'scons test-NAME' - Run the test named "NAME".

       'scons <command> dump' - Dump the state of the SCons environment to the
                                screen instead of doing <command>, e.g.
                                'scons build dump'. For debugging purposes.

       'scons samples' - Compile the C++ and Fortran samples.

       'scons msi' - Build a Windows installer (.msi) for Cantera.

       'scons sphinx' - Build the Sphinx documentation

       'scons doxygen' - Build the Doxygen documentation


You'll notice that cantera provides a ``scons help`` subcommand. Running
``scons help`` prints a list of valid command-line variables.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to scons
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you know what arguments the project accepts, you can add them to
the package build phase. This is done by overriding ``build_args`` like so:

.. code-block:: python

   def build_args(self, spec, prefix):
       args = [
         f"PREFIX={prefix}",
         f"ZLIB={spec['zlib'].prefix}",
       ]

       if spec.satisfies("+debug"):
           args.append("DEBUG=yes")
       else:
           args.append("DEBUG=no")

       return args


``SConsPackage`` also provides an ``install_args`` function that you can
override to pass additional arguments to ``scons install``.

^^^^^^^^^^^^^^^^^
Compiler wrappers
^^^^^^^^^^^^^^^^^

By default, SCons builds all packages in a separate execution environment,
and doesn't pass any environment variables from the user environment.
Even changes to ``PATH`` are not propagated unless the package developer
does so.

This is particularly troublesome for Spack's compiler wrappers, which depend
on environment variables to manage dependencies and linking flags. In many
cases, SCons packages are not compatible with Spack's compiler wrappers,
and linking must be done manually.

First of all, check the list of valid options for anything relating to
environment variables. For example, cantera has the following option:

.. code-block:: none

   * env_vars: [ string ]
       Environment variables to propagate through to SCons. Either the
       string "all" or a comma separated list of variable names, e.g.
       "LD_LIBRARY_PATH,HOME".
       - default: "LD_LIBRARY_PATH,PYTHONPATH"


In the case of cantera, using ``env_vars=all`` allows us to use
Spack's compiler wrappers. If you don't see an option related to
environment variables, try using Spack's compiler wrappers by passing
``spack_cc``, ``spack_cxx``, and ``spack_fc`` via the ``CC``, ``CXX``,
and ``FC`` arguments, respectively. If you pass them to the build and
you see an error message like:

.. code-block:: none

   Spack compiler must be run from Spack! Input 'SPACK_PREFIX' is missing.


you'll know that the package isn't compatible with Spack's compiler
wrappers. In this case, you'll have to use the path to the actual
compilers, which are stored in ``self.compiler.cc`` and friends.
Note that this may involve passing additional flags to the build to
locate dependencies, a task normally done by the compiler wrappers.
serf is an example of a package with this limitation.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the SCons build system, see:
http://scons.org/documentation.html
