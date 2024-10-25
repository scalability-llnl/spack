.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _basic-usage:

===========
Basic Usage
===========

The ``spack`` command has many *subcommands*.  You'll only need a
small subset of them for typical usage.

Note that Spack colorizes output.  ``less -R`` should be used with
Spack to maintain this colorization.  E.g.:

.. code-block:: console

    $ spack find | less -R

It is recommended that the following be put in your ``.bashrc`` file:

.. code-block:: sh

    alias less='less -R'

If you do not see colorized output when using ``less -R`` it is because color
is being disabled in the piped output. In this case, tell spack to force
colorized output with a flag

.. code-block:: console

    $ spack --color always find | less -R

or an environment variable

.. code-block:: console

   $ SPACK_COLOR=always spack find | less -R

--------------------------
Listing available packages
--------------------------

To install software with Spack, you need to know what software is
available.  You can see a list of available package names at the
`packages.spack.io <https://packages.spack.io>`_ website, or
using the ``spack list`` command.

.. _cmd-spack-list:

^^^^^^^^^^^^^^
``spack list``
^^^^^^^^^^^^^^

The ``spack list`` command prints out a list of all of the packages Spack
can install:

.. command-output:: spack list
   :ellipsis: 10

There are thousands of them, so we've truncated the output above, but you
can find a `full list here <https://packages.spack.io>`_.
Packages are listed by name in alphabetical order.
A pattern to match with no wildcards, ``*`` or ``?``,
will be treated as though it started and ended with
``*``, so ``util`` is equivalent to ``*util*``.  All patterns will be treated
as case-insensitive. You can also add the ``-d`` to search the description of
the package in addition to the name.  Some examples:

All packages whose names contain "sql":

.. command-output:: spack list sql

All packages whose names or descriptions contain documentation:

.. command-output:: spack list --search-description documentation

.. _cmd-spack-info:

^^^^^^^^^^^^^^
``spack info``
^^^^^^^^^^^^^^

To get more information on a particular package from `spack list`, use
`spack info`.  Just supply the name of a package:

.. command-output:: spack info --all mpich

Most of the information is self-explanatory.  The *safe versions* are
versions that Spack knows the checksum for, and it will use the
checksum to verify that these versions download without errors or
viruses.

:ref:`Dependencies <sec-specs>` and :ref:`virtual dependencies
<sec-virtual-dependencies>` are described in more detail later.

.. _cmd-spack-versions:

^^^^^^^^^^^^^^^^^^
``spack versions``
^^^^^^^^^^^^^^^^^^

To see *more* available versions of a package, run ``spack versions``.
For example:

.. command-output:: spack versions libelf

There are two sections in the output.  *Safe versions* are versions
for which Spack has a checksum on file.  It can verify that these
versions are downloaded correctly.

In many cases, Spack can also show you what versions are available out
on the web---these are *remote versions*.  Spack gets this information
by scraping it directly from package web pages.  Depending on the
package and how its releases are organized, Spack may or may not be
able to find remote versions.

---------------------------
Installing and uninstalling
---------------------------

.. _cmd-spack-install:

^^^^^^^^^^^^^^^^^
``spack install``
^^^^^^^^^^^^^^^^^

``spack install`` will install any package shown by ``spack list``.
For example, To install the latest version of the ``mpileaks``
package, you might type this:

.. code-block:: console

   $ spack install mpileaks

If ``mpileaks`` depends on other packages, Spack will install the
dependencies first.  It then fetches the ``mpileaks`` tarball, expands
it, verifies that it was downloaded without errors, builds it, and
installs it in its own directory under ``$SPACK_ROOT/opt``. You'll see
a number of messages from Spack, a lot of build output, and a message
that the package is installed.

.. code-block:: console

   $ spack install mpileaks
   ... dependency build output ...
   ==> Installing mpileaks-1.0-ph7pbnhl334wuhogmugriohcwempqry2
   ==> No binary for mpileaks-1.0-ph7pbnhl334wuhogmugriohcwempqry2 found: installing from source
   ==> mpileaks: Executing phase: 'autoreconf'
   ==> mpileaks: Executing phase: 'configure'
   ==> mpileaks: Executing phase: 'build'
   ==> mpileaks: Executing phase: 'install'
   [+] ~/spack/opt/linux-rhel7-broadwell/gcc-8.1.0/mpileaks-1.0-ph7pbnhl334wuhogmugriohcwempqry2

The last line, with the ``[+]``, indicates where the package is
installed.

Add the Spack debug option (one or more times) -- ``spack -d install
mpileaks`` -- to get additional (and even more verbose) output.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Building a specific version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack can also build *specific versions* of a package.  To do this,
just add ``@`` after the package name, followed by a version:

.. code-block:: console

   $ spack install mpich@3.0.4

Any number of versions of the same package can be installed at once
without interfering with each other.  This is good for multi-user
sites, as installing a version that one user needs will not disrupt
existing installations for other users.

In addition to different versions, Spack can customize the compiler,
compile-time options (variants), compiler flags, and platform (for
cross compiles) of an installation.  Spack is unique in that it can
also configure the *dependencies* a package is built with.  For example,
two configurations of the same version of a package, one built with boost
1.39.0, and the other version built with version 1.43.0, can coexist.

This can all be done on the command line using the *spec* syntax.
Spack calls the descriptor used to refer to a particular package
configuration a **spec**.  In the commands above, ``mpileaks`` and
``mpileaks@3.0.4`` are both valid *specs*.  We'll talk more about how
you can use them to customize an installation in :ref:`sec-specs`.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Reusing installed dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, when you run ``spack install``, Spack tries hard to reuse existing installations
as dependencies, either from a local store or from remote buildcaches if configured.
This minimizes unwanted rebuilds of common dependencies, in particular if
you update Spack frequently.

In case you want the latest versions and configurations to be installed instead,
you can add the ``--fresh`` option:

.. code-block:: console

   $ spack install --fresh mpich

Reusing installations in this mode is "accidental", and happening only if
there's a match between existing installations and what Spack would have installed
anyhow.

You can use the ``spack spec -I mpich`` command to see what
will be reused and what will be built before you install.

You can configure Spack to use the ``--fresh`` behavior by default in
``concretizer.yaml``:

.. code-block:: yaml

   concretizer:
     reuse: false

.. _cmd-spack-uninstall:

^^^^^^^^^^^^^^^^^^^
``spack uninstall``
^^^^^^^^^^^^^^^^^^^

To uninstall a package, type ``spack uninstall <package>``.  This will ask
the user for confirmation before completely removing the directory
in which the package was installed.

.. code-block:: console

   $ spack uninstall mpich

If there are still installed packages that depend on the package to be
uninstalled, spack will refuse to uninstall it.

To uninstall a package and every package that depends on it, you may give the
``--dependents`` option.

.. code-block:: console

   $ spack uninstall --dependents mpich

will display a list of all the packages that depend on ``mpich`` and, upon
confirmation, will uninstall them in the right order.

A command like

.. code-block:: console

   $ spack uninstall mpich

may be ambiguous if multiple ``mpich`` configurations are installed.
For example, if both ``mpich@3.0.2`` and ``mpich@3.1`` are installed,
``mpich`` could refer to either one. Because it cannot determine which
one to uninstall, Spack will ask you either to provide a version number
to remove the ambiguity or use the ``--all`` option to uninstall all of
the matching packages.

You may force uninstall a package with the ``--force`` option

.. code-block:: console

   $ spack uninstall --force mpich

but you risk breaking other installed packages. In general, it is safer to
remove dependent packages *before* removing their dependencies or use the
``--dependents`` option.


.. _nondownloadable:

^^^^^^^^^^^^^^^^^^
Garbage collection
^^^^^^^^^^^^^^^^^^

When Spack builds software from sources, if often installs tools that are needed
just to build or test other software. These are not necessary at runtime.
To support cases where removing these tools can be a benefit Spack provides
the ``spack gc`` ("garbage collector") command, which will uninstall all unneeded packages:

.. code-block:: console

   $ spack find
   ==> 24 installed packages
   -- linux-ubuntu18.04-broadwell / gcc@9.0.1 ----------------------
   autoconf@2.69    findutils@4.6.0  libiconv@1.16        libszip@2.1.1  m4@1.4.18    openjpeg@2.3.1  pkgconf@1.6.3  util-macros@1.19.1
   automake@1.16.1  gdbm@1.18.1      libpciaccess@0.13.5  libtool@2.4.6  mpich@3.3.2  openssl@1.1.1d  readline@8.0   xz@5.2.4
   cmake@3.16.1     hdf5@1.10.5      libsigsegv@2.12      libxml2@2.9.9  ncurses@6.1  perl@5.30.0     texinfo@6.5    zlib@1.2.11

   $ spack gc
   ==> The following packages will be uninstalled:

       -- linux-ubuntu18.04-broadwell / gcc@9.0.1 ----------------------
       vn47edz autoconf@2.69    6m3f2qn findutils@4.6.0  ubl6bgk libtool@2.4.6  pksawhz openssl@1.1.1d  urdw22a readline@8.0
       ki6nfw5 automake@1.16.1  fklde6b gdbm@1.18.1      b6pswuo m4@1.4.18      k3s2csy perl@5.30.0     lp5ya3t texinfo@6.5
       ylvgsov cmake@3.16.1     5omotir libsigsegv@2.12  leuzbbh ncurses@6.1    5vmfbrq pkgconf@1.6.3   5bmv4tg util-macros@1.19.1

   ==> Do you want to proceed? [y/N] y

   [ ... ]

   $ spack find
   ==> 9 installed packages
   -- linux-ubuntu18.04-broadwell / gcc@9.0.1 ----------------------
   hdf5@1.10.5  libiconv@1.16  libpciaccess@0.13.5  libszip@2.1.1  libxml2@2.9.9  mpich@3.3.2  openjpeg@2.3.1  xz@5.2.4  zlib@1.2.11

In the example above Spack went through all the packages in the package database
and removed everything that is not either:

1. A package installed upon explicit request of the user
2. A ``link`` or ``run`` dependency, even transitive, of one of the packages at point 1.

You can check :ref:`cmd-spack-find-metadata` to see how to query for explicitly installed packages
or :ref:`dependency-types` for a more thorough treatment of dependency types.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Marking packages explicit or implicit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Spack will mark packages a user installs as explicitly installed,
while all of its dependencies will be marked as implicitly installed. Packages
can be marked manually as explicitly or implicitly installed by using
``spack mark``. This can be used in combination with ``spack gc`` to clean up
packages that are no longer required.

.. code-block:: console

  $ spack install m4
  ==> 29005: Installing libsigsegv
  [...]
  ==> 29005: Installing m4
  [...]

  $ spack install m4 ^libsigsegv@2.11
  ==> 39798: Installing libsigsegv
  [...]
  ==> 39798: Installing m4
  [...]

  $ spack find -d
  ==> 4 installed packages
  -- linux-fedora32-haswell / gcc@10.1.1 --------------------------
  libsigsegv@2.11

  libsigsegv@2.12

  m4@1.4.18
      libsigsegv@2.12

  m4@1.4.18
      libsigsegv@2.11

  $ spack gc
  ==> There are no unused specs. Spack's store is clean.

  $ spack mark -i m4 ^libsigsegv@2.11
  ==> m4@1.4.18 : marking the package implicit

  $ spack gc
  ==> The following packages will be uninstalled:

      -- linux-fedora32-haswell / gcc@10.1.1 --------------------------
      5fj7p2o libsigsegv@2.11  c6ensc6 m4@1.4.18

  ==> Do you want to proceed? [y/N]

In the example above, we ended up with two versions of ``m4`` since they depend
on different versions of ``libsigsegv``. ``spack gc`` will not remove any of
the packages since both versions of ``m4`` have been installed explicitly
and both versions of ``libsigsegv`` are required by the ``m4`` packages.

``spack mark`` can also be used to implement upgrade workflows. The following
example demonstrates how the ``spack mark`` and ``spack gc`` can be used to
only keep the current version of a package installed.

When updating Spack via ``git pull``, new versions for either ``libsigsegv``
or ``m4`` might be introduced. This will cause Spack to install duplicates.
Since we only want to keep one version, we mark everything as implicitly
installed before updating Spack. If there is no new version for either of the
packages, ``spack install`` will simply mark them as explicitly installed and
``spack gc`` will not remove them.

.. code-block:: console

  $ spack install m4
  ==> 62843: Installing libsigsegv
  [...]
  ==> 62843: Installing m4
  [...]

  $ spack mark -i -a
  ==> m4@1.4.18 : marking the package implicit

  $ git pull
  [...]

  $ spack install m4
  [...]
  ==> m4@1.4.18 : marking the package explicit
  [...]

  $ spack gc
  ==> There are no unused specs. Spack's store is clean.

When using this workflow for installations that contain more packages, care
has to be taken to either only mark selected packages or issue ``spack install``
for all packages that should be kept.

You can check :ref:`cmd-spack-find-metadata` to see how to query for explicitly
or implicitly installed packages.

^^^^^^^^^^^^^^^^^^^^^^^^^
Non-Downloadable Tarballs
^^^^^^^^^^^^^^^^^^^^^^^^^

The tarballs for some packages cannot be automatically downloaded by
Spack.  This could be for a number of reasons:

#. The author requires users to manually accept a license agreement
   before downloading (``jdk`` and ``galahad``).

#. The software is proprietary and cannot be downloaded on the open
   Internet.

To install these packages, one must create a mirror and manually add
the tarballs in question to it (see :ref:`mirrors`):

#. Create a directory for the mirror.  You can create this directory
   anywhere you like, it does not have to be inside ``~/.spack``:

   .. code-block:: console

       $ mkdir ~/.spack/manual_mirror

#. Register the mirror with Spack by creating ``~/.spack/mirrors.yaml``:

   .. code-block:: yaml

       mirrors:
         manual: file://~/.spack/manual_mirror

#. Put your tarballs in it.  Tarballs should be named
   ``<package>/<package>-<version>.tar.gz``.  For example:

   .. code-block:: console

       $ ls -l manual_mirror/galahad

       -rw-------. 1 me me 11657206 Jun 21 19:25 galahad-2.60003.tar.gz

#. Install as usual:

   .. code-block:: console

       $ spack install galahad


-------------------------
Seeing installed packages
-------------------------

We know that ``spack list`` shows you the names of available packages,
but how do you figure out which are already installed?

.. _cmd-spack-find:

^^^^^^^^^^^^^^
``spack find``
^^^^^^^^^^^^^^

``spack find`` shows the *specs* of installed packages.  A spec is
like a name, but it has a version, compiler, architecture, and build
options associated with it.  In spack, you can have many installations
of the same package with different specs.

Running ``spack find`` with no arguments lists installed packages:

.. code-block:: console

   $ spack find
   ==> 74 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
   ImageMagick@6.8.9-10  libdwarf@20130729  py-dateutil@2.4.0
   adept-utils@1.0       libdwarf@20130729  py-ipython@2.3.1
   atk@2.14.0            libelf@0.8.12      py-matplotlib@1.4.2
   boost@1.55.0          libelf@0.8.13      py-nose@1.3.4
   bzip2@1.0.6           libffi@3.1         py-numpy@1.9.1
   cairo@1.14.0          libmng@2.0.2       py-pygments@2.0.1
   callpath@1.0.2        libpng@1.6.16      py-pyparsing@2.0.3
   cmake@3.0.2           libtiff@4.0.3      py-pyside@1.2.2
   dbus@1.8.6            libtool@2.4.2      py-pytz@2014.10
   dbus@1.9.0            libxcb@1.11        py-setuptools@11.3.1
   dyninst@8.1.2         libxml2@2.9.2      py-six@1.9.0
   fontconfig@2.11.1     libxml2@2.9.2      python@2.7.8
   freetype@2.5.3        llvm@3.0           qhull@1.0
   gdk-pixbuf@2.31.2     memaxes@0.5        qt@4.8.6
   glib@2.42.1           mesa@8.0.5         qt@5.4.0
   graphlib@2.0.0        mpich@3.0.4        readline@6.3
   gtkplus@2.24.25       mpileaks@1.0       sqlite@3.8.5
   harfbuzz@0.9.37       mrnet@4.1.0        stat@2.1.0
   hdf5@1.8.13           ncurses@5.9        tcl@8.6.3
   icu@54.1              netcdf@4.3.3       tk@src
   jpeg@9a               openssl@1.0.1h     vtk@6.1.0
   launchmon@1.0.1       pango@1.36.8       xcb-proto@1.11
   lcms@2.6              pixman@0.32.6      xz@5.2.0
   libdrm@2.4.33         py-dateutil@2.4.0  zlib@1.2.8

   -- linux-debian7-x86_64 / gcc@4.9.2 --------------------------------
   libelf@0.8.10  mpich@3.0.4

Packages are divided into groups according to their architecture and
compiler.  Within each group, Spack tries to keep the view simple, and
only shows the version of installed packages.

.. _cmd-spack-find-metadata:

""""""""""""""""""""""""""""""""
Viewing more metadata
""""""""""""""""""""""""""""""""

``spack find`` can filter the package list based on the package name,
spec, or a number of properties of their installation status.  For
example, missing dependencies of a spec can be shown with
``--missing``, deprecated packages can be included with
``--deprecated``, packages which were explicitly installed with
``spack install <package>`` can be singled out with ``--explicit`` and
those which have been pulled in only as dependencies with
``--implicit``.

In some cases, there may be different configurations of the *same*
version of a package installed.  For example, there are two
installations of ``libdwarf@20130729`` above.  We can look at them
in more detail using ``spack find --deps``, and by asking only to show
``libdwarf`` packages:

.. code-block:: console

   $ spack find --deps libdwarf
   ==> 2 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       libdwarf@20130729-d9b90962
           ^libelf@0.8.12
       libdwarf@20130729-b52fac98
           ^libelf@0.8.13

Now we see that the two instances of ``libdwarf`` depend on
*different* versions of ``libelf``: 0.8.12 and 0.8.13.  This view can
become complicated for packages with many dependencies.  If you just
want to know whether two packages' dependencies differ, you can use
``spack find --long``:

.. code-block:: console

   $ spack find --long libdwarf
   ==> 2 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
   libdwarf@20130729-d9b90962  libdwarf@20130729-b52fac98

Now the ``libdwarf`` installs have hashes after their names.  These are
hashes over all of the dependencies of each package.  If the hashes
are the same, then the packages have the same dependency configuration.

If you want to know the path where each package is installed, you can
use ``spack find --paths``:

.. code-block:: console

   $ spack find --paths
   ==> 74 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       ImageMagick@6.8.9-10  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/ImageMagick@6.8.9-10-4df950dd
       adept-utils@1.0       ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/adept-utils@1.0-5adef8da
       atk@2.14.0            ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/atk@2.14.0-3d09ac09
       boost@1.55.0          ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/boost@1.55.0
       bzip2@1.0.6           ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/bzip2@1.0.6
       cairo@1.14.0          ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/cairo@1.14.0-fcc2ab44
       callpath@1.0.2        ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/callpath@1.0.2-5dce4318
   ...

You can restrict your search to a particular package by supplying its
name:

.. code-block:: console

   $ spack find --paths libelf
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       libelf@0.8.11  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/libelf@0.8.11
       libelf@0.8.12  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/libelf@0.8.12
       libelf@0.8.13  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/libelf@0.8.13

""""""""""""""""""""""""""""""""
Spec queries
""""""""""""""""""""""""""""""""

``spack find`` actually does a lot more than this.  You can use
*specs* to query for specific configurations and builds of each
package. If you want to find only libelf versions greater than version
0.8.12, you could say:

.. code-block:: console

   $ spack find libelf@0.8.12:
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       libelf@0.8.12  libelf@0.8.13

Finding just the versions of libdwarf built with a particular version
of libelf would look like this:

.. code-block:: console

   $ spack find --long libdwarf ^libelf@0.8.12
   ==> 1 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
   libdwarf@20130729-d9b90962

We can also search for packages that have a certain attribute. For example,
``spack find libdwarf +debug`` will show only installations of libdwarf
with the 'debug' compile-time option enabled.

The full spec syntax is discussed in detail in :ref:`sec-specs`.


""""""""""""""""""""""""""""""""
Machine-readable output
""""""""""""""""""""""""""""""""

If you only want to see very specific things about installed packages,
Spack has some options for you.  ``spack find --format`` can be used to
output only specific fields:

.. code-block:: console

   $ spack find --format "{name}-{version}-{hash}"
   autoconf-2.69-icynozk7ti6h4ezzgonqe6jgw5f3ulx4
   automake-1.16.1-o5v3tc77kesgonxjbmeqlwfmb5qzj7zy
   bzip2-1.0.6-syohzw57v2jfag5du2x4bowziw3m5p67
   bzip2-1.0.8-zjny4jwfyvzbx6vii3uuekoxmtu6eyuj
   cmake-3.15.1-7cf6onn52gywnddbmgp7qkil4hdoxpcb
   ...

or:

.. code-block:: console

   $ spack find --format "{hash:7}"
   icynozk
   o5v3tc7
   syohzw5
   zjny4jw
   7cf6onn
   ...

This uses the same syntax as described in documentation for
:meth:`~spack.spec.Spec.format` -- you can use any of the options there.
This is useful for passing metadata about packages to other command-line
tools.

Alternately, if you want something even more machine readable, you can
output each spec as JSON records using ``spack find --json``.  This will
output metadata on specs and all dependencies as json:

.. code-block:: console

    $ spack find --json sqlite@3.28.0
    [
     {
      "name": "sqlite",
      "hash": "3ws7bsihwbn44ghf6ep4s6h4y2o6eznv",
      "version": "3.28.0",
      "arch": {
       "platform": "darwin",
       "platform_os": "mojave",
       "target": "x86_64"
      },
      "compiler": {
       "name": "apple-clang",
       "version": "10.0.0"
      },
      "namespace": "builtin",
      "parameters": {
       "fts": true,
       "functions": false,
       "cflags": [],
       "cppflags": [],
       "cxxflags": [],
       "fflags": [],
       "ldflags": [],
       "ldlibs": []
      },
      "dependencies": {
       "readline": {
        "hash": "722dzmgymxyxd6ovjvh4742kcetkqtfs",
        "type": [
         "build",
         "link"
        ]
       }
      }
     },
     ...
    ]

You can use this with tools like `jq <https://stedolan.github.io/jq/>`_ to quickly create JSON records
structured the way you want:

.. code-block:: console

    $ spack find --json sqlite@3.28.0 | jq -C '.[] | { name, version, hash }'
    {
      "name": "sqlite",
      "version": "3.28.0",
      "hash": "3ws7bsihwbn44ghf6ep4s6h4y2o6eznv"
    }
    {
      "name": "readline",
      "version": "7.0",
      "hash": "722dzmgymxyxd6ovjvh4742kcetkqtfs"
    }
    {
      "name": "ncurses",
      "version": "6.1",
      "hash": "zvaa4lhlhilypw5quj3akyd3apbq5gap"
    }


^^^^^^^^^^^^^^
``spack diff``
^^^^^^^^^^^^^^

It's often the case that you have two versions of a spec that you need to
disambiguate. Let's say that we've installed two variants of zlib, one with
and one without the optimize variant:

.. code-block:: console

   $ spack install zlib
   $ spack install zlib -optimize

When we do ``spack find`` we see the two versions.

.. code-block:: console

    $ spack find zlib
    ==> 2 installed packages
    -- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
    zlib@1.2.11  zlib@1.2.11


Let's now say that we want to uninstall zlib. We run the command, and hit a problem
real quickly since we have two!

.. code-block:: console

    $ spack uninstall zlib
    ==> Error: zlib matches multiple packages:

        -- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
        efzjziy zlib@1.2.11  sl7m27m zlib@1.2.11

    ==> Error: You can either:
        a) use a more specific spec, or
        b) specify the spec by its hash (e.g. `spack uninstall /hash`), or
        c) use `spack uninstall --all` to uninstall ALL matching specs.

Oh no! We can see from the above that we have two different versions of zlib installed,
and the only difference between the two is the hash. This is a good use case for
``spack diff``, which can easily show us the "diff" or set difference
between properties for two packages. Let's try it out.
Since the only difference we see in the ``spack find`` view is the hash, let's use
``spack diff`` to look for more detail. We will provide the two hashes:

.. code-block:: console

    $ spack diff /efzjziy /sl7m27m
    ==> Warning: This interface is subject to change.

    --- zlib@1.2.11efzjziyc3dmb5h5u5azsthgbgog5mj7g
    +++ zlib@1.2.11sl7m27mzkbejtkrajigj3a3m37ygv4u2
    @@ variant_value @@
    -  zlib optimize False
    +  zlib optimize True


The output is colored, and written in the style of a git diff. This means that you
can copy and paste it into a GitHub markdown as a code block with language "diff"
and it will render nicely! Here is an example:

.. code-block:: md

    ```diff
    --- zlib@1.2.11/efzjziyc3dmb5h5u5azsthgbgog5mj7g
    +++ zlib@1.2.11/sl7m27mzkbejtkrajigj3a3m37ygv4u2
    @@ variant_value @@
    -  zlib optimize False
    +  zlib optimize True
    ```

Awesome! Now let's read the diff. It tells us that our first zlib was built with ``~optimize``
(``False``) and the second was built with ``+optimize`` (``True``). You can't see it in the docs
here, but the output above is also colored based on the content being an addition (+) or
subtraction (-).

This is a small example, but you will be able to see differences for any attributes on the
installation spec. Running ``spack diff A B`` means we'll see which spec attributes are on
``B`` but not on ``A`` (green) and which are on ``A`` but not on ``B`` (red). Here is another
example with an additional difference type, ``version``:

.. code-block:: console

    $ spack diff python@2.7.8 python@3.8.11
    ==> Warning: This interface is subject to change.

    --- python@2.7.8/tsxdi6gl4lihp25qrm4d6nys3nypufbf
    +++ python@3.8.11/yjtseru4nbpllbaxb46q7wfkyxbuvzxx
    @@ variant_value @@
    -  python patches a8c52415a8b03c0e5f28b5d52ae498f7a7e602007db2b9554df28cd5685839b8
    +  python patches 0d98e93189bc278fbc37a50ed7f183bd8aaf249a8e1670a465f0db6bb4f8cf87
    @@ version @@
    -  openssl 1.0.2u
    +  openssl 1.1.1k
    -  python 2.7.8
    +  python 3.8.11

Let's say that we were only interested in one kind of attribute above, ``version``.
We can ask the command to only output this attribute.  To do this, you'd add
the ``--attribute`` for attribute parameter, which defaults to all. Here is how you
would filter to show just versions:

.. code-block:: console

    $ spack diff --attribute version python@2.7.8 python@3.8.11
    ==> Warning: This interface is subject to change.

    --- python@2.7.8/tsxdi6gl4lihp25qrm4d6nys3nypufbf
    +++ python@3.8.11/yjtseru4nbpllbaxb46q7wfkyxbuvzxx
    @@ version @@
    -  openssl 1.0.2u
    +  openssl 1.1.1k
    -  python 2.7.8
    +  python 3.8.11

And you can add as many attributes as you'd like with multiple `--attribute` arguments
(for lots of attributes, you can use ``-a`` for short). Finally, if you want to view the
data as json (and possibly pipe into an output file) just add ``--json``:


.. code-block:: console

    $ spack diff --json python@2.7.8 python@3.8.11


This data will be much longer because along with the differences for ``A`` vs. ``B`` and
``B`` vs. ``A``, the JSON output also showsthe intersection.


------------------------
Using installed packages
------------------------

There are several different ways to use Spack packages once you have
installed them. As you've seen, spack packages are installed into long
paths with hashes, and you need a way to get them into your path. The
easiest way is to use :ref:`spack load <cmd-spack-load>`, which is
described in this section.

Some more advanced ways to use Spack packages include:

* :ref:`environments <environments>`, which you can use to bundle a
  number of related packages to "activate" all at once, and
* :ref:`environment modules <modules>`, which are commonly used on
  supercomputing clusters. Spack generates module files for every
  installation automatically, and you can customize how this is done.

.. _cmd-spack-load:

^^^^^^^^^^^^^^^^^^^^^^^
``spack load / unload``
^^^^^^^^^^^^^^^^^^^^^^^

If you have :ref:`shell support <shell-support>` enabled you can use the
``spack load`` command to quickly get a package on your ``PATH``.

For example this will add the ``mpich`` package built with ``gcc`` to
your path:

.. code-block:: console

   $ spack install mpich %gcc@4.4.7

   # ... wait for install ...

   $ spack load mpich %gcc@4.4.7
   $ which mpicc
   ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/mpich@3.0.4/bin/mpicc

These commands will add appropriate directories to your ``PATH``
and ``MANPATH`` according to the
:ref:`prefix inspections <customize-env-modifications>` defined in your
modules configuration.
When you no longer want to use a package, you can type unload or
unuse similarly:

.. code-block:: console

   $ spack unload mpich %gcc@4.4.7


"""""""""""""""
Ambiguous specs
"""""""""""""""

If a spec used with load/unload or is ambiguous (i.e. more than one
installed package matches it), then Spack will warn you:

.. code-block:: console

   $ spack load libelf
   ==> Error: libelf matches multiple packages.
   Matching packages:
     qmm4kso libelf@0.8.13%gcc@4.4.7 arch=linux-debian7-x86_64
     cd2u6jt libelf@0.8.13%intel@15.0.0 arch=linux-debian7-x86_64
   Use a more specific spec

You can either type the ``spack load`` command again with a fully
qualified argument, or you can add just enough extra constraints to
identify one package.  For example, above, the key differentiator is
that one ``libelf`` is built with the Intel compiler, while the other
used ``gcc``.  You could therefore just type:

.. code-block:: console

   $ spack load libelf %intel

To identify just the one built with the Intel compiler. If you want to be
*very* specific, you can load it by its hash. For example, to load the
first ``libelf`` above, you would run:

.. code-block:: console

   $ spack load /qmm4kso

To see which packages that you have loaded to your environment you would
use ``spack find --loaded``.

.. code-block:: console

    $ spack find --loaded
    ==> 2 installed packages
    -- linux-debian7 / gcc@4.4.7 ------------------------------------
    libelf@0.8.13

    -- linux-debian7 / intel@15.0.0 ---------------------------------
    libelf@0.8.13

You can also use ``spack load --list`` to get the same output, but it
does not have the full set of query options that ``spack find`` offers.

We'll learn more about Spack's spec syntax in :ref:`a later section <sec-specs>`.


.. _extensions:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python packages and virtual environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack can install a large number of Python packages. Their names are
typically prefixed with ``py-``. Installing and using them is no
different from any other package:

.. code-block:: console

   $ spack install py-numpy
   $ spack load py-numpy
   $ python3
   >>> import numpy

The ``spack load`` command sets the ``PATH`` variable so that the right Python
executable is used, and makes sure that ``numpy`` and its dependencies can be
located in the ``PYTHONPATH``.

Spack is different from other Python package managers in that it installs
every package into its *own* prefix. This is in contrast to ``pip``, which
installs all packages into the same prefix, be it in a virtual environment
or not.

For many users, **virtual environments** are more convenient than repeated
``spack load`` commands, particularly when working with multiple Python
packages. Fortunately Spack supports environments itself, which together
with a view are no different from Python virtual environments.

The recommended way of working with Python extensions such as ``py-numpy``
is through :ref:`Environments <environments>`. The following example creates
a Spack environment with ``numpy`` in the current working directory. It also
puts a filesystem view in ``./view``, which is a more traditional combined
prefix for all packages in the environment.

.. code-block:: console

   $ spack env create --with-view view --dir .
   $ spack -e . add py-numpy
   $ spack -e . concretize
   $ spack -e . install

Now you can activate the environment and start using the packages:

.. code-block:: console

   $ spack env activate .
   $ python3
   >>> import numpy

The environment view is also a virtual environment, which is useful if you are
sharing the environment with others who are unfamiliar with Spack. They can
either use the Python executable directly:

.. code-block:: console

   $ ./view/bin/python3
   >>> import numpy

or use the activation script:

.. code-block:: console

   $ source ./view/bin/activate
   $ python3
   >>> import numpy

In general, there should not be much difference between ``spack env activate``
and using the virtual environment. The main advantage of ``spack env activate``
is that it knows about more packages than just Python packages, and it may set
additional runtime variables that are not covered by the virtual environment
activation script.

See :ref:`environments` for a more in-depth description of Spack
environments and customizations to views.


.. _sec-specs:

--------------------
Specs & dependencies
--------------------

We know that ``spack install``, ``spack uninstall``, and other
commands take a package name with an optional version specifier.  In
Spack, that descriptor is called a *spec*.  Spack uses specs to refer
to a particular build configuration (or configurations) of a package.
Specs are more than a package name and a version; you can use them to
specify the compiler, compiler version, architecture, compile options,
and dependency options for a build.  In this section, we'll go over
the full syntax of specs.

Here is an example of a much longer spec than we've seen thus far:

.. code-block:: none

   mpileaks @1.2:1.4 %gcc@4.7.5 +debug -qt target=x86_64 ^callpath @1.1 %gcc@4.7.2

If provided to ``spack install``, this will install the ``mpileaks``
library at some version between ``1.2`` and ``1.4`` (inclusive),
built using ``gcc`` at version 4.7.5 for a generic ``x86_64`` architecture,
with debug options enabled, and without Qt support.  Additionally, it
says to link it with the ``callpath`` library (which it depends on),
and to build callpath with ``gcc`` 4.7.2.  Most specs will not be as
complicated as this one, but this is a good example of what is
possible with specs.

More formally, a spec consists of the following pieces:

* Package name identifier (``mpileaks`` above)
* ``@`` Optional version specifier (``@1.2:1.4``)
* ``%`` Optional compiler specifier, with an optional compiler version
  (``gcc`` or ``gcc@4.7.3``)
* ``+`` or ``-`` or ``~`` Optional variant specifiers (``+debug``,
  ``-qt``, or ``~qt``) for boolean variants. Use ``++`` or ``--`` or
  ``~~`` to propagate variants through the dependencies (``++debug``,
  ``--qt``, or ``~~qt``).
* ``name=<value>`` Optional variant specifiers that are not restricted to
  boolean variants. Use ``name==<value>`` to propagate variant through the
  dependencies.
* ``name=<value>`` Optional compiler flag specifiers. Valid flag names are
  ``cflags``, ``cxxflags``, ``fflags``, ``cppflags``, ``ldflags``, and ``ldlibs``.
  Use ``name==<value>`` to propagate compiler flags through the dependencies.
* ``target=<value> os=<value>`` Optional architecture specifier
  (``target=haswell os=CNL10``)
* ``^`` Dependency specs (``^callpath@1.1``)

There are two things to notice here.  The first is that specs are
recursively defined.  That is, each dependency after ``^`` is a spec
itself.  The second is that everything is optional *except* for the
initial package name identifier.  Users can be as vague or as specific
as they want about the details of building packages, and this makes
spack good for beginners and experts alike.

To really understand what's going on above, we need to think about how
software is structured.  An executable or a library (these are
generally the artifacts produced by building software) depends on
other libraries in order to run.  We can represent the relationship
between a package and its dependencies as a graph.  Here is the full
dependency graph for ``mpileaks``:

.. graphviz::

   digraph {
       mpileaks -> mpich
       mpileaks -> callpath -> mpich
       callpath -> dyninst
       dyninst  -> libdwarf -> libelf
       dyninst  -> libelf
   }

Each box above is a package and each arrow represents a dependency on
some other package.  For example, we say that the package ``mpileaks``
*depends on* ``callpath`` and ``mpich``.  ``mpileaks`` also depends
*indirectly* on ``dyninst``, ``libdwarf``, and ``libelf``, in that
these libraries are dependencies of ``callpath``.  To install
``mpileaks``, Spack has to build all of these packages.  Dependency
graphs in Spack have to be acyclic, and the *depends on* relationship
is directional, so this is a *directed, acyclic graph* or *DAG*.

The package name identifier in the spec is the root of some dependency
DAG, and the DAG itself is implicit.  Spack knows the precise
dependencies among packages, but users do not need to know the full
DAG structure. Each ``^`` in the full spec refers to some dependency
of the root package. Spack will raise an error if you supply a name
after ``^`` that the root does not actually depend on (e.g. ``mpileaks
^emacs@23.3``).

Spack further simplifies things by only allowing one configuration of
each package within any single build.  Above, both ``mpileaks`` and
``callpath`` depend on ``mpich``, but ``mpich`` appears only once in
the DAG.  You cannot build an ``mpileaks`` version that depends on one
version of ``mpich`` *and* on a ``callpath`` version that depends on
some *other* version of ``mpich``.  In general, such a configuration
would likely behave unexpectedly at runtime, and Spack enforces this
to ensure a consistent runtime environment.

The point of specs is to abstract this full DAG from Spack users.  If
a user does not care about the DAG at all, she can refer to mpileaks
by simply writing ``mpileaks``.  If she knows that ``mpileaks``
indirectly uses ``dyninst`` and she wants a particular version of
``dyninst``, then she can refer to ``mpileaks ^dyninst@8.1``.  Spack
will fill in the rest when it parses the spec; the user only needs to
know package names and minimal details about their relationship.

When spack prints out specs, it sorts package names alphabetically to
normalize the way they are displayed, but users do not need to worry
about this when they write specs.  The only restriction on the order
of dependencies within a spec is that they appear *after* the root
package.  For example, these two specs represent exactly the same
configuration:

.. code-block:: none

   mpileaks ^callpath@1.0 ^libelf@0.8.3
   mpileaks ^libelf@0.8.3 ^callpath@1.0

You can put all the same modifiers on dependency specs that you would
put on the root spec.  That is, you can specify their versions,
compilers, variants, and architectures just like any other spec.
Specifiers are associated with the nearest package name to their left.
For example, above, ``@1.1`` and ``%gcc@4.7.2`` associates with the
``callpath`` package, while ``@1.2:1.4``, ``%gcc@4.7.5``, ``+debug``,
``-qt``, and ``target=haswell os=CNL10`` all associate with the ``mpileaks`` package.

In the diagram above, ``mpileaks`` depends on ``mpich`` with an
unspecified version, but packages can depend on other packages with
*constraints* by adding more specifiers.  For example, ``mpileaks``
could depend on ``mpich@1.2:`` if it can only build with version
``1.2`` or higher of ``mpich``.

.. note:: Windows Spec Syntax Caveats
   Windows has a few idiosyncrasies when it comes to the Spack spec syntax and the use of certain shells
   Spack's spec dependency syntax uses the carat (``^``) character, however this is an escape string in CMD
   so it must be escaped with an additional carat (i.e. ``^^``).
   CMD also will attempt to interpret strings with ``=`` characters in them. Any spec including this symbol
   must double quote the string.

   Note: All of these issues are unique to CMD, they can be avoided by using Powershell.

   For more context on these caveats see the related issues: `carat <https://github.com/spack/spack/issues/42833>`_ and `equals <https://github.com/spack/spack/issues/43348>`_

Below are more details about the specifiers that you can add to specs.

.. _version-specifier:

^^^^^^^^^^^^^^^^^
Version specifier
^^^^^^^^^^^^^^^^^

A version specifier ``pkg@<specifier>`` comes after a package name
and starts with ``@``. It can be something abstract that matches
multiple known versions, or a specific version. During concretization,
Spack will pick the optimal version within the spec's constraints
according to policies set for the particular Spack installation.

The version specifier can be *a specific version*, such as ``@=1.0.0`` or
``@=1.2a7``. Or, it can be *a range of versions*, such as ``@1.0:1.5``.
Version ranges are inclusive, so this example includes both ``1.0``
and any ``1.5.x`` version. Version ranges can be unbounded, e.g. ``@:3``
means any version up to and including ``3``. This would include ``3.4``
and ``3.4.2``.  Similarly, ``@4.2:`` means any version above and including
``4.2``.  As a short-hand, ``@3`` is equivalent to the range ``@3:3`` and
includes any version with major version ``3``.

Versions are ordered lexicograpically by its components. For more details
on the order, see :ref:`the packaging guide <version-comparison>`.

Notice that you can distinguish between the specific version ``@=3.2`` and
the range ``@3.2``. This is useful for packages that follow a versioning
scheme that omits the zero patch version number: ``3.2``, ``3.2.1``,
``3.2.2``, etc. In general it is preferable to use the range syntax
``@3.2``, since ranges also match versions with one-off suffixes, such as
``3.2-custom``.

A version specifier can also be a list of ranges and specific versions,
separated by commas.  For example, ``@1.0:1.5,=1.7.1`` matches any version
in the range ``1.0:1.5`` and the specific version ``1.7.1``.

^^^^^^^^^^^^
Git versions
^^^^^^^^^^^^

For packages with a ``git`` attribute, ``git`` references
may be specified instead of a numerical version i.e. branches, tags
and commits. Spack will stage and build based off the ``git``
reference provided.  Acceptable syntaxes for this are:

.. code-block:: sh

    # commit hashes
   foo@abcdef1234abcdef1234abcdef1234abcdef1234    # 40 character hashes are automatically treated as git commits
   foo@git.abcdef1234abcdef1234abcdef1234abcdef1234

    # branches and tags
   foo@git.develop # use the develop branch
   foo@git.0.19 # use the 0.19 tag

Spack always needs to associate a Spack version with the git reference,
which is used for version comparison. This Spack version is heuristically
taken from the closest valid git tag among ancestors of the git ref.

Once a Spack version is associated with a git ref, it always printed with
the git ref.  For example, if the commit ``@git.abcdefg`` is tagged
``0.19``, then the spec will be shown as ``@git.abcdefg=0.19``.

If the git ref is not exactly a tag, then the distance to the nearest tag
is also part of the resolved version. ``@git.abcdefg=0.19.git.8`` means
that the commit is 8 commits away from the ``0.19`` tag.

In cases where Spack cannot resolve a sensible version from a git ref,
users can specify the Spack version to use for the git ref. This is done
by appending ``=`` and the Spack version to the git ref. For example:

.. code-block:: sh

   foo@git.my_ref=3.2 # use the my_ref tag or branch, but treat it as version 3.2 for version comparisons
   foo@git.abcdef1234abcdef1234abcdef1234abcdef1234=develop # use the given commit, but treat it as develop for version comparisons

Details about how versions are compared and how Spack determines if
one version is less than another are discussed in the developer guide.

^^^^^^^^^^^^^^^^^^
Compiler specifier
^^^^^^^^^^^^^^^^^^

A compiler specifier comes somewhere after a package name and starts
with ``%``.  It tells Spack what compiler(s) a particular package
should be built with.  After the ``%`` should come the name of some
registered Spack compiler.  This might include ``gcc``, or ``intel``,
but the specific compilers available depend on the site.  You can run
``spack compilers`` to get a list; more on this below.

The compiler spec can be followed by an optional *compiler version*.
A compiler version specifier looks exactly like a package version
specifier.  Version specifiers will associate with the nearest package
name or compiler specifier to their left in the spec.

If the compiler spec is omitted, Spack will choose a default compiler
based on site policies.


.. _basic-variants:

^^^^^^^^
Variants
^^^^^^^^

Variants are named options associated with a particular package. They are
optional, as each package must provide default values for each variant it
makes available. Variants can be specified using
a flexible parameter syntax ``name=<value>``. For example,
``spack install mercury debug=True`` will install mercury built with debug
flags. The names of particular variants available for a package depend on
what was provided by the package author. ``spack info <package>`` will
provide information on what build variants are available.

For compatibility with earlier versions, variants which happen to be
boolean in nature can be specified by a syntax that represents turning
options on and off. For example, in the previous spec we could have
supplied ``mercury +debug`` with the same effect of enabling the debug
compile time option for the libelf package.

Depending on the package a variant may have any default value.  For
``mercury`` here, ``debug`` is ``False`` by default, and we turned it on
with ``debug=True`` or ``+debug``.  If a variant is ``True`` by default
you can turn it off by either adding ``-name`` or ``~name`` to the spec.

There are two syntaxes here because, depending on context, ``~`` and
``-`` may mean different things.  In most shells, the following will
result in the shell performing home directory substitution:

.. code-block:: sh

   mpileaks ~debug   # shell may try to substitute this!
   mpileaks~debug    # use this instead

If there is a user called ``debug``, the ``~`` will be incorrectly
expanded.  In this situation, you would want to write ``libelf
-debug``.  However, ``-`` can be ambiguous when included after a
package name without spaces:

.. code-block:: sh

   mpileaks-debug     # wrong!
   mpileaks -debug    # right

Spack allows the ``-`` character to be part of package names, so the
above will be interpreted as a request for the ``mpileaks-debug``
package, not a request for ``mpileaks`` built without ``debug``
options.  In this scenario, you should write ``mpileaks~debug`` to
avoid ambiguity.

When spack normalizes specs, it prints them out with no spaces boolean
variants using the backwards compatibility syntax and uses only ``~``
for disabled boolean variants.  The ``-`` and spaces on the command
line are provided for convenience and legibility.

Spack allows variants to propagate their value to the package's
dependency by using ``++``, ``--``, and ``~~`` for boolean variants.
For example, for a ``debug`` variant:

.. code-block:: sh

    mpileaks ++debug   # enabled debug will be propagated to dependencies
    mpileaks +debug    # only mpileaks will have debug enabled

To propagate the value of non-boolean variants Spack uses ``name==value``.
For example, for the ``stackstart`` variant:

.. code-block:: sh

    mpileaks stackstart==4   # variant will be propagated to dependencies
    mpileaks stackstart=4    # only mpileaks will have this variant value

^^^^^^^^^^^^^^
Compiler Flags
^^^^^^^^^^^^^^

Compiler flags are specified using the same syntax as non-boolean variants,
but fulfill a different purpose. While the function of a variant is set by
the package, compiler flags are used by the compiler wrappers to inject
flags into the compile line of the build. Additionally, compiler flags can
be inherited by dependencies by using ``==``.
``spack install libdwarf cppflags=="-g"`` will install both libdwarf and
libelf with the ``-g`` flag injected into their compile line.

.. note::

   versions of spack prior to 0.19.0 will propagate compiler flags using
   the ``=`` syntax.

Notice that the value of the compiler flags must be quoted if it
contains any spaces. Any of ``cppflags=-O3``, ``cppflags="-O3"``,
``cppflags='-O3'``, and ``cppflags="-O3 -fPIC"`` are acceptable, but
``cppflags=-O3 -fPIC`` is not. Additionally, if the value of the
compiler flags is not the last thing on the line, it must be followed
by a space. The command ``spack install libelf cppflags="-O3"%intel``
will be interpreted as an attempt to set ``cppflags="-O3%intel"``.

The six compiler flags are injected in the order of implicit make commands
in GNU Autotools. If all flags are set, the order is
``$cppflags $cflags|$cxxflags $ldflags <command> $ldlibs`` for C and C++ and
``$fflags $cppflags $ldflags <command> $ldlibs`` for Fortran.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Compiler environment variables and additional RPATHs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes compilers require setting special environment variables to
operate correctly. Spack handles these cases by allowing custom environment
modifications in the ``environment`` attribute of the compiler configuration
section. See also the :ref:`configuration_environment_variables` section
of the configuration files docs for more information.

It is also possible to specify additional ``RPATHs`` that the
compiler will add to all executables generated by that compiler.  This is
useful for forcing certain compilers to RPATH their own runtime libraries, so
that executables will run without the need to set ``LD_LIBRARY_PATH``.

.. code-block:: yaml

  compilers:
    - compiler:
        spec: gcc@4.9.3
        paths:
          cc: /opt/gcc/bin/gcc
          c++: /opt/gcc/bin/g++
          f77: /opt/gcc/bin/gfortran
          fc: /opt/gcc/bin/gfortran
        environment:
          unset:
            - BAD_VARIABLE
          set:
            GOOD_VARIABLE_NUM: 1
            GOOD_VARIABLE_STR: good
          prepend_path:
            PATH: /path/to/binutils
          append_path:
            LD_LIBRARY_PATH: /opt/gcc/lib
        extra_rpaths:
        - /path/to/some/compiler/runtime/directory
        - /path/to/some/other/compiler/runtime/directory


^^^^^^^^^^^^^^^^^^^^^^^
Architecture specifiers
^^^^^^^^^^^^^^^^^^^^^^^

Each node in the dependency graph of a spec has an architecture attribute.
This attribute is a triplet of platform, operating system and processor.
You can specify the elements either separately, by using
the reserved keywords ``platform``, ``os`` and ``target``:

.. code-block:: console

   $ spack install libelf platform=linux
   $ spack install libelf os=ubuntu18.04
   $ spack install libelf target=broadwell

Normally users don't have to bother specifying the architecture if they
are installing software for their current host, as in that case the
values will be detected automatically.  If you need fine-grained control
over which packages use which targets (or over *all* packages' default
target), see :ref:`package-preferences`.


.. _support-for-microarchitectures:

"""""""""""""""""""""""""""""""""""""""
Support for specific microarchitectures
"""""""""""""""""""""""""""""""""""""""

Spack knows how to detect and optimize for many specific microarchitectures
(including recent Intel, AMD and IBM chips) and encodes this information in
the ``target`` portion of the architecture specification. A complete list of
the microarchitectures known to Spack can be obtained in the following way:

.. command-output:: spack arch --known-targets

When a spec is installed Spack matches the compiler being used with the
microarchitecture being targeted to inject appropriate optimization flags
at compile time. Giving a command such as the following:

.. code-block:: console

   $ spack install zlib%gcc@9.0.1 target=icelake

will produce compilation lines similar to:

.. code-block:: console

   $ /usr/bin/gcc-9 -march=icelake-client -mtune=icelake-client -c ztest10532.c
   $ /usr/bin/gcc-9 -march=icelake-client -mtune=icelake-client -c -fPIC -O2 ztest10532.
   ...

where the flags ``-march=icelake-client -mtune=icelake-client`` are injected
by Spack based on the requested target and compiler.

If Spack knows that the requested compiler can't optimize for the current target
or can't build binaries for that target at all, it will exit with a meaningful error message:

.. code-block:: console

   $ spack install zlib%gcc@5.5.0 target=icelake
   ==> Error: cannot produce optimized binary for micro-architecture "icelake" with gcc@5.5.0 [supported compiler versions are 8:]

When instead an old compiler is selected on a recent enough microarchitecture but there is
no explicit ``target`` specification, Spack will optimize for the best match it can find instead
of failing:

.. code-block:: console

   $ spack arch
   linux-ubuntu18.04-broadwell

   $ spack spec zlib%gcc@4.8
   Input spec
   --------------------------------
   zlib%gcc@4.8

   Concretized
   --------------------------------
   zlib@1.2.11%gcc@4.8+optimize+pic+shared arch=linux-ubuntu18.04-haswell

   $ spack spec zlib%gcc@9.0.1
   Input spec
   --------------------------------
   zlib%gcc@9.0.1

   Concretized
   --------------------------------
   zlib@1.2.11%gcc@9.0.1+optimize+pic+shared arch=linux-ubuntu18.04-broadwell

In the snippet above, for instance, the microarchitecture was demoted to ``haswell`` when
compiling with ``gcc@4.8`` since support to optimize for ``broadwell`` starts from ``gcc@4.9:``.

Finally, if Spack has no information to match compiler and target, it will
proceed with the installation but avoid injecting any microarchitecture
specific flags.

.. warning::

   Currently, Spack doesn't print any warning to the user if it has no information
   on which optimization flags should be used for a given compiler. This behavior
   might change in the future.

.. _sec-virtual-dependencies:

--------------------
Virtual dependencies
--------------------

The dependency graph for ``mpileaks`` we saw above wasn't *quite*
accurate.  ``mpileaks`` uses MPI, which is an interface that has many
different implementations.  Above, we showed ``mpileaks`` and
``callpath`` depending on ``mpich``, which is one *particular*
implementation of MPI.  However, we could build either with another
implementation, such as ``openmpi`` or ``mvapich``.

Spack represents interfaces like this using *virtual dependencies*.
The real dependency DAG for ``mpileaks`` looks like this:

.. graphviz::

   digraph {
       mpi [color=red]
       mpileaks -> mpi
       mpileaks -> callpath -> mpi
       callpath -> dyninst
       dyninst  -> libdwarf -> libelf
       dyninst  -> libelf
   }

Notice that ``mpich`` has now been replaced with ``mpi``. There is no
*real* MPI package, but some packages *provide* the MPI interface, and
these packages can be substituted in for ``mpi`` when ``mpileaks`` is
built.

You can see what virtual packages a particular package provides by
getting info on it:

.. command-output:: spack info --virtuals mpich

Spack is unique in that its virtual packages can be versioned, just
like regular packages.  A particular version of a package may provide
a particular version of a virtual package, and we can see above that
``mpich`` versions ``1`` and above provide all ``mpi`` interface
versions up to ``1``, and ``mpich`` versions ``3`` and above provide
``mpi`` versions up to ``3``.  A package can *depend on* a particular
version of a virtual package, e.g. if an application needs MPI-2
functions, it can depend on ``mpi@2:`` to indicate that it needs some
implementation that provides MPI-2 functions.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Constraining virtual packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When installing a package that depends on a virtual package, you can
opt to specify the particular provider you want to use, or you can let
Spack pick.  For example, if you just type this:

.. code-block:: console

   $ spack install mpileaks

Then spack will pick a provider for you according to site policies.
If you really want a particular version, say ``mpich``, then you could
run this instead:

.. code-block:: console

   $ spack install mpileaks ^mpich

This forces spack to use some version of ``mpich`` for its
implementation.  As always, you can be even more specific and require
a particular ``mpich`` version:

.. code-block:: console

   $ spack install mpileaks ^mpich@3

The ``mpileaks`` package in particular only needs MPI-1 commands, so
any MPI implementation will do.  If another package depends on
``mpi@2`` and you try to give it an insufficient MPI implementation
(e.g., one that provides only ``mpi@:1``), then Spack will raise an
error.  Likewise, if you try to plug in some package that doesn't
provide MPI, Spack will raise an error.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Explicit binding of virtual dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are packages that provide more than just one virtual dependency. When interacting with them, users
might want to utilize just a subset of what they could provide, and use other providers for virtuals they
need.

It is possible to be more explicit and tell Spack which dependency should provide which virtual, using a
special syntax:

.. code-block:: console

   $ spack spec strumpack ^[virtuals=mpi] intel-parallel-studio+mkl ^[virtuals=lapack] openblas

Concretizing the spec above produces the following DAG:

.. figure:: images/strumpack_virtuals.svg
   :scale: 60 %
   :align: center

where ``intel-parallel-studio`` *could* provide ``mpi``, ``lapack``, and ``blas`` but is used only for the former. The ``lapack``
and ``blas`` dependencies are satisfied by ``openblas``.

^^^^^^^^^^^^^^^^^^^^^^^^
Specifying Specs by Hash
^^^^^^^^^^^^^^^^^^^^^^^^

Complicated specs can become cumbersome to enter on the command line,
especially when many of the qualifications are necessary to distinguish
between similar installs. To avoid this, when referencing an existing spec,
Spack allows you to reference specs by their hash. We previously
discussed the spec hash that Spack computes. In place of a spec in any
command, substitute ``/<hash>`` where ``<hash>`` is any amount from
the beginning of a spec hash.

For example, lets say that you accidentally installed two different
``mvapich2`` installations. If you want to uninstall one of them but don't
know what the difference is, you can run:

.. code-block:: console

   $ spack find --long mvapich2
   ==> 2 installed packages.
   -- linux-centos7-x86_64 / gcc@6.3.0 ----------
   qmt35td mvapich2@2.2%gcc
   er3die3 mvapich2@2.2%gcc


You can then uninstall the latter installation using:

.. code-block:: console

   $ spack uninstall /er3die3


Or, if you want to build with a specific installation as a dependency,
you can use:

.. code-block:: console

   $ spack install trilinos ^/er3die3


If the given spec hash is sufficiently long as to be unique, Spack will
replace the reference with the spec to which it refers. Otherwise, it will
prompt for a more qualified hash.

Note that this will not work to reinstall a dependency uninstalled by
``spack uninstall --force``.

.. _cmd-spack-providers:

^^^^^^^^^^^^^^^^^^^
``spack providers``
^^^^^^^^^^^^^^^^^^^

You can see what packages provide a particular virtual package using
``spack providers``.  If you wanted to see what packages provide
``mpi``, you would just run:

.. command-output:: spack providers mpi

And if you *only* wanted to see packages that provide MPI-2, you would
add a version specifier to the spec:

.. command-output:: spack providers mpi@2

Notice that the package versions that provide insufficient MPI
versions are now filtered out.


-----------------------------
Deprecating insecure packages
-----------------------------

``spack deprecate`` allows for the removal of insecure packages with
minimal impact to their dependents.

.. warning::

  The ``spack deprecate`` command is designed for use only in
  extraordinary circumstances. This is a VERY big hammer to be used
  with care.

The ``spack deprecate`` command will remove one package and replace it
with another by replacing the deprecated package's prefix with a link
to the deprecator package's prefix.

.. warning::

  The ``spack deprecate`` command makes no promises about binary
  compatibility. It is up to the user to ensure the deprecator is
  suitable for the deprecated package.

Spack tracks concrete deprecated specs and ensures that no future packages
concretize to a deprecated spec.

The first spec given to the ``spack deprecate`` command is the package
to deprecate. It is an abstract spec that must describe a single
installed package. The second spec argument is the deprecator
spec. By default it must be an abstract spec that describes a single
installed package, but with the ``-i/--install-deprecator`` it can be
any abstract spec that Spack will install and then use as the
deprecator. The ``-I/--no-install-deprecator`` option will ensure
the default behavior.

By default, ``spack deprecate`` will deprecate all dependencies of the
deprecated spec, replacing each by the dependency of the same name in
the deprecator spec. The ``-d/--dependencies`` option will ensure the
default, while the ``-D/--no-dependencies`` option will deprecate only
the root of the deprecate spec in favor of the root of the deprecator
spec.

``spack deprecate`` can use symbolic links or hard links. The default
behavior is symbolic links, but the ``-l/--link-type`` flag can take
options ``hard`` or ``soft``.

-----------------------
Verifying installations
-----------------------

The ``spack verify`` command can be used to verify the validity of
Spack-installed packages any time after installation.

At installation time, Spack creates a manifest of every file in the
installation prefix. For links, Spack tracks the mode, ownership, and
destination. For directories, Spack tracks the mode, and
ownership. For files, Spack tracks the mode, ownership, modification
time, hash, and size. The Spack verify command will check, for every
file in each package, whether any of those attributes have changed. It
will also check for newly added files or deleted files from the
installation prefix. Spack can either check all installed packages
using the `-a,--all` or accept specs listed on the command line to
verify.

The ``spack verify`` command can also verify for individual files that
they haven't been altered since installation time. If the given file
is not in a Spack installation prefix, Spack will report that it is
not owned by any package. To check individual files instead of specs,
use the ``-f,--files`` option.

Spack installation manifests are part of the tarball signed by Spack
for binary package distribution. When installed from a binary package,
Spack uses the packaged installation manifest instead of creating one
at install time.

The ``spack verify`` command also accepts the ``-l,--local`` option to
check only local packages (as opposed to those used transparently from
``upstream`` spack instances) and the ``-j,--json`` option to output
machine-readable json data for any errors.

-----------------------
Filesystem requirements
-----------------------

By default, Spack needs to be run from a filesystem that supports
``flock`` locking semantics.  Nearly all local filesystems and recent
versions of NFS support this, but parallel filesystems or NFS volumes may
be configured without ``flock`` support enabled.  You can determine how
your filesystems are mounted with ``mount``.  The output for a Lustre
filesystem might look like this:

.. code-block:: console

   $ mount | grep lscratch
   mds1-lnet0@o2ib100:/lsd on /p/lscratchd type lustre (rw,nosuid,lazystatfs,flock)
   mds2-lnet0@o2ib100:/lse on /p/lscratche type lustre (rw,nosuid,lazystatfs,flock)

Note the ``flock`` option on both Lustre mounts.

If you do not see this or a similar option for your filesystem, you have
a few options. First, you can move your Spack installation to a
filesystem that supports locking. Second, you could ask your system
administrator to enable ``flock`` for your filesystem.

If none of those work, you can disable locking in one of two ways:

  1. Run Spack with the ``-L`` or ``--disable-locks`` option to disable
     locks on a call-by-call basis.
  2. Edit :ref:`config.yaml <config-yaml>` and set the ``locks`` option
     to ``false`` to always disable locking.

.. warning::

   If you disable locking, concurrent instances of Spack will have no way
   to avoid stepping on each other.  You must ensure that there is only
   **one** instance of Spack running at a time.  Otherwise, Spack may end
   up with a corrupted database file, or you may not be able to see all
   installed packages in commands like ``spack find``.

   If you are unfortunate enough to run into this situation, you may be
   able to fix it by running ``spack reindex``.

This issue typically manifests with the error below:

.. code-block:: console

   $ ./spack find
   Traceback (most recent call last):
   File "./spack", line 176, in <module>
     main()
   File "./spack", line 154,' in main
     return_val = command(parser, args)
   File "./spack/lib/spack/spack/cmd/find.py", line 170, in find
     specs = set(spack.installed_db.query(\**q_args))
   File "./spack/lib/spack/spack/database.py", line 551, in query
     with self.read_transaction():
   File "./spack/lib/spack/spack/database.py", line 598, in __enter__
     if self._enter() and self._acquire_fn:
   File "./spack/lib/spack/spack/database.py", line 608, in _enter
     return self._db.lock.acquire_read(self._timeout)
   File "./spack/lib/spack/llnl/util/lock.py", line 103, in acquire_read
     self._lock(fcntl.LOCK_SH, timeout)   # can raise LockError.
   File "./spack/lib/spack/llnl/util/lock.py", line 64, in _lock
     fcntl.lockf(self._fd, op | fcntl.LOCK_NB)
   IOError: [Errno 38] Function not implemented

A nicer error message is TBD in future versions of Spack.

---------------
Troubleshooting
---------------

The ``spack audit`` command:

.. command-output:: spack audit -h

can be used to detect a number of configuration issues. This command detects
configuration settings which might not be strictly wrong but are not likely
to be useful outside of special cases.

It can also be used to detect dependency issues with packages - for example
cases where a package constrains a dependency with a variant that doesn't
exist (in this case Spack could report the problem ahead of time but
automatically performing the check would slow down most runs of Spack).

A detailed list of the checks currently implemented for each subcommand can be
printed with:

.. command-output:: spack -v audit list

Depending on the use case, users might run the appropriate subcommands to obtain
diagnostics. Issues, if found, are reported to stdout:

.. code-block:: console

   % spack audit packages lammps
   PKG-DIRECTIVES: 1 issue found
   1. lammps: wrong variant in "conflicts" directive
       the variant 'adios' does not exist
       in /home/spack/spack/var/spack/repos/builtin/packages/lammps/package.py


------------
Getting Help
------------

.. _cmd-spack-help:

^^^^^^^^^^^^^^
``spack help``
^^^^^^^^^^^^^^

If you don't find what you need here, the ``help`` subcommand will
print out out a list of *all* of spack's options and subcommands:

.. command-output:: spack help

Adding an argument, e.g. ``spack help <subcommand>``, will print out
usage information for a particular subcommand:

.. command-output:: spack help install

Alternately, you can use ``spack --help`` in place of ``spack help``, or
``spack <subcommand> --help`` to get help on a particular subcommand.
