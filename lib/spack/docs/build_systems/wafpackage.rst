.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _wafpackage:

---
Waf
---

Like SCons, Waf is a general-purpose build system that does not rely
on Makefiles to build software.

^^^^^^
Phases
^^^^^^

The ``WafBuilder`` and ``WafPackage`` base classes come with the following phases:

#. ``configure`` - configure the project
#. ``build`` - build the project
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   $ python waf configure --prefix=/path/to/installation/prefix
   $ python waf build
   $ python waf install


Each of these are standard Waf commands and can be found by running:

.. code-block:: console

   $ python waf --help


Each phase provides a ``<phase>`` function that runs:

.. code-block:: console

   $ python waf -j<jobs> <phase>


where ``<jobs>`` is the number of parallel jobs to build with. Each phase
also has a ``<phase_args>`` function that can pass arguments to this call.
All of these functions are empty. The ``configure`` phase
automatically adds  ``--prefix=/path/to/installation/prefix``, so you
don't need to add that in the ``configure_args``.

^^^^^^^
Testing
^^^^^^^

``WafPackage`` also provides ``test`` and ``installtest`` methods,
which are run after the ``build`` and ``install`` phases, respectively.
By default, these phases do nothing, but you can override them to
run package-specific unit tests.

.. code-block:: python

   def installtest(self):
       with working_dir("test"):
           pytest = which("py.test")
           pytest()


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Each Waf package comes with a custom ``waf`` build script, written in
Python. This script contains instructions to build the project.

The package also comes with a ``wscript`` file. This file is used to
override the default ``configure``, ``build``, and ``install`` phases
to customize the Waf project. It also allows developers to override
the default ``./waf --help`` message. Check this file to find useful
information about dependencies and the minimum versions that are
supported.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

``WafPackage`` does not require ``waf`` to build. ``waf`` is only
needed to create the ``./waf`` script. Since ``./waf`` is a Python
script, Python is needed to build the project. ``WafPackage`` adds
the following dependency automatically:

.. code-block:: python

   depends_on("python@2.5:", type="build")


Waf only supports Python 2.5 and up.

^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to waf
^^^^^^^^^^^^^^^^^^^^^^^^

As previously mentioned, each phase comes with a ``<phase_args>``
function that can be used to pass arguments to that particular
phase. For example, if you need to pass arguments to the build
phase, you can use:

.. code-block:: python

   def build_args(self, spec, prefix):
       args = []

       if self.run_tests:
           args.append("--test")

       return args


A list of valid options can be found by running ``./waf --help``.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the Waf build system, see:
https://waf.io/book/
