.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _bootstrapping:

=============
Bootstrapping
=============

In the :ref:`Getting started <getting_started>` Section we already mentioned that
Spack can bootstrap some of its dependencies, including ``clingo``. In fact, there
is an entire command dedicated to the management of every aspect of bootstrapping:

.. command-output:: spack bootstrap --help

Spack is configured to bootstrap its dependencies lazily by default; i.e. the first time they are needed and
can't be found. You can readily check if any prerequisite for using Spack is missing by running:

.. code-block:: console

   % spack bootstrap status
   Spack v0.19.0 - python@3.8

   [FAIL] Core Functionalities
     [B] MISSING "clingo": required to concretize specs

   [FAIL] Binary packages
     [B] MISSING "gpg2": required to sign/verify buildcaches


   Spack will take care of bootstrapping any missing dependency marked as [B]. Dependencies marked as [-] are instead required to be found on the system.

   % echo $?
   1

In the case of the output shown above Spack detected that both ``clingo`` and ``gnupg``
are missing and it's giving detailed information on why they are needed and whether
they can be bootstrapped. The return code of this command summarizes the results, if any
dependencies are missing the return code is ``1``, otherwise ``0``. Running a command that
concretizes a spec, like:

.. code-block:: console

   % spack solve zlib
   ==> Bootstrapping clingo from pre-built binaries
   ==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.1/build_cache/darwin-catalina-x86_64/apple-clang-12.0.0/clingo-bootstrap-spack/darwin-catalina-x86_64-apple-clang-12.0.0-clingo-bootstrap-spack-p5on7i4hejl775ezndzfdkhvwra3hatn.spack
   ==> Installing "clingo-bootstrap@spack%apple-clang@12.0.0~docs~ipo+python build_type=Release arch=darwin-catalina-x86_64" from a buildcache
   [ ... ]

automatically triggers the bootstrapping of clingo from pre-built binaries as expected.

Users can also bootstrap all the dependencies needed by Spack in a single command, which
might be useful to setup containers or other similar environments:

.. code-block:: console

   $ spack bootstrap now
   ==> Bootstrapping clingo from pre-built binaries
   ==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.3/build_cache/linux-centos7-x86_64-gcc-10.2.1-clingo-bootstrap-spack-shqedxgvjnhiwdcdrvjhbd73jaevv7wt.spec.json
   ==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.3/build_cache/linux-centos7-x86_64/gcc-10.2.1/clingo-bootstrap-spack/linux-centos7-x86_64-gcc-10.2.1-clingo-bootstrap-spack-shqedxgvjnhiwdcdrvjhbd73jaevv7wt.spack
   ==> Installing "clingo-bootstrap@spack%gcc@10.2.1~docs~ipo+python+static_libstdcpp build_type=Release arch=linux-centos7-x86_64" from a buildcache
   ==> Bootstrapping patchelf from pre-built binaries
   ==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.3/build_cache/linux-centos7-x86_64-gcc-10.2.1-patchelf-0.15.0-htk62k7efo2z22kh6kmhaselru7bfkuc.spec.json
   ==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.3/build_cache/linux-centos7-x86_64/gcc-10.2.1/patchelf-0.15.0/linux-centos7-x86_64-gcc-10.2.1-patchelf-0.15.0-htk62k7efo2z22kh6kmhaselru7bfkuc.spack
   ==> Installing "patchelf@0.15.0%gcc@10.2.1 ldflags="-static-libstdc++ -static-libgcc"  arch=linux-centos7-x86_64" from a buildcache

-----------------------
The Bootstrapping store
-----------------------

The software installed for bootstrapping purposes is deployed in a separate store.
Its location can be checked with the following command:

.. code-block:: console

   % spack bootstrap root

It can also be changed with the same command by just specifying the newly desired path:

.. code-block:: console

   % spack bootstrap root /opt/spack/bootstrap

You can check what is installed in the bootstrapping store at any time using:

.. code-block:: console

   % spack -b find
   ==> Showing internal bootstrap store at "/Users/spack/.spack/bootstrap/store"
   ==> 11 installed packages
   -- darwin-catalina-x86_64 / apple-clang@12.0.0 ------------------
   clingo-bootstrap@spack  libassuan@2.5.5  libgpg-error@1.42  libksba@1.5.1  pinentry@1.1.1  zlib@1.2.11
   gnupg@2.3.1             libgcrypt@1.9.3  libiconv@1.16      npth@1.6       python@3.8

In case it is needed you can remove all the software in the current bootstrapping store with:

.. code-block:: console

   % spack clean -b
   ==> Removing bootstrapped software and configuration in "/Users/spack/.spack/bootstrap"

   % spack -b find
   ==> Showing internal bootstrap store at "/Users/spack/.spack/bootstrap/store"
   ==> 0 installed packages

--------------------------------------------
Enabling and disabling bootstrapping methods
--------------------------------------------

Bootstrapping is always performed by trying the methods listed by:

.. command-output:: spack bootstrap list

in the order they appear, from top to bottom. By default Spack is
configured to try first bootstrapping from pre-built binaries and to
fall-back to bootstrapping from sources if that failed.

If need be, you can disable bootstrapping altogether by running:

.. code-block:: console

   % spack bootstrap disable

in which case it's your responsibility to ensure Spack runs in an
environment where all its prerequisites are installed. You can
also configure Spack to skip certain bootstrapping methods by disabling
them specifically:

.. code-block:: console

   % spack bootstrap disable github-actions
   ==> "github-actions" is now disabled and will not be used for bootstrapping

tells Spack to skip trying to bootstrap from binaries. To add the "github-actions" method back you can:

.. code-block:: console

   % spack bootstrap enable github-actions

There is also an option to reset the bootstrapping configuration to Spack's defaults:

.. code-block:: console

   % spack bootstrap reset
   ==> Bootstrapping configuration is being reset to Spack's defaults. Current configuration will be lost.
   Do you want to continue? [Y/n]
   %

----------------------------------------
Creating a mirror for air-gapped systems
----------------------------------------

Spack's default configuration for bootstrapping relies on the user having
access to the internet, either to fetch pre-compiled binaries or source tarballs.
Sometimes though Spack is deployed on air-gapped systems where such access is denied.

To help with similar situations Spack has a command that recreates, in a local folder
of choice, a mirror containing the source tarballs and/or binary packages needed for
bootstrapping.

.. code-block:: console

   % spack bootstrap mirror --binary-packages /opt/bootstrap
   ==> Adding "clingo-bootstrap@spack+python %apple-clang target=x86_64" and dependencies to the mirror at /opt/bootstrap/local-mirror
   ==> Adding "gnupg@2.3: %apple-clang target=x86_64" and dependencies to the mirror at /opt/bootstrap/local-mirror
   ==> Adding "patchelf@0.13.1:0.13.99 %apple-clang target=x86_64" and dependencies to the mirror at /opt/bootstrap/local-mirror
   ==> Adding binary packages from "https://github.com/alalazo/spack-bootstrap-mirrors/releases/download/v0.1-rc.2/bootstrap-buildcache.tar.gz" to the mirror at /opt/bootstrap/local-mirror

   To register the mirror on the platform where it's supposed to be used run the following command(s):
     % spack bootstrap add --trust local-sources /opt/bootstrap/metadata/sources
     % spack bootstrap add --trust local-binaries /opt/bootstrap/metadata/binaries


This command needs to be run on a machine with internet access and the resulting folder
has to be moved over to the air-gapped system. Once the local sources are added using the
commands suggested at the prompt, they can be used to bootstrap Spack.
