.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _packaging-guide:

===============
Packaging Guide
===============

This guide is intended for developers or administrators who want to
package software so that Spack can install it.  It assumes that you
have at least some familiarity with Python, and that you've read the
:ref:`basic usage guide <basic-usage>`, especially the part about
:ref:`specs <sec-specs>`.

There are two key parts of Spack:

#. **Specs**: expressions for describing builds of software, and
#. **Packages**: Python modules that describe how to build
   software according to a spec.

Specs allow a user to describe a *particular* build in a way that a
package author can understand.  Packages allow the packager to
encapsulate the build logic for different versions, compilers,
options, platforms, and dependency combinations in one place.
Essentially, a package translates a spec into build logic.

Packages in Spack are written in pure Python, so you can do anything
in Spack that you can do in Python.  Python was chosen as the
implementation language for two reasons.  First, Python is becoming
ubiquitous in the scientific software community. Second, it's a modern
language and has many powerful features to help make package writing
easy.

---------------------------
Creating & editing packages
---------------------------

.. _cmd-spack-create:

^^^^^^^^^^^^^^^^
``spack create``
^^^^^^^^^^^^^^^^

The ``spack create`` command creates a directory with the package name and
generates a ``package.py`` file with a boilerplate package template. If given
a URL pointing to a tarball or other software archive, ``spack create`` is
smart enough to determine basic information about the package, including its name
and build system. In most cases, ``spack create`` plus a few modifications is
all you need to get a package working.

Here's an example:

.. code-block:: console

   $ spack create https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2

Spack examines the tarball URL and tries to figure out the name of the package
to be created. If the name contains uppercase letters, these are automatically
converted to lowercase. If the name contains underscores or periods, these are
automatically converted to dashes.

Spack also searches for *additional* versions located in the same directory of
the website. Spack prompts you to tell you how many versions it found and asks
you how many you would like to download and checksum:

.. code-block:: console

   $ spack create https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
   ==> This looks like a URL for gmp
   ==> Found 16 versions of gmp:

     6.1.2   https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
     6.1.1   https://gmplib.org/download/gmp/gmp-6.1.1.tar.bz2
     6.1.0   https://gmplib.org/download/gmp/gmp-6.1.0.tar.bz2
     ...
     5.0.0   https://gmplib.org/download/gmp/gmp-5.0.0.tar.bz2

   How many would you like to checksum? (default is 1, q to abort)

Spack will automatically download the number of tarballs you specify
(starting with the most recent) and checksum each of them.

You do not *have* to download all of the versions up front. You can
always choose to download just one tarball initially, and run
:ref:`cmd-spack-checksum` later if you need more versions.

Let's say you download 3 tarballs:

.. code-block:: console

	How many would you like to checksum? (default is 1, q to abort) 3
	==> Downloading...
	==> Fetching https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
	######################################################################## 100.0%
	==> Fetching https://gmplib.org/download/gmp/gmp-6.1.1.tar.bz2
	######################################################################## 100.0%
	==> Fetching https://gmplib.org/download/gmp/gmp-6.1.0.tar.bz2
	######################################################################## 100.0%
	==> Checksummed 3 versions of gmp:
	==> This package looks like it uses the autotools build system
	==> Created template for gmp package
	==> Created package file: /Users/Adam/spack/var/spack/repos/builtin/packages/gmp/package.py

Spack automatically creates a directory in the appropriate repository,
generates a boilerplate template for your package, and opens up the new
``package.py`` in your favorite ``$EDITOR``:

.. code-block:: python
   :linenos:

   #
   # This is a template package file for Spack.  We've put "FIXME"
   # next to all the things you'll want to change. Once you've handled
   # them, you can save this file and test your package like this:
   #
   #     spack install gmp
   #
   # You can edit this file again by typing:
   #
   #     spack edit gmp
   #
   # See the Spack documentation for more information on packaging.
   # If you submit this package back to Spack as a pull request,
   # please first remove this boilerplate and all FIXME comments.
   #
   from spack import *


   class Gmp(AutotoolsPackage):
       """FIXME: Put a proper description of your package here."""

       # FIXME: Add a proper url for your package's homepage here.
       homepage = "http://www.example.com"
       url      = "https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2"

       # FIXME: Add a list of GitHub accounts to
       # notify when the package is updated.
       # maintainers = ['github_user1', 'github_user2']

       version('6.1.2', '8ddbb26dc3bd4e2302984debba1406a5')
       version('6.1.1', '4c175f86e11eb32d8bf9872ca3a8e11d')
       version('6.1.0', '86ee6e54ebfc4a90b643a65e402c4048')

       # FIXME: Add dependencies if required.
       # depends_on('foo')

       def configure_args(self):
           # FIXME: Add arguments other than --prefix
           # FIXME: If not needed delete the function
           args = []
           return args

The tedious stuff (creating the class, checksumming archives) has been
done for you. You'll notice that ``spack create`` correctly detected that
``gmp`` uses the Autotools build system. It created a new ``Gmp`` package
that subclasses the ``AutotoolsPackage`` base class. This base class
provides basic installation methods common to all Autotools packages:

.. code-block:: bash

   ./configure --prefix=/path/to/installation/directory

   make
   make check
   make install

For most Autotools packages, this is sufficient. If you need to add
additional arguments to the ``./configure`` call, add them via the
``configure_args`` function.

In the generated package, the download ``url`` attribute is already
set. All the things you still need to change are marked with
``FIXME`` labels. You can delete the commented instructions between
the license and the first import statement after reading them.
The rest of the tasks you need to do are as follows:

#. Add a description.

   Immediately inside the package class is a *docstring* in
   triple-quotes (``"""``).  It is used to generate the description
   shown when users run ``spack info``.

#. Change the ``homepage`` to a useful URL.

   The ``homepage`` is displayed when users run ``spack info`` so
   that they can learn more about your package.

#. Add a comma-separated list of maintainers.

   The ``maintainers`` field is a list of GitHub accounts of people
   who want to be notified any time the package is modified. When a
   pull request is submitted that updates the package, these people
   will be requested to review the PR. This is useful for developers
   who maintain a Spack package for their own software, as well as
   users who rely on a piece of software and want to ensure that the
   package doesn't break. It also gives users a list of people to
   contact for help when someone reports a build error with the package.

#. Add ``depends_on()`` calls for the package's dependencies.

   ``depends_on`` tells Spack that other packages need to be built
   and installed before this one. See :ref:`dependencies`.

#. Get the installation working.

   Your new package may require specific flags during ``configure``.
   These can be added via ``configure_args``. Specifics will differ
   depending on the package and its build system.
   :ref:`Implementing the install method <install-method>` is
   covered in detail later.

Passing a URL to ``spack create`` is a convenient and easy way to get
a basic package template, but what if your software is licensed and
cannot be downloaded from a URL? You can still create a boilerplate
``package.py`` by telling ``spack create`` what name you want to use:

.. code-block:: console

   $ spack create --name intel

This will create a simple ``intel`` package with an ``install()``
method that you can craft to install your package.

What if ``spack create <url>`` guessed the wrong name or build system?
For example, if your package uses the Autotools build system but does
not come with a ``configure`` script, Spack won't realize it uses
Autotools. You can overwrite the old package with ``--force`` and specify
a name with ``--name`` or a build system template to use with ``--template``:

.. code-block:: console

   $ spack create --name gmp https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
   $ spack create --force --template autotools https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2

.. note::

   If you are creating a package that uses the Autotools build system
   but does not come with a ``configure`` script, you'll need to add an
   ``autoreconf`` method to your package that explains how to generate
   the ``configure`` script. You may also need the following dependencies:

   .. code-block:: python

      depends_on('autoconf', type='build')
      depends_on('automake', type='build')
      depends_on('libtool',  type='build')
      depends_on('m4',       type='build')

A complete list of available build system templates can be found by running
``spack create --help``.

.. _cmd-spack-edit:

^^^^^^^^^^^^^^
``spack edit``
^^^^^^^^^^^^^^

One of the easiest ways to learn how to write packages is to look at
existing ones.  You can edit a package file by name with the ``spack
edit`` command:

.. code-block:: console

   $ spack edit gmp

So, if you used ``spack create`` to create a package, then saved and
closed the resulting file, you can get back to it with ``spack edit``.
The ``gmp`` package actually lives in
``$SPACK_ROOT/var/spack/repos/builtin/packages/gmp/package.py``,
but ``spack edit`` provides a much simpler shortcut and saves you the
trouble of typing the full path.

----------------------------
Naming & directory structure
----------------------------

This section describes how packages need to be named, and where they
live in Spack's directory structure.  In general, :ref:`cmd-spack-create`
handles creating package files for you, so you can skip most of the
details here.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``var/spack/repos/builtin/packages``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Spack installation directory is structured like a standard UNIX
install prefix (``bin``, ``lib``, ``include``, ``var``, ``opt``,
etc.).  Most of the code for Spack lives in ``$SPACK_ROOT/lib/spack``.
Packages themselves live in ``$SPACK_ROOT/var/spack/repos/builtin/packages``.

If you ``cd`` to that directory, you will see directories for each
package:

.. command-output:: cd $SPACK_ROOT/var/spack/repos/builtin/packages && ls
   :shell:
   :ellipsis: 10

Each directory contains a file called ``package.py``, which is where
all the python code for the package goes.  For example, the ``libelf``
package lives in:

.. code-block:: none

   $SPACK_ROOT/var/spack/repos/builtin/packages/libelf/package.py

Alongside the ``package.py`` file, a package may contain extra
directories or files (like patches) that it needs to build.

^^^^^^^^^^^^^
Package Names
^^^^^^^^^^^^^

Packages are named after the directory containing ``package.py``. So,
``libelf``'s ``package.py`` lives in a directory called ``libelf``.
The ``package.py`` file defines a class called ``Libelf``, which
extends Spack's ``Package`` class.  For example, here is
``$SPACK_ROOT/var/spack/repos/builtin/packages/libelf/package.py``:

.. code-block:: python
   :linenos:

   from spack import *

   class Libelf(Package):
       """ ... description ... """
       homepage = ...
       url = ...
       version(...)
       depends_on(...)

       def install():
           ...

The **directory name** (``libelf``) determines the package name that
users should provide on the command line. e.g., if you type any of
these:

.. code-block:: console

   $ spack info libelf
   $ spack versions libelf
   $ spack install libelf@0.8.13

Spack sees the package name in the spec and looks for
``libelf/package.py`` in ``var/spack/repos/builtin/packages``.
Likewise, if you run ``spack install py-numpy``, Spack looks for
``py-numpy/package.py``.

Spack uses the directory name as the package name in order to give
packagers more freedom in naming their packages. Package names can
contain letters, numbers, and dashes. Using a Python identifier
(e.g., a class name or a module name) would make it difficult to
support these options.  So, you can name a package ``3proxy`` or
``foo-bar`` and Spack won't care. It just needs to see that name
in the packages directory.

^^^^^^^^^^^^^^^^^^^
Package class names
^^^^^^^^^^^^^^^^^^^

Spack loads ``package.py`` files dynamically, and it needs to find a
special class name in the file for the load to succeed.  The **class
name** (``Libelf`` in our example) is formed by converting words
separated by ``-`` in the file name to CamelCase. If the name
starts with a number, we prefix the class name with ``_``. Here are
some examples:

=================  =================
 Module Name         Class Name
=================  =================
 ``foo-bar``         ``FooBar``
 ``3proxy``          ``_3proxy``
=================  =================

In general, you won't have to remember this naming convention because
:ref:`cmd-spack-create` and :ref:`cmd-spack-edit` handle the details for you.

-----------------
Trusted Downloads
-----------------

Spack verifies that the source code it downloads is not corrupted or
compromised; or at least, that it is the same version the author of
the Spack package saw when the package was created.  If Spack uses a
download method it can verify, we say the download method is
*trusted*.  Trust is important for *all downloads*: Spack
has no control over the security of the various sites from which it
downloads source code, and can never assume that any particular site
hasn't been compromised.

Trust is established in different ways for different download methods.
For the most common download method --- a single-file tarball --- the
tarball is checksummed.  Git downloads using ``commit=`` are trusted
implicitly, as long as a hash is specified.

Spack also provides untrusted download methods: tarball URLs may be
supplied without a checksum, or Git downloads may specify a branch or
tag instead of a hash.  If the user does not control or trust the
source of an untrusted download, it is a security risk.  Unless otherwise
specified by the user for special cases, Spack should by default use
*only* trusted download methods.

Unfortunately, Spack does not currently provide that guarantee.  It
does provide the following mechanisms for safety:

#. By default, Spack will only install a tarball package if it has a
   checksum and that checksum matches.  You can override this with
   ``spack install --no-checksum``.

#. Numeric versions are almost always tarball downloads, whereas
   non-numeric versions not named ``develop`` frequently download
   untrusted branches or tags from a version control system.  As long
   as a package has at least one numeric version, and no non-numeric
   version named ``develop``, Spack will prefer it over any
   non-numeric versions.

^^^^^^^^^
Checksums
^^^^^^^^^

For tarball downloads, Spack can currently support checksums using the
MD5, SHA-1, SHA-224, SHA-256, SHA-384, and SHA-512 algorithms.  It
determines the algorithm to use based on the hash length.

.. _versions-and-fetching:

---------------------
Versions and fetching
---------------------

The most straightforward way to add new versions to your package is to
add a line like this in the package class:

.. code-block:: python

   class Foo(Package):

       url = "http://example.com/foo-1.0.tar.gz"

       version('8.2.1', '4136d7b4c04df68b686570afa26988ac')
       version('8.2.0', '1c9f62f0778697a09d36121ead88e08e')
       version('8.1.2', 'd47dd09ed7ae6e7fd6f9a816d7f5fdf6')

Versions should be listed in descending order, from newest to oldest.

^^^^^^^^^^^^^
Date Versions
^^^^^^^^^^^^^

If you wish to use dates as versions, it is best to use the format
``@yyyy-mm-dd``.  This will ensure they sort in the correct order.

Alternately, you might use a hybrid release-version / date scheme.
For example, ``@1.3_2016-08-31`` would mean the version from the
``1.3`` branch, as of August 31, 2016.

^^^^^^^^^^^^
Version URLs
^^^^^^^^^^^^

By default, each version's URL is extrapolated from the ``url`` field
in the package.  For example, Spack is smart enough to download
version ``8.2.1`` of the ``Foo`` package above from
http://example.com/foo-8.2.1.tar.gz.

If the URL is particularly complicated or changes based on the release,
you can override the default URL generation algorithm by defining your
own ``url_for_version()`` function. For example, the download URL for
OpenMPI contains the major.minor version in one spot and the
major.minor.patch version in another:

https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.1.tar.bz2

In order to handle this, you can define a ``url_for_version()`` function
like so:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/openmpi/package.py
   :pyobject: Openmpi.url_for_version

With the use of this ``url_for_version()``, Spack knows to download OpenMPI ``2.1.1``
from http://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.1.tar.bz2
but download OpenMPI ``1.10.7`` from http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.7.tar.bz2.

You'll notice that OpenMPI's ``url_for_version()`` function makes use of a special
``Version`` function called ``up_to()``. When you call ``version.up_to(2)`` on a
version like ``1.10.0``, it returns ``1.10``. ``version.up_to(1)`` would return
``1``. This can be very useful for packages that place all ``X.Y.*`` versions in
a single directory and then places all ``X.Y.Z`` versions in a sub-directory.

There are a few ``Version`` properties you should be aware of. We generally
prefer numeric versions to be separated by dots for uniformity, but not all
tarballs are named that way. For example, ``icu4c`` separates its major and minor
versions with underscores, like ``icu4c-57_1-src.tgz``. The value ``57_1`` can be
obtained with the use of the ``version.underscored`` property. Note that Python
properties don't need parentheses. There are other separator properties as well:

===================  ======
Property             Result
===================  ======
version.dotted       1.2.3
version.dashed       1-2-3
version.underscored  1_2_3
version.joined       123
===================  ======

.. note::

   Python properties don't need parentheses. ``version.dashed`` is correct.
   ``version.dashed()`` is incorrect.

In addition, these version properties can be combined with ``up_to()``.
For example:

.. code-block:: python

   >>> version = Version('1.2.3')
   >>> version.up_to(2).dashed
   Version('1-2')
   >>> version.underscored.up_to(2)
   Version('1_2')


As you can see, order is not important. Just keep in mind that ``up_to()`` and
the other version properties return ``Version`` objects, not strings.

If a URL cannot be derived systematically, or there is a special URL for one
of its versions, you can add an explicit URL for a particular version:

.. code-block:: python

   version('8.2.1', '4136d7b4c04df68b686570afa26988ac',
           url='http://example.com/foo-8.2.1-special-version.tar.gz')


When you supply a custom URL for a version, Spack uses that URL
*verbatim* and does not perform extrapolation. The order of precedence
of these methods is:

#. package-level ``url``
#. ``url_for_version()``
#. version-specific ``url``

so if your package contains a ``url_for_version()``, it can be overridden
by a version-specific ``url``.

If your package does not contain a package-level ``url`` or ``url_for_version()``,
Spack can determine which URL to download from even if only some of the versions
specify their own ``url``. Spack will use the nearest URL *before* the requested
version. This is useful for packages that have an easy to extrapolate URL, but
keep changing their URL format every few releases. With this method, you only
need to specify the ``url`` when the URL changes.

"""""""""""""""""""""""
Mirrors of the main URL
"""""""""""""""""""""""

Spack supports listing mirrors of the main URL in a package by defining
the ``urls`` attribute:

.. code-block:: python

  class Foo(Package):

    urls = [
        'http://example.com/foo-1.0.tar.gz',
        'http://mirror.com/foo-1.0.tar.gz'
    ]

instead of just a single ``url``. This attribute is a list of possible URLs that
will be tried in order when fetching packages. Notice that either one of ``url``
or ``urls`` can be present in a package, but not both at the same time.

A well-known case of packages that can be fetched from multiple mirrors is that
of GNU. For that, Spack goes a step further and defines a mixin class that
takes care of all of the plumbing and requires packagers to just define a proper
``gnu_mirror_path`` attribute:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/autoconf/package.py
   :lines: 9-18

^^^^^^^^^^^^^^^^^^^^^^^^
Skipping the expand step
^^^^^^^^^^^^^^^^^^^^^^^^

Spack normally expands archives (e.g. ``*.tar.gz`` and ``*.zip``) automatically
into a standard stage source directory (``self.stage.source_path``) after
downloading them. If you want to skip this step (e.g., for self-extracting
executables and other custom archive types), you can add ``expand=False`` to a
``version`` directive.

.. code-block:: python

   version('8.2.1', '4136d7b4c04df68b686570afa26988ac',
           url='http://example.com/foo-8.2.1-special-version.sh', expand=False)

When ``expand`` is set to ``False``, Spack sets the current working
directory to the directory containing the downloaded archive before it
calls your ``install`` method.  Within ``install``, the path to the
downloaded archive is available as ``self.stage.archive_file``.

Here is an example snippet for packages distributed as self-extracting
archives.  The example sets permissions on the downloaded file to make
it executable, then runs it with some arguments.

.. code-block:: python

   def install(self, spec, prefix):
       set_executable(self.stage.archive_file)
       installer = Executable(self.stage.archive_file)
       installer('--prefix=%s' % prefix, 'arg1', 'arg2', 'etc.')


^^^^^^^^^^^^^^^^^^^^^^^^
Deprecating old versions
^^^^^^^^^^^^^^^^^^^^^^^^

There are many reasons to remove old versions of software:

#. Security vulnerabilities (most serious reason)
#. Changing build systems that increase package complexity
#. Changing dependencies/patches/resources/flags that increase package complexity
#. Maintainer/developer inability/unwillingness to support old versions
#. No longer available for download (right to be forgotten)
#. Package or version rename

At the same time, there are many reasons to keep old versions of software:

#. Reproducibility
#. Requirements for older packages (e.g. some packages still rely on Qt 3)

In general, you should not remove old versions from a ``package.py``. Instead,
you should first deprecate them using the following syntax:

.. code-block:: python

   version('1.2.3', sha256='...', deprecated=True)


This has two effects. First, ``spack info`` will no longer advertise that
version. Second, commands like ``spack install`` that fetch the package will
require user approval:

.. code-block:: console

   $ spack install openssl@1.0.1e
   ==> Warning: openssl@1.0.1e is deprecated and may be removed in a future Spack release.
   ==>   Fetch anyway? [y/N]


If you use ``spack install --deprecated``, this check can be skipped.

This also applies to package recipes that are renamed or removed. You should
first deprecate all versions before removing a package. If you need to rename
it, you can deprecate the old package and create a new package at the same
time.

Version deprecations should always last at least one Spack minor release cycle
before the version is completely removed. For example, if a version is
deprecated in Spack 0.16.0, it should not be removed until Spack 0.17.0. No
version should be removed without such a deprecation process. This gives users
a chance to complain about the deprecation in case the old version is needed
for some application. If you require a deprecated version of a package, simply
submit a PR to remove ``deprecated=True`` from the package. However, you may be
asked to help maintain this version of the package if the current maintainers
are unwilling to support this older version.


^^^^^^^^^^^^^^^^
Download caching
^^^^^^^^^^^^^^^^

Spack maintains a cache (described :ref:`here <caching>`) which saves files
retrieved during package installations to avoid re-downloading in the case that
a package is installed with a different specification (but the same version) or
reinstalled on account of a change in the hashing scheme. It may (rarely) be
necessary to avoid caching for a particular version by adding ``no_cache=True``
as an option to the ``version()`` directive. Example situations would be a
"snapshot"-like Version Control System (VCS) tag, a VCS branch such as
``v6-16-00-patches``, or a URL specifying a regularly updated snapshot tarball.

^^^^^^^^^^^^^^^^^^
Version comparison
^^^^^^^^^^^^^^^^^^

Most Spack versions are numeric, a tuple of integers; for example,
``apex@0.1``, ``ferret@6.96`` or ``py-netcdf@1.2.3.1``.  Spack knows
how to compare and sort numeric versions.

Some Spack versions involve slight extensions of numeric syntax; for
example, ``py-sphinx-rtd-theme@0.1.10a0``.  In this case, numbers are
always considered to be "newer" than letters.  This is for consistency
with `RPM <https://bugzilla.redhat.com/show_bug.cgi?id=50977>`_.

Spack versions may also be arbitrary non-numeric strings; any string
here will suffice; for example, ``@develop``, ``@master``, ``@local``.
Versions are compared as follows. First, a version string is split into
multiple fields based on delimiters such as ``.``, ``-`` etc. Then
matching fields are compared using the rules below:

#. The following develop-like strings are greater (newer) than all
   numbers and are ordered as ``develop > main > master > head > trunk``.

#. Numbers are all less than the chosen develop-like strings above,
   and are sorted numerically.

#. All other non-numeric versions are less than numeric versions, and
   are sorted alphabetically.

The logic behind this sort order is two-fold:

#. Non-numeric versions are usually used for special cases while
   developing or debugging a piece of software.  Keeping most of them
   less than numeric versions ensures that Spack chooses numeric
   versions by default whenever possible.

#. The most-recent development version of a package will usually be
   newer than any released numeric versions.  This allows the
   ``@develop`` version to satisfy dependencies like ``depends_on(abc,
   when="@x.y.z:")``

^^^^^^^^^^^^^^^^^
Version selection
^^^^^^^^^^^^^^^^^

When concretizing, many versions might match a user-supplied spec.
For example, the spec ``python`` matches all available versions of the
package ``python``.  Similarly, ``python@3:`` matches all versions of
Python3.  Given a set of versions that match a spec, Spack
concretization uses the following priorities to decide which one to
use:

#. If the user provided a list of versions in ``packages.yaml``, the
   first matching version in that list will be used.

#. If one or more versions is specified as ``preferred=True``, in
   either ``packages.yaml`` or ``package.py``, the largest matching
   version will be used.  ("Latest" is defined by the sort order
   above).

#. If no preferences in particular are specified in the package or in
   ``packages.yaml``, then the largest matching non-develop version
   will be used.  By avoiding ``@develop``, this prevents users from
   accidentally installing a ``@develop`` version.

#. If all else fails and ``@develop`` is the only matching version, it
   will be used.


.. _cmd-spack-checksum:

^^^^^^^^^^^^^^^^^^
``spack checksum``
^^^^^^^^^^^^^^^^^^

If you want to add new versions to a package you've already created,
this is automated with the ``spack checksum`` command.  Here's an
example for ``libelf``:

.. code-block:: console

   $ spack checksum libelf
   ==> Found 16 versions of libelf.
     0.8.13    http://www.mr511.de/software/libelf-0.8.13.tar.gz
     0.8.12    http://www.mr511.de/software/libelf-0.8.12.tar.gz
     0.8.11    http://www.mr511.de/software/libelf-0.8.11.tar.gz
     0.8.10    http://www.mr511.de/software/libelf-0.8.10.tar.gz
     0.8.9     http://www.mr511.de/software/libelf-0.8.9.tar.gz
     0.8.8     http://www.mr511.de/software/libelf-0.8.8.tar.gz
     0.8.7     http://www.mr511.de/software/libelf-0.8.7.tar.gz
     0.8.6     http://www.mr511.de/software/libelf-0.8.6.tar.gz
     0.8.5     http://www.mr511.de/software/libelf-0.8.5.tar.gz
     ...
     0.5.2     http://www.mr511.de/software/libelf-0.5.2.tar.gz

   How many would you like to checksum? (default is 1, q to abort)

This does the same thing that ``spack create`` does, but it allows you
to go back and add new versions easily as you need them (e.g., as
they're released).  It fetches the tarballs you ask for and prints out
a list of ``version`` commands ready to copy/paste into your package
file:

.. code-block:: console

   ==> Checksummed new versions of libelf:
       version('0.8.13', '4136d7b4c04df68b686570afa26988ac')
       version('0.8.12', 'e21f8273d9f5f6d43a59878dc274fec7')
       version('0.8.11', 'e931910b6d100f6caa32239849947fbf')
       version('0.8.10', '9db4d36c283d9790d8fa7df1f4d7b4d9')

By default, Spack will search for new tarball downloads by scraping
the parent directory of the tarball you gave it.  So, if your tarball
is at ``http://example.com/downloads/foo-1.0.tar.gz``, Spack will look
in ``http://example.com/downloads/`` for links to additional versions.
If you need to search another path for download links, you can supply
some extra attributes that control how your package finds new
versions. See the documentation on :ref:`attribute_list_url` and
:ref:`attribute_list_depth`.

.. note::

  * This command assumes that Spack can extrapolate new URLs from an
    existing URL in the package, and that Spack can find similar URLs
    on a webpage.  If that's not possible, e.g. if the package's
    developers don't name their tarballs consistently, you'll need to
    manually add ``version`` calls yourself.

  * For ``spack checksum`` to work, Spack needs to be able to
    ``import`` your package in Python.  That means it can't have any
    syntax errors, or the ``import`` will fail.  Use this once you've
    got your package in working order.

--------------------
Finding new versions
--------------------

You've already seen the ``homepage`` and ``url`` package attributes:

.. code-block:: python
   :linenos:

   from spack import *


   class Mpich(Package):
      """MPICH is a high performance and widely portable implementation of
         the Message Passing Interface (MPI) standard."""
      homepage = "http://www.mpich.org"
      url      = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"

These are class-level attributes used by Spack to show users
information about the package, and to determine where to download its
source code.

Spack uses the tarball URL to extrapolate where to find other tarballs
of the same package (e.g. in :ref:`cmd-spack-checksum`, but
this does not always work.  This section covers ways you can tell
Spack to find tarballs elsewhere.

.. _attribute_list_url:

^^^^^^^^^^^^
``list_url``
^^^^^^^^^^^^

When spack tries to find available versions of packages (e.g. with
:ref:`cmd-spack-checksum`), it spiders the parent directory
of the tarball in the ``url`` attribute.  For example, for libelf, the
url is:

.. code-block:: python

   url = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"

Here, Spack spiders ``http://www.mr511.de/software/`` to find similar
tarball links and ultimately to make a list of available versions of
``libelf``.

For many packages, the tarball's parent directory may be unlistable,
or it may not contain any links to source code archives.  In fact,
many times additional package downloads aren't even available in the
same directory as the download URL.

For these, you can specify a separate ``list_url`` indicating the page
to search for tarballs.  For example, ``libdwarf`` has the homepage as
the ``list_url``, because that is where links to old versions are:

.. code-block:: python
   :linenos:

   class Libdwarf(Package):
       homepage = "http://www.prevanders.net/dwarf.html"
       url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
       list_url = homepage

.. _attribute_list_depth:

^^^^^^^^^^^^^^
``list_depth``
^^^^^^^^^^^^^^

``libdwarf`` and many other packages have a listing of available
versions on a single webpage, but not all do.  For example, ``mpich``
has a tarball URL that looks like this:

.. code-block:: python

   url = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"

But its downloads are in many different subdirectories of
``http://www.mpich.org/static/downloads/``.  So, we need to add a
``list_url`` *and* a ``list_depth`` attribute:

.. code-block:: python
   :linenos:

   class Mpich(Package):
       homepage   = "http://www.mpich.org"
       url        = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
       list_url   = "http://www.mpich.org/static/downloads/"
       list_depth = 1

By default, Spack only looks at the top-level page available at
``list_url``.  ``list_depth = 1`` tells it to follow up to 1 level of
links from the top-level page.  Note that here, this implies 1
level of subdirectories, as the ``mpich`` website is structured much
like a filesystem.  But ``list_depth`` really refers to link depth
when spidering the page.

.. _vcs-fetch:

-------------------------------
Fetching from code repositories
-------------------------------

For some packages, source code is provided in a Version Control System
(VCS) repository rather than in a tarball.  Spack can fetch packages
from VCS repositories. Currently, Spack supports fetching with `Git
<git-fetch_>`_, `Mercurial (hg) <hg-fetch_>`_, `Subversion (svn)
<svn-fetch_>`_, and `Go <go-fetch_>`_.  In all cases, the destination
is the standard stage source path.

To fetch a package from a source repository, Spack needs to know which
VCS to use and where to download from. Much like with ``url``, package
authors can specify a class-level ``git``, ``hg``, ``svn``, or ``go``
attribute containing the correct download location.

Many packages developed with Git have both a Git repository as well as
release tarballs available for download. Packages can define both a
class-level tarball URL and VCS. For example:

.. code-block:: python

   class Trilinos(CMakePackage):

       homepage = "https://trilinos.org/"
       url      = "https://github.com/trilinos/Trilinos/archive/trilinos-release-12-12-1.tar.gz"
       git      = "https://github.com/trilinos/Trilinos.git"

       version('develop', branch='develop')
       version('master',  branch='master')
       version('12.12.1', 'ecd4606fa332212433c98bf950a69cc7')
       version('12.10.1', '667333dbd7c0f031d47d7c5511fd0810')
       version('12.8.1',  '9f37f683ee2b427b5540db8a20ed6b15')

If a package contains both a ``url`` and ``git`` class-level attribute,
Spack decides which to use based on the arguments to the ``version()``
directive. Versions containing a specific branch, tag, or revision are
assumed to be for VCS download methods, while versions containing a
checksum are assumed to be for URL download methods.

Like ``url``, if a specific version downloads from a different repository
than the default repo, it can be overridden with a version-specific argument.

.. note::

   In order to reduce ambiguity, each package can only have a single VCS
   top-level attribute in addition to ``url``. In the rare case that a
   package uses multiple VCS, a fetch strategy can be specified for each
   version. For example, the ``rockstar`` package contains:

   .. code-block:: python

      class Rockstar(MakefilePackage):

          homepage = "https://bitbucket.org/gfcstanford/rockstar"

          version('develop', git='https://bitbucket.org/gfcstanford/rockstar.git')
          version('yt', hg='https://bitbucket.org/MatthewTurk/rockstar')


.. _git-fetch:

^^^
Git
^^^

Git fetching supports the following parameters to ``version``:

* ``git``: URL of the git repository, if different than the class-level ``git``.
* ``branch``: Name of a branch to fetch.
* ``tag``: Name of a tag to fetch.
* ``commit``: SHA hash (or prefix) of a commit to fetch.
* ``submodules``: Also fetch submodules recursively when checking out this repository.
* ``submodules_delete``: A list of submodules to forcibly delete from the repository
  after fetching. Useful if a version in the repository has submodules that
  have disappeared/are no longer accessible.
* ``get_full_repo``: Ensure the full git history is checked out with all remote
  branch information. Normally (``get_full_repo=False``, the default), the git
  option ``--depth 1`` will be used if the version of git and the specified
  transport protocol support it, and ``--single-branch`` will be used if the
  version of git supports it.

Only one of ``tag``, ``branch``, or ``commit`` can be used at a time.

The destination directory for the clone is the standard stage source path.

Default branch
  To fetch a repository's default branch:

  .. code-block:: python

     class Example(Package):

         git = "https://github.com/example-project/example.git"

         version('develop')

  This download method is untrusted, and is not recommended. Aside from HTTPS,
  there is no way to verify that the repository has not been compromised, and
  the commit you get when you install the package likely won't be the same
  commit that was used when the package was first written. Additionally, the
  default branch may change. It is best to at least specify a branch name.

Branches
  To fetch a particular branch, use the ``branch`` parameter:

  .. code-block:: python

     version('experimental', branch='experimental')

  This download method is untrusted, and is not recommended. Branches are
  moving targets, so the commit you get when you install the package likely
  won't be the same commit that was used when the package was first written.

Tags
  To fetch from a particular tag, use ``tag`` instead:

  .. code-block:: python

     version('1.0.1', tag='v1.0.1')

  This download method is untrusted, and is not recommended. Although tags
  are generally more stable than branches, Git allows tags to be moved.
  Many developers use tags to denote rolling releases, and may move the
  tag when a bug is patched.

Commits
  Finally, to fetch a particular commit, use ``commit``:

  .. code-block:: python

     version('2014-10-08', commit='9d38cd4e2c94c3cea97d0e2924814acc')

  This doesn't have to be a full hash; you can abbreviate it as you'd
  expect with git:

  .. code-block:: python

     version('2014-10-08', commit='9d38cd')

  This download method *is trusted*.  It is the recommended way to
  securely download from a Git repository.

  It may be useful to provide a saner version for commits like this,
  e.g. you might use the date as the version, as done above. Or, if you
  know the commit at which a release was cut, you can use the release
  version. It's up to the package author to decide what makes the most
  sense. Although you can use the commit hash as the version number,
  this is not recommended, as it won't sort properly.

Submodules
  You can supply ``submodules=True`` to cause Spack to fetch submodules
  recursively along with the repository at fetch time. For more information
  about git submodules see the manpage of git: ``man git-submodule``.

  .. code-block:: python

     version('1.0.1', tag='v1.0.1', submodules=True)


.. _github-fetch:

^^^^^^
GitHub
^^^^^^

If a project is hosted on GitHub, *any* valid Git branch, tag, or hash
may be downloaded as a tarball.  This is accomplished simply by
constructing an appropriate URL.  Spack can checksum any package
downloaded this way, thereby producing a trusted download.  For
example, the following downloads a particular hash, and then applies a
checksum.

.. code-block:: python

       version('1.9.5.1.1', 'd035e4bc704d136db79b43ab371b27d2',
               url='https://www.github.com/jswhit/pyproj/tarball/0be612cc9f972e38b50a90c946a9b353e2ab140f')

.. _hg-fetch:

^^^^^^^^^
Mercurial
^^^^^^^^^

Fetching with Mercurial works much like `Git <git-fetch>`_, but you
use the ``hg`` parameter.
The destination directory is still the standard stage source path.

Default branch
  Add the ``hg`` attribute with no ``revision`` passed to ``version``:

  .. code-block:: python

     class Example(Package):

         hg = "https://bitbucket.org/example-project/example"

         version('develop')

  This download method is untrusted, and is not recommended. As with
  Git's default fetching strategy, there is no way to verify the
  integrity of the download.

Revisions
  To fetch a particular revision, use the ``revision`` parameter:

  .. code-block:: python

     version('1.0', revision='v1.0')

  Unlike ``git``, which has special parameters for different types of
  revisions, you can use ``revision`` for branches, tags, and commits
  when you fetch with Mercurial. Like Git, fetching specific branches
  or tags is an untrusted download method, and is not recommended.
  The recommended fetch strategy is to specify a particular commit
  hash as the revision.


.. _svn-fetch:

^^^^^^^^^^
Subversion
^^^^^^^^^^

To fetch with subversion, use the ``svn`` and ``revision`` parameters.
The destination directory will be the standard stage source path.

Fetching the head
  Simply add an ``svn`` parameter to the package:

  .. code-block:: python

     class Example(Package):

         svn = "https://outreach.scidac.gov/svn/example/trunk"

         version('develop')

  This download method is untrusted, and is not recommended for the
  same reasons as mentioned above.

Fetching a revision
  To fetch a particular revision, add a ``revision`` argument to the
  version directive:

  .. code-block:: python

     version('develop', revision=128)

  This download method is untrusted, and is not recommended.

  Unfortunately, Subversion has no commit hashing scheme like Git and
  Mercurial do, so there is no way to guarantee that the download you
  get is the same as the download used when the package was created.
  Use at your own risk.

Subversion branches are handled as part of the directory structure, so
you can check out a branch or tag by changing the URL. If you want to
package multiple branches, simply add a ``svn`` argument to each
version directive.

.. _go-fetch:

^^
Go
^^

Go isn't a VCS, it is a programming language with a builtin command,
`go get <https://golang.org/cmd/go/#hdr-Download_and_install_packages_and_dependencies>`_,
that fetches packages and their dependencies automatically.
The destination directory will be the standard stage source path.

This strategy can clone a Git repository, or download from another source location.
For example:

.. code-block:: python

   class ThePlatinumSearcher(Package):

       homepage = "https://github.com/monochromegane/the_platinum_searcher"
       go       = "github.com/monochromegane/the_platinum_searcher/..."

       version('head')

Go cannot be used to fetch a particular commit or branch, it always
downloads the head of the repository. This download method is untrusted,
and is not recommended. Use another fetch strategy whenever possible.

--------
Variants
--------

Many software packages can be configured to enable optional
features, which often come at the expense of additional dependencies or
longer build-times. To be flexible enough and support a wide variety of
use cases, Spack permits to expose to the end-user the ability to choose
which features should be activated in a package at the time it is installed.
The mechanism to be employed is the :py:func:`spack.directives.variant` directive.

^^^^^^^^^^^^^^^^
Boolean variants
^^^^^^^^^^^^^^^^

In their simplest form variants are boolean options specified at the package
level:

  .. code-block:: python

    class Hdf5(AutotoolsPackage):
        ...
        variant(
            'shared', default=True, description='Builds a shared version of the library'
        )

with a default value and a description of their meaning / use in the package.
*Variants can be tested in any context where a spec constraint is expected.*
In the example above the ``shared`` variant is tied to the build of shared dynamic
libraries. To pass the right option at configure time we can branch depending on
its value:

  .. code-block:: python

    def configure_args(self):
        ...
        if '+shared' in self.spec:
            extra_args.append('--enable-shared')
        else:
            extra_args.append('--disable-shared')
            extra_args.append('--enable-static-exec')

As explained in :ref:`basic-variants` the constraint ``+shared`` means
that the boolean variant is set to ``True``, while ``~shared`` means it is set
to ``False``.
Another common example is the optional activation of an extra dependency
which requires to use the variant in the ``when`` argument of
:py:func:`spack.directives.depends_on`:

  ..  code-block:: python

    class Hdf5(AutotoolsPackage):
        ...
        variant('szip', default=False, description='Enable szip support')
        depends_on('szip', when='+szip')

as shown in the snippet above where ``szip`` is modeled to be an optional
dependency of ``hdf5``.

^^^^^^^^^^^^^^^^^^^^^
Multi-valued variants
^^^^^^^^^^^^^^^^^^^^^

If need be, Spack can go beyond Boolean variants and permit an arbitrary
number of allowed values. This might be useful when modeling
options that are tightly related to each other.
The values in this case are passed to the :py:func:`spack.directives.variant`
directive as a tuple:

  .. code-block:: python

    class Blis(Package):
        ...
        variant(
            'threads', default='none', description='Multithreading support',
            values=('pthreads', 'openmp', 'none'), multi=False
        )

In the example above the argument ``multi`` is set to ``False`` to indicate
that only one among all the variant values can be active at any time. This
constraint is enforced by the parser and an error is emitted if a user
specifies two or more values at the same time:

  .. code-block:: console

    $ spack spec blis threads=openmp,pthreads
    Input spec
    --------------------------------
    blis threads=openmp,pthreads

    Concretized
    --------------------------------
    ==> Error: multiple values are not allowed for variant "threads"

Another useful note is that *Python's* ``None`` *is not allowed as a default value*
and therefore it should not be used to denote that no feature was selected.
Users should instead select another value, like ``'none'``, and handle it explicitly
within the package recipe if need be:

  .. code-block:: python

      if self.spec.variants['threads'].value == 'none':
         options.append('--no-threads')

In cases where multiple values can be selected at the same time ``multi`` should
be set to ``True``:

  .. code-block:: python

    class Gcc(AutotoolsPackage):
        ...
        variant(
            'languages', default='c,c++,fortran',
            values=('ada', 'brig', 'c', 'c++', 'fortran',
                    'go', 'java', 'jit', 'lto', 'objc', 'obj-c++'),
            multi=True,
            description='Compilers and runtime libraries to build'
        )

Within a package recipe a multi-valued variant is tested using a ``key=value`` syntax:

  .. code-block:: python

    if 'languages=jit' in spec:
        options.append('--enable-host-shared')

"""""""""""""""""""""""""""""""""""""""""""
Complex validation logic for variant values
"""""""""""""""""""""""""""""""""""""""""""
To cover complex use cases, the :py:func:`spack.directives.variant` directive
could accept as the ``values`` argument a full-fledged object which has
``default`` and other arguments of the directive embedded as attributes.

An example, already implemented in Spack's core, is :py:class:`spack.variant.DisjointSetsOfValues`.
This class is used to implement a few convenience functions, like
:py:func:`spack.variant.any_combination_of`:

  ..  code-block:: python

    class Adios(AutotoolsPackage):
        ...
        variant(
            'staging',
            values=any_combination_of('flexpath', 'dataspaces'),
            description='Enable dataspaces and/or flexpath staging transports'
        )

that allows any combination of the specified values, and also allows the
user to specify ``'none'`` (as a string) to choose none of them.
The objects returned by these functions can be modified at will by chaining
method calls to change the default value, customize the error message or
other similar operations:

  .. code-block:: python

    class Mvapich2(AutotoolsPackage):
        ...
        variant(
            'process_managers',
            description='List of the process managers to activate',
            values=disjoint_sets(
                ('auto',), ('slurm',), ('hydra', 'gforker', 'remshell')
            ).prohibit_empty_set().with_error(
                "'slurm' or 'auto' cannot be activated along with "
                "other process managers"
            ).with_default('auto').with_non_feature_values('auto'),
        )

------------------------------------
Resources (expanding extra tarballs)
------------------------------------

Some packages (most notably compilers) provide optional features if additional
resources are expanded within their source tree before building. In Spack it is
possible to describe such a need with the ``resource`` directive :

  .. code-block:: python

     resource(
        name='cargo',
        git='https://github.com/rust-lang/cargo.git',
        tag='0.10.0',
        destination='cargo'
     )

Based on the keywords present among the arguments the appropriate ``FetchStrategy``
will be used for the resource. The keyword ``destination`` is relative to the source
root of the package and should point to where the resource is to be expanded.

.. _license:

-----------------
Licensed software
-----------------

In order to install licensed software, Spack needs to know a few more
details about a package. The following class attributes should be defined.

^^^^^^^^^^^^^^^^^^^^
``license_required``
^^^^^^^^^^^^^^^^^^^^

Boolean. If set to ``True``, this software requires a license. If set to
``False``, all of the following attributes will be ignored. Defaults to
``False``.

^^^^^^^^^^^^^^^^^^^
``license_comment``
^^^^^^^^^^^^^^^^^^^

String. Contains the symbol used by the license manager to denote a comment.
Defaults to ``#``.

^^^^^^^^^^^^^^^^^
``license_files``
^^^^^^^^^^^^^^^^^

List of strings. These are files that the software searches for when
looking for a license. All file paths must be relative to the installation
directory. More complex packages like Intel may require multiple
licenses for individual components. Defaults to the empty list.

^^^^^^^^^^^^^^^^
``license_vars``
^^^^^^^^^^^^^^^^

List of strings. Environment variables that can be set to tell the software
where to look for a license if it is not in the usual location. Defaults
to the empty list.

^^^^^^^^^^^^^^^
``license_url``
^^^^^^^^^^^^^^^

String. A URL pointing to license setup instructions for the software.
Defaults to the empty string.

For example, let's take a look at the package for the PGI compilers.

.. code-block:: python

   # Licensing
   license_required = True
   license_comment  = '#'
   license_files    = ['license.dat']
   license_vars     = ['PGROUPD_LICENSE_FILE', 'LM_LICENSE_FILE']
   license_url      = 'http://www.pgroup.com/doc/pgiinstall.pdf'

As you can see, PGI requires a license. Its license manager, FlexNet, uses
the ``#`` symbol to denote a comment. It expects the license file to be
named ``license.dat`` and to be located directly in the installation prefix.
If you would like the installation file to be located elsewhere, simply set
``PGROUPD_LICENSE_FILE`` or ``LM_LICENSE_FILE`` after installation. For
further instructions on installation and licensing, see the URL provided.

Let's walk through a sample PGI installation to see exactly what Spack is
and isn't capable of. Since PGI does not provide a download URL, it must
be downloaded manually. It can either be added to a mirror or located in
the current directory when ``spack install pgi`` is run. See :ref:`mirrors`
for instructions on setting up a mirror.

After running ``spack install pgi``, the first thing that will happen is
Spack will create a global license file located at
``$SPACK_ROOT/etc/spack/licenses/pgi/license.dat``. It will then open up the
file using the editor set in ``$EDITOR``, or vi if unset. It will look like
this:

.. code-block:: sh

   # A license is required to use pgi.
   #
   # The recommended solution is to store your license key in this global
   # license file. After installation, the following symlink(s) will be
   # added to point to this file (relative to the installation prefix):
   #
   #   license.dat
   #
   # Alternatively, use one of the following environment variable(s):
   #
   #   PGROUPD_LICENSE_FILE
   #   LM_LICENSE_FILE
   #
   # If you choose to store your license in a non-standard location, you may
   # set one of these variable(s) to the full pathname to the license file, or
   # port@host if you store your license keys on a dedicated license server.
   # You will likely want to set this variable in a module file so that it
   # gets loaded every time someone tries to use pgi.
   #
   # For further information on how to acquire a license, please refer to:
   #
   #   http://www.pgroup.com/doc/pgiinstall.pdf
   #
   # You may enter your license below.

You can add your license directly to this file, or tell FlexNet to use a
license stored on a separate license server. Here is an example that
points to a license server called licman1:

.. code-block:: none

   SERVER licman1.mcs.anl.gov 00163eb7fba5 27200
   USE_SERVER

If your package requires the license to install, you can reference the
location of this global license using ``self.global_license_file``.
After installation, symlinks for all of the files given in
``license_files`` will be created, pointing to this global license.
If you install a different version or variant of the package, Spack
will automatically detect and reuse the already existing global license.

If the software you are trying to package doesn't rely on license files,
Spack will print a warning message, letting the user know that they
need to set an environment variable or pointing them to installation
documentation.

.. _patching:

-------
Patches
-------

Depending on the host architecture, package version, known bugs, or
other issues, you may need to patch your software to get it to build
correctly.  Like many other package systems, spack allows you to store
patches alongside your package files and apply them to source code
after it's downloaded.

^^^^^^^^^
``patch``
^^^^^^^^^

You can specify patches in your package file with the ``patch()``
directive.  ``patch`` looks like this:

.. code-block:: python

   class Mvapich2(Package):
       ...
       patch('ad_lustre_rwcontig_open_source.patch', when='@1.9:')

The first argument can be either a URL or a filename.  It specifies a
patch file that should be applied to your source.  If the patch you
supply is a filename, then the patch needs to live within the spack
source tree.  For example, the patch above lives in a directory
structure like this:

.. code-block:: none

   $SPACK_ROOT/var/spack/repos/builtin/packages/
       mvapich2/
           package.py
           ad_lustre_rwcontig_open_source.patch

If you supply a URL instead of a filename, you need to supply a
``sha256`` checksum, like this:

.. code-block:: python

   patch('http://www.nwchem-sw.org/images/Tddft_mxvec20.patch',
         sha256='252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866')

Spack includes the hashes of patches in its versioning information, so
that the same package with different patches applied will have different
hash identifiers.  To ensure that the hashing scheme is consistent, you
must use a ``sha256`` checksum for the patch.  Patches will be fetched
from their URLs, checked, and applied to your source code.  You can use
the GNU utils ``sha256sum`` or the macOS ``shasum -a 256`` commands to
generate a checksum for a patch file.

Spack can also handle compressed patches.  If you use these, Spack needs
a little more help.  Specifically, it needs *two* checksums: the
``sha256`` of the patch and ``archive_sha256`` for the compressed
archive.  ``archive_sha256`` helps Spack ensure that the downloaded
file is not corrupted or malicious, before running it through a tool like
``tar`` or ``zip``.  The ``sha256`` of the patch is still required so
that it can be included in specs.  Providing it in the package file
ensures that Spack won't have to download and decompress patches it won't
end up using at install time.  Both the archive and patch checksum are
checked when patch archives are downloaded.

.. code-block:: python

   patch('http://www.nwchem-sw.org/images/Tddft_mxvec20.patch.gz',
         sha256='252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866',
         archive_sha256='4e8092a161ec6c3a1b5253176fcf33ce7ba23ee2ff27c75dbced589dabacd06e')

``patch`` keyword arguments are described below.

""""""""""""""""""""""""""""""
``sha256``, ``archive_sha256``
""""""""""""""""""""""""""""""

Hashes of downloaded patch and compressed archive, respectively.  Only
needed for patches fetched from URLs.

""""""""
``when``
""""""""

If supplied, this is a spec that tells spack when to apply
the patch.  If the installed package spec matches this spec, the
patch will be applied.  In our example above, the patch is applied
when mvapich is at version ``1.9`` or higher.

"""""""""
``level``
"""""""""

This tells spack how to run the ``patch`` command.  By default,
the level is 1 and spack runs ``patch -p 1``.  If level is 2,
spack will run ``patch -p 2``, and so on.

A lot of people are confused by level, so here's a primer.  If you
look in your patch file, you may see something like this:

.. code-block:: diff
   :linenos:

   --- a/src/mpi/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 12:05:44.806417000 -0800
   +++ b/src/mpi/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 11:53:03.295622000 -0800
   @@ -8,7 +8,7 @@
     *   Copyright (C) 2008 Sun Microsystems, Lustre group
     \*/

   -#define _XOPEN_SOURCE 600
   +//#define _XOPEN_SOURCE 600
    #include <stdlib.h>
    #include <malloc.h>
    #include "ad_lustre.h"

Lines 1-2 show paths with synthetic ``a/`` and ``b/`` prefixes.  These
are placeholders for the two ``mvapich2`` source directories that
``diff`` compared when it created the patch file.  This is git's
default behavior when creating patch files, but other programs may
behave differently.

``-p1`` strips off the first level of the prefix in both paths,
allowing the patch to be applied from the root of an expanded mvapich2
archive.  If you set level to ``2``, it would strip off ``src``, and
so on.

It's generally easier to just structure your patch file so that it
applies cleanly with ``-p1``, but if you're using a patch you didn't
create yourself, ``level`` can be handy.

"""""""""""""""
``working_dir``
"""""""""""""""

This tells spack where to run the ``patch`` command.  By default,
the working directory is the source path of the stage (``.``).
However, sometimes patches are made with respect to a subdirectory
and this is where the working directory comes in handy. Internally,
the working directory is given to ``patch`` via the ``-d`` option.
Let's take the example patch from above and assume for some reason,
it can only be downloaded in the following form:

.. code-block:: diff
   :linenos:

   --- a/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 12:05:44.806417000 -0800
   +++ b/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 11:53:03.295622000 -0800
   @@ -8,7 +8,7 @@
     *   Copyright (C) 2008 Sun Microsystems, Lustre group
     \*/

   -#define _XOPEN_SOURCE 600
   +//#define _XOPEN_SOURCE 600
    #include <stdlib.h>
    #include <malloc.h>
    #include "ad_lustre.h"

Hence, the patch needs to applied in the ``src/mpi`` subdirectory, and the
``working_dir='src/mpi'`` option would exactly do that.

^^^^^^^^^^^^^^^^^^^^^
Patch functions
^^^^^^^^^^^^^^^^^^^^^

In addition to supplying patch files, you can write a custom function
to patch a package's source.  For example, the ``py-pyside`` package
contains some custom code for tweaking the way the PySide build
handles ``RPATH``:

.. _pyside-patch:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/py-pyside/package.py
   :pyobject: PyPyside.patch
   :linenos:

A ``patch`` function, if present, will be run after patch files are
applied and before ``install()`` is run.

You could put this logic in ``install()``, but putting it in a patch
function gives you some benefits.  First, spack ensures that the
``patch()`` function is run once per code checkout.  That means that
if you run install, hit ctrl-C, and run install again, the code in the
patch function is only run once.  Also, you can tell Spack to run only
the patching part of the build using the :ref:`cmd-spack-patch` command.

.. _patch_dependency_patching:

^^^^^^^^^^^^^^^^^^^
Dependency patching
^^^^^^^^^^^^^^^^^^^

So far we've covered how the ``patch`` directive can be used by a package
to patch *its own* source code. Packages can *also* specify patches to be
applied to their dependencies, if they require special modifications.  As
with all packages in Spack, a patched dependency library can coexist with
other versions of that library.  See the `section on depends_on
<dependency_dependency_patching_>`_ for more details.

.. _patch_inspecting_patches:

^^^^^^^^^^^^^^^^^^^
Inspecting patches
^^^^^^^^^^^^^^^^^^^

If you want to better understand the patches that Spack applies to your
packages, you can do that using ``spack spec``, ``spack find``, and other
query commands.  Let's look at ``m4``.  If you run ``spack spec m4``, you
can see the patches that would be applied to ``m4``::

  $ spack spec m4
  Input spec
  --------------------------------
  m4

  Concretized
  --------------------------------
  m4@1.4.18%apple-clang@9.0.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=darwin-highsierra-x86_64
      ^libsigsegv@2.11%apple-clang@9.0.0 arch=darwin-highsierra-x86_64

You can also see patches that have been applied to installed packages
with ``spack find -v``::

  $ spack find -v m4
  ==> 1 installed package
  -- darwin-highsierra-x86_64 / apple-clang@9.0.0 -----------------
  m4@1.4.18 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv

.. _cmd-spack-resource:

In both cases above, you can see that the patches' sha256 hashes are
stored on the spec as a variant.  As mentioned above, this means that you
can have multiple, differently-patched versions of a package installed at
once.

You can look up a patch by its sha256 hash (or a short version of it)
using the ``spack resource show`` command::

  $ spack resource show 3877ab54
  3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00
      path:       /home/spackuser/src/spack/var/spack/repos/builtin/packages/m4/gnulib-pgi.patch
      applies to: builtin.m4

``spack resource show`` looks up downloadable resources from package
files by hash and prints out information about them.  Above, we see that
the ``3877ab54`` patch applies to the ``m4`` package.  The output also
tells us where to find the patch.

Things get more interesting if you want to know about dependency
patches. For example, when ``dealii`` is built with ``boost@1.68.0``, it
has to patch boost to work correctly.  If you didn't know this, you might
wonder where the extra boost patches are coming from::

  $ spack spec dealii ^boost@1.68.0 ^hdf5+fortran | grep '\^boost'
      ^boost@1.68.0
          ^boost@1.68.0%apple-clang@9.0.0+atomic+chrono~clanglibcpp cxxstd=default +date_time~debug+exception+filesystem+graph~icu+iostreams+locale+log+math~mpi+multithreaded~numpy patches=2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199,b37164268f34f7133cbc9a4066ae98fda08adf51e1172223f6a969909216870f ~pic+program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer~versionedlayout+wave arch=darwin-highsierra-x86_64
  $ spack resource show b37164268
  b37164268f34f7133cbc9a4066ae98fda08adf51e1172223f6a969909216870f
      path:       /home/spackuser/src/spack/var/spack/repos/builtin/packages/dealii/boost_1.68.0.patch
      applies to: builtin.boost
      patched by: builtin.dealii

Here you can see that the patch is applied to ``boost`` by ``dealii``,
and that it lives in ``dealii``'s directory in Spack's ``builtin``
package repository.

.. _handling_rpaths:

---------------
Handling RPATHs
---------------

Spack installs each package in a way that ensures that all of its
dependencies are found when it runs.  It does this using `RPATHs
<http://en.wikipedia.org/wiki/Rpath>`_.  An RPATH is a search
path, stored in a binary (an executable or library), that tells the
dynamic loader where to find its dependencies at runtime. You may be
familiar with `LD_LIBRARY_PATH
<http://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html>`_
on Linux or `DYLD_LIBRARY_PATH
<https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/dyld.1.html>`_
on Mac OS X.  RPATH is similar to these paths, in that it tells
the loader where to find libraries.  Unlike them, it is embedded in
the binary and not set in each user's environment.

RPATHs in Spack are handled in one of three ways:

#. For most packages, RPATHs are handled automatically using Spack's
   :ref:`compiler wrappers <compiler-wrappers>`.  These wrappers are
   set in standard variables like ``CC``, ``CXX``, ``F77``, and ``FC``,
   so most build systems (autotools and many gmake systems) pick them
   up and use them.
#. CMake also respects Spack's compiler wrappers, but many CMake
   builds have logic to overwrite RPATHs when binaries are
   installed. Spack provides the ``std_cmake_args`` variable, which
   includes parameters necessary for CMake build use the right
   installation RPATH.  It can be used like this when ``cmake`` is
   invoked:

   .. code-block:: python

      class MyPackage(Package):
          ...
          def install(self, spec, prefix):
              cmake('..', *std_cmake_args)
              make()
              make('install')

#. If you need to modify the build to add your own RPATHs, you can
   use the ``self.rpath`` property of your package, which will
   return a list of all the RPATHs that Spack will use when it
   links.  You can see this how this is used in the :ref:`PySide
   example <pyside-patch>` above.

.. _attribute_parallel:

---------------
Parallel builds
---------------

Spack supports parallel builds on an individual package and at the
installation level.  Package-level parallelism is established by the
``--jobs`` option and its configuration and package recipe equivalents.
Installation-level parallelism is driven by the DAG(s) of the requested
package or packages.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Package-level build parallelism
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Spack will invoke ``make()``, or any other similar tool,
with a ``-j <njobs>`` argument, so those builds run in parallel.
The parallelism is determined by the value of the ``build_jobs`` entry
in ``config.yaml`` (see :ref:`here <build-jobs>` for more details on
how this value is computed).

If a package does not build properly in parallel, you can override
this setting by adding ``parallel = False`` to your package.  For
example, OpenSSL's build does not work in parallel, so its package
looks like this:

.. code-block:: python
   :emphasize-lines: 8
   :linenos:

   class Openssl(Package):
       homepage = "http://www.openssl.org"
       url      = "http://www.openssl.org/source/openssl-1.0.1h.tar.gz"

       version('1.0.1h', '8d6d684a9430d5cc98a62a5d8fbda8cf')
       depends_on("zlib")

       parallel = False

Similarly, you can disable parallel builds only for specific make
commands, as ``libdwarf`` does:

.. code-block:: python
   :emphasize-lines: 9, 12
   :linenos:

   class Libelf(Package):
       ...

       def install(self, spec, prefix):
           configure("--prefix=" + prefix,
                     "--enable-shared",
                     "--disable-dependency-tracking",
                     "--disable-debug")
           make()

           # The mkdir commands in libelf's install can fail in parallel
           make("install", parallel=False)

The first make will run in parallel here, but the second will not.  If
you set ``parallel`` to ``False`` at the package level, then each call
to ``make()`` will be sequential by default, but packagers can call
``make(parallel=True)`` to override it.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Install-level build parallelism
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack supports the concurrent installation of packages within a Spack
instance across multiple processes using file system locks.  This
parallelism is separate from the package-level achieved through build
systems' use of the ``-j <njobs>`` option.  With install-level parallelism,
processes coordinate the installation of the dependencies of specs
provided on the command line and as part of an environment build with
only **one process** being allowed to install a given package at a time.
Refer to :ref:`Dependencies` for more information on dependencies and
:ref:`installing-environment` for how to install an environment.

Concurrent processes may be any combination of interactive sessions and
batch jobs.  Which means a ``spack install`` can be running in a terminal
window while a batch job is running ``spack install`` on the same or
overlapping dependencies without any process trying to re-do the work of
another.

For example, if you are using SLURM, you could launch an installation
of ``mpich`` using the following command:

.. code-block:: console

   $ srun -N 2 -n 8 spack install -j 4 mpich@3.3.2

This will create eight concurrent, four-job installs on two different
nodes.

Alternatively, you could run the same installs on one node by entering
the following at the command line of a bash shell:

.. code-block:: console

   $ for i in {1..12}; do nohup spack install -j 4 mpich@3.3.2 >> mpich_install.txt 2>&1 &; done

.. note::

   The effective parallelism is based on the maximum number of packages
   that can be installed at the same time, which is limited by the
   number of packages with no (remaining) uninstalled dependencies.


.. _dependencies:

------------
Dependencies
------------

We've covered how to build a simple package, but what if one package
relies on another package to build?  How do you express that in a
package file?  And how do you refer to the other package in the build
script for your own package?

Spack makes this relatively easy.  Let's take a look at the
``libdwarf`` package to see how it's done:

.. code-block:: python
   :emphasize-lines: 9
   :linenos:

   class Libdwarf(Package):
       homepage = "http://www.prevanders.net/dwarf.html"
       url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
       list_url = homepage

       version('20130729', '4cc5e48693f7b93b7aa0261e63c0e21d')
       ...

       depends_on("libelf")

       def install(self, spec, prefix):
           ...

^^^^^^^^^^^^^^^^
``depends_on()``
^^^^^^^^^^^^^^^^

The highlighted ``depends_on('libelf')`` call tells Spack that it
needs to build and install the ``libelf`` package before it builds
``libdwarf``.  This means that in your ``install()`` method, you are
guaranteed that ``libelf`` has been built and installed successfully,
so you can rely on it for your libdwarf build.

^^^^^^^^^^^^^^^^
Dependency specs
^^^^^^^^^^^^^^^^

``depends_on`` doesn't just take the name of another package. It can
take a full spec as well. This means that you can restrict the versions or
other configuration options of ``libelf`` that ``libdwarf`` will build
with. For example, suppose that in the ``libdwarf`` package you write:

.. code-block:: python

   depends_on('libelf@0.8')

Now ``libdwarf`` will require ``libelf`` at *exactly* version ``0.8``.
You can also specify a requirement for a particular variant or for
specific compiler flags:

.. code-block:: python

   depends_on('libelf@0.8+debug')
   depends_on('libelf debug=True')
   depends_on('libelf cppflags="-fPIC"')

Both users *and* package authors can use the same spec syntax to refer
to different package configurations. Users use the spec syntax on the
command line to find installed packages or to install packages with
particular constraints, and package authors can use specs to describe
relationships between packages.

^^^^^^^^^^^^^^
Version ranges
^^^^^^^^^^^^^^

Although some packages require a specific version for their dependencies,
most can be built with a range of version. For example, if you are
writing a package for a legacy Python module that only works with Python
2.4 through 2.6, this would look like:

.. code-block:: python

   depends_on('python@2.4:2.6')

Version ranges in Spack are *inclusive*, so ``2.4:2.6`` means any version
greater than or equal to ``2.4`` and up to and including ``2.6``. If you
want to specify that a package works with any version of Python 3, this
would look like:

.. code-block:: python

   depends_on('python@3:')

Here we leave out the upper bound. If you want to say that a package
requires Python 2, you can similarly leave out the lower bound:

.. code-block:: python

   depends_on('python@:2.9')

Notice that we didn't use ``@:3``. Version ranges are *inclusive*, so
``@:3`` means "up to and including 3".

What if a package can only be built with Python 2.6? You might be
inclined to use:

.. code-block:: python

   depends_on('python@2.6')

However, this would be wrong. Spack assumes that all version constraints
are absolute, so it would try to install Python at exactly ``2.6``. The
correct way to specify this would be:

.. code-block:: python

   depends_on('python@2.6.0:2.6.999')

A spec can contain multiple version ranges separated by commas.
For example, if you need Boost 1.59.0 or newer, but there are known
issues with 1.64.0, 1.65.0, and 1.66.0, you can say:

.. code-block:: python

   depends_on('boost@1.59.0:1.63,1.65.1,1.67.0:')


.. _dependency-types:

^^^^^^^^^^^^^^^^
Dependency types
^^^^^^^^^^^^^^^^

Not all dependencies are created equal, and Spack allows you to specify
exactly what kind of a dependency you need. For example:

.. code-block:: python

   depends_on('cmake', type='build')
   depends_on('py-numpy', type=('build', 'run'))
   depends_on('libelf', type=('build', 'link'))
   depends_on('py-pytest', type='test')

The following dependency types are available:

* **"build"**: the dependency will be added to the ``PATH`` and
  ``PYTHONPATH`` at build-time.
* **"link"**: the dependency will be added to Spack's compiler
  wrappers, automatically injecting the appropriate linker flags,
  including ``-I``, ``-L``, and RPATH/RUNPATH handling.
* **"run"**: the dependency will be added to the ``PATH`` and
  ``PYTHONPATH`` at run-time. This is true for both ``spack load``
  and the module files Spack writes.
* **"test"**: the dependency will be added to the ``PATH`` and
  ``PYTHONPATH`` at build-time. The only difference between
  "build" and "test" is that test dependencies are only built
  if the user requests unit tests with ``spack install --test``.

One of the advantages of the ``build`` dependency type is that although the
dependency needs to be installed in order for the package to be built, it
can be uninstalled without concern afterwards. ``link`` and ``run`` disallow
this because uninstalling the dependency would break the package. Another
consequence of this is that ``build``-only dependencies do not affect the
hash of the package. The same is true for ``test`` dependencies.

If the dependency type is not specified, Spack uses a default of
``('build', 'link')``. This is the common case for compiler languages.
Non-compiled packages like Python modules commonly use
``('build', 'run')``. This means that the compiler wrappers don't need to
inject the dependency's ``prefix/lib`` directory, but the package needs to
be in ``PATH`` and ``PYTHONPATH`` during the build process and later when
a user wants to run the package.

^^^^^^^^^^^^^^^^^^^^^^^^
Conditional dependencies
^^^^^^^^^^^^^^^^^^^^^^^^

You may have a package that only requires a dependency under certain
conditions. For example, you may have a package that has optional MPI support,
- MPI is only a dependency when you want to enable MPI support for the
package. In that case, you could say something like:

.. code-block:: python

   variant('mpi', default=False, description='Enable MPI support')

   depends_on('mpi', when='+mpi')

``when`` can include constraints on the variant, version, compiler, etc. and
the :mod:`syntax<spack.spec>` is the same as for Specs written on the command
line.

If a dependency/feature of a package isn't typically used, you can save time
by making it conditional (since Spack will not build the dependency unless it
is required for the Spec).

.. _dependency_dependency_patching:

^^^^^^^^^^^^^^^^^^^
Dependency patching
^^^^^^^^^^^^^^^^^^^

Some packages maintain special patches on their dependencies, either to
add new features or to fix bugs.  This typically makes a package harder
to maintain, and we encourage developers to upstream (contribute back)
their changes rather than maintaining patches.  However, in some cases
it's not possible to upstream. Maybe the dependency's developers don't
accept changes, or maybe they just haven't had time to integrate them.

For times like these, Spack's ``depends_on`` directive can optionally
take a patch or list of patches:

.. code-block:: python

    class SpecialTool(Package):
        ...
        depends_on('binutils', patches='special-binutils-feature.patch')
        ...

Here, the ``special-tool`` package requires a special feature in
``binutils``, so it provides an extra ``patches=<filename>`` keyword
argument.  This is similar to the `patch directive <patching_>`_, with
one small difference.  Here, ``special-tool`` is responsible for the
patch, so it should live in ``special-tool``'s directory in the package
repository, not the ``binutils`` directory.

If you need something more sophisticated than this, you can simply nest a
``patch()`` directive inside of ``depends_on``:

.. code-block:: python

    class SpecialTool(Package):
        ...
        depends_on(
            'binutils',
            patches=patch('special-binutils-feature.patch',
                          level=3,
                          when='@:1.3'),   # condition on binutils
            when='@2.0:')                  # condition on special-tool
        ...

Note that there are two optional ``when`` conditions here -- one on the
``patch`` directive and the other on ``depends_on``.  The condition in
the ``patch`` directive applies to ``binutils`` (the package being
patched), while the condition in ``depends_on`` applies to
``special-tool``.  See `patch directive <patching_>`_ for details on all
the arguments the ``patch`` directive can take.

Finally, if you need *multiple* patches on a dependency, you can provide
a list for ``patches``, e.g.:

.. code-block:: python

    class SpecialTool(Package):
        ...
        depends_on(
            'binutils',
            patches=[
                'binutils-bugfix1.patch',
                'binutils-bugfix2.patch',
                patch('https://example.com/special-binutils-feature.patch',
                      sha256='252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866',
                      when='@:1.3')],
            when='@2.0:')
        ...

As with ``patch`` directives, patches are applied in the order they
appear in the package file (or in this case, in the list).

.. note::

   You may wonder whether dependency patching will interfere with other
   packages that depend on ``binutils``.  It won't.

   As described in patching_, Patching a package adds the ``sha256`` of
   the patch to the package's spec, which means it will have a
   *different* unique hash than other versions without the patch.  The
   patched version coexists with unpatched versions, and Spack's support
   for handling_rpaths_ guarantees that each installation finds the
   right version. If two packages depend on ``binutils`` patched *the
   same* way, they can both use a single installation of ``binutils``.

.. _setup-dependent-environment:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Influence how dependents are built or run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack provides a mechanism for dependencies to influence the
environment of their dependents by overriding  the
:meth:`setup_dependent_run_environment <spack.package.PackageBase.setup_dependent_run_environment>`
or the
:meth:`setup_dependent_build_environment <spack.package.PackageBase.setup_dependent_build_environment>`
methods.
The Qt package, for instance, uses this call:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/qt/package.py
   :pyobject: Qt.setup_dependent_build_environment
   :linenos:

to set the ``QTDIR`` environment variable so that packages
that depend on a particular Qt installation will find it.
Another good example of how a dependency can influence
the build environment of dependents is the Python package:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/python/package.py
   :pyobject: Python.setup_dependent_build_environment
   :linenos:

In the method above it is ensured that any package that depends on Python
will have the ``PYTHONPATH``, ``PYTHONHOME`` and ``PATH`` environment
variables set appropriately before starting the installation. To make things
even simpler the ``python setup.py`` command is also inserted into the module
scope of dependents by overriding a third method called
:meth:`setup_dependent_package <spack.package.PackageBase.setup_dependent_package>`
:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/python/package.py
   :pyobject: Python.setup_dependent_package
   :linenos:

This allows most python packages to have a very simple install procedure,
like the following:

.. code-block:: python

   def install(self, spec, prefix):
       setup_py('install', '--prefix={0}'.format(prefix))

Finally the Python package takes also care of the modifications to ``PYTHONPATH``
to allow dependencies to run correctly:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/python/package.py
    :pyobject: Python.setup_dependent_run_environment
    :linenos:


.. _packaging_conflicts:

---------
Conflicts
---------

Sometimes packages have known bugs, or limitations, that would prevent them
to build e.g. against other dependencies or with certain compilers. Spack
makes it possible to express such constraints with the ``conflicts`` directive.

Adding the following to a package:

.. code-block:: python

    conflicts('%intel', when='@:1.2',
              msg='<myNicePackage> <= v1.2 cannot be built with Intel ICC, '
                  'please use a newer release.')

we express the fact that the current package *cannot be built* with the Intel
compiler when we are trying to install a version "<=1.2". The ``when`` argument
can be omitted, in which case the conflict will always be active.
Conflicts are always evaluated after the concretization step has been performed,
and if any match is found a detailed error message is shown to the user.
You can add an additional message via the ``msg=`` parameter to a conflict that
provideds more specific instructions for users.

.. _packaging_extensions:

----------
Extensions
----------

Spack's support for package extensions is documented extensively in
:ref:`extensions`.  This section documents how to make your own
extendable packages and extensions.

To support extensions, a package needs to set its ``extendable``
property to ``True``, e.g.:

.. code-block:: python

   class Python(Package):
       ...
       extendable = True
       ...

To make a package into an extension, simply add an
``extends`` call in the package definition, and pass it the name of an
extendable package:

.. code-block:: python

   class PyNumpy(Package):
       ...
       extends('python')
       ...

Now, the ``py-numpy`` package can be used as an argument to ``spack
activate``.  When it is activated, all the files in its prefix will be
symbolically linked into the prefix of the python package.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Adding additional constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some packages produce a Python extension, but are only compatible with
Python 3, or with Python 2.  In those cases, a ``depends_on()``
declaration should be made in addition to the ``extends()``
declaration:

.. code-block:: python

   class Icebin(Package):
       extends('python', when='+python')
       depends_on('python@3:', when='+python')

Many packages produce Python extensions for *some* variants, but not
others: they should extend ``python`` only if the appropriate
variant(s) are selected.  This may be accomplished with conditional
``extends()`` declarations:

.. code-block:: python

   class FooLib(Package):
       variant('python', default=True, description='Build the Python extension Module')
       extends('python', when='+python')
       ...

Sometimes, certain files in one package will conflict with those in
another, which means they cannot both be activated (symlinked) at the
same time.  In this case, you can tell Spack to ignore those files
when it does the activation:

.. code-block:: python

   class PySncosmo(Package):
       ...
       # py-sncosmo binaries are duplicates of those from py-astropy
       extends('python', ignore=r'bin/.*')
       depends_on('py-astropy')
       ...

The code above will prevent everything in the ``$prefix/bin/`` directory
from being linked in at activation time.

.. note::

   You can call *either* ``depends_on`` or ``extends`` on any one
   package, but not both.  For example you cannot both
   ``depends_on('python')`` and ``extends(python)`` in the same
   package.  ``extends`` implies ``depends_on``.

-----
Views
-----

As covered in :ref:`filesystem-views`, the ``spack view`` command can be
used to symlink a number of packages into a merged prefix. The methods of
``PackageViewMixin`` can be overridden to customize how packages are added
to views. Generally this can be used to create copies of specific files rather
than symlinking them when symlinking does not work. For example, ``Python``
overrides ``add_files_to_view`` in order to create a copy of the ``python``
binary since the real path of the Python executable is used to detect
extensions; as a consequence python extension packages (those inheriting from
``PythonPackage``) likewise override ``add_files_to_view`` in order to rewrite
shebang lines which point to the Python interpreter.

^^^^^^^^^^^^^^^^^^^^^^^^^
Activation & deactivation
^^^^^^^^^^^^^^^^^^^^^^^^^

Adding an extension to a view is referred to as an activation. If the view is
maintained in the Spack installation prefix of the extendee this is called a
global activation. Activations may involve updating some centralized state
that is maintained by the extendee package, so there can be additional work
for adding extensions compared with non-extension packages.

Spack's ``Package`` class has default ``activate`` and ``deactivate``
implementations that handle symbolically linking extensions' prefixes
into a specified view. Extendable packages can override these methods
to add custom activate/deactivate logic of their own.  For example,
the ``activate`` and ``deactivate`` methods in the Python class handle
symbolic linking of extensions, but they also handle details surrounding
Python's ``.pth`` files, and other aspects of Python packaging.

Spack's extensions mechanism is designed to be extensible, so that
other packages (like Ruby, R, Perl, etc.)  can provide their own
custom extension management logic, as they may not handle modules the
same way that Python does.

Let's look at Python's activate function:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/python/package.py
   :pyobject: Python.activate
   :linenos:

This function is called on the *extendee* (Python).  It first calls
``activate`` in the superclass, which handles symlinking the
extension package's prefix into the specified view.  It then does
some special handling of the ``easy-install.pth`` file, part of
Python's setuptools.

Deactivate behaves similarly to activate, but it unlinks files:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/python/package.py
   :pyobject: Python.deactivate
   :linenos:

Both of these methods call some custom functions in the Python
package.  See the source for Spack's Python package for details.

^^^^^^^^^^^^^^^^^^^^
Activation arguments
^^^^^^^^^^^^^^^^^^^^

You may have noticed that the ``activate`` function defined above
takes keyword arguments.  These are the keyword arguments from
``extends()``, and they are passed to both activate and deactivate.

This capability allows an extension to customize its own activation by
passing arguments to the extendee.  Extendees can likewise implement
custom ``activate()`` and ``deactivate()`` functions to suit their
needs.

The only keyword argument supported by default is the ``ignore``
argument, which can take a regex, list of regexes, or a predicate to
determine which files *not* to symlink during activation.

.. _virtual-dependencies:

--------------------
Virtual dependencies
--------------------

In some cases, more than one package can satisfy another package's
dependency.  One way this can happen is if a package depends on a
particular *interface*, but there are multiple *implementations* of
the interface, and the package could be built with any of them.  A
*very* common interface in HPC is the `Message Passing Interface (MPI)
<http://www.mcs.anl.gov/research/projects/mpi/>`_, which is used in
many large-scale parallel applications.

MPI has several different implementations (e.g., `MPICH
<http://www.mpich.org>`_, `OpenMPI <http://www.open-mpi.org>`_, and
`MVAPICH <http://mvapich.cse.ohio-state.edu>`_) and scientific
applications can be built with any one of them.  Complicating matters,
MPI does not have a standardized ABI, so a package built with one
implementation cannot simply be relinked with another implementation.
Many package managers handle interfaces like this by requiring many
similar package files, e.g., ``foo``, ``foo-mvapich``, ``foo-mpich``,
but Spack avoids this explosion of package files by providing support
for *virtual dependencies*.

^^^^^^^^^^^^
``provides``
^^^^^^^^^^^^

In Spack, ``mpi`` is handled as a *virtual package*.  A package like
``mpileaks`` can depend on it just like any other package, by
supplying a ``depends_on`` call in the package definition.  For example:

.. code-block:: python
   :linenos:
   :emphasize-lines: 7

   class Mpileaks(Package):
       homepage = "https://github.com/hpc/mpileaks"
       url = "https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

       version('1.0', '8838c574b39202a57d7c2d68692718aa')

       depends_on("mpi")
       depends_on("adept-utils")
       depends_on("callpath")

Here, ``callpath`` and ``adept-utils`` are concrete packages, but
there is no actual package file for ``mpi``, so we say it is a
*virtual* package.  The syntax of ``depends_on``, is the same for
both.  If we look inside the package file of an MPI implementation,
say MPICH, we'll see something like this:

.. code-block:: python

   class Mpich(Package):
       provides('mpi')
       ...

The ``provides("mpi")`` call tells Spack that the ``mpich`` package
can be used to satisfy the dependency of any package that
``depends_on('mpi')``.

^^^^^^^^^^^^^^^^^^^^
Versioned Interfaces
^^^^^^^^^^^^^^^^^^^^

Just as you can pass a spec to ``depends_on``, so can you pass a spec
to ``provides`` to add constraints.  This allows Spack to support the
notion of *versioned interfaces*.  The MPI standard has gone through
many revisions, each with new functions added, and each revision of
the standard has a version number.  Some packages may require a recent
implementation that supports MPI-3 functions, but some MPI versions may
only provide up to MPI-2.  Others may need MPI 2.1 or higher.  You can
indicate this by adding a version constraint to the spec passed to
``provides``:

.. code-block:: python

   provides("mpi@:2")

Suppose that the above ``provides`` call is in the ``mpich2`` package.
This says that ``mpich2`` provides MPI support *up to* version 2, but
if a package ``depends_on("mpi@3")``, then Spack will *not* build that
package with ``mpich2``.

^^^^^^^^^^^^^^^^^
``provides when``
^^^^^^^^^^^^^^^^^

The same package may provide different versions of an interface
depending on *its* version.  Above, we simplified the ``provides``
call in ``mpich`` to make the explanation easier.  In reality, this is
how ``mpich`` calls ``provides``:

.. code-block:: python

   provides('mpi@:3', when='@3:')
   provides('mpi@:1', when='@1:')

The ``when`` argument to ``provides`` allows you to specify optional
constraints on the *providing* package, or the *provider*.  The
provider only provides the declared virtual spec when *it* matches
the constraints in the when clause.  Here, when ``mpich`` is at
version 3 or higher, it provides MPI up to version 3.  When ``mpich``
is at version 1 or higher, it provides the MPI virtual package at
version 1.

The ``when`` qualifier ensures that Spack selects a suitably high
version of ``mpich`` to satisfy some other package that ``depends_on``
a particular version of MPI.  It will also prevent a user from
building with too low a version of ``mpich``.  For example, suppose
the package ``foo`` declares this:

.. code-block:: python

   class Foo(Package):
       ...
       depends_on('mpi@2')

Suppose a user invokes ``spack install`` like this:

.. code-block:: console

   $ spack install foo ^mpich@1.0

Spack will fail with a constraint violation, because the version of
MPICH requested is too low for the ``mpi`` requirement in ``foo``.

.. _abstract-and-concrete:

-------------------------
Abstract & concrete specs
-------------------------

Now that we've seen how spec constraints can be specified :ref:`on the
command line <sec-specs>` and within package definitions, we can talk
about how Spack puts all of this information together.  When you run
this:

.. code-block:: console

   $ spack install mpileaks ^callpath@1.0+debug ^libelf@0.8.11

Spack parses the command line and builds a spec from the description.
The spec says that ``mpileaks`` should be built with the ``callpath``
library at 1.0 and with the debug option enabled, and with ``libelf``
version 0.8.11.  Spack will also look at the ``depends_on`` calls in
all of these packages, and it will build a spec from that.  The specs
from the command line and the specs built from package descriptions
are then combined, and the constraints are checked against each other
to make sure they're satisfiable.

What we have after this is done is called an *abstract spec*.  An
abstract spec is partially specified.  In other words, it could
describe more than one build of a package.  Spack does this to make
things easier on the user: they should only have to specify as much of
the package spec as they care about.  Here's an example partial spec
DAG, based on the constraints above:

.. code-block:: none

   mpileaks
       ^callpath@1.0+debug
           ^dyninst
               ^libdwarf
                   ^libelf@0.8.11
           ^mpi

.. graphviz::

   digraph {
       mpileaks -> mpi
       mpileaks -> "callpath@1.0+debug" -> mpi
       "callpath@1.0+debug" -> dyninst
       dyninst  -> libdwarf -> "libelf@0.8.11"
       dyninst  -> "libelf@0.8.11"
   }

This diagram shows a spec DAG output as a tree, where successive
levels of indentation represent a depends-on relationship.  In the
above DAG, we can see some packages annotated with their constraints,
and some packages with no annotations at all.  When there are no
annotations, it means the user doesn't care what configuration of that
package is built, just so long as it works.

^^^^^^^^^^^^^^
Concretization
^^^^^^^^^^^^^^

An abstract spec is useful for the user, but you can't install an
abstract spec.  Spack has to take the abstract spec and "fill in" the
remaining unspecified parts in order to install.  This process is
called **concretization**.  Concretization happens in between the time
the user runs ``spack install`` and the time the ``install()`` method
is called.  The concretized version of the spec above might look like
this:

.. code-block:: none

   mpileaks@2.3%gcc@4.7.3 arch=linux-debian7-x86_64
       ^callpath@1.0%gcc@4.7.3+debug arch=linux-debian7-x86_64
           ^dyninst@8.1.2%gcc@4.7.3 arch=linux-debian7-x86_64
               ^libdwarf@20130729%gcc@4.7.3 arch=linux-debian7-x86_64
                   ^libelf@0.8.11%gcc@4.7.3 arch=linux-debian7-x86_64
           ^mpich@3.0.4%gcc@4.7.3 arch=linux-debian7-x86_64

.. graphviz::

   digraph {
       "mpileaks@2.3\n%gcc@4.7.3\n arch=linux-debian7-x86_64" -> "mpich@3.0.4\n%gcc@4.7.3\n arch=linux-debian7-x86_64"
       "mpileaks@2.3\n%gcc@4.7.3\n arch=linux-debian7-x86_64" -> "callpath@1.0\n%gcc@4.7.3+debug\n arch=linux-debian7-x86_64" -> "mpich@3.0.4\n%gcc@4.7.3\n arch=linux-debian7-x86_64"
       "callpath@1.0\n%gcc@4.7.3+debug\n arch=linux-debian7-x86_64" -> "dyninst@8.1.2\n%gcc@4.7.3\n arch=linux-debian7-x86_64"
       "dyninst@8.1.2\n%gcc@4.7.3\n arch=linux-debian7-x86_64" -> "libdwarf@20130729\n%gcc@4.7.3\n arch=linux-debian7-x86_64" -> "libelf@0.8.11\n%gcc@4.7.3\n arch=linux-debian7-x86_64"
       "dyninst@8.1.2\n%gcc@4.7.3\n arch=linux-debian7-x86_64" -> "libelf@0.8.11\n%gcc@4.7.3\n arch=linux-debian7-x86_64"
   }

Here, all versions, compilers, and platforms are filled in, and there
is a single version (no version ranges) for each package.  All
decisions about configuration have been made, and only after this
point will Spack call the ``install()`` method for your package.

Concretization in Spack is based on certain selection policies that
tell Spack how to select, e.g., a version, when one is not specified
explicitly.  Concretization policies are discussed in more detail in
:ref:`configuration`.  Sites using Spack can customize them to match
the preferences of their own users.

.. _cmd-spack-spec:

^^^^^^^^^^^^^^
``spack spec``
^^^^^^^^^^^^^^

For an arbitrary spec, you can see the result of concretization by
running ``spack spec``.  For example:

.. code-block:: console

   $ spack spec dyninst@8.0.1
   dyninst@8.0.1
       ^libdwarf
           ^libelf

   dyninst@8.0.1%gcc@4.7.3 arch=linux-debian7-x86_64
       ^libdwarf@20130729%gcc@4.7.3 arch=linux-debian7-x86_64
           ^libelf@0.8.13%gcc@4.7.3 arch=linux-debian7-x86_64

This is useful when you want to know exactly what Spack will do when
you ask for a particular spec.

.. _concretization-policies:

^^^^^^^^^^^^^^^^^^^^^^^^^^^
``Concretization Policies``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A user may have certain preferences for how packages should
be concretized on their system.  For example, one user may prefer packages
built with OpenMPI and the Intel compiler.  Another user may prefer
packages be built with MVAPICH and GCC.

See the :ref:`concretization-preferences` section for more details.

.. _install-method:

------------------
Conflicting Specs
------------------

Suppose a user needs to install package C, which depends on packages A
and B.  Package A builds a library with a Python2 extension, and
package B builds a library with a Python3 extension.  Packages A and B
cannot be loaded together in the same Python runtime:

.. code-block:: python

    class A(Package):
        variant('python', default=True, 'enable python bindings')
        depends_on('python@2.7', when='+python')
        def install(self, spec, prefix):
            # do whatever is necessary to enable/disable python
            # bindings according to variant

    class B(Package):
        variant('python', default=True, 'enable python bindings')
        depends_on('python@3.2:', when='+python')
        def install(self, spec, prefix):
            # do whatever is necessary to enable/disable python
            # bindings according to variant

Package C needs to use the libraries from packages A and B, but does
not need either of the Python extensions.  In this case, package C
should simply depend on the ``~python`` variant of A and B:

.. code-block:: python

    class C(Package):
        depends_on('A~python')
        depends_on('B~python')

This may require that A or B be built twice, if the user wishes to use
the Python extensions provided by them: once for ``+python`` and once
for ``~python``.  Other than using a little extra disk space, that
solution has no serious problems.

.. _installation_procedure:

---------------------------------------
Implementing the installation procedure
---------------------------------------

The last element of a package is its **installation procedure**.  This is
where the real work of installation happens, and it's the main part of
the package you'll need to customize for each piece of software.

Defining an installation procedure means overriding a set of methods or attributes
that will be called at some point during the installation of the package.
The package base class, usually specialized for a given build system, determines the
actual set of entities available for overriding.
The classes that are currently provided by Spack are:

    +-------------------------------+----------------------------------+
    |        **Base Class**         |           **Purpose**            |
    +===============================+==================================+
    | :py:class:`.Package`          | General base class not           |
    |                               | specialized for any build system |
    +-------------------------------+----------------------------------+
    | :py:class:`.MakefilePackage`  | Specialized class for packages   |
    |                               | built invoking                   |
    |                               | hand-written Makefiles           |
    +-------------------------------+----------------------------------+
    | :py:class:`.AutotoolsPackage` | Specialized class for packages   |
    |                               | built using GNU Autotools        |
    +-------------------------------+----------------------------------+
    | :py:class:`.CMakePackage`     | Specialized class for packages   |
    |                               | built using CMake                |
    +-------------------------------+----------------------------------+
    | :py:class:`.CudaPackage`      | A helper class for packages that |
    |                               | use CUDA                         |
    +-------------------------------+----------------------------------+
    | :py:class:`.QMakePackage`     | Specialized class for packages   |
    |                               | build using QMake                |
    +-------------------------------+----------------------------------+
    | :py:class:`.ROCmPackage`      | A helper class for packages that |
    |                               | use ROCm                         |
    +-------------------------------+----------------------------------+
    | :py:class:`.SConsPackage`     | Specialized class for packages   |
    |                               | built using SCons                |
    +-------------------------------+----------------------------------+
    | :py:class:`.WafPackage`       | Specialized class for packages   |
    |                               | built using Waf                  |
    +-------------------------------+----------------------------------+
    | :py:class:`.RPackage`         | Specialized class for            |
    |                               | :py:class:`.R` extensions        |
    +-------------------------------+----------------------------------+
    | :py:class:`.OctavePackage`    | Specialized class for            |
    |                               | :py:class:`.Octave` packages     |
    +-------------------------------+----------------------------------+
    | :py:class:`.PythonPackage`    | Specialized class for            |
    |                               | :py:class:`.Python` extensions   |
    +-------------------------------+----------------------------------+
    | :py:class:`.PerlPackage`      | Specialized class for            |
    |                               | :py:class:`.Perl` extensions     |
    +-------------------------------+----------------------------------+
    | :py:class:`.IntelPackage`     | Specialized class for licensed   |
    |                               | Intel software                   |
    +-------------------------------+----------------------------------+


.. note::
    Choice of the appropriate base class for a package
        In most cases packagers don't have to worry about the selection of the right base class
        for a package, as ``spack create`` will make the appropriate choice on their behalf. In those
        rare cases where manual intervention is needed we need to stress that a
        package base class depends on the *build system* being used, not the language of the package.
        For example, a Python extension installed with CMake would ``extends('python')`` and
        subclass from :py:class:`.CMakePackage`.

^^^^^^^^^^^^^^^^^^^^^
Installation pipeline
^^^^^^^^^^^^^^^^^^^^^

When a user runs ``spack install``, Spack:

1. Fetches an archive for the correct version of the software.
2. Expands the archive.
3. Sets the current working directory to the root directory of the expanded archive.

Then, depending on the base class of the package under consideration, it will execute
a certain number of **phases** that reflect the way a package of that type is usually built.
The name and order in which the phases will be executed can be obtained either reading the API
docs at :py:mod:`~.spack.build_systems`, or using the ``spack info`` command:

.. code-block:: console
    :emphasize-lines: 13,14

    $ spack info m4
    AutotoolsPackage:    m4
    Homepage:            https://www.gnu.org/software/m4/m4.html

    Safe versions:
        1.4.17    ftp://ftp.gnu.org/gnu/m4/m4-1.4.17.tar.gz

    Variants:
        Name       Default   Description

        sigsegv    on        Build the libsigsegv dependency

    Installation Phases:
        autoreconf    configure    build    install

    Build Dependencies:
        libsigsegv

    ...


Typically, phases have default implementations that fit most of the common cases:

.. literalinclude:: _spack_root/lib/spack/spack/build_systems/autotools.py
    :pyobject: AutotoolsPackage.configure
    :linenos:

It is thus just sufficient for a packager to override a few
build system specific helper methods or attributes to provide, for instance,
configure arguments:

.. literalinclude::  _spack_root/var/spack/repos/builtin/packages/m4/package.py
    :pyobject: M4.configure_args
    :linenos:

.. note::
    Each specific build system has a list of attributes that can be overridden to
    fine-tune the installation of a package without overriding an entire phase. To
    have more information on them the place to go is the API docs of the :py:mod:`~.spack.build_systems`
    module.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Overriding an entire phase
^^^^^^^^^^^^^^^^^^^^^^^^^^

In extreme cases it may be necessary to override an entire phase. Regardless
of the build system, the signature is the same. For example, the signature
for the install phase is:

.. code-block:: python

   class Foo(Package):
       def install(self, spec, prefix):
           ...

``self``
    For those not used to Python instance methods, this is the
    package itself.  In this case it's an instance of ``Foo``, which
    extends ``Package``.  For API docs on Package objects, see
    :py:class:`Package <spack.package.Package>`.

``spec``
    This is the concrete spec object created by Spack from an
    abstract spec supplied by the user.  It describes what should be
    installed.  It will be of type :py:class:`Spec <spack.spec.Spec>`.

``prefix``
    This is the path that your install method should copy build
    targets into.  It acts like a string, but it's actually its own
    special type, :py:class:`Prefix <spack.util.prefix.Prefix>`.

The arguments ``spec`` and ``prefix`` are passed only for convenience, as they always
correspond to ``self.spec`` and ``self.spec.prefix`` respectively.

As mentioned in :ref:`install-environment`, you will usually not need to refer
to dependencies explicitly in your package file, as the compiler wrappers take care of most of
the heavy lifting here.  There will be times, though, when you need to refer to
the install locations of dependencies, or when you need to do something different
depending on the version, compiler, dependencies, etc. that your package is
built with.  These parameters give you access to this type of information.

.. _install-environment:

-----------------------
The build environment
-----------------------

In general, you should not have to do much differently in your install
method than you would when installing a package on the command line.
In fact, you may need to do *less* than you would on the command line.

Spack tries to set environment variables and modify compiler calls so
that it *appears* to the build system that you're building with a
standard system install of everything.  Obviously that's not going to
cover *all* build systems, but it should make it easy to port packages
to Spack if they use a standard build system.  Usually with autotools
or cmake, building and installing is easy.  With builds that use
custom Makefiles, you may need to add logic to modify the makefiles.

The remainder of the section covers the way Spack's build environment
works.

^^^^^^^^^^^^^^^^^^^^^
Forking ``install()``
^^^^^^^^^^^^^^^^^^^^^

To give packagers free reign over their install environment, Spack forks
a new process each time it invokes a package's ``install()`` method.
This allows packages to have a sandboxed build environment, without
impacting the environments ofother jobs that the main Spack process runs.
Packages are free to change the environment or to modify Spack internals,
because each ``install()`` call has its own dedicated process.

^^^^^^^^^^^^^^^^^^^^^
Environment variables
^^^^^^^^^^^^^^^^^^^^^

Spack sets a number of standard environment variables that serve two
purposes:

#. Make build systems use Spack's compiler wrappers for their builds.
#. Allow build systems to find dependencies more easily

The Compiler environment variables that Spack sets are:

  ============  ===============================
    Variable     Purpose
  ============  ===============================
    ``CC``       C compiler
    ``CXX``      C++ compiler
    ``F77``      Fortran 77 compiler
    ``FC``       Fortran 90 and above compiler
  ============  ===============================

Spack sets these variables so that they point to *compiler
wrappers*. These are covered in :ref:`their own section
<compiler-wrappers>` below.

All of these are standard variables respected by most build systems.
If your project uses ``Autotools`` or ``CMake``, then it should pick
them up automatically when you run ``configure`` or ``cmake`` in the
``install()`` function.  Many traditional builds using GNU Make and
BSD make also respect these variables, so they may work with these
systems.

If your build system does *not* automatically pick these variables up
from the environment, then you can simply pass them on the command
line or use a patch as part of your build process to get the correct
compilers into the project's build system.  There are also some file
editing commands you can use -- these are described later in the
`section on file manipulation <file-manipulation_>`_.

In addition to the compiler variables, these variables are set before
entering ``install()`` so that packages can locate dependencies
easily:

=====================  ====================================================
``PATH``               Set to point to ``/bin`` directories of dependencies
``CMAKE_PREFIX_PATH``  Path to dependency prefixes for CMake
``PKG_CONFIG_PATH``    Path to any pkgconfig directories for dependencies
``PYTHONPATH``         Path to site-packages dir of any python dependencies
=====================  ====================================================

``PATH`` is set up to point to dependencies ``/bin`` directories so
that you can use tools installed by dependency packages at build time.
For example, ``$MPICH_ROOT/bin/mpicc`` is frequently used by dependencies of
``mpich``.

``CMAKE_PREFIX_PATH`` contains a colon-separated list of prefixes
where ``cmake`` will search for dependency libraries and headers.
This causes all standard CMake find commands to look in the paths of
your dependencies, so you *do not* have to manually specify arguments
like ``-DDEPENDENCY_DIR=/path/to/dependency`` to ``cmake``.  More on
this is `in the CMake documentation <http://www.cmake.org/cmake/help/v3.0/variable/CMAKE_PREFIX_PATH.html>`_.

``PKG_CONFIG_PATH`` is for packages that attempt to discover
dependencies using the GNU ``pkg-config`` tool.  It is similar to
``CMAKE_PREFIX_PATH`` in that it allows a build to automatically
discover its dependencies.

If you want to see the environment that a package will build with, or
if you want to run commands in that environment to test them out, you
can use the :ref:`cmd-spack-build-env` command, documented
below.

^^^^^^^^^^^^^^^^^^^^^
Failing the build
^^^^^^^^^^^^^^^^^^^^^

Sometimes you don't want a package to successfully install unless some
condition is true.  You can explicitly cause the build to fail from
``install()`` by raising an ``InstallError``, for example:

.. code-block:: python

   if spec.architecture.startswith('darwin'):
       raise InstallError('This package does not build on Mac OS X!')

.. _shell-wrappers:

^^^^^^^^^^^^^^^^^^^^^^^
Shell command functions
^^^^^^^^^^^^^^^^^^^^^^^

Recall the install method from ``libelf``:

.. literalinclude::  _spack_root/var/spack/repos/builtin/packages/libelf/package.py
   :pyobject: Libelf.install
   :linenos:

Normally in Python, you'd have to write something like this in order
to execute shell commands:

.. code-block:: python

   import subprocess
   subprocess.check_call('configure', '--prefix={0}'.format(prefix))

We've tried to make this a bit easier by providing callable wrapper
objects for some shell commands.  By default, ``configure``,
``cmake``, and ``make`` wrappers are are provided, so you can call
them more naturally in your package files.

If you need other commands, you can use ``which`` to get them:

.. code-block:: python

   sed = which('sed')
   sed('s/foo/bar/', filename)

The ``which`` function will search the ``PATH`` for the application.

Callable wrappers also allow spack to provide some special features.
For example, in Spack, ``make`` is parallel by default, and Spack
figures out the number of cores on your machine and passes an
appropriate value for ``-j<numjobs>`` when it calls ``make`` (see the
``parallel`` `package attribute <attribute_parallel>`).  In
a package file, you can supply a keyword argument, ``parallel=False``,
to the ``make`` wrapper to disable parallel make.  In the ``libelf``
package, this allows us to avoid race conditions in the library's
build system.

^^^^^^^^^^^^^^
Compiler flags
^^^^^^^^^^^^^^

Compiler flags set by the user through the Spec object can be passed
to the build in one of three ways. By default, the build environment
injects these flags directly into the compiler commands using Spack's
compiler wrappers. In cases where the build system requires knowledge
of the compiler flags, they can be registered with the build system by
alternatively passing them through environment variables or as build
system arguments. The flag_handler method can be used to change this
behavior.

Packages can override the flag_handler method with one of three
built-in flag_handlers. The built-in flag_handlers are named
``inject_flags``, ``env_flags``, and ``build_system_flags``. The
``inject_flags`` method is the default. The ``env_flags`` method puts
all of the flags into the environment variables that ``make`` uses as
implicit variables ('CFLAGS', 'CXXFLAGS', etc.). The
``build_system_flags`` method adds the flags as
arguments to the invocation of ``configure`` or ``cmake``,
respectively.

.. warning::

   Passing compiler flags using build system arguments is only
   supported for CMake and Autotools packages. Individual packages may
   also differ in whether they properly respect these arguments.

Individual packages may also define their own ``flag_handler``
methods. The ``flag_handler`` method takes the package instance
(``self``), the name of the flag, and a list of the values of the
flag. It will be called on each of the six compiler flags supported in
Spack. It should return a triple of ``(injf, envf, bsf)`` where
``injf`` is a list of flags to inject via the Spack compiler wrappers,
``envf`` is a list of flags to set in the appropriate environment
variables, and ``bsf`` is a list of flags to pass to the build system
as arguments.

.. warning::

   Passing a non-empty list of flags to ``bsf`` for a build system
   that does not support build system arguments will result in an
   error.

Here are the definitions of the three built-in flag handlers:

.. code-block:: python

   def inject_flags(pkg, name, flags):
       return (flags, None, None)

   def env_flags(pkg, name, flags):
       return (None, flags, None)

   def build_system_flags(pkg, name, flags):
       return (None, None, flags)

.. note::

   Returning ``[]`` and ``None`` are equivalent in a ``flag_handler``
   method.

Packages can override the default behavior either by specifying one of
the built-in flag handlers,

.. code-block:: python

   flag_handler = env_flags

or by implementing the flag_handler method. Suppose for a package
``Foo`` we need to pass ``cflags``, ``cxxflags``, and ``cppflags``
through the environment, the rest of the flags through compiler
wrapper injection, and we need to add ``-lbar`` to ``ldlibs``. The
following flag handler method accomplishes that.

.. code-block:: python

   def flag_handler(self, name, flags):
       if name in ['cflags', 'cxxflags', 'cppflags']:
           return (None, flags, None)
       elif name == 'ldlibs':
           flags.append('-lbar')
       return (flags, None, None)

Because these methods can pass values through environment variables,
it is important not to override these variables unnecessarily
(E.g. setting ``env['CFLAGS']``) in other package methods when using
non-default flag handlers. In the ``setup_environment`` and
``setup_dependent_environment`` methods, use the ``append_flags``
method of the ``EnvironmentModifications`` class to append values to a
list of flags whenever the flag handler is ``env_flags``. If the
package passes flags through the environment or the build system
manually (in the install method, for example), we recommend using the
default flag handler, or removing manual references and implementing a
custom flag handler method that adds the desired flags to export as
environment variables or pass to the build system. Manual flag passing
is likely to interfere with the ``env_flags`` and
``build_system_flags`` methods.

In rare circumstances such as compiling and running small unit tests, a
package developer may need to know what are the appropriate compiler
flags to enable features like ``OpenMP``, ``c++11``, ``c++14`` and
alike. To that end the compiler classes in ``spack`` implement the
following **properties**: ``openmp_flag``, ``cxx98_flag``, ``cxx11_flag``,
``cxx14_flag``, and ``cxx17_flag``, which can be accessed in a package by
``self.compiler.cxx11_flag`` and alike. Note that the implementation is
such that if a given compiler version does not support this feature, an
error will be produced. Therefore package developers can also use these
properties to assert that a compiler supports the requested feature. This
is handy when a package supports additional variants like

.. code-block:: python

   variant('openmp', default=True, description="Enable OpenMP support.")

.. _blas_lapack_scalapack:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Blas, Lapack and ScaLapack libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiple packages provide implementations of ``Blas``, ``Lapack`` and ``ScaLapack``
routines.  The names of the resulting static and/or shared libraries
differ from package to package. In order to make the ``install()`` method
independent of the choice of ``Blas`` implementation, each package which
provides it implements ``@property def blas_libs(self):`` to return an object
of
`LibraryList <https://spack.readthedocs.io/en/latest/llnl.util.html#llnl.util.filesystem.LibraryList>`_
type which simplifies usage of a set of libraries.
The same applies to packages which provide ``Lapack`` and ``ScaLapack``.
Package developers are requested to use this interface. Common usage cases are:

1. Space separated list of full paths

.. code-block:: python

   lapack_blas = spec['lapack'].libs + spec['blas'].libs
   options.append(
      '--with-blas-lapack-lib={0}'.format(lapack_blas.joined())
   )

2. Names of libraries and directories which contain them

.. code-block:: python

   blas = spec['blas'].libs
   options.extend([
     '-DBLAS_LIBRARY_NAMES={0}'.format(';'.join(blas.names)),
     '-DBLAS_LIBRARY_DIRS={0}'.format(';'.join(blas.directories))
   ])

3. Search and link flags

.. code-block:: python

   math_libs = spec['scalapack'].libs + spec['lapack'].libs + spec['blas'].libs
   options.append(
     '-DMATH_LIBS:STRING={0}'.format(math_libs.ld_flags)
   )


For more information, see documentation of
`LibraryList <https://spack.readthedocs.io/en/latest/llnl.util.html#llnl.util.filesystem.LibraryList>`_
class.


.. _prefix-objects:

^^^^^^^^^^^^^^^^^^^^^
Prefix objects
^^^^^^^^^^^^^^^^^^^^^

Spack passes the ``prefix`` parameter to the install method so that
you can pass it to ``configure``, ``cmake``, or some other installer,
e.g.:

.. code-block:: python

   configure('--prefix={0}'.format(prefix))

For the most part, prefix objects behave exactly like strings.  For
packages that do not have their own install target, or for those that
implement it poorly (like ``libdwarf``), you may need to manually copy
things into particular directories under the prefix.  For this, you
can refer to standard subdirectories without having to construct paths
yourself, e.g.:

.. code-block:: python

   def install(self, spec, prefix):
       mkdirp(prefix.bin)
       install('foo-tool', prefix.bin)

       mkdirp(prefix.include)
       install('foo.h', prefix.include)

       mkdirp(prefix.lib)
       install('libfoo.a', prefix.lib)


Attributes of this object are created on the fly when you request them,
so any of the following will work:

======================  =======================
Prefix Attribute        Location
======================  =======================
``prefix.bin``          ``$prefix/bin``
``prefix.lib64``        ``$prefix/lib64``
``prefix.share.man``    ``$prefix/share/man``
``prefix.foo.bar.baz``  ``$prefix/foo/bar/baz``
======================  =======================

Of course, this only works if your file or directory is a valid Python
variable name. If your file or directory contains dashes or dots, use
``join`` instead:

.. code-block:: python

   prefix.lib.join('libz.a')


.. _spec-objects:

------------
Spec objects
------------

When ``install`` is called, most parts of the build process are set up
for you.  The correct version's tarball has been downloaded and
expanded.  Environment variables like ``CC`` and ``CXX`` are set to
point to the correct compiler and version.  An install prefix has
already been selected and passed in as ``prefix``.  In most cases this
is all you need to get ``configure``, ``cmake``, or another install
working correctly.

There will be times when you need to know more about the build
configuration.  For example, some software requires that you pass
special parameters to ``configure``, like
``--with-libelf=/path/to/libelf`` or ``--with-mpich``.  You might also
need to supply special compiler flags depending on the compiler.  All
of this information is available in the spec.

^^^^^^^^^^^^^^^^^^^^^^^^
Testing spec constraints
^^^^^^^^^^^^^^^^^^^^^^^^

You can test whether your spec is configured a certain way by using
the ``satisfies`` method.  For example, if you want to check whether
the package's version is in a particular range, you can use specs to
do that, e.g.:

.. code-block:: python

   configure_args = [
       '--prefix={0}'.format(prefix)
   ]

   if spec.satisfies('@1.2:1.4'):
       configure_args.append("CXXFLAGS='-DWITH_FEATURE'")

   configure(*configure_args)

This works for compilers, too:

.. code-block:: python

   if spec.satisfies('%gcc'):
       configure_args.append('CXXFLAGS="-g3 -O3"')
   if spec.satisfies('%intel'):
       configure_args.append('CXXFLAGS="-xSSE2 -fast"')

Or for combinations of spec constraints:

.. code-block:: python

   if spec.satisfies('@1.2%intel'):
       tty.error("Version 1.2 breaks when using Intel compiler!")

You can also do similar satisfaction tests for dependencies:

.. code-block:: python

   if spec.satisfies('^dyninst@8.0'):
       configure_args.append('CXXFLAGS=-DSPECIAL_DYNINST_FEATURE')

This could allow you to easily work around a bug in a particular
dependency version.

You can use ``satisfies()`` to test for particular dependencies,
e.g. ``foo.satisfies('^openmpi@1.2')`` or ``foo.satisfies('^mpich')``,
or you can use Python's built-in ``in`` operator:

.. code-block:: python

   if 'libelf' in spec:
       print "this package depends on libelf"

This is useful for virtual dependencies, as you can easily see what
implementation was selected for this build:

.. code-block:: python

   if 'openmpi' in spec:
       configure_args.append('--with-openmpi')
   elif 'mpich' in spec:
       configure_args.append('--with-mpich')
   elif 'mvapich' in spec:
       configure_args.append('--with-mvapich')

It's also a bit more concise than satisfies.  The difference between
the two functions is that ``satisfies()`` tests whether spec
constraints overlap at all, while ``in`` tests whether a spec or any
of its dependencies satisfy the provided spec.

^^^^^^^^^^^^^^^^^^^^^^^
Architecture specifiers
^^^^^^^^^^^^^^^^^^^^^^^

As mentioned in :ref:`support-for-microarchitectures` each node in a concretized spec
object has an architecture attribute which is a triplet of ``platform``, ``os`` and ``target``.
Each of these three items can be queried to take decisions when configuring, building or
installing a package.

""""""""""""""""""""""""""""""""""""""""""""""
Querying the platform and the operating system
""""""""""""""""""""""""""""""""""""""""""""""

Sometimes the actions to be taken to install a package might differ depending on the
platform we are installing for. If that is the case we can use conditionals:

.. code-block:: python

   if spec.platform == 'darwin':
       # Actions that are specific to Darwin
       args.append('--darwin-specific-flag')

and branch based on the current spec platform. If we need to make a package directive
conditional on the platform we can instead employ the usual spec syntax and pass the
corresponding constraint to the appropriate argument of that directive:

.. code-block:: python

   class Libnl(AutotoolsPackage):

       conflicts('platform=darwin', msg='libnl requires FreeBSD or Linux')

Similar considerations are also valid for the ``os`` part of a spec's architecture.
For instance:

.. code-block:: python

   class Glib(AutotoolsPackage)

       patch('old-kernels.patch', when='os=centos6')

will apply the patch only when the operating system is Centos 6.

.. note::

   Even though experienced Python programmers might recognize that there are other ways
   to retrieve information on the platform:

   .. code-block:: python

      if sys.platform == 'darwin':
          # Actions that are specific to Darwin
          args.append('--darwin-specific-flag')

   querying the spec architecture's platform should be considered the preferred. The key difference
   is that a query on ``sys.platform``, or anything similar, is always bound to the host on which the
   interpreter running Spack is located and as such it won't work correctly in environments where
   cross-compilation is required.

"""""""""""""""""""""""""""""""""""""
Querying the target microarchitecture
"""""""""""""""""""""""""""""""""""""

The third item of the architecture tuple is the ``target`` which abstracts the information on the
CPU microarchitecture. A list of all the targets known to Spack can be obtained via the
command line:

.. command-output:: spack arch --known-targets

Within directives each of the names above can be used to match a particular target:

.. code-block:: python

   class Julia(Package):
       # This patch is only applied on icelake microarchitectures
       patch("icelake.patch", when="target=icelake")

It's also possible to select all the architectures belonging to the same family
using an open range:

.. code-block:: python

   class Julia(Package):
       # This patch is applied on all x86_64 microarchitectures.
       # The trailing colon that denotes an open range of targets
       patch("generic_x86_64.patch", when="target=x86_64:")

in a way that resembles what was shown in :ref:`versions-and-fetching` for versions.
Where ``target`` objects really shine though is when they are used in methods
called at configure, build or install time. In that case we can test targets
for supported features, for instance:

.. code-block:: python

   if 'avx512' in spec.target:
       args.append('--with-avx512')

The snippet above will append the ``--with-avx512`` item to a list of arguments only if the corresponding
feature is supported by the current target. Sometimes we need to take different actions based
on the architecture family and not on the specific microarchitecture. In those cases
we can check the ``family`` attribute:

.. code-block:: python

   if spec.target.family == 'ppc64le':
       args.append('--enable-power')

Possible values for the ``family`` attribute are displayed by ``spack arch --known-targets``
under the "Generic architectures (families)" header.
Finally it's possible to perform actions based on whether the current microarchitecture
is compatible with a known one:

.. code-block:: python

   if spec.target > 'haswell':
       args.append('--needs-at-least-haswell')

The snippet above will add an item to a list of configure options only if the current
architecture is a superset of ``haswell`` or, said otherwise, only if the current
architecture is a later microarchitecture still compatible with ``haswell``.

.. admonition:: Using Spack on unknown microarchitectures

   If Spack is used on an unknown microarchitecture it will try to perform a best match
   of the features it detects and will select the closest microarchitecture it has
   information for. In case nothing matches, it will create on the fly a new generic
   architecture. This is done to allow users to still be able to use Spack
   for their work. The software built won't be probably as optimized as it could but just
   as you need a newer compiler to build for newer architectures, you may need newer
   versions of Spack for new architectures to be correctly labeled.

^^^^^^^^^^^^^^^^^^^^^^
Accessing Dependencies
^^^^^^^^^^^^^^^^^^^^^^

You may need to get at some file or binary that's in the installation
prefix of one of your dependencies. You can do that by sub-scripting
the spec:

.. code-block:: python

   spec['mpi']

The value in the brackets needs to be some package name, and spec
needs to depend on that package, or the operation will fail.  For
example, the above code will fail if the ``spec`` doesn't depend on
``mpi``.  The value returned is itself just another ``Spec`` object,
so you can do all the same things you would do with the package's
own spec:

.. code-block:: python

   spec['mpi'].prefix.bin
   spec['mpi'].version

.. _multimethods:

^^^^^^^^^^^^^^^^^^^^^^^^^^
Multimethods and ``@when``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack allows you to make multiple versions of instance functions in
packages, based on whether the package's spec satisfies particular
criteria.

The ``@when`` annotation lets packages declare multiple versions of
methods like ``install()`` that depend on the package's spec.  For
example:

.. code-block:: python

   class SomePackage(Package):
       ...

       def install(self, prefix):
           # Do default install

       @when('arch=chaos_5_x86_64_ib')
       def install(self, prefix):
           # This will be executed instead of the default install if
           # the package's sys_type() is chaos_5_x86_64_ib.

       @when('arch=linux-debian7-x86_64')
       def install(self, prefix):
           # This will be executed if the package's sys_type() is
           # linux-debian7-x86_64.

In the above code there are three versions of ``install()``, two of which
are specialized for particular platforms.  The version that is called
depends on the architecture of the package spec.

Note that this works for methods other than install, as well.  So,
if you only have part of the install that is platform specific, you
could do something more like this:

.. code-block:: python

   class SomePackage(Package):
      ...
       # virtual dependence on MPI.
       # could resolve to mpich, mpich2, OpenMPI
       depends_on('mpi')

       def setup(self):
           # do nothing in the default case
           pass

       @when('^openmpi')
       def setup(self):
           # do something special when this is built with OpenMPI for
           # its MPI implementations.

       def install(self, prefix):
           # Do common install stuff
           self.setup()
           # Do more common install stuff

You can write multiple ``@when`` specs that satisfy the package's spec,
for example:

.. code-block:: python

   class SomePackage(Package):
       ...
       depends_on('mpi')

       def setup_mpi(self):
           # the default, called when no @when specs match
           pass

       @when('^mpi@3:')
       def setup_mpi(self):
           # this will be called when mpi is version 3 or higher
           pass

       @when('^mpi@2:')
       def setup_mpi(self):
           # this will be called when mpi is version 2 or higher
           pass

       @when('^mpi@1:')
       def setup_mpi(self):
           # this will be called when mpi is version 1 or higher
           pass

In situations like this, the first matching spec, in declaration order
will be called.  As before, if no ``@when`` spec matches, the default
method (the one without the ``@when`` decorator) will be called.

.. warning::

   The default version of decorated methods must **always** come
   first.  Otherwise it will override all of the platform-specific
   versions.  There's not much we can do to get around this because of
   the way decorators work.

.. _compiler-wrappers:

---------------------
Compiler wrappers
---------------------

As mentioned, ``CC``, ``CXX``, ``F77``, and ``FC`` are set to point to
Spack's compiler wrappers.  These are simply called ``cc``, ``c++``,
``f77``, and ``f90``, and they live in ``$SPACK_ROOT/lib/spack/env``.

``$SPACK_ROOT/lib/spack/env`` is added first in the ``PATH``
environment variable when ``install()`` runs so that system compilers
are not picked up instead.

All of these compiler wrappers point to a single compiler wrapper
script that figures out which *real* compiler it should be building
with.  This comes either from spec `concretization
<abstract-and-concrete>`_ or from a user explicitly asking for a
particular compiler using, e.g., ``%intel`` on the command line.

In addition to invoking the right compiler, the compiler wrappers add
flags to the compile line so that dependencies can be easily found.
These flags are added for each dependency, if they exist:

Compile-time library search paths
* ``-L$dep_prefix/lib``
* ``-L$dep_prefix/lib64``

Runtime library search paths (RPATHs)
* ``$rpath_flag$dep_prefix/lib``
* ``$rpath_flag$dep_prefix/lib64``

Include search paths
* ``-I$dep_prefix/include``

An example of this would be the ``libdwarf`` build, which has one
dependency: ``libelf``.  Every call to ``cc`` in the ``libdwarf``
build will have ``-I$LIBELF_PREFIX/include``,
``-L$LIBELF_PREFIX/lib``, and ``$rpath_flag$LIBELF_PREFIX/lib``
inserted on the command line.  This is done transparently to the
project's build system, which will just think it's using a system
where ``libelf`` is readily available.  Because of this, you **do
not** have to insert extra ``-I``, ``-L``, etc. on the command line.

Another useful consequence of this is that you often do *not* have to
add extra parameters on the ``configure`` line to get autotools to
find dependencies.  The ``libdwarf`` install method just calls
configure like this:

.. code-block:: python

   configure("--prefix=" + prefix)

Because of the ``-L`` and ``-I`` arguments, configure will
successfully find ``libdwarf.h`` and ``libdwarf.so``, without the
packager having to provide ``--with-libdwarf=/path/to/libdwarf`` on
the command line.

.. note::

    For most compilers, ``$rpath_flag`` is ``-Wl,-rpath,``. However, NAG
    passes its flags to GCC instead of passing them directly to the linker.
    Therefore, its ``$rpath_flag`` is doubly wrapped: ``-Wl,-Wl,,-rpath,``.
    ``$rpath_flag`` can be overridden on a compiler specific basis in
    ``lib/spack/spack/compilers/$compiler.py``.

The compiler wrappers also pass the compiler flags specified by the user from
the command line (``cflags``, ``cxxflags``, ``fflags``, ``cppflags``, ``ldflags``,
and/or ``ldlibs``). They do not override the canonical autotools flags with the
same names (but in ALL-CAPS) that may be passed into the build by particularly
challenging package scripts.

---------------------
MPI support in Spack
---------------------

It is common for high performance computing software/packages to use the
Message Passing Interface ( ``MPI``).  As a result of conretization, a
given package can be built using different implementations of MPI such as
``Openmpi``, ``MPICH`` or ``IntelMPI``.  That is, when your package
declares that it ``depends_on('mpi')``, it can be built with any of these
``mpi`` implementations. In some scenarios, to configure a package, one
has to provide it with appropriate MPI compiler wrappers such as
``mpicc``, ``mpic++``.  However different implementations of ``MPI`` may
have different names for those wrappers.

Spack provides an idiomatic way to use MPI compilers in your package.  To
use MPI wrappers to compile your whole build, do this in your
``install()`` method:

.. code-block:: python

   env['CC'] = spec['mpi'].mpicc
   env['CXX'] = spec['mpi'].mpicxx
   env['F77'] = spec['mpi'].mpif77
   env['FC'] = spec['mpi'].mpifc

That's all.  A longer explanation of why this works is below.

We don't try to force any particular build method on packagers.  The
decision to use MPI wrappers depends on the way the package is written,
on common practice, and on "what works".  Loosely, There are three types
of MPI builds:

  1. Some build systems work well without the wrappers and can treat MPI
     as an external library, where the person doing the build has to
     supply includes/libs/etc.  This is fairly uncommon.

  2. Others really want the wrappers and assume you're using an MPI
     "compiler" – i.e., they have no mechanism to add MPI
     includes/libraries/etc.

  3. CMake's ``FindMPI`` needs the compiler wrappers, but it uses them to
     extract ``–I`` / ``-L`` / ``-D`` arguments, then treats MPI like a
     regular library.

Note that some CMake builds fall into case 2 because they either don't
know about or don't like CMake's ``FindMPI`` support – they just assume
an MPI compiler. Also, some autotools builds fall into case 3 (e.g. `here
is an autotools version of CMake's FindMPI
<https://github.com/tgamblin/libra/blob/master/m4/lx_find_mpi.m4>`_).

Given all of this, we leave the use of the wrappers up to the packager.
Spack will support all three ways of building MPI packages.

^^^^^^^^^^^^^^^^^^^^^
Packaging Conventions
^^^^^^^^^^^^^^^^^^^^^

As mentioned above, in the ``install()`` method, ``CC``, ``CXX``,
``F77``, and ``FC`` point to Spack's wrappers around the chosen compiler.
Spack's wrappers are not the MPI compiler wrappers, though they do
automatically add ``–I``, ``–L``, and ``–Wl,-rpath`` args for
dependencies in a similar way.  The MPI wrappers are a bit different in
that they also add ``-l`` arguments for the MPI libraries, and some add
special ``-D`` arguments to trigger build options in MPI programs.

For case 1 above, you generally don't need to do more than patch your
Makefile or add configure args as you normally would.

For case 3, you don't need to do much of anything, as Spack puts the MPI
compiler wrappers in the PATH, and the build will find them and
interrogate them.

For case 2, things are a bit more complicated, as you'll need to tell the
build to use the MPI compiler wrappers instead of Spack's compiler
wrappers.  All it takes some lines like this:

.. code-block:: python

   env['CC'] = spec['mpi'].mpicc
   env['CXX'] = spec['mpi'].mpicxx
   env['F77'] = spec['mpi'].mpif77
   env['FC'] = spec['mpi'].mpifc

Or, if you pass CC, CXX, etc. directly to your build with, e.g.,
`--with-cc=<path>`, you'll want to substitute `spec['mpi'].mpicc` in
there instead, e.g.:

.. code-block:: python

   configure('—prefix=%s' % prefix,
             '—with-cc=%s' % spec['mpi'].mpicc)

Now, you may think that doing this will lose the includes, library paths,
and RPATHs that Spack's compiler wrapper get you, but we've actually set
things up so that the MPI compiler wrappers use Spack's compiler wrappers
when run from within Spack. So using the MPI wrappers should really be as
simple as the code above.

^^^^^^^^^^^^^^^^^^^^^
``spec['mpi']``
^^^^^^^^^^^^^^^^^^^^^

Ok, so how does all this work?

If your package has a virtual dependency like ``mpi``, then referring to
``spec['mpi']`` within ``install()`` will get you the concrete ``mpi``
implementation in your dependency DAG.  That is a spec object just like
the one passed to install, only the MPI implementations all set some
additional properties on it to help you out.  E.g., in mvapich2, you'll
find this:

.. literalinclude:: _spack_root/var/spack/repos/builtin/packages/mvapich2/package.py
   :pyobject: Mvapich2.setup_dependent_package

That code allows the mvapich2 package to associate an ``mpicc`` property
with the ``mvapich2`` node in the DAG, so that dependents can access it.
``openmpi`` and ``mpich`` do similar things.  So, no matter what MPI
you're using, spec['mpi'].mpicc gets you the location of the MPI
compilers. This allows us to have a fairly simple polymorphic interface
for information about virtual dependencies like MPI.

^^^^^^^^^^^^^^^^^^^^^
Wrapping wrappers
^^^^^^^^^^^^^^^^^^^^^

Spack likes to use its own compiler wrappers to make it easy to add
``RPATHs`` to builds, and to try hard to ensure that your builds use the
right dependencies.  This doesn't play nicely by default with MPI, so we
have to do a couple tricks.

  1. If we build MPI with Spack's wrappers, mpicc and friends will be
     installed with hard-coded paths to Spack's wrappers, and using them
     from outside of Spack will fail because they only work within Spack.
     To fix this, we patch mpicc and friends to use the regular
     compilers.  Look at the filter_compilers method in mpich, openmpi,
     or mvapich2 for details.

  2. We still want to use the Spack compiler wrappers when Spack is
     calling mpicc. Luckily, wrappers in all mainstream MPI
     implementations provide environment variables that allow us to
     dynamically set the compiler to be used by mpicc, mpicxx, etc.
     Denis pasted some code from this below – Spack's build environment
     sets ``MPICC``, ``MPICXX``, etc. for mpich derivatives and
     ``OMPI_CC``, ``OMPI_CXX``, etc. for OpenMPI. This makes the MPI
     compiler wrappers use the Spack compiler wrappers so that your
     dependencies still get proper RPATHs even if you use the MPI
     wrappers.

^^^^^^^^^^^^^^^^^^^^^
MPI on Cray machines
^^^^^^^^^^^^^^^^^^^^^

The Cray programming environment notably uses ITS OWN compiler wrappers,
which function like MPI wrappers.  On Cray systems, the ``CC``, ``cc``,
and ``ftn`` wrappers ARE the MPI compiler wrappers, and it's assumed that
you'll use them for all of your builds.  So on Cray we don't bother with
``mpicc``, ``mpicxx``, etc, Spack MPI implementations set
``spec['mpi'].mpicc`` to point to Spack's wrappers, which wrap the Cray
wrappers, which wrap the regular compilers and include MPI flags.  That
may seem complicated, but for packagers, that means the same code for
using MPI wrappers will work, even on even on a Cray:

.. code-block:: python

   env['CC'] = spec['mpi'].mpicc

This is because on Cray, ``spec['mpi'].mpicc`` is just ``spack_cc``.

.. _sanity-checks:

------------------------
Checking an installation
------------------------

By default, Spack assumes that a build has failed if nothing is
written to the install prefix, and that it has succeeded if anything
(a file, a directory, etc.)  is written to the install prefix after
``install()`` completes.

Consider a simple autotools build like this:

.. code-block:: python

   def install(self, spec, prefix):
       configure("--prefix={0}".format(prefix))
       make()
       make("install")

If you are using using standard autotools or CMake, ``configure`` and
``make`` will not write anything to the install prefix.  Only ``make
install`` writes the files, and only once the build is already
complete.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``sanity_check_is_file`` and ``sanity_check_is_dir``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unfortunately, many builds of scientific
software modify the install prefix *before* ``make install``. Builds
like this can falsely report that they were successfully installed if
an error occurs before the install is complete but after files have
been written to the ``prefix``.

You can optionally specify *sanity checks* to deal with this problem.
Add properties like this to your package:

.. code-block:: python

   class MyPackage(Package):
       ...

       sanity_check_is_file = ['include/libelf.h']
       sanity_check_is_dir  = [lib]

       def install(self, spec, prefix):
           configure("--prefix=" + prefix)
           make()
           make("install")

Now, after ``install()`` runs, Spack will check whether
``$prefix/include/libelf.h`` exists and is a file, and whether
``$prefix/lib`` exists and is a directory.  If the checks fail, then
the build will fail and the install prefix will be removed.  If they
succeed, Spack considers the build successful and keeps the prefix in
place.

^^^^^^^^^^^^^^^^
Build-time tests
^^^^^^^^^^^^^^^^

Sometimes packages finish to build "correctly" and issues with their run-time
behavior are discovered only at a later stage, maybe after a full software stack
relying on them has already been built. To avoid situations of that kind it's possible
to write build-time tests that will be executed only if the option ``--run-tests``
of ``spack install`` has been activated.

The proper way to write these tests is relying on two decorators that come with
any base class listed in :ref:`installation_procedure`.

.. code-block:: python

   @run_after('build')
   @on_package_attributes(run_tests=True)
   def check_build(self):
        # Custom implementation goes here
        pass

The first decorator ``run_after('build')`` schedules this
function to be invoked after the ``build`` phase has been executed, while the
second one makes the invocation  conditional on the fact that ``self.run_tests == True``.
It is also possible to schedule a function to be invoked *before* a given phase
using the ``run_before`` decorator.

.. note::

    Default implementations for build-time tests

        Packages that are built using specific build systems may already have a
        default implementation for build-time tests. For instance :py:class:`~.AutotoolsPackage`
        based packages will try to invoke ``make test`` and ``make check`` if
        Spack is asked to run tests.
        More information on each class is available in the the :py:mod:`~.spack.build_systems`
        documentation.

.. warning::

    The API for adding tests is not yet considered stable and may change drastically in future releases.

.. _cmd-spack-test:

^^^^^^^^^^^^^
Install Tests
^^^^^^^^^^^^^

.. warning::

   The API for adding and running install tests is not yet considered
   stable and may change drastically in future releases. Packages with
   install tests will be refactored to match changes to the API.

While build tests are integrated with the build system, install tests
are for testing package installations independent of the build process.

Install tests are executed in a test stage directory that defaults to
``~/.spack/test``. You can change the location in the high-level ``config``
by adding the ``test_stage`` path as follows:

.. code-block:: yaml

   config:
     test_stage: /path/to/stage

""""""""""""""""""""
Adding install tests
""""""""""""""""""""

Install tests are added to a package by defining a ``test`` method
with the following signature:

.. code-block:: python

   def test(self):

These tests run in an environment that provides access to the
package and all of its dependencies, including ``test``-type
dependencies.

Standard python ``assert`` statements and other error reporting
mechanisms can be used in the ``test`` method. Spack will report
such errors as test failures.

You can implement multiple tests (or test parts) within the ``test``
method, where each is run separately and testing continues after
failures by using the ``run_test`` method. The signature for the
method is:

.. code-block:: python

   def run_test(self, exe, options=[], expected=[], status=0, installed=False,
                purpose='', skip_missing=False, work_dir=None):

The test fails if there is no executable named ``exe`` found in the
paths of the ``PATH`` variable **unless** ``skip_missing`` is ``True``.
The test also fails if the resulting path is not within the prefix of
the package being tested when ``installed`` is ``True``.

The executable runs in ``work_dir``, when specified, using the provided
``options``. The return code is checked against the ``status`` argument,
which can be an integer or list of integers representing status codes
corresponding to successful execution (e.g. ``status=[0,3,7]``).
Spack also checks that every string in ``expected`` is a regex matching
part of the output from the test run (e.g.
``expected=['completed successfully', 'converged in']``). Default behavior
is to behave as though ``status=[0]`` and ``expected=[]`` are specified.

Output from the test is written to its log file. The ``purpose`` argument
serves as the heading in text logs to highlight the start of each test part.

"""""""""""""""""""""""""
Enabling test compilation
"""""""""""""""""""""""""

Some tests may require access to the compiler with which the package
was built, especially to test library-only packages. You must enable
loading the package's compiler configuration by setting the attribute
``test_requires_compiler`` to ``True``. Doing so makes the compiler
available in the test environment through the canonical environment
variables (``CC``, ``CXX``, ``FC``, ``F77``).

"""""""""""""""""""""""
Adding build-time files
"""""""""""""""""""""""

.. note::

    We highly recommend the re-use of build-time tests and input files
    for testing installed software.  These files are easier to keep
    synchronized with the software than creating custom install tests.

You can use the ``cache_extra_test_sources`` method copy directories
and or files from the build stage directory to the package's installation
directory.

For example, a package method for copying everything in the ``tests``
subdirectory plus the ``foo.c`` and ``bar.c`` files from ``examples``
can be implemented as follows:

.. code-block:: python

   @run_after('install')
   def cache_test_sources(self):
       srcs = ['tests', 'examples/foo.c', 'examples/bar.c']
       self.cache_extra_test_sources(srcs)

The use of the ``run_after`` directive ensures the associated files
are copied **after** the package is installed during the build process.

The method copies files to the package's metadata directory under
the ``self.install_test_root``. All files in the package source's
``tests`` directory for the example above will be copied to the
``join_path(self.install_test_root, 'tests')`` directory. The two
files listed under the staged ``examples`` directory will be copied
to the ``join_path(self.install_test_root, 'examples')`` directory.

.. note::

    While source and input files are generally recommended, binaries
    may also be cached by the build process for install testing.

"""""""""""""""""""
Adding custom files
"""""""""""""""""""

Some tests may require additional files not available from the build.
Examples include:

- test source files
- test input files
- test build scripts
- expected test output

These extra files should be added to the ``test`` subdirectory of the
package in the repository. Spack will automaticaly copy any files in
that directory to the test staging directory during install testing.
The ``test`` method can access those files from the
``self.test_suite.current_test_data_dir`` directory.

.. _cmd-spack-test-list:

"""""""""""""""""""
``spack test list``
"""""""""""""""""""

Packages available for install testing can be found using the
``spack test list`` command. The command outputs all installed
packages that have defined ``test`` methods.

.. _cmd-spack-test-run:

""""""""""""""""""
``spack test run``
""""""""""""""""""

Install tests can be run for one or more installed packages using
the ``spack test run`` command. A ``test suite`` is created from
the provided specs.  If no specs are provided it will test all specs
in the active environment or all specs installed in Spack if no
environment is active.

Test suites can be named using the ``--alias`` option. Unaliased
Test suites will use the content hash of their specs as their name.

Some of the more commonly used debugging options are:

- ``--fail-fast`` stops testing each package after the first failure
- ``--fail-first`` stops testing packages after the first failure

Test output is written to a text log file by default but ``junit``
and ``cdash`` are outputs are available through the ``--log-format``
option.

.. _cmd-spack-test-results:

""""""""""""""""""""""
``spack test results``
""""""""""""""""""""""

The ``spack test results`` command shows results for all completed
test suites. Providing the alias or content hash limits reporting
to the corresponding test suite.

The ``--logs`` option includes the output generated by the associated
test(s) to facilitate debugging.

The ``--failed`` option limits results shown to that of the failed
tests, if any, of matching packages.

.. _cmd-spack-test-find:

"""""""""""""""""""
``spack test find``
"""""""""""""""""""

The ``spack test find`` command lists the aliases or content hashes
of all test suites whose results are available.

.. _cmd-spack-test-remove:

"""""""""""""""""""""
``spack test remove``
"""""""""""""""""""""

The ``spack test remove`` command removes test suites to declutter
the test results directory. You are prompted to confirm the removal
of each test suite **unless** you use the ``--yes-to-all`` option.

.. _file-manipulation:

---------------------------
File manipulation functions
---------------------------

Many builds are not perfect. If a build lacks an install target, or if
it does not use systems like CMake or autotools, which have standard
ways of setting compilers and options, you may need to edit files or
install some files yourself to get them working with Spack.

You can do this with standard Python code, and Python has rich
libraries with functions for file manipulation and filtering.  Spack
also provides a number of convenience functions of its own to make
your life even easier.  These functions are described in this section.

All of the functions in this section can be included by simply
running:

.. code-block:: python

   from spack import *

This is already part of the boilerplate for packages created with
``spack create``.

^^^^^^^^^^^^^^^^^^^
Filtering functions
^^^^^^^^^^^^^^^^^^^

:py:func:`filter_file(regex, repl, *filenames, **kwargs) <spack.filter_file>`
  Works like ``sed`` but with Python regular expression syntax.  Takes
  a regular expression, a replacement, and a set of files.  ``repl``
  can be a raw string or a callable function.  If it is a raw string,
  it can contain ``\1``, ``\2``, etc. to refer to capture groups in
  the regular expression.  If it is a callable, it is passed the
  Python ``MatchObject`` and should return a suitable replacement
  string for the particular match.

  Examples:

  #. Filtering a Makefile to force it to use Spack's compiler wrappers:

     .. code-block:: python

        filter_file(r'^CC\s*=.*',  spack_cc,  'Makefile')
        filter_file(r'^CXX\s*=.*', spack_cxx, 'Makefile')
        filter_file(r'^F77\s*=.*', spack_f77, 'Makefile')
        filter_file(r'^FC\s*=.*',  spack_fc,  'Makefile')

  #. Replacing ``#!/usr/bin/perl`` with ``#!/usr/bin/env perl`` in ``bib2xhtml``:

     .. code-block:: python

        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl', prefix.bin.bib2xhtml)

  #. Switching the compilers used by ``mpich``'s MPI wrapper scripts from
     ``cc``, etc. to the compilers used by the Spack build:

     .. code-block:: python

        filter_file('CC="cc"', 'CC="%s"' % self.compiler.cc,
                    prefix.bin.mpicc)

        filter_file('CXX="c++"', 'CXX="%s"' % self.compiler.cxx,
                    prefix.bin.mpicxx)

:py:func:`change_sed_delimiter(old_delim, new_delim, *filenames) <spack.change_sed_delim>`
    Some packages, like TAU, have a build system that can't install
    into directories with, e.g. '@' in the name, because they use
    hard-coded ``sed`` commands in their build.

    ``change_sed_delimiter`` finds all ``sed`` search/replace commands
    and change the delimiter.  e.g., if the file contains commands
    that look like ``s///``, you can use this to change them to
    ``s@@@``.

    Example of changing ``s///`` to ``s@@@`` in TAU:

    .. code-block:: python

       change_sed_delimiter('@', ';', 'configure')
       change_sed_delimiter('@', ';', 'utils/FixMakefile')
       change_sed_delimiter('@', ';', 'utils/FixMakefile.sed.default')

^^^^^^^^^^^^^^
File functions
^^^^^^^^^^^^^^

:py:func:`ancestor(dir, n=1) <spack.ancestor>`
  Get the n\ :sup:`th` ancestor of the directory ``dir``.

:py:func:`can_access(path) <spack.can_access>`
  True if we can read and write to the file at ``path``.  Same as
  native python ``os.access(file_name, os.R_OK|os.W_OK)``.

:py:func:`install(src, dest) <spack.install>`
  Install a file to a particular location.  For example, install a
  header into the ``include`` directory under the install ``prefix``:

  .. code-block:: python

     install('my-header.h', prefix.include)

:py:func:`join_path(*paths) <spack.join_path>`
  An alias for ``os.path.join``. This joins paths using the OS path separator.

:py:func:`mkdirp(*paths) <spack.mkdirp>`
  Create each of the directories in ``paths``, creating any parent
  directories if they do not exist.

:py:func:`working_dir(dirname, kwargs) <spack.working_dir>`
  This is a Python `Context Manager
  <https://docs.python.org/2/library/contextlib.html>`_ that makes it
  easier to work with subdirectories in builds.  You use this with the
  Python ``with`` statement to change into a working directory, and
  when the with block is done, you change back to the original
  directory.  Think of it as a safe ``pushd`` / ``popd`` combination,
  where ``popd`` is guaranteed to be called at the end, even if
  exceptions are thrown.

  Example usage:

  #. The ``libdwarf`` build first runs ``configure`` and ``make`` in a
     subdirectory called ``libdwarf``.  It then implements the
     installation code itself.  This is natural with ``working_dir``:

     .. code-block:: python

        with working_dir('libdwarf'):
            configure("--prefix=" + prefix, "--enable-shared")
            make()
            install('libdwarf.a',  prefix.lib)

  #. Many CMake builds require that you build "out of source", that
     is, in a subdirectory.  You can handle creating and ``cd``'ing to
     the subdirectory like the LLVM package does:

     .. code-block:: python

        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DLLVM_REQUIRES_RTTI=1',
                  '-DPYTHON_EXECUTABLE=/usr/bin/python',
                  '-DPYTHON_INCLUDE_DIR=/usr/include/python2.6',
                  '-DPYTHON_LIBRARY=/usr/lib64/libpython2.6.so',
                  *std_cmake_args)
            make()
            make("install")

     The ``create=True`` keyword argument causes the command to create
     the directory if it does not exist.

:py:func:`touch(path) <spack.touch>`
  Create an empty file at ``path``.

.. _make-package-findable:

----------------------------------------------------------
Making a package discoverable with ``spack external find``
----------------------------------------------------------

The simplest way to make a package discoverable with
:ref:`spack external find <cmd-spack-external-find>` is to:

1. Define the executables associated with the package
2. Implement a method to determine the versions of these executables

^^^^^^^^^^^^^^^^^
Minimal detection
^^^^^^^^^^^^^^^^^

The first step is fairly simple, as it requires only to
specify a package level ``executables`` attribute:

.. code-block:: python

   class Foo(Package):
       # Each string provided here is treated as a regular expression, and
       # would match for example 'foo', 'foobar', and 'bazfoo'.
       executables = ['foo']

This attribute must be a list of strings. Each string is a regular
expression (e.g. 'gcc' would match 'gcc', 'gcc-8.3', 'my-weird-gcc', etc.) to
determine a set of system executables that might be part or this package. Note
that to match only executables named 'gcc' the regular expression ``'^gcc$'``
must be used.

Finally to determine the version of each executable the ``determine_version``
method must be implemented:

.. code-block:: python

   @classmethod
   def determine_version(cls, exe):
       """Return either the version of the executable passed as argument
       or ``None`` if the version cannot be determined.

       Args:
           exe (str): absolute path to the executable being examined
       """

This method receives as input the path to a single executable and must return
as output its version as a string; if the user cannot determine the version
or determines that the executable is not an instance of the package, they can
return None and the exe will be discarded as a candidate.
Implementing the two steps above is mandatory, and gives the package the
basic ability to detect if a spec is present on the system at a given version.

.. note::
   Any executable for which the ``determine_version`` method returns ``None``
   will be discarded and won't appear in later stages of the workflow described below.

^^^^^^^^^^^^^^^^^^^^^^^^
Additional functionality
^^^^^^^^^^^^^^^^^^^^^^^^

Besides the two mandatory steps described above, there are also optional
methods that can be implemented to either increase the amount of details
being detected or improve the robustness of the detection logic in a package.

""""""""""""""""""""""""""""""
Variants and custom attributes
""""""""""""""""""""""""""""""

The ``determine_variants`` method can be optionally implemented in a package
to detect additional details of the spec:

.. code-block:: python

   @classmethod
   def determine_variants(cls, exes, version_str):
       """Return either a variant string, a tuple of a variant string
       and a dictionary of extra attributes that will be recorded in
       packages.yaml or a list of those items.

       Args:
           exes (list of str): list of executables (absolute paths) that
               live in the same prefix and share the same version
           version_str (str): version associated with the list of
               executables, as detected by ``determine_version``
       """

This method takes as input a list of executables that live in the same prefix and
share the same version string, and returns either:

1. A variant string
2. A tuple of a variant string and a dictionary of extra attributes
3. A list of items matching either 1 or 2 (if multiple specs are detected
   from the set of executables)

If extra attributes are returned, they will be recorded in ``packages.yaml``
and be available for later reuse. As an example, the ``gcc`` package will record
by default the different compilers found and an entry in ``packages.yaml``
would look like:

.. code-block:: yaml

   packages:
     gcc:
       externals:
       - spec: 'gcc@9.0.1 languages=c,c++,fortran'
         prefix: /usr
         extra_attributes:
           compilers:
             c: /usr/bin/x86_64-linux-gnu-gcc-9
             c++: /usr/bin/x86_64-linux-gnu-g++-9
             fortran: /usr/bin/x86_64-linux-gnu-gfortran-9

This allows us, for instance, to keep track of executables that would be named
differently if built by Spack (e.g. ``x86_64-linux-gnu-gcc-9``
instead of just ``gcc``).

.. TODO: we need to gather some more experience on overriding 'prefix'
   and other special keywords in extra attributes, but as soon as we are
   confident that this is the way to go we should document the process.
   See https://github.com/spack/spack/pull/16526#issuecomment-653783204

"""""""""""""""""""""""""""
Filter matching executables
"""""""""""""""""""""""""""

Sometimes defining the appropriate regex for the ``executables``
attribute might prove to be difficult, especially if one has to
deal with corner cases or exclude "red herrings". To help keeping
the regular expressions as simple as possible, each package can
optionally implement a ``filter_executables`` method:

.. code-block:: python

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        """Return a filtered list of the executables in prefix"""

which takes as input a prefix and a list of matching executables and
returns a filtered list of said executables.

Using this method has the advantage of allowing custom logic for
filtering, and does not restrict the user to regular expressions
only.  Consider the case of detecting the GNU C++ compiler. If we
try to search for executables that match ``g++``, that would have
the unwanted side effect of selecting also ``clang++`` - which is
a C++ compiler provided by another package - if present on the system.
Trying to select executables that contain ``g++`` but not ``clang``
would be quite complicated to do using regex only. Employing the
``filter_detected_exes`` method it becomes:

.. code-block:: python

   class Gcc(Package):
      executables = ['g++']

      def filter_detected_exes(cls, prefix, exes_in_prefix):
         return [x for x in exes_in_prefix if 'clang' not in x]

Another possibility that this method opens is to apply certain
filtering logic when specific conditions are met (e.g. take some
decisions on an OS and not on another).

^^^^^^^^^^^^^^^^^^
Validate detection
^^^^^^^^^^^^^^^^^^

To increase detection robustness, packagers may also implement a method
to validate the detected Spec objects:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Validate a detected spec. Raise an exception if validation fails."""

This method receives a detected spec along with its extra attributes and can be
used to check that certain conditions are met by the spec. Packagers can either
use assertions or raise an ``InvalidSpecDetected`` exception when the check fails.
In case the conditions are not honored the spec will be discarded and any message
associated with the assertion or the exception will be logged as the reason for
discarding it.

As an example, a package that wants to check that the ``compilers`` attribute is
in the extra attributes can implement this method like this:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Check that 'compilers' is in the extra attributes."""
       msg = ('the extra attribute "compilers" must be set for '
              'the detected spec "{0}"'.format(spec))
       assert 'compilers' in extra_attributes, msg

or like this:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Check that 'compilers' is in the extra attributes."""
       if 'compilers' not in extra_attributes:
           msg = ('the extra attribute "compilers" must be set for '
                  'the detected spec "{0}"'.format(spec))
           raise InvalidSpecDetected(msg)

.. _determine_spec_details:

^^^^^^^^^^^^^^^^^^^^^^^^^
Custom detection workflow
^^^^^^^^^^^^^^^^^^^^^^^^^

In the rare case when the mechanisms described so far don't fit the
detection of a package, the implementation of all the methods above
can be disregarded and instead a custom ``determine_spec_details``
method can be implemented directly in the package class (note that
the definition of the ``executables`` attribute is still required):

.. code-block:: python

   @classmethod
   def determine_spec_details(cls, prefix, exes_in_prefix):
       # exes_in_prefix = a set of paths, each path is an executable
       # prefix = a prefix that is common to each path in exes_in_prefix

       # return None or [] if none of the exes represent an instance of
       # the package. Return one or more Specs for each instance of the
       # package which is thought to be installed in the provided prefix

This method takes as input a set of discovered executables (which match
those specified by the user) as well as a common prefix shared by all
of those executables. The function must return one or more :py:class:`spack.spec.Spec` associated
with the executables (it can also return ``None`` to indicate that no
provided executables are associated with the package).

As an example, consider a made-up package called ``foo-package`` which
builds an executable called ``foo``. ``FooPackage`` would appear as
follows:

.. code-block:: python

   class FooPackage(Package):
       homepage = "..."
       url = "..."

       version(...)

       # Each string provided here is treated as a regular expression, and
       # would match for example 'foo', 'foobar', and 'bazfoo'.
       executables = ['foo']

       @classmethod
       def determine_spec_details(cls, prefix, exes_in_prefix):
           candidates = list(x for x in exes_in_prefix
                             if os.path.basename(x) == 'foo')
           if not candidates:
               return
           # This implementation is lazy and only checks the first candidate
           exe_path = candidates[0]
           exe = Executable(exe_path)
           output = exe('--version', output=str, error=str)
           version_str = ...  # parse output for version string
           return Spec.from_detection(
               'foo-package@{0}'.format(version_str)
           )

.. _package-lifecycle:

-----------------------------
Style guidelines for packages
-----------------------------

The following guidelines are provided, in the interests of making
Spack packages work in a consistent manner:

^^^^^^^^^^^^^
Variant Names
^^^^^^^^^^^^^

Spack packages with variants similar to already-existing Spack
packages should use the same name for their variants.  Standard
variant names are:

  ======= ======== ========================
  Name    Default   Description
  ======= ======== ========================
  shared   True     Build shared libraries
  mpi      True     Use MPI
  python   False    Build Python extension
  ======= ======== ========================

If specified in this table, the corresponding default should be used
when declaring a variant.

The semantics of the `shared` variant are important. When a package is
built `~shared`, the package guarantees that no shared libraries are
built. When a package is built `+shared`, the package guarantees that
shared libraries are built, but it makes no guarantee about whether
static libraries are built.

^^^^^^^^^^^^^
Version Lists
^^^^^^^^^^^^^

Spack packages should list supported versions with the newest first.

---------------------------
Packaging workflow commands
---------------------------

When you are building packages, you will likely not get things
completely right the first time.

The ``spack install`` command performs a number of tasks before it
finally installs each package.  It downloads an archive, expands it in
a temporary directory, and only then gives control to the package's
``install()`` method.  If the build doesn't go as planned, you may
want to clean up the temporary directory, or if the package isn't
downloading properly, you might want to run *only* the ``fetch`` stage
of the build.

Spack performs best-effort installation of package dependencies by default,
which means it will continue to install as many dependencies as possible
after detecting failures.  If you are trying to install a package with a
lot of dependencies where one or more may fail to build, you might want to
try the ``--fail-fast`` option to stop the installation process on the first
failure.

A typical package workflow might look like this:

.. code-block:: console

   $ spack edit mypackage
   $ spack install --fail-fast mypackage
   ... build breaks! ...
   $ spack clean mypackage
   $ spack edit mypackage
   $ spack install --fail-fast mypackage
   ... repeat clean/install until install works ...

Below are some commands that will allow you some finer-grained
control over the install process.

.. _cmd-spack-fetch:

^^^^^^^^^^^^^^^
``spack fetch``
^^^^^^^^^^^^^^^

The first step of ``spack install``.  Takes a spec and determines the
correct download URL to use for the requested package version, then
downloads the archive, checks it against an MD5 checksum, and stores
it in a staging directory if the check was successful.  The staging
directory will be located under the first writable directory in the
``build_stage`` configuration setting.

When run after the archive has already been downloaded, ``spack
fetch`` is idempotent and will not download the archive again.

.. _cmd-spack-stage:

^^^^^^^^^^^^^^^
``spack stage``
^^^^^^^^^^^^^^^

The second step in ``spack install`` after ``spack fetch``.  Expands
the downloaded archive in its temporary directory, where it will be
built by ``spack install``.  Similar to ``fetch``, if the archive has
already been expanded,  ``stage`` is idempotent.

.. _cmd-spack-patch:

^^^^^^^^^^^^^^^
``spack patch``
^^^^^^^^^^^^^^^

After staging, Spack applies patches to downloaded packages, if any
have been specified in the package file.  This command will run the
install process through the fetch, stage, and patch phases.  Spack
keeps track of whether patches have already been applied and skips
this step if they have been.  If Spack discovers that patches didn't
apply cleanly on some previous run, then it will restage the entire
package before patching.

.. _cmd-spack-restage:

^^^^^^^^^^^^^^^^^
``spack restage``
^^^^^^^^^^^^^^^^^

Restores the source code to pristine state, as it was before building.

Does this in one of two ways:

#. If the source was fetched as a tarball, deletes the entire build
   directory and re-expands the tarball.

#. If the source was checked out from a repository, this deletes the
   build directory and checks it out again.

.. _cmd-spack-clean:

^^^^^^^^^^^^^^^
``spack clean``
^^^^^^^^^^^^^^^

Cleans up Spack's temporary and cached files.  This command can be used to
recover disk space if temporary files from interrupted or failed installs
accumulate.

When called with ``--stage`` or without arguments this removes all staged
files.

The ``--downloads`` option removes cached :ref:`cached <caching>` downloads.

You can force the removal of all install failure tracking markers using the
``--failures`` option.  Note that ``spack install`` will automatically clear
relevant failure markings prior to performing the requested installation(s).

Long-lived caches, like the virtual package index, are removed using the
``--misc-cache`` option.

The ``--python-cache`` option removes `.pyc`, `.pyo`, and `__pycache__`
folders.

To remove all of the above, the command can be called with ``--all``.

When called with positional arguments, this command cleans up temporary files
only for a particular package. If ``fetch``, ``stage``, or ``install``
are run again after this, Spack's build process will start from scratch.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Keeping the stage directory on success
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, ``spack install`` will delete the staging area once a
package has been successfully built and installed.  Use
``--keep-stage`` to leave the build directory intact:

.. code-block:: console

   $ spack install --keep-stage <spec>

This allows you to inspect the build directory and potentially debug
the build.  You can use ``clean`` later to get rid of the
unwanted temporary files.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Keeping the install prefix on failure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, ``spack install`` will delete any partially constructed
install prefix if anything fails during ``install()``.  If you want to
keep the prefix anyway (e.g. to diagnose a bug), you can use
``--keep-prefix``:

.. code-block:: console

   $ spack install --keep-prefix <spec>

Note that this may confuse Spack into thinking that the package has
been installed properly, so you may need to use ``spack uninstall --force``
to get rid of the install prefix before you build again:

.. code-block:: console

   $ spack uninstall --force <spec>

---------------------
Graphing dependencies
---------------------

.. _cmd-spack-graph:

^^^^^^^^^^^^^^^
``spack graph``
^^^^^^^^^^^^^^^

Spack provides the ``spack graph`` command for graphing dependencies.
The command by default generates an ASCII rendering of a spec's
dependency graph.  For example:

.. command-output:: spack graph hdf5

At the top is the root package in the DAG, with dependency edges emerging
from it.  On a color terminal, the edges are colored by which dependency
they lead to.

.. command-output:: spack graph --deptype=link hdf5

The ``deptype`` argument tells Spack what types of dependencies to graph.
By default it includes link and run dependencies but not build
dependencies.  Supplying ``--deptype=link`` will show only link
dependencies.  The default is ``--deptype=all``, which is equivalent to
``--deptype=build,link,run,test``.  Options for ``deptype`` include:

* Any combination of ``build``, ``link``, ``run``, and ``test`` separated
  by commas.
* ``all`` for all types of dependencies.

You can also use ``spack graph`` to generate graphs in the widely used
`Dot <http://www.graphviz.org/doc/info/lang.html>`_ format.  For example:

.. command-output:: spack graph --dot hdf5

This graph can be provided as input to other graphing tools, such as
those in `Graphviz <http://www.graphviz.org>`_.  If you have graphviz
installed, you can write straight to PDF like this:

.. code-block:: console

   $ spack graph --dot hdf5 | dot -Tpdf > hdf5.pdf

.. _packaging-shell-support:

-------------------------
Interactive shell support
-------------------------

Spack provides some limited shell support to make life easier for
packagers.  You can enable these commands by sourcing a setup file in
the ``share/spack`` directory.  For ``bash`` or ``ksh``, run:

.. code-block:: sh

   export SPACK_ROOT=/path/to/spack
   . $SPACK_ROOT/share/spack/setup-env.sh

For ``csh`` and ``tcsh`` run:

.. code-block:: csh

   setenv SPACK_ROOT /path/to/spack
   source $SPACK_ROOT/share/spack/setup-env.csh

``spack cd`` will then be available.

.. _cmd-spack-cd:

^^^^^^^^^^^^
``spack cd``
^^^^^^^^^^^^

``spack cd`` allows you to quickly cd to pertinent directories in Spack.
Suppose you've staged a package but you want to modify it before you
build it:

.. code-block:: console

   $ spack stage libelf
   ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.13.tar.gz
   ######################################################################## 100.0%
   ==> Staging archive: ~/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3 arch=linux-debian7-x86_64/libelf-0.8.13.tar.gz
   ==> Created stage in ~/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3 arch=linux-debian7-x86_64.
   $ spack cd libelf
   $ pwd
   ~/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3 arch=linux-debian7-x86_64/libelf-0.8.13

``spack cd`` here changed the current working directory to the
directory containing the expanded ``libelf`` source code.  There are a
number of other places you can cd to in the spack directory hierarchy:

.. command-output:: spack cd --help

Some of these change directory into package-specific locations (stage
directory, install directory, package directory) and others change to
core spack locations.  For example, ``spack cd --module-dir`` will take you to
the main python source directory of your spack install.

.. _cmd-spack-build-env:

^^^^^^^^^^^^^^^^^^^
``spack build-env``
^^^^^^^^^^^^^^^^^^^

``spack build-env`` functions much like the standard unix ``build-env``
command, but it takes a spec as an argument.  You can use it to see the
environment variables that will be set when a particular build runs,
for example:

.. code-block:: console

   $ spack build-env mpileaks@1.1%intel

This will display the entire environment that will be set when the
``mpileaks@1.1%intel`` build runs.

To run commands in a package's build environment, you can simply
provide them after the spec argument to ``spack build-env``:

.. code-block:: console

   $ spack cd mpileaks@1.1%intel
   $ spack build-env mpileaks@1.1%intel ./configure

This will cd to the build directory and then run ``configure`` in the
package's build environment.

.. _cmd-spack-location:

^^^^^^^^^^^^^^^^^^
``spack location``
^^^^^^^^^^^^^^^^^^

``spack location`` is the same as ``spack cd`` but it does not require
shell support.  It simply prints out the path you ask for, rather than
cd'ing to it.  In bash, this:

.. code-block:: console

   $ cd $(spack location --build-dir <spec>)

is the same as:

.. code-block:: console

   $ spack cd --build-dir <spec>

``spack location`` is intended for use in scripts or makefiles that
need to know where packages are installed.  e.g., in a makefile you
might write:

.. code-block:: makefile

   DWARF_PREFIX = $(spack location --install-dir libdwarf)
   CXXFLAGS += -I$DWARF_PREFIX/include
   CXXFLAGS += -L$DWARF_PREFIX/lib
