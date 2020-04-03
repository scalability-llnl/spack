.. Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

=========
Workflows
=========

The process of using Spack involves building packages, running
binaries from those packages, and developing software that depends on
those packages.  Spack supports a variety of workflows to suit a variety of situations
and user preferences, there is no single way to do all these things.
This chapter demonstrates different workflows that have been
developed, pointing out the pros and cons of them.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combinatorial Sets of Installs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose that you are now tasked with systematically building many
incompatible versions of packages.  For example, you need to build
``petsc`` 9 times for 3 different MPI implementations on 3 different
compilers, in order to support user needs.  In this case, you will
need to either create 9 different ``packages.yaml`` files; or more
likely, create 9 different ``spack install`` command lines with the
correct options in the spec.  Here is a real-life example of this kind
of usage:

.. code-block:: sh

   #!/bin/bash

   compilers=(
       %gcc
       %intel
       %pgi
   )

   mpis=(
       openmpi+psm~verbs
       openmpi~psm+verbs
       mvapich2+psm~mrail
       mvapich2~psm+mrail
       mpich+verbs
   )

   for compiler in "${compilers[@]}"
   do
       # Serial installs
       spack install szip           $compiler
       spack install hdf            $compiler
       spack install hdf5           $compiler
       spack install netcdf         $compiler
       spack install netcdf-fortran $compiler
       spack install ncview         $compiler

       # Parallel installs
       for mpi in "${mpis[@]}"
       do
           spack install $mpi            $compiler
           spack install hdf5~cxx+mpi    $compiler ^$mpi
           spack install parallel-netcdf $compiler ^$mpi
       done
   done

.. _filesystem-views:

^^^^^^^^^^^^^^^^
Filesystem Views
^^^^^^^^^^^^^^^^

Filesystem views offer an alternative to environment modules, another
way to assemble packages in a useful way and load them into a user's
environment.

A single-prefix filesystem view is a single directory tree that is the
union of the directory hierarchies of a number of installed packages;
it is similar to the directory hierarchy that might exist under
``/usr/local``.  The files of the view's installed packages are
brought into the view by symbolic or hard links, referencing the
original Spack installation.

A combinatorial filesystem view can contain more software than a
single-prefix view. Combinatorial filesystem views are created by
defining a projection for each spec or set of specs. The syntax for
this will be discussed in the section for the ``spack view`` command
under `adding_projections_to_views`_.

The projection for a spec or set of specs specifies the naming scheme
for the directory structure under the root of the view into which the
package will be linked. For example, the spec ``zlib@1.2.8%gcc@4.4.7``
could be projected to ``MYVIEW/zlib-1.2.8-gcc``.

When software is built and installed, absolute paths are frequently
"baked into" the software, making it non-relocatable.  This happens
not just in RPATHs, but also in shebangs, configuration files, and
assorted other locations.

Therefore, programs run out of a Spack view will typically still look
in the original Spack-installed location for shared libraries and
other resources.  This behavior is not easily changed; in general,
there is no way to know where absolute paths might be written into an
installed package, and how to relocate it.  Therefore, the original
Spack tree must be kept in place for a filesystem view to work, even
if the view is built with hardlinks.

.. FIXME: reference the relocation work of Hegner and Gartung (PR #1013)

.. _cmd-spack-view:

""""""""""""""
``spack view``
""""""""""""""

A filesystem view is created, and packages are linked in, by the ``spack
view`` command's ``symlink`` and ``hardlink`` sub-commands.  The
``spack view remove`` command can be used to unlink some or all of the
filesystem view.

The following example creates a filesystem view based
on an installed ``cmake`` package and then removes from the view the
files in the ``cmake`` package while retaining its dependencies.

.. code-block:: console

   $ spack view --verbose symlink myview cmake@3.5.2
   ==> Linking package: "ncurses"
   ==> Linking package: "zlib"
   ==> Linking package: "openssl"
   ==> Linking package: "cmake"

   $ ls myview/
   bin  doc  etc  include  lib  share

   $ ls myview/bin/
   captoinfo  clear  cpack     ctest    infotocap        openssl  tabs  toe   tset
   ccmake     cmake  c_rehash  infocmp  ncurses6-config  reset    tic   tput

   $ spack view --verbose --dependencies false rm myview cmake@3.5.2
   ==> Removing package: "cmake"

   $ ls myview/bin/
   captoinfo  c_rehash  infotocap        openssl  tabs  toe   tset
   clear      infocmp   ncurses6-config  reset    tic   tput

.. note::

    If the set of packages being included in a view is inconsistent,
    then it is possible that two packages will provide the same file.  Any
    conflicts of this type are handled on a first-come-first-served basis,
    and a warning is printed.

.. note::

    When packages are removed from a view, empty directories are
    purged.

.. _adding_projections_to_views:

""""""""""""""""""""""""""""
Controlling View Projections
""""""""""""""""""""""""""""

The default projection into a view is to link every package into the
root of the view. This can be changed by adding a ``projections.yaml``
configuration file to the view. The projection configuration file for
a view located at ``/my/view`` is stored in
``/my/view/.spack/projections.yaml``.

When creating a view, the projection configuration file can also be
specified from the command line using the ``--projection-file`` option
to the ``spack view`` command.

The projections configuration file is a mapping of partial specs to
spec format strings, as shown in the example below.

.. code-block:: yaml

   projections:
     zlib: {name}-{version}
     ^mpi: {name}-{version}/{^mpi.name}-{^mpi.version}-{compiler.name}-{compiler.version}
     all: {name}-{version}/{compiler.name}-{compiler.version}

The entries in the projections configuration file must all be either
specs or the keyword ``all``. For each spec, the projection used will
be the first non-``all`` entry that the spec satisfies, or ``all`` if
there is an entry for ``all`` and no other entry is satisfied by the
spec. Where the keyword ``all`` appears in the file does not
matter. Given the example above, any spec satisfying ``zlib@1.2.8``
will be linked into ``/my/view/zlib-1.2.8/``, any spec satisfying
``hdf5@1.8.10+mpi %gcc@4.9.3 ^mvapich2@2.2`` will be linked into
``/my/view/hdf5-1.8.10/mvapich2-2.2-gcc-4.9.3``, and any spec
satisfying ``hdf5@1.8.10~mpi %gcc@4.9.3`` will be linked into
``/my/view/hdf5-1.8.10/gcc-4.9.3``.

If the keyword ``all`` does not appear in the projections
configuration file, any spec that does not satisfy any entry in the
file will be linked into the root of the view as in a single-prefix
view. Any entries that appear below the keyword ``all`` in the
projections configuration file will not be used, as all specs will use
the projection under ``all`` before reaching those entries.

""""""""""""""""""
Fine-Grain Control
""""""""""""""""""

The ``--exclude`` and ``--dependencies`` option flags allow for
fine-grained control over which packages and dependencies do or not
get included in a view.  For example, suppose you are developing the
``appsy`` package.  You wish to build against a view of all ``appsy``
dependencies, but not ``appsy`` itself:

.. code-block:: console

   $ spack view --dependencies yes --exclude appsy symlink /path/to/MYVIEW/ appsy

Alternately, you wish to create a view whose purpose is to provide
binary executables to end users.  You only need to include
applications they might want, and not those applications'
dependencies.  In this case, you might use:

.. code-block:: console

   $ spack view --dependencies no symlink /path/to/MYVIEW/ cmake


"""""""""""""""""""""""
Hybrid Filesystem Views
"""""""""""""""""""""""

Although filesystem views are usually created by Spack, users are free
to add to them by other means.  For example, imagine a filesystem
view, created by Spack, that looks something like:

.. code-block:: console

   /path/to/MYVIEW/bin/programA -> /path/to/spack/.../bin/programA
   /path/to/MYVIEW/lib/libA.so -> /path/to/spack/.../lib/libA.so

Now, the user may add to this view by non-Spack means; for example, by
running a classic install script.  For example:

.. code-block:: console

   $ tar -xf B.tar.gz
   $ cd B/
   $ ./configure --prefix=/path/to/MYVIEW \
               --with-A=/path/to/MYVIEW
   $ make && make install

The result is a hybrid view:

.. code-block:: console

   /path/to/MYVIEW/bin/programA -> /path/to/spack/.../bin/programA
   /path/to/MYVIEW/bin/programB
   /path/to/MYVIEW/lib/libA.so -> /path/to/spack/.../lib/libA.so
   /path/to/MYVIEW/lib/libB.so

In this case, real files coexist, interleaved with the "view"
symlinks.  At any time one can delete ``/path/to/MYVIEW`` or use
``spack view`` to manage it surgically.  None of this will affect the
real Spack install area.

^^^^^^^^^^^^^^^^^^
Global Activations
^^^^^^^^^^^^^^^^^^

:ref:`cmd-spack-activate` may be used as an alternative to loading
Python (and similar systems) packages directly or creating a view.
If extensions are globally activated, then ``spack load python`` will
also load all the extensions activated for the given ``python``.
This reduces the need for users to load a large number of packages.

However, Spack global activations have two potential drawbacks:

#. Activated packages that involve compiled C extensions may still
   need their dependencies to be loaded manually.  For example,
   ``spack load openblas`` might be required to make ``py-numpy``
   work.

#. Global activations "break" a core feature of Spack, which is that
   multiple versions of a package can co-exist side-by-side.  For example,
   suppose you wish to run a Python package in two different
   environments but the same basic Python --- one with
   ``py-numpy@1.7`` and one with ``py-numpy@1.8``.  Spack extensions
   will not support this potential debugging use case.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Discussion: Running Binaries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modules, extension packages and filesystem views are all ways to
assemble sets of Spack packages into a useful environment.  They are
all semantically similar, in that conflicting installed packages
cannot simultaneously be loaded, activated or included in a view.

With all of these approaches, there is no guarantee that the
environment created will be consistent.  It is possible, for example,
to simultaneously load application A that uses OpenMPI and application
B that uses MPICH.  Both applications will run just fine in this
inconsistent environment because they rely on RPATHs, not the
environment, to find their dependencies.

In general, environments set up using modules vs. views will work
similarly.  Both can be used to set up ephemeral or long-lived
testing/development environments.  Operational differences between the
two approaches can make one or the other preferable in certain
environments:

* Filesystem views do not require environment module infrastructure.
  Although Spack can install ``environment-modules``, users might be
  hostile to its use.  Filesystem views offer a good solution for
  sysadmins serving users who just "want all the stuff I need in one
  place" and don't want to hear about Spack.

* Although modern build systems will find dependencies wherever they
  might be, some applications with hand-built make files expect their
  dependencies to be in one place.  One common problem is makefiles
  that assume that ``netcdf`` and ``netcdf-fortran`` are installed in
  the same tree.  Or, one might use an IDE that requires tedious
  configuration of dependency paths; and it's easier to automate that
  administration in a view-building script than in the IDE itself.
  For all these cases, a view will be preferable to other ways to
  assemble an environment.

* On systems with I-node quotas, modules might be preferable to views
  and extension packages.

* Views and activated extensions maintain state that is semantically
  equivalent to the information in a ``spack module tcl loads`` script.
  Administrators might find things easier to maintain without the
  added "heavyweight" state of a view.

------------------------------
Developing Software with Spack
------------------------------

For any project, one needs to assemble an
environment of that application's dependencies.  You might consider
loading a series of modules or creating a filesystem view.  This
approach, while obvious, has some serious drawbacks:

1. There is no guarantee that an environment created this way will be
   consistent.  Your application could end up with dependency A
   expecting one version of MPI, and dependency B expecting another.
   The linker will not be happy...

2. Suppose you need to debug a package deep within your software DAG.
   If you build that package with a manual environment, then it
   becomes difficult to have Spack auto-build things that depend on
   it.  That could be a serious problem, depending on how deep the
   package in question is in your dependency DAG.

3. At its core, Spack is a sophisticated concretization algorithm that
   matches up packages with appropriate dependencies and creates a
   *consistent* environment for the package it's building.  Writing a
   list of ``spack load`` commands for your dependencies is at least
   as hard as writing the same list of ``depends_on()`` declarations
   in a Spack package.  But it makes no use of Spack concretization
   and is more error-prone.

4. Spack provides an automated, systematic way not just to find a
   packages's dependencies --- but also to build other packages on
   top.  Any Spack package can become a dependency for another Spack
   package, offering a powerful vision of software re-use.  If you
   build your package A outside of Spack, then your ability to use it
   as a building block for other packages in an automated way is
   diminished: other packages depending on package A will not
   be able to use Spack to fulfill that dependency.

5. If you are reading this manual, you probably love Spack.  You're
   probably going to write a Spack package for your software so
   prospective users can install it with the least amount of pain.
   Why should you go to additional work to find dependencies in your
   development environment?  Shouldn't Spack be able to help you build
   your software based on the package you've already written?

In this section, we show how Spack can be used in the software
development process to greatest effect, and how development packages
can be seamlessly integrated into the Spack ecosystem.  We will show
how this process works by example, assuming the software you are
creating is called ``mylib``.

^^^^^^^^^^^^^^^^^^^^^
Write the CMake Build
^^^^^^^^^^^^^^^^^^^^^

For now, the techniques in this section only work for CMake-based
projects, although they could be easily extended to other build
systems in the future.  We will therefore assume you are using CMake
to build your project.

The ``CMakeLists.txt`` file should be written as normal.  A few caveats:

1. Your project should produce binaries with RPATHs.  This will ensure
   that they work the same whether built manually or automatically by
   Spack.  For example:

.. code-block:: cmake

   # enable @rpath in the install name for any shared library being built
   # note: it is planned that a future version of CMake will enable this by default
   set(CMAKE_MACOSX_RPATH 1)

   # Always use full RPATH
   # http://www.cmake.org/Wiki/CMake_RPATH_handling
   # http://www.kitware.com/blog/home/post/510

   # use, i.e. don't skip the full RPATH for the build tree
   SET(CMAKE_SKIP_BUILD_RPATH  FALSE)

   # when building, don't use the install RPATH already
   # (but later on when installing)
   SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

   # add the automatically determined parts of the RPATH
   # which point to directories outside the build tree to the install RPATH
   SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

   # the RPATH to be used when installing, but only if it's not a system directory
   LIST(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/lib" isSystemDir)
   IF("${isSystemDir}" STREQUAL "-1")
      SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
   ENDIF("${isSystemDir}" STREQUAL "-1")


2. Spack provides a CMake variable called
   ``SPACK_TRANSITIVE_INCLUDE_PATH``, which contains the ``include/``
   directory for all of your project's transitive dependencies.  It
   can be useful if your project ``#include``s files from package B,
   which ``#include`` files from package C, but your project only
   lists project B as a dependency.  This works in traditional
   single-tree build environments, in which B and C's include files
   live in the same place.  In order to make it work with Spack as
   well, you must add the following to ``CMakeLists.txt``.  It will
   have no effect when building without Spack:

   .. code-block:: cmake

      # Include all the transitive dependencies determined by Spack.
      # If we're not running with Spack, this does nothing...
      include_directories($ENV{SPACK_TRANSITIVE_INCLUDE_PATH})

   .. note::

      Note that this feature is controversial and could break with
      future versions of GNU ld.  The best practice is to make sure
      anything you ``#include`` is listed as a dependency in your
      CMakeLists.txt (and Spack package).

.. _write-the-spack-package:

^^^^^^^^^^^^^^^^^^^^^^^
Write the Spack Package
^^^^^^^^^^^^^^^^^^^^^^^

The Spack package also needs to be written, in tandem with setting up
the build (for example, CMake).  The most important part of this task
is declaring dependencies.  Here is an example of the Spack package
for the ``mylib`` package (ellipses for brevity):

.. code-block:: python

   class Mylib(CMakePackage):
       """Misc. reusable utilities used by Myapp."""

       homepage = "https://github.com/citibeth/mylib"
       url = "https://github.com/citibeth/mylib/tarball/123"

       version('0.1.2', '3a6acd70085e25f81b63a7e96c504ef9')
       version('develop', git='https://github.com/citibeth/mylib.git',
           branch='develop')

       variant('everytrace', default=False,
               description='Report errors through Everytrace')
       ...

       extends('python')

       depends_on('eigen')
       depends_on('everytrace', when='+everytrace')
       depends_on('proj', when='+proj')
       ...
       depends_on('cmake', type='build')
       depends_on('doxygen', type='build')

       def cmake_args(self):
           spec = self.spec
           return [
               '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
               '-DUSE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
               ...
               '-DUSE_UDUNITS2=%s' % ('YES' if '+udunits2' in spec else 'NO'),
               '-DUSE_GTEST=%s' % ('YES' if '+googletest' in spec else 'NO')]

This is a standard Spack package that can be used to install
``mylib`` in a production environment.  The list of dependencies in
the Spack package will generally be a repeat of the list of CMake
dependencies.  This package also has some features that allow it to be
used for development:

1. It subclasses ``CMakePackage`` instead of ``Package``.  This
   eliminates the need to write an ``install()`` method, which is
   defined in the superclass.  Instead, one just needs to write the
   ``configure_args()`` method.  That method should return the
   arguments needed for the ``cmake`` command (beyond the standard
   CMake arguments, which Spack will include already).  These
   arguments are typically used to turn features on/off in the build.

2. It specifies a non-checksummed version ``develop``.  Running
   ``spack install mylib@develop`` the ``@develop`` version will
   install the latest version off the develop branch.  This method of
   download is useful for the developer of a project while it is in
   active development; however, it should only be used by developers
   who control and trust the repository in question!

3. The ``url``, ``url_for_version()`` and ``homepage`` attributes are
   not used in development.  Don't worry if you don't have any, or if
   they are behind a firewall.

^^^^^^^^^^^^^^^^
Build with Spack
^^^^^^^^^^^^^^^^

Now that you have a Spack package, you can use Spack to find its
dependencies automatically.  For example:

.. code-block:: console

   $ cd mylib
   $ spack setup mylib@local

The result will be a file ``spconfig.py`` in the top-level
``mylib/`` directory.  It is a short script that calls CMake with the
dependencies and options determined by Spack --- similar to what
happens in ``spack install``, but now written out in script form.
From a developer's point of view, you can think of ``spconfig.py`` as
a stand-in for the ``cmake`` command.

.. note::

   You can invent any "version" you like for the ``spack setup``
   command.

.. note::

   Although ``spack setup`` does not build your package, it does
   create and install a module file, and mark in the database that
   your package has been installed.  This can lead to errors, of
   course, if you don't subsequently install your package.
   Also... you will need to ``spack uninstall`` before you run
   ``spack setup`` again.


You can now build your project as usual with CMake:

.. code-block:: console

   $ mkdir build; cd build
   $ ../spconfig.py ..   # Instead of cmake ..
   $ make
   $ make install

Once your ``make install`` command is complete, your package will be
installed, just as if you'd run ``spack install``.  Except you can now
edit, re-build and re-install as often as needed, without checking
into Git or downloading tarballs.

.. note::

   The build you get this way will be *almost* the same as the build
   from ``spack install``.  The only difference is, you will not be
   using Spack's compiler wrappers.  This difference has not caused
   problems in our experience, as long as your project sets
   RPATHs as shown above.  You DO use RPATHs, right?

^^^^^^^^^^^^^^^^^^^^
Build Other Software
^^^^^^^^^^^^^^^^^^^^

Now that you've built ``mylib`` with Spack, you might want to build
another package that depends on it --- for example, ``myapp``.  This
is accomplished easily enough:

.. code-block:: console

   $ spack install myapp ^mylib@local

Note that auto-built software has now been installed *on top of*
manually-built software, without breaking Spack's "web."  This
property is useful if you need to debug a package deep in the
dependency hierarchy of your application.  It is a *big* advantage of
using ``spack setup`` to build your package's environment.

If you feel your software is stable, you might wish to install it with
``spack install`` and skip the source directory.  You can just use,
for example:

.. code-block:: console

   $ spack install mylib@develop

.. _release-your-software:

^^^^^^^^^^^^^^^^^^^^^
Release Your Software
^^^^^^^^^^^^^^^^^^^^^

You are now ready to release your software as a tarball with a
numbered version, and a Spack package that can build it.  If you're
hosted on GitHub, this process will be a bit easier.

#. Put tag(s) on the version(s) in your GitHub repo you want to be
   release versions.  For example, a tag ``v0.1.0`` for version 0.1.0.

#. Set the ``url`` in your ``package.py`` to download a tarball for
   the appropriate version.  GitHub will give you a tarball for any
   commit in the repo, if you tickle it the right way.  For example:

   .. code-block:: python

      url = 'https://github.com/citibeth/mylib/tarball/v0.1.2'

#. Use Spack to determine your version's hash, and cut'n'paste it into
   your ``package.py``:

   .. code-block:: console

      $ spack checksum mylib 0.1.2
      ==> Found 1 versions of mylib
        0.1.2     https://github.com/citibeth/mylib/tarball/v0.1.2

      How many would you like to checksum? (default is 5, q to abort)
      ==> Downloading...
      ==> Trying to fetch from https://github.com/citibeth/mylib/tarball/v0.1.2
      ######################################################################## 100.0%
      ==> Checksummed new versions of mylib:
            version('0.1.2', '3a6acd70085e25f81b63a7e96c504ef9')

#. You should now be able to install released version 0.1.2 of your package with:

   .. code-block:: console

      $ spack install mylib@0.1.2

#. There is no need to remove the `develop` version from your package.
   Spack concretization will always prefer numbered version to
   non-numeric versions.  Users will only get it if they ask for it.

^^^^^^^^^^^^^^^^^^^^^^^^
Distribute Your Software
^^^^^^^^^^^^^^^^^^^^^^^^

Once you've released your software, other people will want to build
it; and you will need to tell them how.  In the past, that has meant a
few paragraphs of prose explaining which dependencies to install.  But
now you use Spack, and those instructions are written in executable
Python code.  But your software has many dependencies, and you know
Spack is the best way to install it:

#. First, you will want to fork Spack's ``develop`` branch.  Your aim
   is to provide a stable version of Spack that you KNOW will install
   your software.  If you make changes to Spack in the process, you
   will want to submit pull requests to Spack core.

#. Add your software's ``package.py`` to that fork.  You should submit
   a pull request for this as well, unless you don't want the public
   to know about your software.

#. Prepare instructions that read approximately as follows:

   #. Download Spack from your forked repo.

   #. Install Spack; see :ref:`getting_started`.

   #. Set up an appropriate ``packages.yaml`` file.  You should tell
      your users to include in this file whatever versions/variants
      are needed to make your software work correctly (assuming those
      are not already in your ``packages.yaml``).

   #. Run ``spack install mylib``.

   #. Run this script to generate the ``module load`` commands or
      filesystem view needed to use this software.

#. Be aware that your users might encounter unexpected bootstrapping
   issues on their machines, especially if they are running on older
   systems.  The :ref:`getting_started` section should cover this, but
   there could always be issues.

^^^^^^^^^^^^^^^^^^^
Other Build Systems
^^^^^^^^^^^^^^^^^^^

``spack setup`` currently only supports CMake-based builds, in
packages that subclass ``CMakePackage``.  The intent is that this
mechanism should support a wider range of build systems; for example,
GNU Autotools.  Someone well-versed in Autotools is needed to develop
this patch and test it out.

Python Distutils is another popular build system that should get
``spack setup`` support.  For non-compiled languages like Python,
``spack diy`` may be used.  Even better is to put the source directory
directly in the user's ``PYTHONPATH``.  Then, edits in source files
are immediately available to run without any install process at all!

^^^^^^^^^^
Conclusion
^^^^^^^^^^

The ``spack setup`` development workflow provides better automation,
flexibility and safety than workflows relying on environment modules
or filesystem views.  However, it has some drawbacks:

#. It currently works only with projects that use the CMake build
   system.  Support for other build systems is not hard to build, but
   will require a small amount of effort for each build system to be
   supported.  It might not work well with some IDEs.

#. It only works with packages that sub-class ``StagedPackage``.
   Currently, most Spack packages do not.  Converting them is not
   hard; but must be done on a package-by-package basis.

#. It requires that users are comfortable with Spack, as they
   integrate Spack explicitly in their workflow.  Not all users are
   willing to do this.

-------------------------------------
Using Spack to Replace Homebrew/Conda
-------------------------------------

Spack is an incredibly powerful package manager, designed for supercomputers
where users have diverse installation needs. But Spack can also be used to
handle simple single-user installations on your laptop. Most macOS users are
already familiar with package managers like Homebrew and Conda, where all
installed packages are symlinked to a single central location like ``/usr/local``.
In this section, we will show you how to emulate the behavior of Homebrew/Conda
using :ref:`environments`!

^^^^^
Setup
^^^^^

First, let's create a new environment. We'll assume that Spack is already set up
correctly, and that you've already sourced the setup script for your shell.
To create a new environment, simply run:

.. code-block:: console

   $ spack env create myenv
   ==> Updating view at /Users/me/spack/var/spack/environments/myenv/.spack-env/view
   ==> Created environment 'myenv' in /Users/me/spack/var/spack/environments/myenv
   $ spack env activate myenv

Here, *myenv* can be anything you want to name your environment. Next, we can add
a list of packages we would like to install into our environment. Let's say we
want a newer version of Bash than the one that comes with macOS, and we want a
few Python libraries. We can run:

.. code-block:: console

   $ spack add bash
   ==> Adding bash to environment myenv
   ==> Updating view at /Users/me/spack/var/spack/environments/myenv/.spack-env/view
   $ spack add python@3:
   ==> Adding python@3: to environment myenv
   ==> Updating view at /Users/me/spack/var/spack/environments/myenv/.spack-env/view
   $ spack add py-numpy py-scipy py-matplotlib
   ==> Adding py-numpy to environment myenv
   ==> Adding py-scipy to environment myenv
   ==> Adding py-matplotlib to environment myenv
   ==> Updating view at /Users/me/spack/var/spack/environments/myenv/.spack-env/view

Each package can be listed on a separate line, or combined into a single line.
Notice that we're explicitly asking for Python 3 here. You can use any spec
you would normally use on the command line with other Spack commands.

Next, we want to manually configure a couple of things. In the ``myenv``
directory, we can find the ``spack.yaml`` that actually defines our environment.

.. code-block:: console

   $ vim ~/spack/var/spack/environments/myenv/spack.yaml

.. code-block:: yaml

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs: [bash, 'python@3:', py-numpy, py-scipy, py-matplotlib]
     view:
       default:
         root: /Users/me/spack/var/spack/environments/myenv/.spack-env/view
         projections: {}
     config: {}
     mirrors: {}
     modules:
       enable: []
     packages: {}
     repos: []
     upstreams: {}
     definitions: []
     concretization: separately

You can see the packages we added earlier in the ``specs:`` section. If you
ever want to add more packages, you can either use ``spack add`` or manually
edit this file.

We also need to change the ``concretization:`` option. By default, Spack
concretizes each spec *separately*, allowing multiple versions of the same
package to coexist. Since we want a single consistent environment, we want to
concretize all of the specs *together*.

Here is what your ``spack.yaml`` looks like with these new settings, and with
some of the sections we don't plan on using removed:

.. code-block:: diff

   spack:
   -  specs: [bash, 'python@3:', py-numpy, py-scipy, py-matplotlib]
   +  specs:
   +  - bash
   +  - 'python@3:'
   +  - py-numpy
   +  - py-scipy
   +  - py-matplotlib
   -  view:
   -    default:
   -      root: /Users/me/spack/var/spack/environments/myenv/.spack-env/view
   -      projections: {}
   +  view: /Users/me/spack/var/spack/environments/myenv/.spack-env/view
   -  config: {}
   -  mirrors: {}
   -  modules:
   -    enable: []
   -  packages: {}
   -  repos: []
   -  upstreams: {}
   -  definitions: []
   +  concretization: together
   -  concretization: separately

""""""""""""""""
Symlink location
""""""""""""""""

In the ``spack.yaml`` file above, you'll notice that by default, Spack symlinks
all installations to ``/Users/me/spack/var/spack/environments/myenv/.spack-env/view``.
You can actually change this to any directory you want. For example, Homebrew
uses ``/usr/local``, while Conda uses ``/Users/me/anaconda``. In order to access
files in these locations, you need to update ``PATH`` and other environment variables
to point to them. Activating the Spack environment does this automatically, but
you can also manually set them in your ``.bashrc``.

.. warning::

   There are several reasons why you shouldn't use ``/usr/local``:

   1. If you are on macOS 10.11+ (El Capitan and newer), Apple makes it hard
      for you. You may notice permissions issues on ``/usr/local`` due to their
      `System Integrity Protection <https://support.apple.com/en-us/HT204899>`_.
      By default, users don't have permissions to install anything in ``/usr/local``,
      and you can't even change this using ``sudo chown`` or ``sudo chmod``.
   2. Other package managers like Homebrew will try to install things to the
      same directory. If you plan on using Homebrew in conjunction with Spack,
      don't symlink things to ``/usr/local``.
   3. If you are on a shared workstation, or don't have sudo privileges, you
      can't do this.

   If you still want to do this anyway, there are several ways around SIP.
   You could disable SIP by booting into recovery mode and running
   ``csrutil disable``, but this is not recommended, as it can open up your OS
   to security vulnerabilities. Another technique is to run ``spack concretize``
   and ``spack install`` using ``sudo``. This is also not recommended.

   The safest way I've found is to create your installation directories using
   sudo, then change ownership back to the user like so:

   .. code-block:: bash

      for directory in .spack bin contrib include lib man share
      do
          sudo mkdir -p /usr/local/$directory
          sudo chown $(id -un):$(id -gn) /usr/local/$directory
      done

   Depending on the packages you install in your environment, the exact list of
   directories you need to create may vary. You may also find some packages
   like Java libraries that install a single file to the installation prefix
   instead of in a subdirectory. In this case, the action is the same, just replace
   ``mkdir -p`` with ``touch`` in the for-loop above.

   But again, it's safer just to use the default symlink location.


^^^^^^^^^^^^
Installation
^^^^^^^^^^^^

To actually concretize the environment, run:

.. code-block:: console

   $ spack concretize

This will tell you which if any packages are already installed, and alert you
to any conflicting specs.

To actually install these packages and symlink them to your ``view:``
directory, simply run:

.. code-block:: console

   $ spack install

Now, when you type ``which python3``, it should find the one you just installed.

In order to change the default shell to our newer Bash installation, we first
need to add it to this list of acceptable shells. Run:

.. code-block:: console

   $ sudo vim /etc/shells

and add the absolute path to your bash executable. Then run:

.. code-block:: console

   $ chsh -s /path/to/bash

Now, when you log out and log back in, ``echo $SHELL`` should point to the
newer version of Bash.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Updating Installed Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say you upgraded to a new version of macOS, or a new version of Python
was released, and you want to rebuild your entire software stack. To do this,
simply run the following commands:

.. code-block:: console

   $ spack env activate myenv
   $ spack concretize --force
   $ spack install

The ``--force`` flag tells Spack to overwrite its previous concretization
decisions, allowing you to choose a new version of Python. If any of the new
packages like Bash are already installed, ``spack install`` won't re-install
them, it will keep the symlinks in place.

^^^^^^^^^^^^^^
Uninstallation
^^^^^^^^^^^^^^

If you decide that Spack isn't right for you, uninstallation is simple.
Just run:

.. code-block:: console

   $ spack env activate myenv
   $ spack uninstall --all

This will uninstall all packages in your environment and remove the symlinks.

------------------------
Using Spack on Travis-CI
------------------------

Spack can be deployed as a provider for userland software in
`Travis-CI <https://http://travis-ci.org>`_.

A starting-point for a ``.travis.yml`` file can look as follows.
It uses `caching <https://docs.travis-ci.com/user/caching/>`_ for
already built environments, so make sure to clean the Travis cache if
you run into problems.

The main points that are implemented below:

#. Travis is detected as having up to 34 cores available, but only 2
   are actually allocated for the user. We limit the parallelism of
   the spack builds in the config.
   (The Travis yaml parser is a bit buggy on the echo command.)

#. Builds over 10 minutes need to be prefixed with ``travis_wait``.
   Alternatively, generate output once with ``spack install -v``.

#. Travis builds are non-interactive. This prevents using bash
   aliases and functions for modules. We fix that by sourcing
   ``/etc/profile`` first (or running everything in a subshell with
   ``bash -l -c '...'``).

.. code-block:: yaml

   language: cpp
   sudo: false
   dist: trusty

   cache:
     apt: true
     directories:
       - $HOME/.cache

   addons:
     apt:
       sources:
         - ubuntu-toolchain-r-test
       packages:
         - g++-4.9
         - environment-modules

   env:
     global:
       - SPACK_ROOT: $HOME/.cache/spack
       - PATH: $PATH:$HOME/.cache/spack/bin

   before_install:
     - export CXX=g++-4.9
     - export CC=gcc-4.9
     - export FC=gfortran-4.9
     - export CXXFLAGS="-std=c++11"

   install:
     - if ! which spack >/dev/null; then
         mkdir -p $SPACK_ROOT &&
         git clone --depth 50 https://github.com/spack/spack.git $SPACK_ROOT &&
         echo -e "config:""\n  build_jobs:"" 2" > $SPACK_ROOT/etc/spack/config.yaml;
       fi
     - travis_wait spack install cmake@3.7.2~openssl~ncurses
     - travis_wait spack install boost@1.62.0~graph~iostream~locale~log~wave
     - spack clean -a
     - source /etc/profile &&
       source $SPACK_ROOT/share/spack/setup-env.sh
     - spack load cmake
     - spack load boost

   script:
     - mkdir -p $HOME/build
     - cd $HOME/build
     - cmake $TRAVIS_BUILD_DIR
     - make -j 2
     - make test

.. _workflow_create_docker_image:

-----------------------------------
Using Spack to Create Docker Images
-----------------------------------

Spack can be the ideal tool to set up images for Docker (and Singularity).

An example ``Dockerfile`` is given below, downloading the latest spack
version.

The following functionality is prepared:

#. Base image: the example starts from a minimal ubuntu.

#. Installing as root: docker images are usually set up as root.
   Since some autotools scripts might complain about this being unsafe, we set
   ``FORCE_UNSAFE_CONFIGURE=1`` to avoid configure errors.

#. Pre-install the spack dependencies, including modules from the packages.
   This avoids needing to build those from scratch via ``spack bootstrap``.
   Package installs are followed by a clean-up of the system package index,
   to avoid outdated information and it saves space.

#. Install spack in ``/usr/local``.
   Add ``setup-env.sh`` to profile scripts, so commands in *login* shells
   can use the whole spack functionality, including modules.

#. Install an example package (``tar``).
   As with system package managers above, ``spack install`` commands should be
   concatenated with a ``&& spack clean -a`` in order to keep image sizes small.

#. Add a startup hook to an *interactive login shell* so spack modules will be
   usable.

In order to build and run the image, execute:

.. code-block:: bash

   docker build -t spack .
   docker run -it spack

.. code-block:: docker

   FROM       ubuntu:16.04
   MAINTAINER Your Name <someone@example.com>

   # general environment for docker
   ENV        DEBIAN_FRONTEND=noninteractive \
              SPACK_ROOT=/usr/local \
              FORCE_UNSAFE_CONFIGURE=1

   # install minimal spack dependencies
   RUN        apt-get update \
              && apt-get install -y --no-install-recommends \
                 autoconf \
                 build-essential \
                 ca-certificates \
                 coreutils \
                 curl \
                 environment-modules \
                 git \
                 python \
                 unzip \
                 vim \
              && rm -rf /var/lib/apt/lists/*

   # load spack environment on login
   RUN        echo "source $SPACK_ROOT/share/spack/setup-env.sh" \
              > /etc/profile.d/spack.sh

   # spack settings
   # note: if you wish to change default settings, add files alongside
   #       the Dockerfile with your desired settings. Then uncomment this line
   #COPY       packages.yaml modules.yaml $SPACK_ROOT/etc/spack/

   # install spack
   RUN        curl -s -L https://api.github.com/repos/spack/spack/tarball \
              | tar xzC $SPACK_ROOT --strip 1
   # note: at this point one could also run ``spack bootstrap`` to avoid
   #       parts of the long apt-get install list above

   # install software
   RUN        spack install tar \
              && spack clean -a

   # need the executables from a package already during image build?
   #RUN        /bin/bash -l -c ' \
   #                spack load tar \
   #                && which tar'

   # image run hook: the -l will make sure /etc/profile environments are loaded
   CMD        /bin/bash -l

^^^^^^^^^^^^^^
Best Practices
^^^^^^^^^^^^^^

"""
MPI
"""
Due to the dependency on Fortran for OpenMPI, which is the spack default
implementation, consider adding ``gfortran`` to the ``apt-get install`` list.

Recent versions of OpenMPI will require you to pass ``--allow-run-as-root``
to your ``mpirun`` calls if started as root user inside Docker.

For execution on HPC clusters, it can be helpful to import the docker
image into Singularity in order to start a program with an *external*
MPI. Otherwise, also add ``openssh-server`` to the ``apt-get install`` list.

""""
CUDA
""""
Starting from CUDA 9.0, Nvidia provides minimal CUDA images based on
Ubuntu.
Please see `their instructions <https://hub.docker.com/r/nvidia/cuda/>`_.
Avoid double-installing CUDA by adding, e.g.

.. code-block:: yaml

   packages:
     cuda:
       paths:
         cuda@9.0.176%gcc@5.4.0 arch=linux-ubuntu16-x86_64: /usr/local/cuda
       buildable: False

to your ``packages.yaml``.
Then ``COPY`` in that file into the image as in the example above.

Users will either need ``nvidia-docker`` or e.g. Singularity to *execute*
device kernels.

"""""""""""
Singularity
"""""""""""
Importing and running the image created above into
`Singularity <http://singularity.lbl.gov/>`_ works like a charm.
Just use the `docker bootstraping mechanism <http://singularity.lbl.gov/quickstart#bootstrap-recipes>`_:

.. code-block:: none

   Bootstrap: docker
   From: registry/user/image:tag

   %runscript
   exec /bin/bash -l

""""""""""""""""""""""
Docker for Development
""""""""""""""""""""""

For examples of how we use docker in development, see
:ref:`docker_for_developers`.

"""""""""""""""""""""""""
Docker on Windows and OSX
"""""""""""""""""""""""""

On Mac OS and Windows, docker runs on a hypervisor that is not allocated much
memory by default, and some spack packages may fail to build due to lack of
memory. To work around this issue, consider configuring your docker installation
to use more of your host memory. In some cases, you can also ease the memory
pressure on parallel builds by limiting the parallelism in your config.yaml.

.. code-block:: yaml

   config:
     build_jobs: 2

------------------
Upstream Bug Fixes
------------------

It is not uncommon to discover a bug in an upstream project while
trying to build with Spack.  Typically, the bug is in a package that
serves a dependency to something else.  This section describes
procedure to work around and ultimately resolve these bugs, while not
delaying the Spack user's main goal.

^^^^^^^^^^^^^^^^^
Buggy New Version
^^^^^^^^^^^^^^^^^

Sometimes, the old version of a package works fine, but a new version
is buggy.  For example, it was once found that `Adios did not build
with hdf5@1.10 <https://github.com/spack/spack/issues/1683>`_.  If the
old version of ``hdf5`` will work with ``adios``, the suggested
procedure is:

#. Revert ``adios`` to the old version of ``hdf5``.  Put in its
   ``adios/package.py``:

   .. code-block:: python

      # Adios does not build with HDF5 1.10
      # See: https://github.com/spack/spack/issues/1683
      depends_on('hdf5@:1.9')

#. Determine whether the problem is with ``hdf5`` or ``adios``, and
   report the problem to the appropriate upstream project.  In this
   case, the problem was with ``adios``.

#. Once a new version of ``adios`` comes out with the bugfix, modify
   ``adios/package.py`` to reflect it:

   .. code-block:: python

      # Adios up to v1.10.0 does not build with HDF5 1.10
      # See: https://github.com/spack/spack/issues/1683
      depends_on('hdf5@:1.9', when='@:1.10.0')
      depends_on('hdf5', when='@1.10.1:')

^^^^^^^^^^^^^^^^
No Version Works
^^^^^^^^^^^^^^^^

Sometimes, *no* existing versions of a dependency work for a build.
This typically happens when developing a new project: only then does
the developer notice that existing versions of a dependency are all
buggy, or the non-buggy versions are all missing a critical feature.

In the long run, the upstream project will hopefully fix the bug and
release a new version.  But that could take a while, even if a bugfix
has already been pushed to the project's repository.  In the meantime,
the Spack user needs things to work.

The solution is to create an unofficial Spack release of the project,
as soon as the bug is fixed in *some* repository.  A study of the `Git
history <https://github.com/citibeth/spack/commits/efischer/develop/var/spack/repos/builtin/packages/py-proj/package.py>`_
of ``py-proj/package.py`` is instructive here:

#. On `April 1 <https://github.com/citibeth/spack/commit/44a1d6a96706affe6ef0a11c3a780b91d21d105a>`_, an initial bugfix was identified for the PyProj project
   and a pull request submitted to PyProj.  Because the upstream
   authors had not yet fixed the bug, the ``py-proj`` Spack package
   downloads from a forked repository, set up by the package's author.
   A non-numeric version number is used to make it easy to upgrade the
   package without recomputing checksums; however, this is an
   untrusted download method and should not be distributed.  The
   package author has now become, temporarily, a maintainer of the
   upstream project:

   .. code-block:: python

      # We need the benefits of this PR
      # https://github.com/jswhit/pyproj/pull/54
      version('citibeth-latlong2',
          git='https://github.com/citibeth/pyproj.git',
          branch='latlong2')


#. By May 14, the upstream project had accepted a pull request with
   the required bugfix.  At this point, the forked repository was
   deleted.  However, the upstream project still had not released a
   new version with a bugfix.  Therefore, a Spack-only release was
   created by specifying the desired hash in the main project
   repository.  The version number ``@1.9.5.1.1`` was chosen for this
   "release" because it's a descendent of the officially released
   version ``@1.9.5.1``.  This is a trusted download method, and can
   be released to the Spack community:

   .. code-block:: python

      # This is not a tagged release of pyproj.
      # The changes in this "version" fix some bugs, especially with Python3 use.
      version('1.9.5.1.1', 'd035e4bc704d136db79b43ab371b27d2',
          url='https://www.github.com/jswhit/pyproj/tarball/0be612cc9f972e38b50a90c946a9b353e2ab140f')

   .. note::

      It would have been simpler to use Spack's Git download method,
      which is also a trusted download in this case:

      .. code-block:: python

         # This is not a tagged release of pyproj.
         # The changes in this "version" fix some bugs, especially with Python3 use.
         version('1.9.5.1.1',
              git='https://github.com/jswhit/pyproj.git',
              commit='0be612cc9f972e38b50a90c946a9b353e2ab140f')

   .. note::

      In this case, the upstream project fixed the bug in its
      repository in a relatively timely manner.  If that had not been
      the case, the numbered version in this step could have been
      released from the forked repository.


#. The author of the Spack package has now become an unofficial
   release engineer for the upstream project.  Depending on the
   situation, it may be advisable to put ``preferred=True`` on the
   latest *officially released* version.

#. As of August 31, the upstream project still had not made a new
   release with the bugfix.  In the meantime, Spack-built ``py-proj``
   provides the bugfix needed by packages depending on it.  As long as
   this works, there is no particular need for the upstream project to
   make a new official release.

#. If the upstream project releases a new official version with the
   bugfix, then the unofficial ``version()`` line should be removed
   from the Spack package.

^^^^^^^
Patches
^^^^^^^

Spack's source patching mechanism provides another way to fix bugs in
upstream projects.  This has advantages and disadvantages compared to the procedures above.

Advantages:

 1. It can fix bugs in existing released versions, and (probably)
    future releases as well.

 2. It is lightweight, does not require a new fork to be set up.

Disadvantages:

 1. It is harder to develop and debug a patch, vs. a branch in a
    repository.  The user loses the automation provided by version
    control systems.

 2. Although patches of a few lines work OK, large patch files can be
    hard to create and maintain.
