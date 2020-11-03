.. Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

=========
Workflows
=========

The process of using Spack involves building packages, running
binaries from those packages, and developing software that depends on
those packages.  For example, one might use Spack to build the
``netcdf`` package, use ``spack load`` to run the ``ncdump`` binary, and
finally, write a small C program to read/write a particular NetCDF file.

Spack supports a variety of workflows to suit a variety of situations
and user preferences, there is no single way to do all these things.
This chapter demonstrates different workflows that have been
developed, pointing out the pros and cons of them.

-----------
Definitions
-----------

First some basic definitions.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Package, Concrete Spec, Installed Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Spack, a package is an abstract recipe to build one piece of software.
Spack packages may be used to build, in principle, any version of that
software with any set of variants.  Examples of packages include
``curl`` and ``zlib``.

A package may be *instantiated* to produce a concrete spec; one
possible realization of a particular package, out of combinatorially
many other realizations.  For example, here is a concrete spec
instantiated from ``curl``:

.. command-output:: spack spec curl

Spack's core concretization algorithm generates concrete specs by
instantiating packages from its repo, based on a set of "hints",
including user input and the ``packages.yaml`` file.  This algorithm
may be accessed at any time with the ``spack spec`` command.

Every time Spack installs a package, that installation corresponds to
a concrete spec.  Only a vanishingly small fraction of possible
concrete specs will be installed at any one Spack site.

^^^^^^^^^^^^^^^
Consistent Sets
^^^^^^^^^^^^^^^

A set of Spack specs is said to be *consistent* if each package is
only instantiated one way within it --- that is, if two specs in the
set have the same package, then they must also have the same version,
variant, compiler, etc.  For example, the following set is consistent:

.. code-block:: console

   curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
       ^openssl@1.0.2k%gcc@5.3.0 arch=linux-SuSE11-x86_64
       ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
   zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64

The following set is not consistent:

.. code-block:: console

   curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
       ^openssl@1.0.2k%gcc@5.3.0 arch=linux-SuSE11-x86_64
       ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
   zlib@1.2.7%gcc@5.3.0 arch=linux-SuSE11-x86_64

The compatibility of a set of installed packages determines what may
be done with it.  It is always possible to ``spack load`` any set of
installed packages, whether or not they are consistent, and run their
binaries from the command line.  However, a set of installed packages
can only be linked together in one binary if it is consistent.

If the user produces a series of ``spack spec`` or ``spack load``
commands, in general there is no guarantee of consistency between
them.  Spack's concretization procedure guarantees that the results of
any *single* ``spack spec`` call will be consistent.  Therefore, the
best way to ensure a consistent set of specs is to create a Spack
package with dependencies, and then instantiate that package.  We will
use this technique below.

-----------------
Building Packages
-----------------

Suppose you are tasked with installing a set of software packages on a
system in order to support one application -- both a core application
program, plus software to prepare input and analyze output.  The
required software might be summed up as a series of ``spack install``
commands placed in a script.  If needed, this script can always be run
again in the future.  For example:

.. code-block:: sh

   #!/bin/sh
   spack install modele-utils
   spack install emacs
   spack install ncview
   spack install nco
   spack install modele-control
   spack install py-numpy

In most cases, this script will not correctly install software
according to your specific needs: choices need to be made for
variants, versions and virtual dependency choices may be needed.  It
*is* possible to specify these choices by extending specs on the
command line; however, the same choices must be specified repeatedly.
For example, if you wish to use ``openmpi`` to satisfy the ``mpi``
dependency, then ``^openmpi`` will have to appear on *every* ``spack
install`` line that uses MPI.  It can get repetitive fast.

Customizing Spack installation options is easier to do in the
``~/.spack/packages.yaml`` file.  In this file, you can specify
preferred versions and variants to use for packages.  For example:

.. code-block:: yaml

   packages:
       python:
           version: [3.5.1]
       modele-utils:
           version: [cmake]

       everytrace:
           version: [develop]
       eigen:
           variants: ~suitesparse
       netcdf:
           variants: +mpi

       all:
           compiler: [gcc@5.3.0]
           providers:
               mpi: [openmpi]
               blas: [openblas]
               lapack: [openblas]


This approach will work as long as you are building packages for just
one application.

^^^^^^^^^^^^^^^^^^^^^
Multiple Applications
^^^^^^^^^^^^^^^^^^^^^

Suppose instead you're building multiple inconsistent applications.
For example, users want package A to be built with ``openmpi`` and
package B with ``mpich`` --- but still share many other lower-level
dependencies.  In this case, a single ``packages.yaml`` file will not
work.  Plans are to implement *per-project* ``packages.yaml`` files.
In the meantime, one could write shell scripts to switch
``packages.yaml`` between multiple versions as needed, using symlinks.

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

------------------------------
Running Binaries from Packages
------------------------------

Once Spack packages have been built, the next step is to use them.  As
with building packages, there are many ways to use them, depending on
the use case.

^^^^^^^^^^^^
Find and Run
^^^^^^^^^^^^

The simplest way to run a Spack binary is to find it and run it!
In many cases, nothing more is needed because Spack builds binaries
with RPATHs.  Spack installation directories may be found with ``spack
location --install-dir`` commands.  For example:

.. code-block:: console

   $ spack location --install-dir cmake
   ~/spack/opt/spack/linux-SuSE11-x86_64/gcc-5.3.0/cmake-3.6.0-7cxrynb6esss6jognj23ak55fgxkwtx7

This gives the root of the Spack package; relevant binaries may be
found within it.  For example:

.. code-block:: console

   $ CMAKE=`spack location --install-dir cmake`/bin/cmake


Standard UNIX tools can find binaries as well.  For example:

.. code-block:: console

   $ find ~/spack/opt -name cmake | grep bin
   ~/spack/opt/spack/linux-SuSE11-x86_64/gcc-5.3.0/cmake-3.6.0-7cxrynb6esss6jognj23ak55fgxkwtx7/bin/cmake

These methods are suitable, for example, for setting up build
processes or GUIs that need to know the location of particular tools.
However, other more powerful methods are generally preferred for user
environments.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using ``spack load`` to Manage the User Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose that Spack has been used to install a set of command-line
programs, which users now wish to use.  One can in principle put a
number of ``spack load`` commands into ``.bashrc``, for example, to
load a set of Spack packages:

.. code-block:: sh

   spack load modele-utils
   spack load emacs
   spack load ncview
   spack load nco
   spack load modele-control

Although simple load scripts like this are useful in many cases, they
have some drawbacks:

1. The set of packages loaded by them will in general not be
   consistent.  They are a decent way to load commands to be called
   from command shells.  See below for better ways to assemble a
   consistent set of packages for building application programs.

2. The ``spack spec`` and ``spack install`` commands use a
   sophisticated concretization algorithm that chooses the "best"
   among several options, taking into account ``packages.yaml`` file.
   The ``spack load`` and ``spack module tcl loads`` commands, on the
   other hand, are not very smart: if the user-supplied spec matches
   more than one installed package, then ``spack module tcl loads`` will
   fail. This default behavior may change in the future.  For now,
   the workaround is to either be more specific on any failing ``spack load``
   commands or to use ``spack load --first`` to allow spack to load the
   first matching spec.


""""""""""""""""""""""
Generated Load Scripts
""""""""""""""""""""""

Another problem with using `spack load` is, it can be slow; a typical
user environment could take several seconds to load, and would not be
appropriate to put into ``.bashrc`` directly.  This is because it
requires the full start-up overhead of python/Spack for each command.
In some circumstances it is preferable to use a series of ``spack
module tcl loads`` (or ``spack module lmod loads``) commands to
pre-compute which modules to load.  This will generate the modulenames
to load the packages using environment modules, rather than Spack's
built-in support for environment modifications. These can be put in a
script that is run whenever installed Spack packages change.  For
example:

.. code-block:: sh

   #!/bin/sh
   #
   # Generate module load commands in ~/env/spackenv

   cat <<EOF | /bin/sh >$HOME/env/spackenv
   FIND='spack module tcl loads --prefix linux-SuSE11-x86_64/'

   \$FIND modele-utils
   \$FIND emacs
   \$FIND ncview
   \$FIND nco
   \$FIND modele-control
   EOF

The output of this file is written in ``~/env/spackenv``:

.. code-block:: sh

   # binutils@2.25%gcc@5.3.0+gold~krellpatch~libiberty arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/binutils-2.25-gcc-5.3.0-6w5d2t4
   # python@2.7.12%gcc@5.3.0~tk~ucs4 arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/python-2.7.12-gcc-5.3.0-2azoju2
   # ncview@2.1.7%gcc@5.3.0 arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/ncview-2.1.7-gcc-5.3.0-uw3knq2
   # nco@4.5.5%gcc@5.3.0 arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/nco-4.5.5-gcc-5.3.0-7aqmimu
   # modele-control@develop%gcc@5.3.0 arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/modele-control-develop-gcc-5.3.0-7rddsij
   # zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/zlib-1.2.8-gcc-5.3.0-fe5onbi
   # curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/curl-7.50.1-gcc-5.3.0-4vlev55
   # hdf5@1.10.0-patch1%gcc@5.3.0+cxx~debug+fortran+mpi+shared~szip~threadsafe arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/hdf5-1.10.0-patch1-gcc-5.3.0-pwnsr4w
   # netcdf@4.4.1%gcc@5.3.0~hdf4+mpi arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/netcdf-4.4.1-gcc-5.3.0-rl5canv
   # netcdf-fortran@4.4.4%gcc@5.3.0 arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/netcdf-fortran-4.4.4-gcc-5.3.0-stdk2xq
   # modele-utils@cmake%gcc@5.3.0+aux+diags+ic arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/modele-utils-cmake-gcc-5.3.0-idyjul5
   # everytrace@develop%gcc@5.3.0+fortran+mpi arch=linux-SuSE11-x86_64
   module load linux-SuSE11-x86_64/everytrace-develop-gcc-5.3.0-p5wmb25

Users may now put ``source ~/env/spackenv`` into ``.bashrc``.

.. note ::

   Some module systems put a prefix on the names of modules created
   by Spack.  For example, that prefix is ``linux-SuSE11-x86_64/`` in
   the above case.  If a prefix is not needed, you may omit the
   ``--prefix`` flag from ``spack module tcl loads``.


"""""""""""""""""""""""
Transitive Dependencies
"""""""""""""""""""""""

In the script above, each ``spack module tcl loads`` command generates a
*single* ``module load`` line.  Transitive dependencies do not usually
need to be loaded, only modules the user needs in ``$PATH``.  This is
because Spack builds binaries with RPATH.  Spack's RPATH policy has
some nice features:

#. Modules for multiple inconsistent applications may be loaded
   simultaneously.  In the above example (Multiple Applications),
   package A and package B can coexist together in the user's $PATH,
   even though they use different MPIs.

#. RPATH eliminates a whole class of strange errors that can happen
   in non-RPATH binaries when the wrong ``LD_LIBRARY_PATH`` is
   loaded.

#. Recursive module systems such as LMod are not necessary.

#. Modules are not needed at all to execute binaries.  If a path to a
   binary is known, it may be executed.  For example, the path for a
   Spack-built compiler can be given to an IDE without requiring the
   IDE to load that compiler's module.

Unfortunately, Spack's RPATH support does not work in all case.  For example:

#. Software comes in many forms --- not just compiled ELF binaries,
   but also as interpreted code in Python, R, JVM bytecode, etc.
   Those systems almost universally use an environment variable
   analogous to ``LD_LIBRARY_PATH`` to dynamically load libraries.

#. Although Spack generally builds binaries with RPATH, it does not
   currently do so for compiled Python extensions (for example,
   ``py-numpy``).  Any libraries that these extensions depend on
   (``blas`` in this case, for example) must be specified in the
   ``LD_LIBRARY_PATH``.`

#. In some cases, Spack-generated binaries end up without a
   functional RPATH for no discernible reason.

In cases where RPATH support doesn't make things "just work," it can
be necessary to load a module's dependencies as well as the module
itself.  This is done by adding the ``--dependencies`` flag to the
``spack module tcl loads`` command.  For example, the following line,
added to the script above, would be used to load SciPy, along with
Numpy, core Python, BLAS/LAPACK and anything else needed:

.. code-block:: sh

   spack module tcl loads --dependencies py-scipy

^^^^^^^^^^^^^^
Dummy Packages
^^^^^^^^^^^^^^

As an alternative to a series of ``module load`` commands, one might
consider dummy packages as a way to create a *consistent* set of
packages that may be loaded as one unit.  The idea here is pretty
simple:

#. Create a package (say, ``mydummy``) with no URL and no
   ``install()`` method, just dependencies.

#. Run ``spack install mydummy`` to install.

An advantage of this method is the set of packages produced will be
consistent.  This means that you can reliably build software against
it.  A disadvantage is the set of packages will be consistent; this
means you cannot load up two applications this way if they are not
consistent with each other.

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

#. Without control for the user, Travis jobs will run on various
   ``x86_64`` microarchitectures. If you plan to cache build results,
   e.g. to accelerate dependency builds, consider building for the
   generic ``x86_64`` target only.
   Limiting the microarchitecture will also find more packages when
   working with the
   `E4S Spack build cache <https://oaciss.uoregon.edu/e4s/e4s_buildcache_inventory.html>`_.

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
     - |
       if ! which spack >/dev/null; then
         mkdir -p $SPACK_ROOT &&
         git clone --depth 50 https://github.com/spack/spack.git $SPACK_ROOT &&
         printf "config:\n  build_jobs: 2\n" > $SPACK_ROOT/etc/spack/config.yaml &&
         printf "packages:\n  all:\n    target: ['x86_64']\n" \
                 > $SPACK_ROOT/etc/spack/packages.yaml;
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
