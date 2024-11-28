.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _repositories:

=================================
Package Repositories (repos.yaml)
=================================

Spack comes with thousands of built-in package recipes in
``var/spack/repos/builtin/``.  This is a **package repository** -- a
directory that Spack searches when it needs to find a package by name.
You may need to maintain packages for restricted, proprietary or
experimental software separately from the built-in repository. Spack
allows you to configure local repositories using either the
``repos.yaml`` or the ``spack repo`` command.

A package repository is a directory structured like this::

  repo/
      repo.yaml
      packages/
          hdf5/
              package.py
          mpich/
              package.py
              mpich-1.9-bugfix.patch
          trilinos/
              package.py
          ...

The top-level ``repo.yaml`` file contains configuration metadata for the
repository. The packages subdirectory, typically ``packages``, contains
subdirectories for each package in the repository.  Each package directory
contains a ``package.py`` file and any patches or other files needed to build the
package.

The ``repo.yaml`` file may also contain a ``subdirectory`` key,
which can modify the name of the subdirectory used for packages. As seen above,
the default value is ``packages``. An empty string (``subdirectory: ''``) requires
a flattened repo structure in which the package names are top-level subdirectories.

Package repositories allow you to:

1. Maintain your own packages separately from Spack;

2. Share your packages (e.g., by hosting them in a shared file system),
   without committing them to the built-in Spack package repository; and

3. Override built-in Spack packages with your own implementation.

Packages in a separate repository can also *depend on* built-in Spack
packages.  So, you can leverage existing recipes without re-implementing
them in your own repository.

---------------------
``repos.yaml``
---------------------

Spack uses the ``repos.yaml`` file in ``~/.spack`` (and :ref:`elsewhere
<configuration>`) to find repositories. Note that the ``repos.yaml``
configuration file is distinct from the ``repo.yaml`` file in each
repository.  For more on the YAML format, and on how configuration file
precedence works in Spack, see :ref:`configuration <configuration>`.

The default ``etc/spack/defaults/repos.yaml`` file looks like this:

.. code-block:: yaml

  repos:
  - $spack/var/spack/repos/builtin

The file starts with ``repos:`` and contains a single ordered list of
paths to repositories. Each path is on a separate line starting with
``-``.  You can add a repository by inserting another path into the list:

.. code-block:: yaml

  repos:
  - /opt/local-repo
  - $spack/var/spack/repos/builtin

When Spack interprets a spec, e.g., ``mpich`` in ``spack install mpich``,
it searches these repositories in order (first to last) to resolve each
package name.  In this example, Spack will look for the following
packages and use the first valid file:

1. ``/opt/local-repo/packages/mpich/package.py``
2. ``$spack/var/spack/repos/builtin/packages/mpich/package.py``

.. note::

  Currently, Spack can only use repositories in the file system. We plan
  to eventually support URLs in ``repos.yaml``, so that you can easily
  point to remote package repositories, but that is not yet implemented.

---------------------
Namespaces
---------------------

Every repository in Spack has an associated **namespace** defined in its
top-level ``repo.yaml`` file.  If you look at
``var/spack/repos/builtin/repo.yaml`` in the built-in repository, you'll
see that its namespace is ``builtin``:

.. code-block:: console

  $ cat var/spack/repos/builtin/repo.yaml
  repo:
    namespace: builtin

Spack records the repository namespace of each installed package.  For
example, if you install the ``mpich`` package from the ``builtin`` repo,
Spack records its fully qualified name as ``builtin.mpich``.  This
accomplishes two things:

1. You can have packages with the same name from different namespaces
   installed at once.

1. You can easily determine which repository a package came from after it
   is installed (more :ref:`below <namespace-example>`).

.. note::

   It may seem redundant for a repository to have both a namespace and a
   path, but repository *paths* may change over time, or, as mentioned
   above, a locally hosted repository path may eventually be hosted at
   some remote URL.

   Namespaces are designed to allow *package authors* to associate a
   unique identifier with their packages, so that the package can be
   identified even if the repository moves. This is why the namespace is
   determined by the ``repo.yaml`` file in the repository rather than the
   local ``repos.yaml`` configuration: the *repository maintainer* sets
   the name.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Uniqueness
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You should choose a namespace that uniquely identifies your package
repository.  For example, if you make a repository for packages written
by your organization, you could use your organization's name.  You can
also nest namespaces using periods, so you could identify a repository by
a sub-organization.  For example, LLNL might use a namespace for its
internal repositories like ``llnl``. Packages from the Physical & Life
Sciences directorate (PLS) might use the ``llnl.pls`` namespace, and
packages created by the Computation directorate might use ``llnl.comp``.

Spack cannot ensure that every repository is named uniquely, but it will
prevent you from registering two repositories with the same namespace at
the same time.  If you try to add a repository that has the same name as
an existing one, e.g., ``builtin``, Spack will print a warning message.

.. _namespace-example:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Namespace example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose that LLNL maintains its own version of ``mpich``, separate from
Spack's built-in ``mpich`` package, and suppose you've installed both
LLNL's and Spack's ``mpich`` packages.  If you just use ``spack find``,
you won't see a difference between these two packages:

.. code-block:: console

  $ spack find
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  mpich@3.2  mpich@3.2

However, if you use ``spack find -N``, Spack will display the packages
with their namespaces:

.. code-block:: console

  $ spack find -N
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  builtin.mpich@3.2  llnl.comp.mpich@3.2

Now you know which one is LLNL's special version, and which one is the
built-in Spack package.  As you might guess, packages that are identical
except for their namespace will still have different hashes:

.. code-block:: console

  $ spack find -lN
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  c35p3gc builtin.mpich@3.2  itoqmox llnl.comp.mpich@3.2

All Spack commands that take a package :ref:`spec <sec-specs>` can also
accept a fully qualified spec with a namespace.  This means you can use
the namespace to be more specific when designating, e.g., which package
you want to uninstall:

.. code-block:: console

  spack uninstall llnl.comp.mpich

----------------------------
Overriding built-in packages
----------------------------

Spack's search semantics mean that you can make your own implementation
of a built-in Spack package (like ``mpich``), put it in a repository, and
use it to override the built-in package.  As long as the repository
containing your ``mpich`` is earlier any other in ``repos.yaml``, any
built-in package that depends on ``mpich`` will be use the one in your
repository.

Suppose you have three repositories: the builtin Spack repo
(``builtin``), a shared repo for your institution (e.g., ``llnl``), and a
repo containing your own prototype packages (``proto``).  Suppose they
contain packages as follows:

  +--------------+------------------------------------+-----------------------------+
  | Namespace    | Path to repo                       | Packages                    |
  +==============+====================================+=============================+
  | ``proto``    | ``~/proto``                        | ``mpich``                   |
  +--------------+------------------------------------+-----------------------------+
  | ``llnl``     | ``/usr/local/llnl``                | ``hdf5``                    |
  +--------------+------------------------------------+-----------------------------+
  | ``builtin``  | ``$spack/var/spack/repos/builtin`` | ``mpich``, ``hdf5``, others |
  +--------------+------------------------------------+-----------------------------+

Suppose that ``hdf5`` depends on ``mpich``.  You can override the
built-in ``hdf5`` by adding the ``llnl`` repo to ``repos.yaml``:

.. code-block:: yaml

   repos:
   - /usr/local/llnl
   - $spack/var/spack/repos/builtin

``spack install hdf5`` will install ``llnl.hdf5 ^builtin.mpich``.

If, instead, ``repos.yaml`` looks like this:

.. code-block:: yaml

   repos:
   - ~/proto
   - /usr/local/llnl
   - $spack/var/spack/repos/builtin

``spack install hdf5`` will install ``llnl.hdf5 ^proto.mpich``.

Any unqualified package name will be resolved by searching ``repos.yaml``
from the first entry to the last.  You can force a particular
repository's package by using a fully qualified name.  For example, if
your ``repos.yaml`` is as above, and you want ``builtin.mpich`` instead
of ``proto.mpich``, you can write::

  spack install hdf5 ^builtin.mpich

which will install ``llnl.hdf5 ^builtin.mpich``.

Similarly, you can force the ``builtin.hdf5`` like this::

  spack install builtin.hdf5 ^builtin.mpich

This will not search ``repos.yaml`` at all, as the ``builtin`` repo is
specified in both cases.  It will install ``builtin.hdf5
^builtin.mpich``.

If you want to see which repositories will be used in a build *before*
you install it, you can use ``spack spec -N``:

.. code-block:: console

   $ spack spec -N hdf5
   Input spec
   --------------------------------
   hdf5

   Normalized
   --------------------------------
   hdf5
       ^zlib@1.1.2:

   Concretized
   --------------------------------
   builtin.hdf5@1.10.0-patch1%apple-clang@7.0.2+cxx~debug+fortran+mpi+shared~szip~threadsafe arch=darwin-elcapitan-x86_64
       ^builtin.openmpi@2.0.1%apple-clang@7.0.2~mxm~pmi~psm~psm2~slurm~sqlite3~thread_multiple~tm~verbs+vt arch=darwin-elcapitan-x86_64
           ^builtin.hwloc@1.11.4%apple-clang@7.0.2 arch=darwin-elcapitan-x86_64
               ^builtin.libpciaccess@0.13.4%apple-clang@7.0.2 arch=darwin-elcapitan-x86_64
                   ^builtin.libtool@2.4.6%apple-clang@7.0.2 arch=darwin-elcapitan-x86_64
                       ^builtin.m4@1.4.17%apple-clang@7.0.2+sigsegv arch=darwin-elcapitan-x86_64
                           ^builtin.libsigsegv@2.10%apple-clang@7.0.2 arch=darwin-elcapitan-x86_64
                   ^builtin.pkg-config@0.29.1%apple-clang@7.0.2+internal_glib arch=darwin-elcapitan-x86_64
                   ^builtin.util-macros@1.19.0%apple-clang@7.0.2 arch=darwin-elcapitan-x86_64
       ^builtin.zlib@1.2.8%apple-clang@7.0.2+pic arch=darwin-elcapitan-x86_64

.. warning::

   You *can* use a fully qualified package name in a ``depends_on``
   directive in a ``package.py`` file, like so::

       depends_on('proto.hdf5')

   This is *not* recommended, as it makes it very difficult for
   multiple repos to be composed and shared.  A ``package.py`` like this
   will fail if the ``proto`` repository is not registered in
   ``repos.yaml``.

.. _cmd-spack-repo:

--------------------------
``spack repo``
--------------------------

Spack's :ref:`configuration system <configuration>` allows repository
settings to come from ``repos.yaml`` files in many locations.  If you
want to see the repositories registered as a result of all configuration
files, use ``spack repo list``.

^^^^^^^^^^^^^^^^^^^
``spack repo list``
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

  $ spack repo list
  ==> 2 package repositories.
  myrepo     ~/myrepo
  builtin    ~/spack/var/spack/repos/builtin

Each repository is listed with its associated namespace.  To get the raw,
merged YAML from all configuration files, use ``spack config get repos``:

.. code-block:: console

   $ spack config get repos
   repos:srepos:
   - ~/myrepo
   - $spack/var/spack/repos/builtin

Note that, unlike ``spack repo list``, this does not include the
namespace, which is read from each repo's ``repo.yaml``.

^^^^^^^^^^^^^^^^^^^^^
``spack repo create``
^^^^^^^^^^^^^^^^^^^^^

To make your own repository, you don't need to construct a directory
yourself; you can use the ``spack repo create`` command.

.. code-block:: console

  $ spack repo create myrepo
  ==> Created repo with namespace 'myrepo'.
  ==> To register it with spack, run this command:
    spack repo add ~/myrepo

  $ ls myrepo
  packages/  repo.yaml

  $ cat myrepo/repo.yaml
  repo:
    namespace: 'myrepo'

By default, the namespace of a new repo matches its directory's name.
You can supply a custom namespace with a second argument, e.g.:

.. code-block:: console

  $ spack repo create myrepo llnl.comp
  ==> Created repo with namespace 'llnl.comp'.
  ==> To register it with spack, run this command:
    spack repo add ~/myrepo

  $ cat myrepo/repo.yaml
  repo:
    namespace: 'llnl.comp'

You can also create repositories with custom structure with the ``-d/--subdirectory``
argument, e.g.:

.. code-block:: console

  $ spack repo create -d applications myrepo apps
  ==> Created repo with namespace 'apps'.
  ==> To register it with Spack, run this command:
    spack repo add ~/myrepo

  $ ls myrepo
  applications/  repo.yaml

  $ cat myrepo/repo.yaml
  repo:
    namespace: apps
    subdirectory: applications

^^^^^^^^^^^^^^^^^^
``spack repo add``
^^^^^^^^^^^^^^^^^^

Once your repository is created, you can register it with Spack with
``spack repo add``:

.. code-block:: console

   $ spack repo add ./myrepo
   ==> Added repo with namespace 'llnl.comp'.

   $ spack repo list
   ==> 2 package repositories.
   llnl.comp    ~/myrepo
   builtin      ~/spack/var/spack/repos/builtin

This simply adds the repo to your ``repos.yaml`` file.

Once a repository is registered like this, you should be able to see its
packages' names in the output of ``spack list``, and you should be able
to build them using ``spack install <name>`` as you would with any
built-in package.

^^^^^^^^^^^^^^^^^^^^^
``spack repo remove``
^^^^^^^^^^^^^^^^^^^^^

You can remove an already-registered repository with ``spack repo rm``.
This will work whether you pass the repository's namespace *or* its
path.

By namespace:

.. code-block:: console

  $ spack repo rm llnl.comp
  ==> Removed repository ~/myrepo with namespace 'llnl.comp'.

  $ spack repo list
  ==> 1 package repository.
  builtin    ~/spack/var/spack/repos/builtin

By path:

.. code-block:: console

  $ spack repo rm ~/myrepo
  ==> Removed repository ~/myrepo

  $ spack repo list
  ==> 1 package repository.
  builtin    ~/spack/var/spack/repos/builtin

--------------------------------
Repo namespaces and Python
--------------------------------

You may have noticed that namespace notation for repositories is similar
to the notation for namespaces in Python.  As it turns out, you *can*
treat Spack repositories like Python packages; this is how they are
implemented.

You could, for example, extend a ``builtin`` package in your own
repository:

.. code-block:: python

   from spack.pkg.builtin.mpich import Mpich

   class MyPackage(Mpich):
       ...

Spack repo namespaces are actually Python namespaces tacked on under
``spack.pkg``.  The search semantics of ``repos.yaml`` are actually
implemented using Python's built-in `sys.path
<https://docs.python.org/2/library/sys.html#sys.path>`_ search.  The
:py:mod:`spack.repo` module implements a custom `Python importer
<https://docs.python.org/2/library/imp.html>`_.

