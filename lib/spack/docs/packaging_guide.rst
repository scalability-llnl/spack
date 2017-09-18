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

---------------------
Versions and fetching
---------------------

The most straightforward way to add new versions to your package is to
add a line like this in the package class:

.. code-block:: python
   :linenos:

   class Foo(Package):
       url = 'http://example.com/foo-1.0.tar.gz'
       version('8.2.1', '4136d7b4c04df68b686570afa26988ac')
       ...

Versions should be listed with the newest version first.

^^^^^^^^^^^^^
Date Versions
^^^^^^^^^^^^^

If you wish to use dates as versions, it is best to use the format
``@date-yyyy-mm-dd``.  This will ensure they sort in the correct
order.  If you want your date versions to be numeric (assuming they
don't conflict with other numeric versions), you can use just
``yyyy.mm.dd``.

Alternately, you might use a hybrid release-version / date scheme.
For example, ``@1.3.2016.08.31`` would mean the version from the
``1.3`` branch, as of August 31, 2016.

^^^^^^^^^^^^
Version URLs
^^^^^^^^^^^^

By default, each version's URL is extrapolated from the ``url`` field
in the package.  For example, Spack is smart enough to download
version ``8.2.1.`` of the ``Foo`` package above from
http://example.com/foo-8.2.1.tar.gz.

If the URL is particularly complicated or changes based on the release,
you can override the default URL generation algorithm by defining your
own ``url_for_version()`` function. For example, the download URL for
OpenMPI contains the major.minor version in one spot and the
major.minor.patch version in another:

https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.1.tar.bz2

In order to handle this, you can define a ``url_for_version()`` function
like so:

.. literalinclude:: ../../../var/spack/repos/builtin/packages/openmpi/package.py
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
*verbatim* and does not perform extrapolation.

^^^^^^^^^^^^^^^^^^^^^
PyPI and version URLs
^^^^^^^^^^^^^^^^^^^^^

In addition to their developer websites, many python packages are hosted at the
`Python Package Index (PyPi) <https://pypi.python.org/pypi>`_. Although links to
these individual files are typically `generated using a hash
<https://bitbucket.org/pypa/pypi/issues/438>`_ it is often possible to find a
reliable link of the format

.. code-block:: sh

  https://pypi.python.org/packages/source/<first letter of package>/<package>/<package>-<version>.<extension>

Packages hosted on GitHub and the like are often developer versions that do not
contain all of the files (e.g. configuration scripts) necessary to support
compilation. For this reason it is ideal to link to a repository such as PyPi
if possible.

More recently, sources are being indexed at `pypi.io <https://pypi.io>`_ as
well. Links obtained from this site follow a similar pattern, namely

.. code-block:: sh

  https://pypi.io/packages/source/<first letter of package>/<package>/<package>-<version>.<extension>

These links currently redirect back to `pypi.python.org
<https://pypi.python.org>`_, but this `may change in the future
<https://bitbucket.org/pypa/pypi/issues/438#comment-27243225>`_.


^^^^^^^^^^^^^^^^^^^^^^^^
Skipping the expand step
^^^^^^^^^^^^^^^^^^^^^^^^

Spack normally expands archives (e.g. `*.tar.gz` and `*.zip`) automatically
after downloading them. If you want to skip this step (e.g., for
self-extracting executables and other custom archive types), you can add
``expand=False`` to a ``version`` directive.

.. code-block:: python

   version('8.2.1', '4136d7b4c04df68b686570afa26988ac',
           url='http://example.com/foo-8.2.1-special-version.tar.gz', expand=False)

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

^^^^^^^^^^^^^^^^
Download caching
^^^^^^^^^^^^^^^^

Spack maintains a cache (described :ref:`here <caching>`) which saves files
retrieved during package installations to avoid re-downloading in the case that
a package is installed with a different specification (but the same version) or
reinstalled on account of a change in the hashing scheme.

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
The following rules determine the sort order of numeric
vs. non-numeric versions:

#. The non-numeric versions ``@develop`` is considered greatest (newest).

#. Numeric versions are all less than ``@develop`` version, and are
   sorted numerically.

#. All other non-numeric versions are less than numeric versions, and
   are sorted alphabetically.

The logic behind this sort order is two-fold:

#. Non-numeric versions are usually used for special cases while
   developing or debugging a piece of software.  Keeping most of them
   less than numeric versions ensures that Spack choose numeric
   versions by default whenever possible.

#. The most-recent development version of a package will usually be
   newer than any released numeric versions.  This allows the
   ``develop`` version to satisfy dependencies like ``depends_on(abc,
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

^^^^^^^^^^^^^
``spack md5``
^^^^^^^^^^^^^

If you have one or more files to checksum, you can use the ``spack md5``
command to do it:

.. code-block:: console

   $ spack md5 foo-8.2.1.tar.gz foo-8.2.2.tar.gz
   ==> 2 MD5 checksums:
   4136d7b4c04df68b686570afa26988ac  foo-8.2.1.tar.gz
   1586b70a49dfe05da5fcc29ef239dce0  foo-8.2.2.tar.gz

``spack md5`` also accepts one or more URLs and automatically downloads
the files for you:

.. code-block:: console

   $ spack md5 http://example.com/foo-8.2.1.tar.gz
   ==> Trying to fetch from http://example.com/foo-8.2.1.tar.gz
   ######################################################################## 100.0%
   ==> 1 MD5 checksum:
   4136d7b4c04df68b686570afa26988ac  foo-8.2.1.tar.gz

Doing this for lots of files, or whenever a new package version is
released, is tedious.  See ``spack checksum`` below for an automated
version of this process.

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

   How many would you like to checksum? (default is 5, q to abort)

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
       list_depth = 2

By default, Spack only looks at the top-level page available at
``list_url``.  ``list_depth`` tells it to follow up to 2 levels of
links from the top-level page.  Note that here, this implies two
levels of subdirectories, as the ``mpich`` website is structured much
like a filesystem.  But ``list_depth`` really refers to link depth
when spidering the page.

.. _vcs-fetch:

-------------------------------
Fetching from code repositories
-------------------------------

For some packages, source code is provided in a Version Control System
(VCS) repository rather than in a tarball.  Spack can fetch packages
from VCS repositories. Currently, Spack supports fetching with `Git
<git-fetch_>`_, `Mercurial (hg) <hg-fetch_>`_, and `Subversion (SVN)
<svn-fetch_>`_.

To fetch a package from a source repository, you add a ``version()``
call to your package with parameters indicating the repository URL and
any branch, tag, or revision to fetch.  See below for the parameters
you'll need for each VCS system.

.. _git-fetch:

^^^
Git
^^^

Git fetching is enabled with the following parameters to ``version``:

* ``git``: URL of the git repository.
* ``tag``: name of a tag to fetch.
* ``branch``: name of a branch to fetch.
* ``commit``: SHA hash (or prefix) of a commit to fetch.
* ``submodules``: Also fetch submodules recursively when checking out this repository.

Only one of ``tag``, ``branch``, or ``commit`` can be used at a time.

Default branch
  To fetch a repository's default branch:

  .. code-block:: python

     class Example(Package):
         ...
         version('develop', git='https://github.com/example-project/example.git')

  This download method is untrusted, and is not recommended.

Tags
  To fetch from a particular tag, use the ``tag`` parameter along with
  ``git``:

  .. code-block:: python

     version('1.0.1', git='https://github.com/example-project/example.git',
             tag='v1.0.1')

  This download method is untrusted, and is not recommended.

Branches
  To fetch a particular branch, use ``branch`` instead:

  .. code-block:: python

     version('experimental', git='https://github.com/example-project/example.git',
             branch='experimental')

  This download method is untrusted, and is not recommended.

Commits
  Finally, to fetch a particular commit, use ``commit``:

  .. code-block:: python

     version('2014-10-08', git='https://github.com/example-project/example.git',
             commit='9d38cd4e2c94c3cea97d0e2924814acc')

  This doesn't have to be a full hash; you can abbreviate it as you'd
  expect with git:

  .. code-block:: python

     version('2014-10-08', git='https://github.com/example-project/example.git',
             commit='9d38cd')

  This download method *is trusted*.  It is the recommended way to
  securely download from a Git repository.

  It may be useful to provide a saner version for commits like this,
  e.g. you might use the date as the version, as done above.  Or you
  could just use the abbreviated commit hash.  It's up to the package
  author to decide what makes the most sense.

Submodules

  You can supply ``submodules=True`` to cause Spack to fetch submodules
  recursively along with the repository at fetch time. For more information
  about git submodules see the manpage of git: ``man git-submodule``.

  .. code-block:: python

     version('1.0.1', git='https://github.com/example-project/example.git',
             tag='v1.0.1', submodules=True)


.. _github-fetch:

^^^^^^
GitHub
^^^^^^

If a project is hosted on GitHub, *any* valid Git branch, tag or hash
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

Fetching with mercurial works much like `git <git-fetch>`_, but you
use the ``hg`` parameter.

Default
  Add the ``hg`` parameter with no ``revision``:

  .. code-block:: python

     version('develop', hg='https://jay.grs.rwth-aachen.de/hg/example')

  This download method is untrusted, and is not recommended.

Revisions
  Add ``hg`` and ``revision`` parameters:

  .. code-block:: python

     version('1.0', hg='https://jay.grs.rwth-aachen.de/hg/example',
             revision='v1.0')

  This download method is untrusted, and is not recommended.

  Unlike ``git``, which has special parameters for different types of
  revisions, you can use ``revision`` for branches, tags, and commits
  when you fetch with Mercurial.

As with git, you can fetch these versions using the ``spack install
example@<version>`` command-line syntax.

.. _svn-fetch:

^^^^^^^^^^
Subversion
^^^^^^^^^^

To fetch with subversion, use the ``svn`` and ``revision`` parameters:

Fetching the head
  Simply add an ``svn`` parameter to ``version``:

  .. code-block:: python

     version('develop', svn='https://outreach.scidac.gov/svn/libmonitor/trunk')

  This download method is untrusted, and is not recommended.

Fetching a revision
  To fetch a particular revision, add a ``revision`` to the
  version call:

  .. code-block:: python

     version('develop', svn='https://outreach.scidac.gov/svn/libmonitor/trunk',
             revision=128)

  This download method is untrusted, and is not recommended.

Subversion branches are handled as part of the directory structure, so
you can check out a branch or tag by changing the ``url``.

-------------------------------------------------
Resources (expanding extra tarballs)
-------------------------------------------------

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

If you supply a URL instead of a filename, you need to supply a checksum,
like this:

.. code-block:: python

   patch('http://www.nwchem-sw.org/images/Tddft_mxvec20.patch.gz',
         md5='f91c6a04df56e228fe946291d2f38c9a')

This directive provides an ``md5`` checksum.  You can use other hashing
algorihtms like ``sha256`` as well.  The patch will be fetched from the
URL, checked, and applied to your source code.  You can use the ``spack
md5`` command to generate a checksum for a patch file.

``patch`` can take two options keyword arguments.  They are:

""""""""""""""""""""""""""""""""""""""
``md5``, ``sha256``, ``sha512``, etc.
""""""""""""""""""""""""""""""""""""""

Use one of these when you supply a patch to be downloaded from a remote
site. The downloaded file will be validated using the given checksum.

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

^^^^^^^^^^^^^^^^^^^^^
Patch functions
^^^^^^^^^^^^^^^^^^^^^

In addition to supplying patch files, you can write a custom function
to patch a package's source.  For example, the ``py-pyside`` package
contains some custom code for tweaking the way the PySide build
handles ``RPATH``:

.. _pyside-patch:

.. literalinclude:: ../../../var/spack/repos/builtin/packages/py-pyside/package.py
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

By default, Spack will invoke ``make()`` with a ``-j <njobs>``
argument, so that builds run in parallel.  It figures out how many
jobs to run by determining how many cores are on the host machine.
Specifically, it uses the number of CPUs reported by Python's
`multiprocessing.cpu_count()
<http://docs.python.org/library/multiprocessing.html#multiprocessing.cpu_count>`_.

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
Version Ranges
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


^^^^^^^^^^^^^^^^
Dependency Types
^^^^^^^^^^^^^^^^

Not all dependencies are created equal, and Spack allows you to specify
exactly what kind of a dependency you need. For example:

.. code-block:: python

   depends_on('cmake', type='build')
   depends_on('py-numpy', type=('build', 'run'))
   depends_on('libelf', type=('build', 'link'))

The following dependency types are available:

* **"build"**: made available during the project's build. The package will
  be added to ``PATH``, the compiler include paths, and ``PYTHONPATH``.
  Other projects which depend on this one will not have these modified
  (building project X doesn't need project Y's build dependencies).
* **"link"**: the project is linked to by the project. The package will be
  added to the current package's ``rpath``.
* **"run"**: the project is used by the project at runtime. The package will
  be added to ``PATH`` and ``PYTHONPATH``.

One of the advantages of the ``build`` dependency type is that although the
dependency needs to be installed in order for the package to be built, it
can be uninstalled without concern afterwards. ``link`` and ``run`` disallow
this because uninstalling the dependency would break the package.

If the dependency type is not specified, Spack uses a default of
``('build', 'link')``. This is the common case for compiler languages.
Non-compiled packages like Python modules commonly use
``('build', 'run')``. This means that the compiler wrappers don't need to
inject the dependency's ``prefix/lib`` directory, but the package needs to
be in ``PATH`` and ``PYTHONPATH`` during the build process and later when
a user wants to run the package.


.. _setup-dependent-environment:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``setup_dependent_environment()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack provides a mechanism for dependencies to provide variables that
can be used in their dependents' build.  Any package can declare a
``setup_dependent_environment()`` function, and this function will be
called before the ``install()`` method of any dependent packages.
This allows dependencies to set up environment variables and other
properties to be used by dependents.

The function declaration should look like this:

.. literalinclude:: ../../../var/spack/repos/builtin/packages/qt/package.py
   :pyobject: Qt.setup_dependent_environment
   :linenos:

Here, the Qt package sets the ``QTDIR`` environment variable so that
packages that depend on a particular Qt installation will find it.

The arguments to this function are:

* **spack_env**: List of environment modifications to be applied when
  the dependent package is built within Spack.
* **run_env**: List of environment modifications to be applied when
  the dependent package is run outside of Spack. These are added to the
  resulting module file.
* **dependent_spec**: The spec of the dependent package about to be
  built. This allows the extendee (self) to query the dependent's state.
  Note that *this* package's spec is available as ``self.spec``.

A good example of using these is in the Python package:

.. literalinclude:: ../../../var/spack/repos/builtin/packages/python/package.py
   :pyobject: Python.setup_dependent_environment
   :linenos:

The first thing that happens here is that the ``python`` command is
inserted into module scope of the dependent.  This allows most python
packages to have a very simple install method, like this:

.. code-block:: python

   def install(self, spec, prefix):
       python('setup.py', 'install', '--prefix={0}'.format(prefix))

Python's ``setup_dependent_environment`` method also sets up some
other variables, creates a directory, and sets up the ``PYTHONPATH``
so that dependent packages can find their dependencies at build time.

.. _packaging_conflicts:

---------
Conflicts
---------

Sometimes packages have known bugs, or limitations, that would prevent them
to build e.g. against other dependencies or with certain compilers. Spack
makes it possible to express such constraints with the ``conflicts`` directive.

Adding the following to a package:

.. code-block:: python

    conflicts('%intel', when='@1.2')

we express the fact that the current package *cannot be built* with the Intel
compiler when we are trying to install version "1.2". The ``when`` argument can
be omitted, in which case the conflict will always be active.
Conflicts are always evaluated after the concretization step has been performed,
and if any match is found a detailed error message is shown to the user.

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

To make a package into an extension, simply add simply add an
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
       variant('python', default=True, description= \
           'Build the Python extension Module')
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

^^^^^^^^^^^^^^^^^^^^^^^^^
Activation & deactivation
^^^^^^^^^^^^^^^^^^^^^^^^^

Spack's ``Package`` class has default ``activate`` and ``deactivate``
implementations that handle symbolically linking extensions' prefixes
into the directory of the parent package.  However, extendable
packages can override these methods to add custom activate/deactivate
logic of their own.  For example, the ``activate`` and ``deactivate``
methods in the Python class use the symbolic linking, but they also
handle details surrounding Python's ``.pth`` files, and other aspects
of Python packaging.

Spack's extensions mechanism is designed to be extensible, so that
other packages (like Ruby, R, Perl, etc.)  can provide their own
custom extension management logic, as they may not handle modules the
same way that Python does.

Let's look at Python's activate function:

.. literalinclude:: ../../../var/spack/repos/builtin/packages/python/package.py
   :pyobject: Python.activate
   :linenos:

This function is called on the *extendee* (Python).  It first calls
``activate`` in the superclass, which handles symlinking the
extension package's prefix into this package's prefix.  It then does
some special handling of the ``easy-install.pth`` file, part of
Python's setuptools.

Deactivate behaves similarly to activate, but it unlinks files:

.. literalinclude:: ../../../var/spack/repos/builtin/packages/python/package.py
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
    | :py:class:`.QMakePackage`     | Specialized class for packages   |
    |                               | build using QMake                |
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

.. literalinclude:: ../../../lib/spack/spack/build_systems/autotools.py
    :pyobject: AutotoolsPackage.configure
    :linenos:

It is thus just sufficient for a packager to override a few
build system specific helper methods or attributes to provide, for instance,
configure arguments:

.. literalinclude::  ../../../var/spack/repos/builtin/packages/m4/package.py
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
can use the :ref:`cmd-spack-env` command, documented
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

.. literalinclude::  ../../../var/spack/repos/builtin/packages/libelf/package.py
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

Compiler flags set by the user through the Spec object can be passed to
the build in one of two ways. For packages inheriting from the
``CmakePackage`` or ``AutotoolsPackage`` classes, the build environment
passes those flags to the relevant environment variables (``CFLAGS``,
``CXXFLAGS``, etc) that are respected by the build system. For all other
packages, the default behavior is to inject the flags directly into the
compiler commands using Spack's compiler wrappers.

Individual packages can override the default behavior for the flag
handling.  Packages can define a ``default_flag_handler`` method that
applies to all sets of flags handled by Spack, or may define
individual methods ``cflags_handler``, ``cxxflags_handler``,
etc. Spack will apply the individual method for a flag set if it
exists, otherwise the ``default_flag_handler`` method if it exists,
and fall back on the default for that package class if neither exists.

These methods are defined on the package class, and take two
parameters in addition to the packages itself. The ``env`` parameter
is an ``EnvironmentModifications`` object that can be used to change
the build environment. The ``flag_val`` parameter is a tuple. Its
first entry is the name of the flag (``cflags``, ``cxxflags``, etc.)
and its second entry is a list of the values for that flag.

There are three primary idioms that can be combined to create whatever
behavior the package requires.

1. The default behavior for packages inheriting from
``AutotoolsPackage`` or ``CmakePackage``.

.. code-block:: python

    def default_flag_handler(self, env, flag_val):
        env.append_flags(flag_val[0].upper(), ' '.join(flag_val[1]))
        return []

2. The default behavior for other packages

.. code-block:: python

    def default_flag_handler(self, env, flag_val):
        return flag_val[1]


3. Packages may have additional flags to add to the build. These flags
can be added to either idiom above. For example:

.. code-block:: python

    def default_flag_handler(self, env, flag_val):
        flags = flag_val[1]
        flags.append('-flag')
        return flags

or

.. code-block:: python

    def default_flag_handler(self, env, flag_val):
        env.append_flags(flag_val[0].upper(), ' '.join(flag_val[1]))
        env.append_flags(flag_val[0].upper(), '-flag')
        return []

Packages may also opt for methods that include aspects of any of the
idioms above. E.g.

.. code-block:: python

    def default_flag_handler(self, env, flag_val):
        flags = []
        if len(flag_val[1]) > 3:
            env.append_flags(flag_val[0].upper(), ' '.join(flag_val[1][3:]))
            flags = flag_val[1][:3]
        else:
            flags = flag_val[1]
        flags.append('-flag')
        return flags

Because these methods can pass values through environment variables,
it is important not to override these variables unnecessarily in other
package methods. In the ``setup_environment`` and
``setup_dependent_environment`` methods, use the ``append_flags``
method of the ``EnvironmentModifications`` class to append values to a
list of flags whenever there is no good reason to override the
existing value. In the ``install`` method and other methods that can
operate on the build environment directly through the ``env``
variable, test for environment variable existance before overriding
values to add compiler flags.

In rare circumstances such as compiling and running small unit tests, a
package developer may need to know what are the appropriate compiler
flags to enable features like ``OpenMP``, ``c++11``, ``c++14`` and
alike. To that end the compiler classes in ``spack`` implement the
following **properties**: ``openmp_flag``, ``cxx11_flag``,
``cxx14_flag``, which can be accessed in a package by
``self.compiler.cxx11_flag`` and alike. Note that the implementation is
such that if a given compiler version does not support this feature, an
error will be produced. Therefore package developers can also use these
properties to assert that a compiler supports the requested feature. This
is handy when a package supports additional variants like

.. code-block:: python

   variant('openmp', default=True, description="Enable OpenMP support.")

^^^^^^^^^^^^^^^^^^^^^^^^^
Blas and Lapack libraries
^^^^^^^^^^^^^^^^^^^^^^^^^

Multiple packages provide implementations of ``Blas`` and ``Lapack``
routines.  The names of the resulting static and/or shared libraries
differ from package to package. In order to make the ``install()`` method
independent of the choice of ``Blas`` implementation, each package which
provides it sets up ``self.spec.blas_libs`` to point to the correct
``Blas`` libraries.  The same applies to packages which provide
``Lapack``. Package developers are advised to use these variables, for
example ``spec['blas'].blas_libs.joined()`` instead of hard-coding them:

.. code-block:: python

   if 'openblas' in spec:
       libs = join_path(spec['blas'].prefix.lib, 'libopenblas.so')
   elif 'intel-mkl' in spec:
       ...

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
``join_path`` instead:

.. code-block:: python

   join_path(prefix.lib, 'libz.a')


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
    ``$rpath_flag`` can be overriden on a compiler specific basis in
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

.. literalinclude:: ../../../var/spack/repos/builtin/packages/mvapich2/package.py
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
  static   True     Build static libraries
  mpi      True     Use MPI
  python   False    Build Python extension
  ======= ======== ========================

If specified in this table, the corresponding default should be used
when declaring a variant.

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

A typical package workflow might look like this:

.. code-block:: console

   $ spack edit mypackage
   $ spack install mypackage
   ... build breaks! ...
   $ spack clean mypackage
   $ spack edit mypackage
   $ spack install mypackage
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
directory will be located under ``$SPACK_HOME/var/spack``.

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

Cleans up all of Spack's temporary and cached files.  This can be used to
recover disk space if temporary files from interrupted or failed installs
accumulate in the staging area.

When called with ``--stage`` or without arguments this removes all staged
files.

When called with ``--downloads`` this will clear all resources
:ref:`cached <caching>` during installs.

When called with ``--user-cache`` this will remove caches in the user home
directory, including cached virtual indices.

To remove all of the above, the command can be called with ``--all``.

When called with positional arguments, cleans up temporary files only
for a particular package. If ``fetch``, ``stage``, or ``install``
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

.. command-output:: spack graph mpileaks

At the top is the root package in the DAG, with dependency edges emerging
from it.  On a color terminal, the edges are colored by which dependency
they lead to.

.. command-output:: spack graph --deptype=all mpileaks

The ``deptype`` argument tells Spack what types of dependencies to graph.
By default it includes link and run dependencies but not build
dependencies.  Supplying ``--deptype=all`` will show the build
dependencies as well.  This is equivalent to
``--deptype=build,link,run``.  Options for ``deptype`` include:

* Any combination of ``build``, ``link``, and ``run`` separated by
  commas.
* ``all`` or ``alldeps`` for all types of dependencies.

The ``--term`` option provides an alternative ``spack graph`` rendering and
interactive search and highlight features. The ``--termprint`` option
provides the same drawing to ``stdout`` (without interactivity):

.. command-output:: spack graph --termprint mpileaks

You can also use ``spack graph`` to generate graphs in the widely used
`Dot <http://www.graphviz.org/doc/info/lang.html>`_ format.  For
example:

.. command-output:: spack graph --dot mpileaks

This graph can be provided as input to other graphing tools, such as
those in `Graphviz <http://www.graphviz.org>`_.

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

.. _cmd-spack-env:

^^^^^^^^^^^^^
``spack env``
^^^^^^^^^^^^^

``spack env`` functions much like the standard unix ``env`` command,
but it takes a spec as an argument.  You can use it to see the
environment variables that will be set when a particular build runs,
for example:

.. code-block:: console

   $ spack env mpileaks@1.1%intel

This will display the entire environment that will be set when the
``mpileaks@1.1%intel`` build runs.

To run commands in a package's build environment, you can simply
provide them after the spec argument to ``spack env``:

.. code-block:: console

   $ spack cd mpileaks@1.1%intel
   $ spack env mpileaks@1.1%intel ./configure

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

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Build System Configuration Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Imagine a developer creating a CMake or Autotools-based project in a
local directory, which depends on libraries A-Z.  Once Spack has
installed those dependencies, one would like to run ``cmake`` with
appropriate command line and environment so CMake can find them.  The
``spack setup`` command does this conveniently, producing a CMake
configuration that is essentially the same as how Spack *would have*
configured the project.  This can be demonstrated with a usage
example:

.. code-block:: console

   $ cd myproject
   $ spack setup myproject@local
   $ mkdir build; cd build
   $ ../spconfig.py ..
   $ make
   $ make install

Notes:

* Spack must have ``myproject/package.py`` in its repository for
  this to work.
* ``spack setup`` produces the executable script ``spconfig.py`` in
  the local directory, and also creates the module file for the
  package.  ``spconfig.py`` is normally run from the user's
  out-of-source build directory.
* The version number given to ``spack setup`` is arbitrary, just
  like ``spack diy``.  ``myproject/package.py`` does not need to
  have any valid downloadable versions listed (typical when a
  project is new).
* spconfig.py produces a CMake configuration that *does not* use the
  Spack wrappers.  Any resulting binaries *will not* use RPATH,
  unless the user has enabled it.  This is recommended for
  development purposes, not production.
* ``spconfig.py`` is human readable, and can serve as a developer
  reference of what dependencies are being used.
* ``make install`` installs the package into the Spack repository,
  where it may be used by other Spack packages.
* CMake-generated makefiles re-run CMake in some circumstances.  Use
  of ``spconfig.py`` breaks this behavior, requiring the developer
  to manually re-run ``spconfig.py`` when a ``CMakeLists.txt`` file
  has changed.

^^^^^^^^^^^^
CMakePackage
^^^^^^^^^^^^

In order to enable ``spack setup`` functionality, the author of
``myproject/package.py`` must subclass from ``CMakePackage`` instead
of the standard ``Package`` superclass.  Because CMake is
standardized, the packager does not need to tell Spack how to run
``cmake; make; make install``.  Instead the packager only needs to
create (optional) methods ``configure_args()`` and ``configure_env()``, which
provide the arguments (as a list) and extra environment variables (as
a dict) to provide to the ``cmake`` command.  Usually, these will
translate variant flags into CMake definitions.  For example:

.. code-block:: python

   def configure_args(self):
       spec = self.spec
       return [
           '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
           '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
           '-DBUILD_GRIDGEN=%s' % ('YES' if '+gridgen' in spec else 'NO'),
           '-DBUILD_COUPLER=%s' % ('YES' if '+coupler' in spec else 'NO'),
           '-DUSE_PISM=%s' % ('YES' if '+pism' in spec else 'NO')
       ]

If needed, a packager may also override methods defined in
``StagedPackage`` (see below).

^^^^^^^^^^^^^
StagedPackage
^^^^^^^^^^^^^

``CMakePackage`` is implemented by subclassing the ``StagedPackage``
superclass, which breaks down the standard ``Package.install()``
method into several sub-stages: ``setup``, ``configure``, ``build``
and ``install``.  Details:

* Instead of implementing the standard ``install()`` method, package
  authors implement the methods for the sub-stages
  ``install_setup()``, ``install_configure()``,
  ``install_build()``, and ``install_install()``.

* The ``spack install`` command runs the sub-stages ``configure``,
  ``build`` and ``install`` in order.  (The ``setup`` stage is
  not run by default; see below).
* The ``spack setup`` command runs the sub-stages ``setup``
  and a dummy install (to create the module file).
* The sub-stage install methods take no arguments (other than
  ``self``).  The arguments ``spec`` and ``prefix`` to the standard
  ``install()`` method may be accessed via ``self.spec`` and
  ``self.prefix``.

^^^^^^^^^^^^^
GNU Autotools
^^^^^^^^^^^^^

The ``setup`` functionality is currently only available for
CMake-based packages.  Extending this functionality to GNU
Autotools-based packages would be easy (and should be done by a
developer who actively uses Autotools).  Packages that use
non-standard build systems can gain ``setup`` functionality by
subclassing ``StagedPackage`` directly.
