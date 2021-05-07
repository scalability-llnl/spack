.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _troubleshooting:

======================
Troubleshooting Spack
======================

**Where is my spack configuration coming from?**

Spack pulls configuration from several files in different directories which get resolved into
final configuration. To learn more about configuration scopes click :ref:`here <configuration-scopes>`.
The `spack config blame` is a useful command to track configuration lines from configuration scopes. This
command can be used with the configuration scopes `compilers`, `config`, `mirrors`, `modules`, `packages`,
and `repo`. For more detail see ``spack config blame --help``. In this example
below we see breakdown of spack configuration pulled from different files for `modules` configuration.


.. code-block:: console

    $ spack config blame modules
    ---                                                                               modules:
    /Users/siddiq90/.spack/modules.yaml:2                                               lmod:
    /Users/siddiq90/.spack/modules.yaml:3                                                 hash_length: 0
    /Users/siddiq90/.spack/modules.yaml:4                                                 core_compilers:
    /Users/siddiq90/.spack/modules.yaml:5                                                 - apple-clang@11.0.3
    /Users/siddiq90/.spack/modules.yaml:6                                                 - gcc@9.3.0
    /Users/siddiq90/.spack/modules.yaml:7                                                 - gcc@10.2.0
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:38             hierarchy:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:39             - mpi
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/darwin/modules.yaml:17    prefix_inspections:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/darwin/modules.yaml:18      lib:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/darwin/modules.yaml:19      - DYLD_FALLBACK_LIBRARY_PATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/darwin/modules.yaml:20      lib64:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/darwin/modules.yaml:21      - DYLD_FALLBACK_LIBRARY_PATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:20             bin:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:21             - PATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:22             man:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:23             - MANPATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:24             share/man:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:25             - MANPATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:26             share/aclocal:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:27             - ACLOCAL_PATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:28             lib/pkgconfig:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:29             - PKG_CONFIG_PATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:30             lib64/pkgconfig:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:31             - PKG_CONFIG_PATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:32             share/pkgconfig:
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:33             - PKG_CONFIG_PATH
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:17             ? ''
    /Users/siddiq90/Documents/github/spack/etc/spack/defaults/modules.yaml:18             : - CMAKE_PREFIX_PATH


If you want full control over your spack configuration, it's best to create a :ref:`spack environment <environments>`
and specify your configuration in `spack.yaml`.


**How to find dependents and dependencies for a spack package?**

You can find dependencies for a given package by using `spack dependencies` command. This will display all
build, link and run dependencies for the spec. In this example below we list all dependencies for the `openmpi` package.

.. code-block:: console

    $ spack dependencies openmpi
    autoconf  binutils  hcoll  ibm-java  jdk   libevent   libtool  lustre  mxm       openjdk  perl        pkgconf    singularity  sqlite  valgrind  zlib
    automake  fca       hwloc  icedtea   knem  libfabric  lsf      m4      opa-psm2  openpbs  pkg-config  rdma-core  slurm        ucx     xpmem


You can see package dependencies and other useful data using `spack info` command. If you want
to find *dependent* packages for a given package, you can use `spack dependents` command. In example
below we show all packages that depends on `caliper` package.

.. code-block:: console

    $ spack dependents caliper
    bookleaf-cpp  draco  flecsi  kripke  lvarray  timemory

**Where is my GPG key stored?**

Spack will store your GPG keys in ``$SPACK_ROOT/var/spack/gpg`` by default. This directory
is empty. For more details see :ref:`cmd-spack-gpg`.

**Permission Denied when creating GPG Keys?**

You may run into this issue where spack is unable to operate on gpg commands due to permission issue. This
is relevant if you are using a facility deployed spack which you don't have access.
The issue is spack is trying to write gpg key in the spack root and you don't have
the appropriate Access Control List (ACL).


.. code-block:: console

   yhe@cori01:/global/cscratch1/sd/yhe/spack-envs/qthreads> spack gpg list
   gpgconf: socketdir is '/global/homes/y/yhe/.gnupg'
   gpgconf: 	no /run/user dir
   gpgconf: 	using homedir as fallback
   gpg: WARNING: unsafe ownership on homedir '/global/common/software/spackecp/e4s-20.10/spack/opt/spack/gpg'
   gpg: failed to create temporary file '/global/common/software/spackecp/e4s-20.10/spack/opt/spack/gpg/.#lk0x000055555585e950.cori01.1848': Permission denied
   gpg: keyblock resource '/global/common/software/spackecp/e4s-20.10/spack/opt/spack/gpg/pubring.kbx': Permission denied
   gpg: failed to create temporary file '/global/common/software/spackecp/e4s-20.10/spack/opt/spack/gpg/.#lk0x000055555585ea10.cori01.1848': Permission denied
   gpg: Fatal: can't create lock for '/global/common/software/spackecp/e4s-20.10/spack/opt/spack/gpg/trustdb.gpg'
   ==> Error: Command exited with status 2:
   '/usr/bin/gpg2' '--list-public-keys'


You can workaround this problem by setting environment variable ``SPACK_GNUPGHOME`` to
an alternate location such as ``$HOME/.gnupg``. This is useful if you are working with multiple spack instance
and you want to use one GPG key to sign your packages.

.. code-block:: console

   # bash, sh, zsh users
   export SPACK_GNUPGHOME=$HOME/.gnupg

   # csh or tcsh
   setenv SPACK_GNUPGHOME $HOME/.gnupg

**How to enable debug messages in spack?**

You can use ``spack -d`` against any command to enable debug messages to stdout.

**How do i find path to installed spec?**

You can use ``spack find -p <spec>`` to show path to install directory.

.. code-block:: console

   $ spack find -p autoconf
   ==> 1 installed package
   -- darwin-catalina-skylake / apple-clang@11.0.3 -----------------
   autoconf@2.69  /Users/siddiq90/projects/spack/opt/spack/darwin-catalina-skylake/apple-clang-11.0.3/autoconf-2.69-3yrvwbu7vqrxylmbrx2ze2ptcjqbfp24

**How do I generate modules for installed specs?**

This may differ depending on your module system (TCL, Lmod) however you can run
the following command based on your module system

.. code-block:: console

   # TCL
   spack module tcl refresh -y --delete-tree

   # Lmod
   spack module lmod refresh -y --delete-tree

The `--delete-tree` option is useful if you want to regenerate all module trees from
scratch. For more details on spack module support click :ref:`here <modules>`.

**How do I find path to modulefile for installed spec?**

Depending on your module system you can use one of the following commands to generate
modules

.. code-block:: console

   # TCL
   spack module tcl find --full-path <spec>

   # Lmod
   spack module lmod find --full-path <spec>