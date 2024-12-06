.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _perlpackage:

----
Perl
----

Much like Octave, Perl has its own language-specific
build system.

^^^^^^
Phases
^^^^^^

The ``PerlBuilder`` and ``PerlPackage`` base classes come with 3 phases that can be overridden:

#. ``configure`` - configure the package
#. ``build`` - build the package
#. ``install`` - install the package

Perl packages have 2 common modules used for module installation:

"""""""""""""""""""""""
``ExtUtils::MakeMaker``
"""""""""""""""""""""""

The ``ExtUtils::MakeMaker`` module is just what it sounds like, a module
designed to generate Makefiles. It can be identified by the presence of
a ``Makefile.PL`` file, and has the following installation steps:

.. code-block:: console

   $ perl Makefile.PL INSTALL_BASE=/path/to/installation/prefix
   $ make
   $ make test  # optional
   $ make install


"""""""""""""""""
``Module::Build``
"""""""""""""""""

The ``Module::Build`` module is a pure-Perl build system, and can be
identified by the presence of a ``Build.PL`` file. It has the following
installation steps:

.. code-block:: console

   $ perl Build.PL --install_base /path/to/installation/prefix
   $ ./Build
   $ ./Build test  # optional
   $ ./Build install


If both ``Makefile.PL`` and ``Build.PL`` files exist in the package,
Spack will use ``Makefile.PL`` by default. If your package uses a
different module, ``PerlPackage`` will need to be extended to support
it.

``PerlPackage`` automatically detects which build steps to use, so there
shouldn't be much work on the package developer's side to get things
working.

^^^^^^^^^^^^^^^^^^^^^
Finding Perl packages
^^^^^^^^^^^^^^^^^^^^^

Most Perl modules are hosted on CPAN - The Comprehensive Perl Archive
Network. If you need to find a package for ``XML::Parser``, for example,
you should search for "CPAN XML::Parser".

Some CPAN pages are versioned. Check for a link to the
"Latest Release" to make sure you have the latest version.

^^^^^^^^^^^^
Package name
^^^^^^^^^^^^

When you use ``spack create`` to create a new Perl package, Spack will
automatically prepend ``perl-`` to the front of the package name. This
helps to keep Perl modules separate from other packages. The same
naming scheme is used for other language extensions, like Python and R.

^^^^^^^^^^^
Description
^^^^^^^^^^^

Most CPAN pages have a short description under "NAME" and a longer
description under "DESCRIPTION". Use whichever you think is more
useful while still being succinct.

^^^^^^^^
Homepage
^^^^^^^^

In the top-right corner of the CPAN page, you'll find a "permalink"
for the package. This should be used instead of the current URL, as
it doesn't contain the version number and will always link to the
latest release.

^^^
URL
^^^

If you haven't found it already, the download URL is on the right
side of the page below the permalink. Search for "Download".

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

Every ``PerlPackage`` obviously depends on Perl at build and run-time,
so ``PerlPackage`` contains:

.. code-block:: python

   extends("perl")


If your package requires a specific version of Perl, you should
specify this.

Although newer versions of Perl include ``ExtUtils::MakeMaker`` and
``Module::Build`` as "core" modules, you may want to add dependencies
on ``perl-extutils-makemaker`` and ``perl-module-build`` anyway. Many
people add Perl as an external package, and we want the build to work
properly. If your package uses ``Makefile.PL`` to build, add:

.. code-block:: python

   depends_on("perl-extutils-makemaker", type="build")


If your package uses ``Build.PL`` to build, add:

.. code-block:: python

   depends_on("perl-module-build", type="build")


^^^^^^^^^^^^^^^^^
Perl dependencies
^^^^^^^^^^^^^^^^^

Below the download URL, you will find a "Dependencies" link, which
takes you to a page listing all of the dependencies of the package.
Packages listed as "Core module" don't need to be added as dependencies,
but all direct dependencies should be added. Don't add dependencies of
dependencies. These should be added as dependencies to the dependency,
not to your package.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to configure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Packages that have non-Perl dependencies often use command-line
variables to specify their installation directory. You can pass
arguments to ``Makefile.PL`` or ``Build.PL`` by overriding
``configure_args`` like so:

.. code-block:: python

   def configure_args(self):
       expat = self.spec["expat"].prefix

       return [
           "EXPATLIBPATH={0}".format(expat.lib),
           "EXPATINCPATH={0}".format(expat.include),
       ]


^^^^^^^
Testing
^^^^^^^

``PerlPackage`` provides a simple stand-alone test of the successfully
installed package to confirm that installed perl module(s) can be used.
These tests can be performed any time after the installation using
``spack -v test run``. (For more information on the command, see 
:ref:`cmd-spack-test-run`.)

The base class automatically detects perl modules based on the presence
of ``*.pm`` files under the package's library directory. For example,
the files under ``perl-bignum``'s perl library are:

.. code-block:: console

   $ find . -name "*.pm"
   ./bigfloat.pm
   ./bigrat.pm
   ./Math/BigFloat/Trace.pm
   ./Math/BigInt/Trace.pm
   ./Math/BigRat/Trace.pm
   ./bigint.pm
   ./bignum.pm


which results in the package having the ``use_modules`` property containing:

.. code-block:: python

   use_modules = [
       "bigfloat",
       "bigrat",
       "Math::BigFloat::Trace",
       "Math::BigInt::Trace",
       "Math::BigRat::Trace",
       "bigint",
       "bignum",
   ]

.. note::

   This list can often be used to catch missing dependencies.

If the list is somehow wrong, you can provide the names of the modules
yourself by overriding ``use_modules`` like so:

 .. code-block:: python

    use_modules = ["bigfloat", "bigrat", "bigint", "bignum"]

If you only want a subset of the automatically detected modules to be
tested, you could instead define the ``skip_modules`` property on the
package. So, instead of overriding ``use_modules`` as shown above, you
could define the following:

 .. code-block:: python

    skip_modules = [
        "Math::BigFloat::Trace",
        "Math::BigInt::Trace",
        "Math::BigRat::Trace",
    ]

for the same use tests.

^^^^^^^^^^^^^^^^^^^^^
Alternatives to Spack
^^^^^^^^^^^^^^^^^^^^^

If you need to maintain a stack of Perl modules for a user and don't
want to add all of them to Spack, a good alternative is ``cpanm``.
If Perl is already installed on your system, it should come with a
``cpan`` executable. To install ``cpanm``, run the following command:

.. code-block:: console

   $ cpan App::cpanminus


Now, you can install any Perl module you want by running:

.. code-block:: console

   $ cpanm Module::Name


Obviously, these commands can only be run if you have root privileges.
Furthermore, ``cpanm`` is not capable of installing non-Perl dependencies.
If you need to install to your home directory or need to install a module
with non-Perl dependencies, Spack is a better option.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

You can find more information on installing Perl modules from source
at: http://www.perlmonks.org/?node_id=128077

More generic Perl module installation instructions can be found at:
http://www.cpan.org/modules/INSTALL.html
