.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _rubypackage:

----
Ruby
----

Like Perl, Python, and R, Ruby has its own build system for
installing Ruby gems.

^^^^^^
Phases
^^^^^^

The ``RubyBuilder`` and ``RubyPackage`` base classes provide the following phases that
can be overridden:

#. ``build`` - build everything needed to install
#. ``install`` - install everything from build directory

For packages that come with a ``*.gemspec`` file, these phases run:

.. code-block:: console

   $ gem build *.gemspec
   $ gem install *.gem


For packages that come with a ``Rakefile`` file, these phases run:

.. code-block:: console

   $ rake package
   $ gem install *.gem


For packages that come pre-packaged as a ``*.gem`` file, the build
phase is skipped and the install phase runs:

.. code-block:: console

   $ gem install *.gem


These are all standard ``gem`` commands and can be found by running:

.. code-block:: console

   $ gem help commands


For packages that only distribute ``*.gem`` files, these files can be
downloaded with the ``expand=False`` option in the ``version`` directive.
The build phase will be automatically skipped.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

When building from source, Ruby packages can be identified by the
presence of any of the following files:

* ``*.gemspec``
* ``Rakefile``
* ``setup.rb`` (not yet supported)

However, not all Ruby packages are released as source code. Some are only
released as ``*.gem`` files. These files can be extracted using:

.. code-block:: console

   $ gem unpack *.gem


^^^^^^^^^^^
Description
^^^^^^^^^^^

The ``*.gemspec`` file may contain something like:

.. code-block:: ruby

   summary = "An implementation of the AsciiDoc text processor and publishing toolchain"
   description = "A fast, open source text processor and publishing toolchain for converting AsciiDoc content to HTML 5, DocBook 5, and other formats."


Either of these can be used for the description of the Spack package.

^^^^^^^^
Homepage
^^^^^^^^

The ``*.gemspec`` file may contain something like:

.. code-block:: ruby

   homepage = "https://asciidoctor.org"


This should be used as the official homepage of the Spack package.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

All Ruby packages require Ruby at build and run-time. For this reason,
the base class contains:

.. code-block:: python

   extends("ruby")


The ``*.gemspec`` file may contain something like:

.. code-block:: ruby

   required_ruby_version = ">= 2.3.0"


This can be added to the Spack package using:

.. code-block:: python

   depends_on("ruby@2.3.0:", type=("build", "run"))


^^^^^^^^^^^^^^^^^
Ruby dependencies
^^^^^^^^^^^^^^^^^

When you install a package with ``gem``, it reads the ``*.gemspec``
file in order to determine the dependencies of the package.
If the dependencies are not yet installed, ``gem`` downloads them
and installs them for you. This may sound convenient, but Spack
cannot rely on this behavior for two reasons:

#. Spack needs to be able to install packages on air-gapped networks.

   If there is no internet connection, ``gem`` can't download the
   package dependencies. By explicitly listing every dependency in
   the ``package.py``, Spack knows what to download ahead of time.

#. Duplicate installations of the same dependency may occur.

   Spack supports *activation* of Ruby extensions, which involves
   symlinking the package installation prefix to the Ruby installation
   prefix. If your package is missing a dependency, that dependency
   will be installed to the installation directory of the same package.
   If you try to activate the package + dependency, it may cause a
   problem if that package has already been activated.

For these reasons, you must always explicitly list all dependencies.
Although the documentation may list the package's dependencies,
often the developers assume people will use ``gem`` and won't have to
worry about it. Always check the ``*.gemspec`` file to find the true
dependencies.

Check for the following clues in the ``*.gemspec`` file:

* ``add_runtime_dependency``

  These packages are required for installation.

* ``add_dependency``

  This is an alias for ``add_runtime_dependency``

* ``add_development_dependency``

  These packages are optional dependencies used for development.
  They should not be added as dependencies of the package.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on Ruby packaging, see:
https://guides.rubygems.org/
