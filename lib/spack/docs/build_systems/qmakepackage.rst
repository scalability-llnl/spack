.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _qmakepackage:

-----
QMake
-----

Much like Autotools and CMake, QMake is a build-script generator
designed by the developers of Qt. In its simplest form, Spack's
``QMakePackage`` runs the following steps:

.. code-block:: console

   $ qmake
   $ make
   $ make check  # optional
   $ make install


QMake does not appear to have a standardized way of specifying
the installation directory, so you may have to set environment
variables or edit ``*.pro`` files to get things working properly.

^^^^^^
Phases
^^^^^^

The ``QMakeBuilder`` and ``QMakePackage`` base classes come with the following phases:

#. ``qmake`` - generate Makefiles
#. ``build`` - build the project
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   $ qmake
   $ make
   $ make install


Any of these phases can be overridden in your package as necessary.
There is also a ``check`` method that looks for a ``check`` target
in the Makefile. If a ``check`` target exists and the user runs:

.. code-block:: console

   $ spack install --test=root <qmake-package>


Spack will run ``make check`` after the build phase.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Packages that use the QMake build system can be identified by the
presence of a ``<project-name>.pro`` file. This file declares things
like build instructions and dependencies.

One thing to look for is the ``minQtVersion`` function:

.. code-block:: none

   minQtVersion(5, 6, 0)


This means that Qt 5.6.0 is the earliest release that will work.
You should specify this in a ``depends_on`` statement.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

At the bare minimum, packages that use the QMake build system need a
``qt`` dependency. Since this is always the case, the ``QMakePackage``
base class already contains:

.. code-block:: python

   depends_on("qt", type="build")


If you want to specify a particular version requirement, or need to
link to the ``qt`` libraries, you can override this in your package:

.. code-block:: python

   depends_on("qt@5.6.0:")

^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to qmake
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to pass any arguments to the ``qmake`` call, you can
override the ``qmake_args`` method like so:

.. code-block:: python

   def qmake_args(self):
       return ["-recursive"]


This method can be used to pass flags as well as variables.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``*.pro`` file in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the ``*.pro`` file used to tell QMake how to build the package is
found in a sub-directory, you can tell Spack to run all phases in this
sub-directory by adding the following to the package:

.. code-block:: python

   build_directory = "src"


^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the QMake build system, see:
http://doc.qt.io/qt-5/qmake-manual.html
