.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _cachedcmakepackage:

------------------
CachedCMakePackage
------------------

The CachedCMakePackage base class is used for CMake-based workflows
that create a CMake cache file prior to running ``cmake``. This is
useful for packages with arguments longer than the system limit, and
for reproducibility.

The documentation for this class assumes that the user is familiar with
the ``CMakePackage`` class from which it inherits. See the documentation
for :ref:`CMakePackage <_cmakepackage>`.

^^^^^^
Phases
^^^^^^

The ``CachedCMakePackage base class comes with the following phases:

#. ``initconfig`` - generate the CMake cache file
#. ``cmake`` - generate the Makefile
#. ``build`` - build the package
#. ``install`` - install the package

By default, these phases run:

.. code-block:: console

   $ mkdir spack-build
   $ cd spack-build
   $ cat << EOF > name-arch-compiler@version.cmake
   # Write information on compilers and dependencies
   # includes information on mpi and cuda if applicable
   $ cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/installation/prefix -C name-arch-compiler@version.cmake
   $ make
   $ make test  # optional
   $ make install

The ``CachedCMakePackage`` class inherits from the ``CMakePackage``
class, and accepts all of the same options and adds all of the same
flags to the ``cmake`` command. Similar to the ``CMakePAckage`` class,
you may need to add a few arguments yourself, and the
``CachedCMakePackage`` provides the same interface to add those
flags.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Adding entries to the CMake cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to adding flags to the ``cmake`` command, you may need to
add entries to the CMake cache in the ``initconfig`` phase. This can
be done by overriding one of four methods:

#. ``CachedCMakePackage.initconfig_compiler_entries``
#. ``CachedCMakePackage.initconfig_mpi_entries``
#. ``CachedCMakePackage.initconfig_hardware_entries``
#. ``CachedCMakePackage.initconfig_package_entries``

Each of these methods returns a list of CMake cache strings. The
distinction between these methods is merely to provide a
well-structured and legible cmake cache file -- otherwise, entries
from each of these methods are handled identically.

Spack also provides convenience methods for generating CMake cache
entries. These methods are available at module scope in every Spack
package. Because CMake parses boolean options, strings, and paths
differently, there are three such methods:

#. ``cmake_cache_option``
#. ``cmake_cache_string``
#. ``cmake_cache_path``

These methods each accept three parameters -- the name of the CMake
variable associated with the entry, the value of the entry, and an
optional comment -- and return strings in the appropriate format to be
returned from any of the ``initconfig*`` methods. Additionally, these
methods may return comments beginning with the ``#`` character.

A typical usage of these methods may look something like this:

.. code-block:: python

   def initconfig_mpi_entries(self)
       # Get existing MPI configurations
       entries = super(self, Foo).initconfig_mpi_entries()

       # The existing MPI configurations key on whether ``mpi`` is in the spec
       # This spec has an MPI variant, and we need to enable MPI when it is on.
       # This hypothetical package controls MPI with the ``FOO_MPI`` option to
       # cmake.
       if '+mpi' in self.spec:
           entries.append(cmake_cache_option('FOO_MPI', True, "enable mpi"))
       else:
           entries.append(cmake_cache_option('FOO_MPI', False, "disable mpi"))

   def initconfig_package_entries(self):
       # Package specific options
       entries = []

       entries.append('#Entries for build options')

       bar_on = '+bar' in self.spec
       entries.append(cmake_cache_option('FOO_BAR', bar_on, 'toggle bar'))

       entries.append('#Entries for dependencies')

       if self.spec['blas'].name == 'baz':  # baz is our blas provider
       entries.append(cmake_cache_string('FOO_BLAS', 'baz', 'Use baz'))
       entries.append(cmake_cache_path('BAZ_PREFIX', self.spec['baz'].prefix))

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on CMake cache files, see:
https://cmake.org/cmake/help/latest/manual/cmake.1.html
