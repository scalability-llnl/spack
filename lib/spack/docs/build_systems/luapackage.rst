.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _luapackage:

---
Lua
---

The ``Lua`` build-system is a helper for the common case of Lua packages that provide
a rockspec file.  This is not meant to take a rock archive, but to build
a source archive or repository that provides a rockspec, which should cover
most lua packages. In the case a Lua package builds by Make rather than
luarocks, prefer MakefilePackage.

^^^^^^
Phases
^^^^^^

The ``LuaBuilder`` and `LuaPackage`` base classes come with the following phases:

#. ``unpack`` - if using a rock, unpacks the rock and moves into the source directory
#. ``preprocess`` - adjust sources or rockspec to fix build
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   # If the archive is a source rock
   $ luarocks unpack <archive>.src.rock
   $ # preprocess is a noop by default
   $ luarocks make <name>.rockspec


Any of these phases can be overridden in your package as necessary.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Packages that use the Lua/LuaRocks build system can be identified by the
presence of a ``*.rockspec`` file in their sourcetree, or can be fetched as
a source rock archive (``.src.rock``). This file declares things like build
instructions and dependencies, the ``.src.rock`` also contains all code.

It is common for the rockspec file to list the lua version required in
a dependency. The LuaPackage class adds appropriate dependencies on a Lua
implementation, but it is a good idea to specify the version required with
a ``depends_on`` statement.  The block normally will be a table definition like
this:

.. code-block:: lua

   dependencies = {
      "lua >= 5.1",
   }

The LuaPackage class supports source repositories and archives containing
a rockspec and directly downloading source rock files.  It *does not* support
downloading dependencies listed inside a rockspec, and thus does not support
directly downloading a rockspec as an archive.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

All base dependencies are added by the build system, but LuaRocks is run to
avoid downloading extra Lua dependencies during build.  If the package needs
Lua libraries outside the standard set, they should be added as dependencies.

To specify a Lua version constraint but allow all lua implementations, prefer
to use ``depends_on("lua-lang@5.1:5.1.99")`` to express any 5.1 compatible
version. If the package requires LuaJit rather than Lua,
a ``depends_on("luajit")`` should be used to ensure a LuaJit distribution is
used instead of the Lua interpreter. Alternately, if only interpreted Lua will
work ``depends_on("lua")`` will express that.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to luarocks make
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to pass any arguments to the ``luarocks make`` call, you can
override the ``luarocks_args`` method like so:

.. code-block:: python

    def luarocks_args(self):
        return ["flag1", "flag2"]

One common use of this is to override warnings or flags for newer compilers, as in:

.. code-block:: python

    def luarocks_args(self):
        return ["CFLAGS='-Wno-error=implicit-function-declaration'"]

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the LuaRocks build system, see:
https://luarocks.org/
