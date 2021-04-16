.. Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

===========
Using Spack
===========

.. TODO: Write an introduction to this part of the guide

--------------------------------
How do I run installed packages?
--------------------------------

^^^^^^^
Problem
^^^^^^^

You have built an application with Spack and now you want to run it.

^^^^^^^^
Solution
^^^^^^^^
There are many ways to use packages once they have been installed
by Spack. Which one to choose depends on the use case. Below we'll
summarize the most common situations.

"""""""""""""""
1) Just run it!
"""""""""""""""

Spack builds applications using ``RPATH`` whenever it can.
This means that binary executables can run without the need to modify
the shell environment to find their library dependencies.
To check where a package has been installed you can use
the ``-p`` option of ``spack find``:

.. code-block:: console

   $ spack find -p cmake
   ==> 3 installed packages
   -- darwin-catalina-x86_64 / apple-clang@11.0.0 ------------------
   cmake@3.18.1  /Users/spack/spack/opt/spack/darwin-catalina-x86_64/apple-clang-11.0.0/cmake-3.18.1-rkhbrznb73yds25caqhypjowwlecgfne

You can then run the application using e.g. its absolute path:

.. code-block:: console

   $ /Users/spack/spack/opt/spack/darwin-catalina-x86_64/apple-clang-11.0.0/cmake-3.18.1-rkhbrznb73yds25caqhypjowwlecgfne/bin/cmake --version
   cmake version 3.18.1

   CMake suite maintained and supported by Kitware (kitware.com/cmake)

"""""""""""""""""
2) ``spack load``
"""""""""""""""""

Another method is to let Spack modify your shell environment
and put the application folder in your ``PATH``. This can be
obtained via the ``spack load`` command:

.. code-block:: console

   $ spack load cmake
   $ which cmake
   /Users/spack/spack/opt/spack/darwin-catalina-x86_64/apple-clang-11.0.0/cmake-3.18.1-rkhbrznb73yds25caqhypjowwlecgfne/bin/cmake

If need be, it's possible to ask Spack which packages have been
loaded into your shell with the ``--loaded`` option of ``spack find``:

.. code-block:: console

   $ spack find --loaded
   ==> 4 installed packages
   -- darwin-catalina-x86_64 / apple-clang@11.0.0 ------------------
   cmake@3.18.1  ncurses@6.2  openssl@1.1.1h  zlib@1.2.11

When you're finished you can unload all the packages to restore the
initial state of your environment:


.. code-block:: console

   $ spack unload -a
   $ spack find --loaded
   ==> 0 installed packages

"""""""""""""""""""""""""""""""
3) Project software into a view
"""""""""""""""""""""""""""""""

Filesystem views are a viable alternative when there is no
need to switch between different configurations of the same
software. A "view" is a single directory tree where multiple
packages installed by Spack are linked into, resulting in a
structure very similar to that of many linux folders e.g.
``/usr/local``.

Views are directly supported by Spack environments. For instance the
``spack.yaml`` file below:

.. code-block:: yaml

   spack:
     specs:
     - clingo@master
     view: ~/local/clingo

generates a view in the ``~/local/clingo`` directory with the
following structure:

.. code-block:: console

   $ tree -L 1 ~/local/clingo
   /Users/spack/local/clingo
   ├── bin
   ├── etc
   ├── include
   ├── lib
   ├── libexec
   ├── man
   └── share

The default projection into a view is to link every package into the
root of the view, as you can see from the example above. This can be
changed by adding a ``projections`` stanza to your configuration.
:ref:`environment_managed_views` shows more details on how to do that
for Spack Environments.
For free-standing views you can instead add a configuration
file named ``projections.yaml`` in the ``.spack`` directory
within the root folder of the view.

In both cases the ``projections`` stanza is a mapping of partial
specs to spec format strings:

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
matter. Given the example above:

1. Any spec satisfying ``zlib@1.2.8`` will be linked into ``<view-root>/zlib-1.2.8/``
2. Any spec satisfying ``hdf5@1.8.10+mpi %gcc@4.9.3 ^mvapich2@2.2`` will be linked into
   ``<view-root>/hdf5-1.8.10/mvapich2-2.2-gcc-4.9.3``
3. Any spec satisfying ``hdf5@1.8.10~mpi %gcc@4.9.3`` will be linked into
   ``<view-root>/hdf5-1.8.10/gcc-4.9.3``.

If the keyword ``all`` does not appear in the projections
configuration file, any spec that does not satisfy any entry in the
file will be linked into the root of the view as in a single-prefix
view. Any entries that appear below the keyword ``all`` in the
projections configuration file will not be used, as all specs will use
the projection under ``all`` before reaching those entries.

^^^^^^^^^^
Discussion
^^^^^^^^^^

`spack load` is a very convenient method to quickly try
applications installed by Spack, but it can be slow so this
technique is not appropriate for use with shell configuration
files like ``.bashrc``.

The files of the view's installed packages are brought into
the view by symbolic or hard links, referencing the original
Spack installation. When software is built and installed,
absolute paths are frequently "baked into" the software,
making it non-relocatable. This happens not just in RPATHs,
but also in shebangs, configuration files, and assorted
other locations.
Programs run out of a Spack view will typically still look
in the original Spack-installed location for shared libraries and
other resources. This behavior is not easily changed. In general,
there is no way to know where absolute paths might be written into an
installed package, and how to relocate it. Therefore, the original
Spack tree must be kept in place for a filesystem view to work, even
if the view is built with hardlinks.

On systems with inode quotas, modules might be preferable to views.

-----------------------------------------------
How do I build a combinatorial set of packages?
-----------------------------------------------

^^^^^^^
Problem
^^^^^^^

You are tasked with installing a set of software packages on a system,
including multiple versions of the same library or application, and
you would like to do it in a way that is as compact and as reproducible
as possible.

^^^^^^^^
Solution
^^^^^^^^

To install a combinatorial set of software you can define
:ref:`environment_spec_matrices` in your ``spack.yaml``
file. For example this code:

.. code-block:: yaml

   spack:
     specs:
       - matrix:
           - ['gromacs+mpi', 'cp2k+mpi']
           - ['^mpich', '^openmpi']
           - ['%gcc', '%intel']

installs four different flavors of both ``gromacs`` and ``cp2k``,
varying the combination of the MPI library and compiler used in each.

^^^^^^^^^^
Discussion
^^^^^^^^^^

This technique is very useful to deploy software stacks on HPC clusters, and
it can be complemented by the addition in the same ``spack.yaml`` file
of more configuration to match site-specific needs. For instance the
following file:

.. code-block:: yaml

   spack:
     specs:
       - matrix:
           - ['gromacs+mpi', 'cp2k+mpi']
           - ['^mpich', '^openmpi']
           - ['%gcc', '%intel']
     config:
       install_tree:
         root: /software/spack
     modules:
       enable:
       - tcl
     view: False

will install the software at a specific location on the filesystem
and generate non-hierarchical module files for it. You can have a
look at the :ref:`environments` section for a comprehensive list
of all the customizations that are allowed within Spack environments.

If the set of software to install is particularly complex, you can
define handles for just part of your constraints as shown in
:ref:`environment_spec_list_references`:

.. code-block:: yaml

   spack:
     definitions:
     - compilers: ['%gcc', '%intel']
     - mpis: [^mpich, ^openmpi]

     specs:
       - matrix:
           - [gromacs+mpi, cp2k+mpi]
           - [$compilers]
           - [$mpis]

and reuse the definitions across your ``spack.yaml`` file.

--------------------------------------------------------------
How do I use Spack for single-user installations on my laptop?
--------------------------------------------------------------

^^^^^^^
Problem
^^^^^^^
You are already using Spack on clusters or workstations and
you would like to use it also to maintain the software
installations on your laptop, in a way that is similar to
what Homebrew or Conda do.

^^^^^^^^
Solution
^^^^^^^^

Spack is an incredibly powerful package manager, designed for supercomputers
where users have diverse installation needs. But Spack can also be used to
handle simple single-user installations on your laptop. Most macOS users are
already familiar with package managers like Homebrew and Conda, where all
installed packages are symlinked to a single central location like ``/usr/local``.

To emulate the same behavior with Spack you can use :ref:`environments`:

.. code-block:: console

   $ spack env create myenv
   ==> Updating view at /Users/me/spack/var/spack/environments/myenv/.spack-env/view
   ==> Created environment 'myenv' in /Users/me/spack/var/spack/environments/myenv
   ==> You can activate this environment with:
   ==>   spack env activate myenv
   $ spack env activate myenv

Here, *myenv* can be anything you want to name your environment. The list of packages
you need can be constructed incrementally from the command line:

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
Any spec you would normally use on the command line with other Spack commands
can be added to the environment.
In the ``myenv`` directory, you can find the ``spack.yaml`` that actually
defines the environment.

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
     view: true

The packages added earlier are in the ``specs:`` section. If you
ever want to add more packages, you can either use ``spack add`` or manually
edit this file.

By default, Spack concretizes each spec *separately*, allowing multiple
versions of the same package to coexist. Since we want a single consistent
environment, we want to concretize all of the specs *together*:

.. code-block:: yaml
   :emphasize-lines: 9

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs: [bash, 'python@3:', py-numpy, py-scipy, py-matplotlib]
     view: true
     concretization: together

The view associated with the environment can be easily changed to any
directory you want. For example, Homebrew uses ``/usr/local``, while Conda
uses ``/Users/me/anaconda``. In order to access files in these locations,
you need to update ``PATH`` and other environment variables
to point to them. Activating the Spack environment does this automatically, but
you can also manually set them in your ``.bashrc``.

.. TODO: Remove warning ?

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


To actually concretize the environment, run:

.. code-block:: console

   $ spack concretize

This will tell you which if any packages are already installed, and alert you
to any conflicting specs. To install these packages and symlink them to your ``view:``
directory, run instead:

.. code-block:: console

   $ spack install

Now, when you type ``which python3``, it should find the one you just installed.

^^^^^^^^^^
Discussion
^^^^^^^^^^

In order to change the default shell to our newer Bash installation, we first
need to add it to the list of acceptable shells. Run:

.. code-block:: console

   $ sudo vim /etc/shells

and add the absolute path to your bash executable. Then:

.. code-block:: console

   $ chsh -s /path/to/bash

If you log out and log back in, ``echo $SHELL`` should point to the
newer version of Bash.

If your OS upgraded to a newer version, or a new version of Python
was released, you may want to rebuild your entire software stack. To do this,
simply run the following commands:

.. code-block:: console

   $ spack env activate myenv
   $ spack concretize --force
   $ spack install

The ``--force`` flag tells Spack to overwrite its previous concretization
decisions, allowing you to choose a new version of Python. If any of the new
packages like Bash are already installed, ``spack install`` won't re-install
them, it will keep the symlinks in place.

If you decide that Spack isn't right for you, uninstallation is as simple as:

.. code-block:: console

   $ spack env activate myenv
   $ spack uninstall --all

This will uninstall all packages in your environment and remove the symlinks.
