.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _mesonpackage:

-----
Meson
-----

Much like Autotools and CMake, Meson is a build system.  But it is
meant to be both fast and as user friendly as possible.  GNOME's goal
is to port modules to use the Meson build system.

^^^^^^
Phases
^^^^^^

The ``MesonBuilder`` and ``MesonPackage`` base classes come with the following phases:

#. ``meson`` - generate ninja files
#. ``build`` - build the project
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   $ mkdir spack-build
   $ cd spack-build
   $ meson .. --prefix=/path/to/installation/prefix
   $ ninja
   $ ninja test  # optional
   $ ninja install


Any of these phases can be overridden in your package as necessary.
There is also a ``check`` method that looks for a ``test`` target
in the build file. If a ``test`` target exists and the user runs:

.. code-block:: console

   $ spack install --test=root <meson-package>


Spack will run ``ninja test`` after the build phase.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Packages that use the Meson build system can be identified by the
presence of a ``meson.build`` file. This file declares things
like build instructions and dependencies.

One thing to look for is the ``meson_version`` key that gets passed
to the ``project`` function:

.. code-block:: none
   :emphasize-lines: 10

   project('gtk+', 'c',
        version: '3.94.0',
        default_options: [
          'buildtype=debugoptimized',
          'warning_level=1',
          # We only need c99, but glib needs GNU-specific features
          # https://github.com/mesonbuild/meson/issues/2289
          'c_std=gnu99',
        ],
        meson_version: '>= 0.43.0',
        license: 'LGPLv2.1+')


This means that Meson 0.43.0 is the earliest release that will work.
You should specify this in a ``depends_on`` statement.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

At the bare minimum, packages that use the Meson build system need
``meson`` and ```ninja``` dependencies. Since this is always the case,
the ``MesonPackage`` base class already contains:

.. code-block:: python

   depends_on("meson", type="build")
   depends_on("ninja", type="build")


If you need to specify a particular version requirement, you can
override this in your package:

.. code-block:: python

   depends_on("meson@0.43.0:", type="build")
   depends_on("ninja", type="build")


^^^^^^^^^^^^^^^^^^^
Finding meson flags
^^^^^^^^^^^^^^^^^^^

To get a list of valid flags that can be passed to ``meson``, run the
following command in the directory that contains ``meson.build``:

.. code-block:: console

   $ meson setup --help


^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to meson
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to pass any arguments to the ``meson`` call, you can
override the ``meson_args`` method like so:

.. code-block:: python

   def meson_args(self):
       return ["--warnlevel=3"]


This method can be used to pass flags as well as variables.

Note that the ``MesonPackage`` base class already defines variants for
``buildtype``, ``default_library`` and ``strip``, which are mapped to default
Meson arguments, meaning that you don't have to specify these.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the Meson build system, see:
https://mesonbuild.com/index.html
