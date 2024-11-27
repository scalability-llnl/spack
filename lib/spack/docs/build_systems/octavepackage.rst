.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _octavepackage:

------
Octave
------

Octave has its own build system for installing packages.

^^^^^^
Phases
^^^^^^

The ``OctaveBuilder`` and ``OctavePackage`` base classes have a single phase:

#. ``install`` - install the package

By default, this phase runs the following command:

.. code-block:: console

   $ octave '--eval' 'pkg prefix <prefix>; pkg install <archive_file>'


Beware that uninstallation is not implemented at the moment. After uninstalling
a package via Spack, you also need to manually uninstall it from Octave via
``pkg uninstall <package_name>``.

^^^^^^^^^^^^^^^^^^^^^^^
Finding Octave packages
^^^^^^^^^^^^^^^^^^^^^^^

Most Octave packages are listed at https://octave.sourceforge.io/packages.php.

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^

Usually, the homepage of a package will list dependencies, i.e.
``Dependencies:	Octave >= 3.6.0 struct >= 1.0.12``. The same information should
be available in the ``DESCRIPTION`` file in the root of each archive.

^^^^^^^^^^^^^^^^^^^^^^
External Documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the Octave build system, see:
https://octave.org/doc/v4.4.0/Installing-and-Removing-Packages.html
