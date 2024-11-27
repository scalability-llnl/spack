.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

================
Feature Overview
================

This is a high-level overview of features that make Spack different
from other `package managers
<http://en.wikipedia.org/wiki/Package_management_system>`_ and `port
systems <http://en.wikipedia.org/wiki/Ports_collection>`_.

---------------------------
Simple package installation
---------------------------

Installing the default version of a package is simple. This will install
the latest version of the ``mpileaks`` package and all of its dependencies:

.. code-block:: console

   $ spack install mpileaks

--------------------------------
Custom versions & configurations
--------------------------------

Spack allows installation to be customized.  Users can specify the
version, build compiler, compile-time options, and cross-compile
platform, all on the command line.

.. code-block:: console

   # Install a particular version by appending @
   $ spack install mpileaks@1.1.2

   # Specify a compiler (and its version), with %
   $ spack install mpileaks@1.1.2 %gcc@4.7.3

   # Add special compile-time options by name
   $ spack install mpileaks@1.1.2 %gcc@4.7.3 debug=True

   # Add special boolean compile-time options with +
   $ spack install mpileaks@1.1.2 %gcc@4.7.3 +debug

   # Add compiler flags using the conventional names
   $ spack install mpileaks@1.1.2 %gcc@4.7.3 cppflags="-O3 -floop-block"

   # Cross-compile for a different micro-architecture with target=
   $ spack install mpileaks@1.1.2 target=icelake

Users can specify as many or few options as they care about. Spack
will fill in the unspecified values with sensible defaults. The two listed
syntaxes for variants are identical when the value is boolean.

----------------------
Customize dependencies
----------------------

Spack allows *dependencies* of a particular installation to be
customized extensively.  Suppose that ``hdf5`` depends
on ``openmpi`` and indirectly on ``hwloc``.  Using ``^``, users can add custom
configurations for the dependencies:

.. code-block:: console

   # Install hdf5 and link it with specific versions of openmpi and hwloc
   $ spack install hdf5@1.10.1 %gcc@4.7.3 +debug ^openmpi+cuda fabrics=auto ^hwloc+gl

------------------------
Non-destructive installs
------------------------

Spack installs every unique package/dependency configuration into its
own prefix, so new installs will not break existing ones.

-------------------------------
Packages can peacefully coexist
-------------------------------

Spack avoids library misconfiguration by using ``RPATH`` to link
dependencies.  When a user links a library or runs a program, it is
tied to the dependencies it was built with, so there is no need to
manipulate ``LD_LIBRARY_PATH`` at runtime.

-------------------------
Creating packages is easy
-------------------------

To create a new packages, all Spack needs is a URL for the source
archive.  The ``spack create`` command will create a boilerplate
package file, and the package authors can fill in specific build steps
in pure Python.

For example, this command:

.. code-block:: console

   $ spack create https://ftp.osuosl.org/pub/blfs/conglomeration/libelf/libelf-0.8.13.tar.gz

creates a simple python file:

.. code-block:: python

   from spack.package import *


   class Libelf(AutotoolsPackage):
       """FIXME: Put a proper description of your package here."""

       # FIXME: Add a proper url for your package's homepage here.
       homepage = "https://www.example.com"
       url = "https://ftp.osuosl.org/pub/blfs/conglomeration/libelf/libelf-0.8.13.tar.gz"

       # FIXME: Add a list of GitHub accounts to
       # notify when the package is updated.
       # maintainers("github_user1", "github_user2")

       version("0.8.13", sha256="591a9b4ec81c1f2042a97aa60564e0cb79d041c52faa7416acb38bc95bd2c76d")

       # FIXME: Add dependencies if required.
       # depends_on("foo")

       def configure_args(self):
           # FIXME: Add arguments other than --prefix
           # FIXME: If not needed delete this function
           args = []
           return args

It doesn't take much python coding to get from there to a working
package:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/libelf/package.py
   :lines: 5-

Spack also provides wrapper functions around common commands like
``configure``, ``make``, and ``cmake`` to make writing packages
simple.
