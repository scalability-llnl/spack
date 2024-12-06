.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _makefilepackage:

--------
Makefile
--------

The most primitive build system a package can use is a plain Makefile.
Makefiles are simple to write for small projects, but they usually
require you to edit the Makefile to set platform and compiler-specific
variables.

^^^^^^
Phases
^^^^^^

The ``MakefileBuilder`` and ``MakefilePackage`` base classes come with 3 phases:

#. ``edit`` - edit the Makefile
#. ``build`` - build the project
#. ``install`` - install the project

By default, ``edit`` does nothing, but you can override it to replace
hard-coded Makefile variables. The ``build`` and ``install`` phases
run:

.. code-block:: console

   $ make
   $ make install


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

The main file that matters for a ``MakefilePackage`` is the Makefile.
This file will be named one of the following ways:

* GNUmakefile (only works with GNU Make)
* Makefile (most common)
* makefile

Some Makefiles also *include* other configuration files. Check for an
``include`` directive in the Makefile.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

Spack assumes that the operating system will have a valid ``make`` utility
installed already, so you don't need to add a dependency on ``make``.
However, if the package uses a ``GNUmakefile`` or the developers recommend
using GNU Make, you should add a dependency on ``gmake``:

.. code-block:: python

   depends_on("gmake", type="build")


^^^^^^^^^^^^^^^^^^^^^^^^^^
Types of Makefile packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

Most of the work involved in packaging software that uses Makefiles
involves overriding or replacing hard-coded variables. Many packages
make the mistake of hard-coding compilers, usually for GCC or Intel.
This is fine if you happen to be using that particular compiler, but
Spack is designed to work with *any* compiler, and you need to ensure
that this is the case.

Depending on how the Makefile is designed, there are 4 common strategies
that can be used to set or override the appropriate variables:

"""""""""""""""""""""
Environment variables
"""""""""""""""""""""

Make has multiple types of
`assignment operators <https://www.gnu.org/software/make/manual/make.html#Setting>`_.
Some Makefiles use ``=`` to assign variables. The only way to override
these variables is to edit the Makefile or override them on the
command-line. However, Makefiles that use ``?=`` for assignment honor
environment variables. Since Spack already sets ``CC``, ``CXX``, ``F77``,
and ``FC``, you won't need to worry about setting these variables. If
there are any other variables you need to set, you can do this in the
``setup_build_environment`` method:

.. code-block:: python

   def setup_build_environment(self, env):
       env.set("PREFIX", prefix)
       env.set("BLASLIB", spec["blas"].libs.ld_flags)


`cbench <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/cbench/package.py>`_
is a good example of a simple package that does this, while
`esmf <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/esmf/package.py>`_
is a good example of a more complex package.

""""""""""""""""""""""
Command-line arguments
""""""""""""""""""""""

If the Makefile ignores environment variables, the next thing to try
is command-line arguments. You can do this by overriding the
``build_targets`` attribute. If you don't need access to the spec,
you can do this like so:

.. code-block:: python

   build_targets = ["CC=cc"]


If you do need access to the spec, you can create a property like so:

.. code-block:: python

   @property
   def build_targets(self):
       spec = self.spec

       return [
           "CC=cc",
           f"BLASLIB={spec['blas'].libs.ld_flags}",
       ]


`cloverleaf <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/cloverleaf/package.py>`_
is a good example of a package that uses this strategy.

"""""""""""""
Edit Makefile
"""""""""""""

Some Makefiles are just plain stubborn and will ignore command-line
variables. The only way to ensure that these packages build correctly
is to directly edit the Makefile. Spack provides a ``FileFilter`` class
and a ``filter`` method to help with this. For example:

.. code-block:: python

   def edit(self, spec, prefix):
       makefile = FileFilter("Makefile")

       makefile.filter(r"^\s*CC\s*=.*",  f"CC = {spack_cc}")
       makefile.filter(r"^\s*CXX\s*=.*", f"CXX = {spack_cxx}")
       makefile.filter(r"^\s*F77\s*=.*", f"F77 = {spack_f77}")
       makefile.filter(r"^\s*FC\s*=.*",  f"FC = {spack_fc}")


`stream <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/stream/package.py>`_
is a good example of a package that involves editing a Makefile to set
the appropriate variables.

"""""""""""
Config file
"""""""""""

More complex packages often involve Makefiles that *include* a
configuration file. These configuration files are primarily composed
of variables relating to the compiler, platform, and the location of
dependencies or names of libraries. Since these config files are
dependent on the compiler and platform, you will often see entire
directories of examples for common compilers and architectures. Use
these examples to help determine what possible values to use.

If the config file is long and only contains one or two variables
that need to be modified, you can use the technique above to edit
the config file. However, if you end up needing to modify most of
the variables, it may be easier to write a new file from scratch.

If each variable is independent of each other, a dictionary works
well for storing variables:

.. code-block:: python

   def edit(self, spec, prefix):
       config = {
           "CC": "cc",
           "MAKE": "make",
       }

       if spec.satisfies("+blas"):
           config["BLAS_LIBS"] = spec["blas"].libs.joined()

       with open("make.inc", "w") as inc:
           for key in config:
               inc.write(f"{key} = {config[key]}\n")


`elk <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/elk/package.py>`_
is a good example of a package that uses a dictionary to store
configuration variables.

If the order of variables is important, it may be easier to store
them in a list:

.. code-block:: python

   def edit(self, spec, prefix):
       config = [
           f"INSTALL_DIR = {prefix}",
           "INCLUDE_DIR = $(INSTALL_DIR)/include",
           "LIBRARY_DIR = $(INSTALL_DIR)/lib",
       ]

       with open("make.inc", "w") as inc:
           for var in config:
               inc.write(f"{var}\n")


`hpl <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/hpl/package.py>`_
is a good example of a package that uses a list to store
configuration variables.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Variables to watch out for
^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is a list of common variables to watch out for. The first
two sections are
`implicit variables <https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html>`_
defined by Make and will always use the same name, while the rest are
user-defined variables and may vary from package to package.

* **Compilers**

  This includes variables such as ``CC``, ``CXX``, ``F77``, ``F90``,
  and ``FC``, as well as variables related to MPI compiler wrappers,
  like ``MPICC`` and friends.

* **Compiler flags**

  This includes variables for specific compilers, like ``CFLAGS``,
  ``CXXFLAGS``, ``F77FLAGS``, ``F90FLAGS``, ``FCFLAGS``, and ``CPPFLAGS``.
  These variables are often hard-coded to contain flags specific to a
  certain compiler. If these flags don't work for every compiler,
  you may want to consider filtering them.

* **Variables that enable or disable features**

  This includes variables like ``MPI``, ``OPENMP``, ``PIC``, and
  ``DEBUG``. These flags often require you to create a variant
  so that you can either build with or without MPI support, for
  example. These flags are often compiler-dependent. You should
  replace them with the appropriate compiler flags, such as
  ``self.compiler.openmp_flag`` or ``self.compiler.pic_flag``.

* **Platform flags**

  These flags control the type of architecture that the executable
  is compiler for. Watch out for variables like ``PLAT`` or ``ARCH``.

* **Dependencies**

  Look out for variables that sound like they could be used to
  locate dependencies, such as ``JAVA_HOME``, ``JPEG_ROOT``, or
  ``ZLIBDIR``. Also watch out for variables that control linking,
  such as ``LIBS``, ``LDFLAGS``, and ``INCLUDES``. These variables
  need to be set to the installation prefix of a dependency, or
  to the correct linker flags to link to that dependency.

* **Installation prefix**

  If your Makefile has an ``install`` target, it needs some way of
  knowing where to install. By default, many packages install to
  ``/usr`` or ``/usr/local``. Since many Spack users won't have
  sudo privileges, it is imperative that each package is installed
  to the proper prefix. Look for variables like ``PREFIX`` or
  ``INSTALL``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Makefiles in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not every package places their Makefile in the root of the package
tarball. If the Makefile is in a sub-directory like ``src``, you
can tell Spack where to locate it like so:

.. code-block:: python

   build_directory = "src"


^^^^^^^^^^^^^^^^^^^
Manual installation
^^^^^^^^^^^^^^^^^^^

Not every Makefile includes an ``install`` target. If this is the
case, you can override the default ``install`` method to manually
install the package:

.. code-block:: python

   def install(self, spec, prefix):
       mkdir(prefix.bin)
       install("foo", prefix.bin)
       install_tree("lib", prefix.lib)


^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on reading and writing Makefiles, see:
https://www.gnu.org/software/make/manual/make.html
