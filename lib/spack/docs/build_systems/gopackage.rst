.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _gopackage:

-----------
GoPackage
-----------

There are a couple of things to be aware of about applications built
with Go:

* The ``go`` command includes more build/install functionality than
  C's ``cc`` but not as much e.g. Python's ``pip``.

  As a result, Go-based projects use a variety of build strategies:
  simple invocations of ``go build``, custom go "scripts" that
  leverage ``go run``, Makefiles, and/or *etc...*.

* Go's dependency management story has evolved from an initial
  do-it-yourself attitude through a small number of commonly used
  tools to an officially supported approach (Go "modules").  The Go
  team provides an `introduction to Go modules
  <https://blog.golang.org/using-go-modules>`_ and maintains a site
  that tracks `the gory details
  <https://github.com/golang/go/wiki/Modules>`_.

  Go modules are the future, ``GOPATH`` will likely be deprecated in
  Go 1.14.

The best approach to packaging a Go-based project for Spack depends on
the details of the project.  ``GoPackage`` is a good fit for simple
situations but another package, e.g. ``MakefilePackage``, might be
better.

In addition to a ``go.mod`` file and ``vendor`` directory (see
:ref:`important_files`), you should check for "Install" documentation
and makefiles in their various guises.  Applications that provide
a makefile might be better built via ``MakefilePackage``; it's up to
the packager to understand the actions taken by the makefile and
decide whether to cut it out of the loop or use it.

Ideas from ``GoPackage`` that might be useful when using other base
classes include:

- Use the package's ``setup_build_environment`` to set
  ``GO111MODULE=on`` to enable module mode and set
  ``GOFLAGS=-mod-vendor`` to install dependencies from the ``vendor``,
  which prevents ``go`` from downloading dependencies at build time.
- If the application hasn't vendored its dependencies, use
  ``modules2tuple`` to generate "bulk" resource statements and include
  them in the package definition via ``import_resources`` (see
  :ref:`packages_without_vendor_dir`).

.. _important_files:

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Applications that are good candidates for ``GoPackage`` will have:

* A ``go.mod`` file in the project's top level.  The ``go.mod`` file
  contains a "module" line that names the module, a ``go X.Y`` line
  that states that the project uses that particular version of go, and
  a series of "require" and "replace" lines that describe the module's
  dependencies.

* A ``vendor`` directory that contains the project's dependencies.  A
  missing ``vendir`` directory means that the packager will probably
  need to define resources (see below) to pull in the dependencies.

^^^^^^
Phases
^^^^^^

The ``GoPackage`` base class comes with the following phases:

#. ``build`` - build the package
#. ``install`` - install the package

By default, the build phase invokes ``go build`` in an environment
that includes ``GO111MODULE=on`` and ``GOFLAGS=-mod-vendor`` and the
install phase copies the files named in ``executables`` into
``prefix.bin``

^^^^^^^^^^^^^^^^^^^^^^^^^^
Simple package definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplest case is a project that uses a simple invocation of ``go
build`` to compile an executable, *and* uses modules, *and* has
vendored its dependencies.

Here's an example of a package definition which is only slightly
complicated by the fact that it requires a newer version of Go than
``GoPackage`` provides by default:

.. code-block:: python

    from spack import *


    class Lazygit(GoPackage):
        """Simple terminal UI for git commands."""

        homepage = "https://github.com/jesseduffield/lazygit"
        url      = "https://github.com/jesseduffield/lazygit/archive/v0.11.3.tar.gz"

        version('0.11.3', sha256='b3c503de6b34fd4284fd70655e7f42feafc07f090e7f7cc00db261f56c583c46')

        depends_on('go@1.13:', type='build')  # go.mod value overrides default

        executables = ['lazygit']

While it generally follows the common patterns of a Spack package,
it's worth calling attention to its:

* adding a *build* dependency on the version of the Go package that it
  requires (from the existing `go.mod`);
* using the default ``build`` and ``install`` steps that ``GoPackage``
  provides; and
* providing the name of the executable to be installed by the default
  ``install`` step.

The ``GoPackage`` provides a ``setup_build_environment`` that sets
``GO111MODULES=on`` and ``GOFLAGS=-mod=vendor`` and its default build
step invokes ``go build``.  Additional arguments to ``go build`` can
be provided by providing a ``build_args`` function, e.g. from the Hugo
package:

.. code-block:: python

    def build_args(self):
        if self.spec.satisfies('+extended'):
            return ['-tags', 'extended']
        return []

to invoke ``go build -tags extended``.

.. _packages_without_vendor_dir:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Packages without vendored dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Packages that can be built with a simple invocation of ``go build``,
that use modules, *but have not vendored their dependencies* require a
bit of extra work.

In particular, in order to satisfy Spack's requirement that nothing is
downloaded during the build step, the package needs to define
"resources" (details in :ref:`resources`) that describe from whence to
fetch each dependency, where to emplace it, and the version of the
package to which it applies.  It is possible (likely) that each
release of the project will have a different set of resources
definitions.

We're following the approach used by the FreeBSD Ports team (for the
curious, their Porters Handbook includes more details about `how to
package Go applications
<https://www.freebsd.org/doc/en_US.ISO8859-1/books/porters-handbook/building.html#using-go>`_
for FreeBSD).

Spack package authors can use `modules2tuple
<https://github.com/dmgk/modules2tuple>`_ (FreeBSD's tool, which has
been extended to emit Spack resource statements) to provide the
resource definitions and the ``import_resources`` directive to include
them without overly-complicating the package definition.

There are four steps to describing the dependencies in the package
definition:

#. Stage the application and check the ``go.mod`` file for any
   constraints on the go release (before overwriting it as a side
   effect of the next step).

#. Use the Go toolchain and the ``go.mod`` file to determine
   the set of required dependencies and build a vendor directory.

#. Run the newly created ``vendor/modules.txt`` file through
   ``modules2tuple`` to generate a JSON file containing resource
   definitions.

   .. code-block:: console

      # in the root directory of the project (where the go.mod file lives``
      $ go mod vendor
      $ modules2tuple -spack -app_version=1.2.3 vendor/modules.txt > resources-1.2.3.json

#. Finally, copy that file into the Spack package directory and add an
   ``import_resources`` statement that refers to it in the package
   definition.

   .. code-block:: python

      # Note that the resource definitions should include a when
      # clause that constrains their version (modules2tuple handles)
      # this automatically.
      import_resources("resources-1.2.3.json")

^^^^^^^^^^^^^^^
Advanced topics
^^^^^^^^^^^^^^^

Packaging projects that don't fit into either of the previous two
categories is "left as an exercise for the reader".

More seriously, you'll need to understand how the project builds
itself and use an appropriate Spack build system.  Most projects that
can't use ``GoPackage`` seem to end up using ``MakefilePackage``.

Things to keep in mind include:

* the package should only have a *build* dependency on go unless
  something unusual is happening at run time, e.g. the application
  runs a "script" via `go run` or calls some other sub-tool of the
  `go` command (e.g. `go fmt`).

* you'll need to provide ``resource`` definitions for dependencies
  (``modules2tuple`` might be helpful) and ensure that ``go`` does not
  access the network while building (probably by enforcing module mode
  and invoking it with the ``-mod=vendor`` flag); and

* ensure that the use of the ``GOFLAGS`` environment variable does not
  conflict with attempts to set arguments on the command line.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^


* The canonical `Go site <https://golang.org/>`_.

* Motivation, background and details about the `go command
  <https://golang.org/doc/articles/go_command.html>`_, Go's general
  purpose build tool.

* `Everything you ever wanted to know <https://golang.org/cmd/go/>`_
  about the go command.

* Digital Ocean's simple introduction to `building Go programs
  <https://www.digitalocean.com/community/tutorials/how-to-build-and-install-go-programs>`_

* The canonical `Using Go modules
  <https://blog.golang.org/using-go-modules>`_ blog post.

* The authoritative `Go modules wiki
  <https://github.com/golang/go/wiki/Modules>`_ page.
