.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)


.. _build-systems:

=============
Build Systems
=============

Spack defines a number of classes which understand how to use common
`build systems  <https://en.wikipedia.org/wiki/List_of_build_automation_software>`_
(Makefiles, CMake, etc.). Spack package definitions can inherit these
classes in order to streamline their builds.

This guide provides information specific to each particular build system.
It assumes that you've read the :ref:`packaging-guide` and expands
on these ideas for each distinct build system that Spack supports:

.. toctree::
   :maxdepth: 1
   :caption: Make-based

   build_systems/makefilepackage

.. toctree::
   :maxdepth: 1
   :caption: Make-incompatible

   build_systems/mavenpackage
   build_systems/sconspackage
   build_systems/wafpackage

.. toctree::
   :maxdepth: 1
   :caption: Build-script generation

   build_systems/autotoolspackage
   build_systems/cmakepackage
   build_systems/cachedcmakepackage
   build_systems/mesonpackage
   build_systems/qmakepackage
   build_systems/sippackage

.. toctree::
   :maxdepth: 1
   :caption: Language-specific

   build_systems/luapackage
   build_systems/octavepackage
   build_systems/perlpackage
   build_systems/pythonpackage
   build_systems/rpackage
   build_systems/racketpackage
   build_systems/rubypackage

.. toctree::
   :maxdepth: 1
   :caption: Other

   build_systems/bundlepackage
   build_systems/cudapackage
   build_systems/custompackage
   build_systems/inteloneapipackage
   build_systems/intelpackage
   build_systems/rocmpackage
   build_systems/sourceforgepackage

For reference, the :py:mod:`Build System API docs <spack.build_systems>`
provide a list of build systems and methods/attributes that can be
overridden. If you are curious about the implementation of a particular
build system, you can view the source code by running:

.. code-block:: console

   $ spack edit --build-system autotools


This will open up the ``AutotoolsPackage`` definition in your favorite
editor. In addition, if you are working with a less common build system
like QMake, SCons, or Waf, it may be useful to see examples of other
packages. You can quickly find examples by running:

.. code-block:: console

   $ cd var/spack/repos/builtin/packages
   $ grep -l QMakePackage */package.py


You can then view these packages with ``spack edit``.

This guide is intended to supplement the
:py:mod:`Build System API docs <spack.build_systems>` with examples of
how to override commonly used methods. It also provides rules of thumb
and suggestions for package developers who are unfamiliar with a
particular build system.
