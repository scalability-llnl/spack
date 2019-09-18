.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _basics-tutorial:

=========================================
Basic Installation Tutorial
=========================================

This tutorial will guide you through the process of installing
software using Spack. We will first cover the `spack install` command,
focusing on the power of the spec syntax and the flexibility it gives
to users. We will also cover the `spack find` command for viewing
installed packages and the `spack uninstall` command. Finally, we will
touch on how Spack manages compilers, especially as it relates to
using Spack-built compilers within Spack. We will include full output
from all of the commands demonstrated, although we will frequently
call attention to only small portions of that output (or merely to the
fact that it succeeded). The provided output is all from an AWS
instance running Ubuntu 16.04

.. _basics-tutorial-install:

----------------
Installing Spack
----------------

Spack works out of the box. Simply clone spack and get going. We will
clone Spack and immediately checkout the most recent release, v0.12.

.. code-block:: console

  $ git clone https://github.com/spack/spack
  git clone https://github.com/spack/spack
  Cloning into 'spack'...
  remote: Enumerating objects: 68, done.
  remote: Counting objects: 100% (68/68), done.
  remote: Compressing objects: 100% (56/56), done.
  remote: Total 135389 (delta 40), reused 16 (delta 9), pack-reused 135321
  Receiving objects: 100% (135389/135389), 47.31 MiB | 1.01 MiB/s, done.
  Resolving deltas: 100% (64414/64414), done.
  Checking connectivity... done.
  $ cd spack
  $ git checkout releases/v0.12
  Branch releases/v0.12 set up to track remote branch releases/v0.12 from origin.
  Switched to a new branch 'releases/v0.12'

Next add Spack to your path. Spack has some nice command line
integration tools, so instead of simply appending to your ``PATH``
variable, source the spack setup script.  Then add Spack to your path.

.. code-block:: console

  $ . share/spack/setup-env.sh

You're good to go!

-----------------
What is in Spack?
-----------------

The ``spack list`` command shows available packages.

.. code-block:: console

  $ spack list
  ==> 2907 packages.
  abinit                           libgpuarray                            py-espresso                     r-mlrmbo
  abyss                            libgridxc                              py-espressopp                   r-mmwrweek
  accfft                           libgtextutils                          py-et-xmlfile                   r-mnormt
  ...

The ``spack list`` command can also take a query string. Spack
automatically adds wildcards to both ends of the string. For example,
we can view all available python packages.

.. code-block:: console

  $ spack list py-
  ==> 479 packages.
  lumpy-sv                               py-funcsigs          py-numpydoc         py-utililib
  perl-file-copy-recursive               py-functools32       py-olefile          py-pywavelets
  py-3to2                                py-future            py-ont-fast5-api    py-pyyaml
  ...

-------------------
Installing Packages
-------------------

Installing a package with Spack is very simple. To install a piece of
software, simply type ``spack install <package_name>``.

.. code-block:: console

  $ spack install zlib
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Warning: No Spack mirrors are currently configured
  ==> No binary for zlib found: installing from source
  ==> Fetching http://zlib.net/fossils/zlib-1.2.11.tar.gz
  ######################################################################## 100.0%
  ==> Staging archive: /home/spack1/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb/zlib-1.2.11.tar.gz
  ==> Created stage in /home/spack1/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> No patches needed for zlib
  ==> Building zlib [Package]
  ==> Executing phase: 'install'
  ==> Successfully installed zlib
    Fetch: 3.27s.  Build: 2.18s.  Total: 5.44s.
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb

Spack can install software either from source or from a binary
cache. Packages in the binary cache are signed with GPG for
security. For the tutorial we have prepared a binary cache so you
don't have to wait on slow compilation from source. To be able to
install from the binary cache, we will need to configure Spack with
the location of the binary cache and trust the GPG key that the binary
cache was signed with.

.. code-block:: console

  $ spack mirror add tutorial /mirror
  $ spack gpg trust /mirror/public.key
  gpg: keybox '/home/spack1/spack/opt/spack/gpg/pubring.kbx' created
  gpg: /home/spack1/spack/opt/spack/gpg/trustdb.gpg: trustdb created
  gpg: key 3B7C69B2: public key "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" imported
  gpg: Total number processed: 1
  gpg:               imported: 1

You'll learn more about configuring Spack later in the tutorial, but
for now you will be able to install the rest of the packages in the
tutorial from a binary cache using the same ``spack install``
command. By default this will install the binary cached version if it
exists and fall back on installing from source.

Spack's spec syntax is the interface by which we can request specific
configurations of the package. The ``%`` sigil is used to specify
compilers.

.. code-block:: console

  $ spack install zlib %clang
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64-gcc-7.2.0-texinfo-6.5-cuqnfgfhhmudqp5f7upmld6ax7pratzw.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64-gcc-4.7-zlib-1.2.11-bq2wtdxakpjytk2tjr7qu23i4py2fi2r.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-dyninst-9.3.2-bu6s2jzievsjkwtcnrtimc5b625j5omf.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64-gcc-7.2.0-openmpi-3.1.3-do5xfer2whhk7gc26atgs3ozr3ljbvs4.spec.yaml
  ...
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.11/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-zlib-1.2.11-4pt75q7qq6lygf3hgnona4lyc2uwedul.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:08:01 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.11-4pt75q7qq6lygf3hgnona4lyc2uwedul

Note that this installation is located separately from the previous
one. We will discuss this in more detail later, but this is part of what
allows Spack to support arbitrarily versioned software.

You can check for particular versions before requesting them. We will
use the ``spack versions`` command to see the available versions, and then
install a different version of ``zlib``.

.. code-block:: console

  $ spack versions zlib
  ==> Safe versions (already checksummed):
    1.2.11  1.2.8  1.2.3
  ==> Remote versions (not yet checksummed):
    1.2.10   1.2.7    1.2.5.1  1.2.4.2  1.2.3.7
    ...

The ``@`` sigil is used to specify versions, both of packages and of
compilers.

.. code-block:: console

  $ spack install zlib@1.2.8
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-zlib-1.2.8-bkyl5bhuep6fmhuxzkmhqy25qefjcvzc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:18:30 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-bkyl5bhuep6fmhuxzkmhqy25qefjcvzc

  $ spack install zlib %gcc@4.7
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-4.7/zlib-1.2.11/linux-ubuntu16.04-x86_64-gcc-4.7-zlib-1.2.11-bq2wtdxakpjytk2tjr7qu23i4py2fi2r.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 04:55:30 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-4.7/zlib-1.2.11-bq2wtdxakpjytk2tjr7qu23i4py2fi2r

The spec syntax also includes compiler flags. Spack accepts
``cppflags``, ``cflags``, ``cxxflags``, ``fflags``, ``ldflags``, and
``ldlibs`` parameters.  The values of these fields must be quoted on
the command line if they include spaces. These values are injected
into the compile line automatically by the Spack compiler wrappers.

.. code-block:: console

  $ spack install zlib @1.2.8 cppflags=-O3
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:31:54 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu

The ``spack find`` command is used to query installed packages. Note that
some packages appear identical with the default output. The ``-l`` flag
shows the hash of each package, and the ``-f`` flag shows any non-empty
compiler flags of those packages.

.. code-block:: console

  $ spack find
  ==> 5 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  zlib@1.2.8  zlib@1.2.8  zlib@1.2.11


  $ spack find -lf
  ==> 5 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  4pt75q7 zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx zlib@1.2.11%gcc


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  bkyl5bh zlib@1.2.8%gcc

  64mns5m zlib@1.2.8%gcc cppflags="-O3"

  5nus6kn zlib@1.2.11%gcc

Spack generates a hash for each spec. This hash is a function of the full
provenance of the package, so any change to the spec affects the
hash. Spack uses this value to compare specs and to generate unique
installation directories for every combinatorial version. As we move into
more complicated packages with software dependencies, we can see that
Spack reuses existing packages to satisfy a dependency only when the
existing package's hash matches the desired spec.

.. code-block:: console

  $ spack install tcl
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing tcl
  ==> Searching for binary cache of tcl
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing tcl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-tcl-8.6.8-qhwyccywhx2i6s7ob2gvjrjtj3rnfuqt.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:07:15 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed tcl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8-qhwyccywhx2i6s7ob2gvjrjtj3rnfuqt

Dependencies can be explicitly requested using the ``^`` sigil. Note that
the spec syntax is recursive. Anything we could specify about the
top-level package, we can also specify about a dependency using ``^``.

.. code-block:: console

  $ spack install tcl %clang ^zlib @1.2.8
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.8/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-zlib-1.2.8-i426yu3o6lyau5fv5ljwsajfkqxj5rl5.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:09:01 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.8-i426yu3o6lyau5fv5ljwsajfkqxj5rl5
  ==> Installing tcl
  ==> Searching for binary cache of tcl
  ==> Installing tcl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/tcl-8.6.8/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-tcl-8.6.8-6wc66etr7y6hgibp2derrdkf763exwvc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:10:21 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed tcl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/tcl-8.6.8-6wc66etr7y6hgibp2derrdkf763exwvc

Packages can also be referred to from the command line by their package
hash. Using the ``spack find -lf`` command earlier we saw that the hash
of our optimized installation of zlib (``cppflags="-O3"``) began with
``64mns5m``. We can now explicitly build with that package without typing
the entire spec, by using the ``/`` sigil to refer to it by hash. As with
other tools like git, you do not need to specify an *entire* hash on the
command line.  You can specify just enough digits to identify a hash
uniquely.  If a hash prefix is ambiguous (i.e., two or more installed
packages share the prefix) then spack will report an error.

.. code-block:: console

  $ spack install tcl ^/64mn
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu
  ==> Installing tcl
  ==> Searching for binary cache of tcl
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing tcl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-tcl-8.6.8-am4pbatrtga3etyusg2akmsvrswwxno2.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:11:53 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed tcl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8-am4pbatrtga3etyusg2akmsvrswwxno2

The ``spack find`` command can also take a ``-d`` flag, which can show
dependency information. Note that each package has a top-level entry,
even if it also appears as a dependency.

.. code-block:: console

  $ spack find -ldf
  ==> 9 installed packages
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  6wc66et    tcl@8.6.8%clang
  i426yu3        ^zlib@1.2.8%clang

  i426yu3    zlib@1.2.8%clang

  4pt75q7    zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx    zlib@1.2.11%gcc


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  am4pbat    tcl@8.6.8%gcc
  64mns5m        ^zlib@1.2.8%gcc cppflags="-O3"

  qhwyccy    tcl@8.6.8%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  bkyl5bh    zlib@1.2.8%gcc

  64mns5m    zlib@1.2.8%gcc cppflags="-O3"

  5nus6kn    zlib@1.2.11%gcc


Let's move on to slightly more complicated packages. ``HDF5`` is a
good example of a more complicated package, with an MPI dependency. If
we install it "out of the box," it will build with ``openmpi``.

.. code-block:: console

  $ spack install hdf5
  ==> Installing libsigsegv
  ==> Searching for binary cache of libsigsegv
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing libsigsegv from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11/linux-ubuntu16.04-x86_64-gcc-5.4.0-libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:08:01 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libsigsegv from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> Installing m4
  ==> Searching for binary cache of m4
  ==> Installing m4 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18/linux-ubuntu16.04-x86_64-gcc-5.4.0-m4-1.4.18-suf5jtcfehivwfesrc5hjy72r4nukyel.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:24:11 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed m4 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-suf5jtcfehivwfesrc5hjy72r4nukyel
  ==> Installing libtool
  ==> Searching for binary cache of libtool
  ==> Installing libtool from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6/linux-ubuntu16.04-x86_64-gcc-5.4.0-libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:12:47 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libtool from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> Installing pkgconf
  ==> Searching for binary cache of pkgconf
  ==> Installing pkgconf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkgconf-1.4.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-pkgconf-1.4.2-fovrh7alpft646n6mhis5mml6k6e5f4v.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:00:47 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed pkgconf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkgconf-1.4.2-fovrh7alpft646n6mhis5mml6k6e5f4v
  ==> Installing util-macros
  ==> Searching for binary cache of util-macros
  ==> Installing util-macros from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/util-macros-1.19.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:31:54 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed util-macros from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr
  ==> Installing libpciaccess
  ==> Searching for binary cache of libpciaccess
  ==> Installing libpciaccess from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libpciaccess-0.13.5/linux-ubuntu16.04-x86_64-gcc-5.4.0-libpciaccess-0.13.5-5urc6tcjae26fbbd2wyfohoszhgxtbmc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:09:34 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libpciaccess from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libpciaccess-0.13.5-5urc6tcjae26fbbd2wyfohoszhgxtbmc
  ==> Installing xz
  ==> Searching for binary cache of xz
  ==> Installing xz from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/xz-5.2.4/linux-ubuntu16.04-x86_64-gcc-5.4.0-xz-5.2.4-teneqii2xv5u6zl5r6qi3pwurc6pmypz.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:05:03 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed xz from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/xz-5.2.4-teneqii2xv5u6zl5r6qi3pwurc6pmypz
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing libxml2
  ==> Searching for binary cache of libxml2
  ==> Installing libxml2 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libxml2-2.9.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-libxml2-2.9.8-wpexsphdmfayxqxd4up5vgwuqgu5woo7.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 04:56:04 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libxml2 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libxml2-2.9.8-wpexsphdmfayxqxd4up5vgwuqgu5woo7
  ==> Installing ncurses
  ==> Searching for binary cache of ncurses
  ==> Installing ncurses from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-ncurses-6.1-3o765ourmesfrji6yeclb4wb5w54aqbh.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:04:49 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed ncurses from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.1-3o765ourmesfrji6yeclb4wb5w54aqbh
  ==> Installing readline
  ==> Searching for binary cache of readline
  ==> Installing readline from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-readline-7.0-nxhwrg7xwc6nbsm2v4ezwe63l6nfidbi.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:04:56 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed readline from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0-nxhwrg7xwc6nbsm2v4ezwe63l6nfidbi
  ==> Installing gdbm
  ==> Searching for binary cache of gdbm
  ==> Installing gdbm from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.14.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-gdbm-1.14.1-q4fpyuo7ouhkeq6d3oabtrppctpvxmes.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:18:34 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed gdbm from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.14.1-q4fpyuo7ouhkeq6d3oabtrppctpvxmes
  ==> Installing perl
  ==> Searching for binary cache of perl
  ==> Installing perl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.26.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-perl-5.26.2-ic2kyoadgp3dxfejcbllyplj2wf524fo.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:12:45 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed perl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.26.2-ic2kyoadgp3dxfejcbllyplj2wf524fo
  ==> Installing autoconf
  ==> Searching for binary cache of autoconf
  ==> Installing autoconf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69/linux-ubuntu16.04-x86_64-gcc-5.4.0-autoconf-2.69-3sx2gxeibc4oasqd4o5h6lnwpcpsgd2q.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:24:03 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed autoconf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69-3sx2gxeibc4oasqd4o5h6lnwpcpsgd2q
  ==> Installing automake
  ==> Searching for binary cache of automake
  ==> Installing automake from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.16.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-automake-1.16.1-rymw7imfehycqxzj4nuy2oiw3abegooy.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:12:03 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed automake from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.16.1-rymw7imfehycqxzj4nuy2oiw3abegooy
  ==> Installing numactl
  ==> Searching for binary cache of numactl
  ==> Installing numactl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/numactl-2.0.11/linux-ubuntu16.04-x86_64-gcc-5.4.0-numactl-2.0.11-ft463odrombnxlc3qew4omckhlq7tqgc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:30:34 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed numactl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/numactl-2.0.11-ft463odrombnxlc3qew4omckhlq7tqgc
  ==> Installing hwloc
  ==> Searching for binary cache of hwloc
  ==> Installing hwloc from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hwloc-1.11.9/linux-ubuntu16.04-x86_64-gcc-5.4.0-hwloc-1.11.9-43tkw5mt6huhv37vqnybqgxtkodbsava.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:08:00 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hwloc from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hwloc-1.11.9-43tkw5mt6huhv37vqnybqgxtkodbsava
  ==> Installing openmpi
  ==> Searching for binary cache of openmpi
  ==> Installing openmpi from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.1.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-openmpi-3.1.3-3njc4q5pqdpptq6jvqjrezkffwokv2sx.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:01:54 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed openmpi from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.1.3-3njc4q5pqdpptq6jvqjrezkffwokv2sx
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.4-ozyvmhzdew66byarohm4p36ep7wtcuiw.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:23:04 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hdf5 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-ozyvmhzdew66byarohm4p36ep7wtcuiw

Spack packages can also have build options, called variants. Boolean
variants can be specified using the ``+`` and ``~`` or ``-``
sigils. There are two sigils for ``False`` to avoid conflicts with
shell parsing in different situations. Variants (boolean or otherwise)
can also be specified using the same syntax as compiler flags.  Here
we can install HDF5 without MPI support.

.. code-block:: console

   $ spack install hdf5~mpi
   ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
   ==> Installing hdf5
   ==> Searching for binary cache of hdf5
   ==> Finding buildcaches in /mirror/build_cache
   ==> Installing hdf5 from binary cache
   ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.4-5vcv5r67vpjzenq4apyebshclelnzuja.spack
   ######################################################################## 100.0%
   gpg: Signature made Sat Nov 10 05:23:24 2018 UTC using RSA key ID 3B7C69B2
   gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
   ==> Successfully installed hdf5 from binary cache
   [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-5vcv5r67vpjzenq4apyebshclelnzuja

We might also want to install HDF5 with a different MPI
implementation. While MPI is not a package itself, packages can depend on
abstract interfaces like MPI. Spack handles these through "virtual
dependencies." A package, such as HDF5, can depend on the MPI
interface. Other packages (``openmpi``, ``mpich``, ``mvapich``, etc.)
provide the MPI interface.  Any of these providers can be requested for
an MPI dependency. For example, we can build HDF5 with MPI support
provided by mpich by specifying a dependency on ``mpich``. Spack also
supports versioning of virtual dependencies. A package can depend on the
MPI interface at version 3, and provider packages specify what version of
the interface *they* provide. The partial spec ``^mpi@3`` can be safisfied
by any of several providers.

.. code-block:: console

  $ spack install hdf5+hl+mpi ^mpich
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-suf5jtcfehivwfesrc5hjy72r4nukyel
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkgconf-1.4.2-fovrh7alpft646n6mhis5mml6k6e5f4v
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.1-3o765ourmesfrji6yeclb4wb5w54aqbh
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0-nxhwrg7xwc6nbsm2v4ezwe63l6nfidbi
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.14.1-q4fpyuo7ouhkeq6d3oabtrppctpvxmes
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.26.2-ic2kyoadgp3dxfejcbllyplj2wf524fo
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69-3sx2gxeibc4oasqd4o5h6lnwpcpsgd2q
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.16.1-rymw7imfehycqxzj4nuy2oiw3abegooy
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> Installing texinfo
  ==> Searching for binary cache of texinfo
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing texinfo from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/texinfo-6.5/linux-ubuntu16.04-x86_64-gcc-5.4.0-texinfo-6.5-zs7a2pcwhq6ho2cj2x26uxfktwkpyucn.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:18:29 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed texinfo from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/texinfo-6.5-zs7a2pcwhq6ho2cj2x26uxfktwkpyucn
  ==> Installing findutils
  ==> Searching for binary cache of findutils
  ==> Installing findutils from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/findutils-4.6.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-findutils-4.6.0-d4iajxsopzrlcjtasahxqeyjkjv5jx4v.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:07:17 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed findutils from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/findutils-4.6.0-d4iajxsopzrlcjtasahxqeyjkjv5jx4v
  ==> Installing mpich
  ==> Searching for binary cache of mpich
  ==> Installing mpich from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpich-3.2.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-mpich-3.2.1-p3f7p2r5ntrynqibosglxvhwyztiwqs5.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:23:57 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mpich from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpich-3.2.1-p3f7p2r5ntrynqibosglxvhwyztiwqs5
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.4-xxd7syhgej6onpyfyewxqcqe7ltkt7ob.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:07:32 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hdf5 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-xxd7syhgej6onpyfyewxqcqe7ltkt7ob

We'll do a quick check in on what we have installed so far.

.. code-block:: console

  $ spack find -ldf
  ==> 32 installed packages
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  6wc66et    tcl@8.6.8%clang
  i426yu3        ^zlib@1.2.8%clang

  i426yu3    zlib@1.2.8%clang

  4pt75q7    zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx    zlib@1.2.11%gcc


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  3sx2gxe    autoconf@2.69%gcc
  suf5jtc        ^m4@1.4.18%gcc
  fypapcp            ^libsigsegv@2.11%gcc
  ic2kyoa        ^perl@5.26.2%gcc
  q4fpyuo            ^gdbm@1.14.1%gcc
  nxhwrg7                ^readline@7.0%gcc
  3o765ou                    ^ncurses@6.1%gcc

  rymw7im    automake@1.16.1%gcc
  ic2kyoa        ^perl@5.26.2%gcc
  q4fpyuo            ^gdbm@1.14.1%gcc
  nxhwrg7                ^readline@7.0%gcc
  3o765ou                    ^ncurses@6.1%gcc

  d4iajxs    findutils@4.6.0%gcc

  q4fpyuo    gdbm@1.14.1%gcc
  nxhwrg7        ^readline@7.0%gcc
  3o765ou            ^ncurses@6.1%gcc

  5vcv5r6    hdf5@1.10.4%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  ozyvmhz    hdf5@1.10.4%gcc
  3njc4q5        ^openmpi@3.1.3%gcc
  43tkw5m            ^hwloc@1.11.9%gcc
  5urc6tc                ^libpciaccess@0.13.5%gcc
  wpexsph                ^libxml2@2.9.8%gcc
  teneqii                    ^xz@5.2.4%gcc
  5nus6kn                    ^zlib@1.2.11%gcc
  ft463od                ^numactl@2.0.11%gcc

  xxd7syh    hdf5@1.10.4%gcc
  p3f7p2r        ^mpich@3.2.1%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  43tkw5m    hwloc@1.11.9%gcc
  5urc6tc        ^libpciaccess@0.13.5%gcc
  wpexsph        ^libxml2@2.9.8%gcc
  teneqii            ^xz@5.2.4%gcc
  5nus6kn            ^zlib@1.2.11%gcc
  ft463od        ^numactl@2.0.11%gcc

  5urc6tc    libpciaccess@0.13.5%gcc

  fypapcp    libsigsegv@2.11%gcc

  o2pfwjf    libtool@2.4.6%gcc

  wpexsph    libxml2@2.9.8%gcc
  teneqii        ^xz@5.2.4%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  suf5jtc    m4@1.4.18%gcc
  fypapcp        ^libsigsegv@2.11%gcc

  p3f7p2r    mpich@3.2.1%gcc

  3o765ou    ncurses@6.1%gcc

  ft463od    numactl@2.0.11%gcc

  3njc4q5    openmpi@3.1.3%gcc
  43tkw5m        ^hwloc@1.11.9%gcc
  5urc6tc            ^libpciaccess@0.13.5%gcc
  wpexsph            ^libxml2@2.9.8%gcc
  teneqii                ^xz@5.2.4%gcc
  5nus6kn                ^zlib@1.2.11%gcc
  ft463od            ^numactl@2.0.11%gcc

  ic2kyoa    perl@5.26.2%gcc
  q4fpyuo        ^gdbm@1.14.1%gcc
  nxhwrg7            ^readline@7.0%gcc
  3o765ou                ^ncurses@6.1%gcc

  fovrh7a    pkgconf@1.4.2%gcc

  nxhwrg7    readline@7.0%gcc
  3o765ou        ^ncurses@6.1%gcc

  am4pbat    tcl@8.6.8%gcc
  64mns5m        ^zlib@1.2.8%gcc cppflags="-O3"

  qhwyccy    tcl@8.6.8%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  zs7a2pc    texinfo@6.5%gcc
  ic2kyoa        ^perl@5.26.2%gcc
  q4fpyuo            ^gdbm@1.14.1%gcc
  nxhwrg7                ^readline@7.0%gcc
  3o765ou                    ^ncurses@6.1%gcc

  milz7fm    util-macros@1.19.1%gcc

  teneqii    xz@5.2.4%gcc

  bkyl5bh    zlib@1.2.8%gcc

  64mns5m    zlib@1.2.8%gcc cppflags="-O3"

  5nus6kn    zlib@1.2.11%gcc


Spack models the dependencies of packages as a directed acyclic graph
(DAG). The ``spack find -d`` command shows the tree representation of
that graph.  We can also use the ``spack graph`` command to view the entire
DAG as a graph.

.. code-block:: console

  $ spack graph hdf5+hl+mpi ^mpich
  o  hdf5
  |\
  o |  zlib
   /
  o  mpich
  o  findutils
  |\
  | |\
  | | |\
  | | | |\
  o | | | |  texinfo
  | | | o |  automake
  | |_|/| |
  |/| | | |
  | | | |/
  | | | o  autoconf
  | |_|/|
  |/| |/
  | |/|
  o | |  perl
  o | |  gdbm
  o | |  readline
  o | |  ncurses
  o | |  pkgconf
   / /
  | o  libtool
  |/
  o  m4
  o  libsigsegv

You may also have noticed that there are some packages shown in the
``spack find -d`` output that we didn't install explicitly. These are
dependencies that were installed implicitly. A few packages installed
implicitly are not shown as dependencies in the ``spack find -d``
output. These are build dependencies. For example, ``libpciaccess`` is a
dependency of openmpi and requires ``m4`` to build. Spack will build ``m4`` as
part of the installation of ``openmpi``, but it does not become a part of
the DAG because it is not linked in at run time. Spack handles build
dependencies differently because of their different (less strict)
consistency requirements. It is entirely possible to have two packages
using different versions of a dependency to build, which obviously cannot
be done with linked dependencies.

``HDF5`` is more complicated than our basic example of zlib and
openssl, but it's still within the realm of software that an experienced
HPC user could reasonably expect to install given a bit of time. Now
let's look at an even more complicated package.

.. code-block:: console

  $ spack install trilinos
  ==> Installing diffutils
  ==> Searching for binary cache of diffutils
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing diffutils from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/diffutils-3.6/linux-ubuntu16.04-x86_64-gcc-5.4.0-diffutils-3.6-2rhuivgjrna2nrxhntyde6md2khcvs34.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:30:17 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed diffutils from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/diffutils-3.6-2rhuivgjrna2nrxhntyde6md2khcvs34
  ==> Installing bzip2
  ==> Searching for binary cache of bzip2
  ==> Installing bzip2 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/bzip2-1.0.6/linux-ubuntu16.04-x86_64-gcc-5.4.0-bzip2-1.0.6-ufczdvsqt6edesm36xiucyry7myhj7e7.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:34:37 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed bzip2 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/bzip2-1.0.6-ufczdvsqt6edesm36xiucyry7myhj7e7
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing boost
  ==> Searching for binary cache of boost
  ==> Installing boost from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/boost-1.68.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-boost-1.68.0-zbgfxapchxa4awxdwpleubfuznblxzvt.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 04:58:55 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed boost from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/boost-1.68.0-zbgfxapchxa4awxdwpleubfuznblxzvt
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkgconf-1.4.2-fovrh7alpft646n6mhis5mml6k6e5f4v
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.1-3o765ourmesfrji6yeclb4wb5w54aqbh
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0-nxhwrg7xwc6nbsm2v4ezwe63l6nfidbi
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.14.1-q4fpyuo7ouhkeq6d3oabtrppctpvxmes
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.26.2-ic2kyoadgp3dxfejcbllyplj2wf524fo
  ==> Installing openssl
  ==> Searching for binary cache of openssl
  ==> Installing openssl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2o/linux-ubuntu16.04-x86_64-gcc-5.4.0-openssl-1.0.2o-b4y3w3bsyvjla6eesv4vt6aplpfrpsha.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:24:10 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed openssl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2o-b4y3w3bsyvjla6eesv4vt6aplpfrpsha
  ==> Installing cmake
  ==> Searching for binary cache of cmake
  ==> Installing cmake from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/cmake-3.12.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-cmake-3.12.3-otafqzhh4xnlq2mpakch7dr3tjfsrjnx.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:33:15 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed cmake from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/cmake-3.12.3-otafqzhh4xnlq2mpakch7dr3tjfsrjnx
  ==> Installing glm
  ==> Searching for binary cache of glm
  ==> Installing glm from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/glm-0.9.7.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-glm-0.9.7.1-jnw622jwcbsymzj2fsx22omjl7tmvaws.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:30:33 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed glm from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/glm-0.9.7.1-jnw622jwcbsymzj2fsx22omjl7tmvaws
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-suf5jtcfehivwfesrc5hjy72r4nukyel
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> util-macros is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr
  ==> libpciaccess is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libpciaccess-0.13.5-5urc6tcjae26fbbd2wyfohoszhgxtbmc
  ==> xz is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/xz-5.2.4-teneqii2xv5u6zl5r6qi3pwurc6pmypz
  ==> libxml2 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libxml2-2.9.8-wpexsphdmfayxqxd4up5vgwuqgu5woo7
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69-3sx2gxeibc4oasqd4o5h6lnwpcpsgd2q
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.16.1-rymw7imfehycqxzj4nuy2oiw3abegooy
  ==> numactl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/numactl-2.0.11-ft463odrombnxlc3qew4omckhlq7tqgc
  ==> hwloc is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hwloc-1.11.9-43tkw5mt6huhv37vqnybqgxtkodbsava
  ==> openmpi is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.1.3-3njc4q5pqdpptq6jvqjrezkffwokv2sx
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.4-oqwnui7wtovuf2id4vjwcxfmxlzjus6y.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:09:10 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hdf5 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-oqwnui7wtovuf2id4vjwcxfmxlzjus6y
  ==> Installing openblas
  ==> Searching for binary cache of openblas
  ==> Installing openblas from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/openblas-0.3.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-openblas-0.3.3-cyeg2yiitpuqglhvbox5gtbgsim2v5vn.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:32:04 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed openblas from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openblas-0.3.3-cyeg2yiitpuqglhvbox5gtbgsim2v5vn
  ==> Installing hypre
  ==> Searching for binary cache of hypre
  ==> Installing hypre from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.15.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hypre-2.15.1-fshksdpecwiq7r6vawfswpboedhbisju.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:07:34 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hypre from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.15.1-fshksdpecwiq7r6vawfswpboedhbisju
  ==> Installing matio
  ==> Searching for binary cache of matio
  ==> Installing matio from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9/linux-ubuntu16.04-x86_64-gcc-5.4.0-matio-1.5.9-lmzdgssvobdljw52mtahelu2ju7osh6h.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:05:13 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed matio from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9-lmzdgssvobdljw52mtahelu2ju7osh6h
  ==> Installing metis
  ==> Searching for binary cache of metis
  ==> Installing metis from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/metis-5.1.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-metis-5.1.0-3wnvp4ji3wwu4v4vymszrhx6naehs6jc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:31:42 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed metis from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/metis-5.1.0-3wnvp4ji3wwu4v4vymszrhx6naehs6jc
  ==> Installing netlib-scalapack
  ==> Searching for binary cache of netlib-scalapack
  ==> Installing netlib-scalapack from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-netlib-scalapack-2.0.2-wotpfwfctgfkzzn2uescucxvvbg3tm6b.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:07:22 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netlib-scalapack from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2-wotpfwfctgfkzzn2uescucxvvbg3tm6b
  ==> Installing mumps
  ==> Searching for binary cache of mumps
  ==> Installing mumps from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-mumps-5.1.1-acsg2dzroox2swssgc5cwgkvdy6jcm5q.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:18:32 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mumps from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1-acsg2dzroox2swssgc5cwgkvdy6jcm5q
  ==> Installing netcdf
  ==> Searching for binary cache of netcdf
  ==> Installing netcdf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.6.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-netcdf-4.6.1-mhm4izpogf4mrjidyskb6ewtzxdi7t6g.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:11:57 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netcdf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.6.1-mhm4izpogf4mrjidyskb6ewtzxdi7t6g
  ==> Installing parmetis
  ==> Searching for binary cache of parmetis
  ==> Installing parmetis from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-parmetis-4.0.3-uv6h3sqx6quqg22hxesi2mw2un3kw6b7.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:12:04 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed parmetis from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3-uv6h3sqx6quqg22hxesi2mw2un3kw6b7
  ==> Installing suite-sparse
  ==> Searching for binary cache of suite-sparse
  ==> Installing suite-sparse from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/suite-sparse-5.3.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-suite-sparse-5.3.0-zaau4kifha2enpdcn3mjlrqym7hm7yon.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:22:54 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed suite-sparse from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/suite-sparse-5.3.0-zaau4kifha2enpdcn3mjlrqym7hm7yon
  ==> Installing trilinos
  ==> Searching for binary cache of trilinos
  ==> Installing trilinos from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-trilinos-12.12.1-rlsruavxqvwk2tgxzxboclbo6ykjf54r.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:18:10 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed trilinos from binary cache

Now we're starting to see the power of Spack. Trilinos in its default
configuration has 23 top level dependecies, many of which have
dependencies of their own. Installing more complex packages can take
days or weeks even for an experienced user. Although we've done a
binary installation for the tutorial, a source installation of
trilinos using Spack takes about 3 hours (depending on the system),
but only 20 seconds of programmer time.

Spack manages constistency of the entire DAG. Every MPI dependency will
be satisfied by the same configuration of MPI, etc. If we install
``trilinos`` again specifying a dependency on our previous HDF5 built
with ``mpich``:

.. code-block:: console

  $ spack install trilinos +hdf5 ^hdf5+hl+mpi ^mpich
  ==> diffutils is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/diffutils-3.6-2rhuivgjrna2nrxhntyde6md2khcvs34
  ==> bzip2 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/bzip2-1.0.6-ufczdvsqt6edesm36xiucyry7myhj7e7
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> boost is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/boost-1.68.0-zbgfxapchxa4awxdwpleubfuznblxzvt
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkgconf-1.4.2-fovrh7alpft646n6mhis5mml6k6e5f4v
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.1-3o765ourmesfrji6yeclb4wb5w54aqbh
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0-nxhwrg7xwc6nbsm2v4ezwe63l6nfidbi
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.14.1-q4fpyuo7ouhkeq6d3oabtrppctpvxmes
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.26.2-ic2kyoadgp3dxfejcbllyplj2wf524fo
  ==> openssl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2o-b4y3w3bsyvjla6eesv4vt6aplpfrpsha
  ==> cmake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/cmake-3.12.3-otafqzhh4xnlq2mpakch7dr3tjfsrjnx
  ==> glm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/glm-0.9.7.1-jnw622jwcbsymzj2fsx22omjl7tmvaws
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-suf5jtcfehivwfesrc5hjy72r4nukyel
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69-3sx2gxeibc4oasqd4o5h6lnwpcpsgd2q
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.16.1-rymw7imfehycqxzj4nuy2oiw3abegooy
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> texinfo is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/texinfo-6.5-zs7a2pcwhq6ho2cj2x26uxfktwkpyucn
  ==> findutils is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/findutils-4.6.0-d4iajxsopzrlcjtasahxqeyjkjv5jx4v
  ==> mpich is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpich-3.2.1-p3f7p2r5ntrynqibosglxvhwyztiwqs5
  ==> hdf5 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-xxd7syhgej6onpyfyewxqcqe7ltkt7ob
  ==> openblas is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openblas-0.3.3-cyeg2yiitpuqglhvbox5gtbgsim2v5vn
  ==> Installing hypre
  ==> Searching for binary cache of hypre
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing hypre from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.15.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hypre-2.15.1-obewuozolon7tkdg4cfxc6ae2tzkronb.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:34:36 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hypre from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.15.1-obewuozolon7tkdg4cfxc6ae2tzkronb
  ==> Installing matio
  ==> Searching for binary cache of matio
  ==> Installing matio from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9/linux-ubuntu16.04-x86_64-gcc-5.4.0-matio-1.5.9-gvyqldhifflmvcrtui3b6s64jcczsxxh.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:25:11 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed matio from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9-gvyqldhifflmvcrtui3b6s64jcczsxxh
  ==> metis is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/metis-5.1.0-3wnvp4ji3wwu4v4vymszrhx6naehs6jc
  ==> Installing netlib-scalapack
  ==> Searching for binary cache of netlib-scalapack
  ==> Installing netlib-scalapack from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-netlib-scalapack-2.0.2-p7iln2pcosw2ipyqoyr7ie6lpva2oj7r.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:32:20 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netlib-scalapack from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2-p7iln2pcosw2ipyqoyr7ie6lpva2oj7r
  ==> Installing mumps
  ==> Searching for binary cache of mumps
  ==> Installing mumps from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-mumps-5.1.1-cumcj5a75cagsznpjrgretxdg6okxaur.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:33:18 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mumps from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1-cumcj5a75cagsznpjrgretxdg6okxaur
  ==> Installing netcdf
  ==> Searching for binary cache of netcdf
  ==> Installing netcdf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.6.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-netcdf-4.6.1-wmmx5sgwfds34v7bkkhiduar5yecrnnd.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:24:01 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netcdf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.6.1-wmmx5sgwfds34v7bkkhiduar5yecrnnd
  ==> Installing parmetis
  ==> Searching for binary cache of parmetis
  ==> Installing parmetis from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-parmetis-4.0.3-jehtatan4y2lcobj6waoqv66jj4libtz.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:07:41 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed parmetis from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3-jehtatan4y2lcobj6waoqv66jj4libtz
  ==> suite-sparse is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/suite-sparse-5.3.0-zaau4kifha2enpdcn3mjlrqym7hm7yon
  ==> Installing trilinos
  ==> Searching for binary cache of trilinos
  ==> Installing trilinos from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-trilinos-12.12.1-kqc52moweigxqxzwzfqajc6ocxwdwn4w.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:30:15 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed trilinos from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-kqc52moweigxqxzwzfqajc6ocxwdwn4w


We see that every package in the trilinos DAG that depends on MPI now
uses ``mpich``.

.. code-block:: console

  $ spack find -d trilinos
  ==> 2 installed packages
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      trilinos@12.12.1
          ^boost@1.68.0
              ^bzip2@1.0.6
              ^zlib@1.2.11
          ^glm@0.9.7.1
          ^hdf5@1.10.4
              ^openmpi@3.1.3
                  ^hwloc@1.11.9
                      ^libpciaccess@0.13.5
                      ^libxml2@2.9.8
                          ^xz@5.2.4
                      ^numactl@2.0.11
          ^hypre@2.15.1
              ^openblas@0.3.3
          ^matio@1.5.9
          ^metis@5.1.0
          ^mumps@5.1.1
              ^netlib-scalapack@2.0.2
          ^netcdf@4.6.1
          ^parmetis@4.0.3
          ^suite-sparse@5.3.0

      trilinos@12.12.1
          ^boost@1.68.0
              ^bzip2@1.0.6
              ^zlib@1.2.11
          ^glm@0.9.7.1
          ^hdf5@1.10.4
              ^mpich@3.2.1
          ^hypre@2.15.1
              ^openblas@0.3.3
          ^matio@1.5.9
          ^metis@5.1.0
          ^mumps@5.1.1
              ^netlib-scalapack@2.0.2
          ^netcdf@4.6.1
          ^parmetis@4.0.3
          ^suite-sparse@5.3.0


As we discussed before, the ``spack find -d`` command shows the
dependency information as a tree. While that is often sufficient, many
complicated packages, including trilinos, have dependencies that
cannot be fully represented as a tree. Again, the ``spack graph``
command shows the full DAG of the dependency information.

.. code-block:: console

  $ spack graph trilinos
  o  trilinos
  |\
  | |\
  | | |\
  | | | |\
  | | | | |\
  | | | | | |\
  | | | | | | |\
  | | | | | | | |\
  | | | | | | | | |\
  | | | | | | | | | |\
  | | | | | | | | | | |\
  | | | | | | | | | | | |\
  | | | | | | | | | | | | |\
  o | | | | | | | | | | | | |  suite-sparse
  |\ \ \ \ \ \ \ \ \ \ \ \ \ \
  | |_|_|/ / / / / / / / / / /
  |/| | | | | | | | | | | | |
  | |\ \ \ \ \ \ \ \ \ \ \ \ \
  | | |_|_|_|_|_|/ / / / / / /
  | |/| | | | | | | | | | | |
  | | | |_|_|_|_|_|_|_|/ / /
  | | |/| | | | | | | | | |
  | | | o | | | | | | | | |  parmetis
  | | |/| | | | | | | | | |
  | |/|/| | | | | | | | | |
  | | | |/ / / / / / / / /
  | | | | | | o | | | | |  mumps
  | |_|_|_|_|/| | | | | |
  |/| | | |_|/| | | | | |
  | | | |/| |/ / / / / /
  | | | | |/| | | | | |
  | | | | o | | | | | |  netlib-scalapack
  | |_|_|/| | | | | | |
  |/| | |/| | | | | | |
  | | |/|/ / / / / / /
  | o | | | | | | | |  metis
  | |/ / / / / / / /
  | | | | | | | o |  glm
  | | |_|_|_|_|/ /
  | |/| | | | | |
  | o | | | | | |  cmake
  | |\ \ \ \ \ \ \
  | o | | | | | | |  openssl
  | |\ \ \ \ \ \ \ \
  | | | | | o | | | |  netcdf
  | | |_|_|/| | | | |
  | |/| | |/| | | | |
  | | | | | |\ \ \ \ \
  | | | | | | | |_|/ /
  | | | | | | |/| | |
  | | | | | | | o | |  matio
  | | |_|_|_|_|/| | |
  | |/| | | | |/ / /
  | | | | | | | o |  hypre
  | |_|_|_|_|_|/| |
  |/| | | | |_|/ /
  | | | | |/| | |
  | | | | | | o |  hdf5
  | | |_|_|_|/| |
  | |/| | | |/ /
  | | | | |/| |
  | | | | o | |  openmpi
  | | |_|/| | |
  | |/| | | | |
  | | | | |\ \ \
  | | | | | o | |  hwloc
  | | | | |/| | |
  | | | | | |\ \ \
  | | | | | | |\ \ \
  | | | | | | o | | |  libxml2
  | | |_|_|_|/| | | |
  | |/| | | |/| | | |
  | | | | | | | | | o  boost
  | | |_|_|_|_|_|_|/|
  | |/| | | | | | | |
  | o | | | | | | | |  zlib
  |  / / / / / / / /
  | | | | | o | | |  xz
  | | | | |  / / /
  | | | | | o | |  libpciaccess
  | | | | |/| | |
  | | | | | |\ \ \
  | | | | | o | | |  util-macros
  | | | | |  / / /
  | | | o | | | |  numactl
  | | | |\ \ \ \ \
  | | | | |_|_|/ /
  | | | |/| | | |
  | | | | |\ \ \ \
  | | | | | |_|/ /
  | | | | |/| | |
  | | | | | |\ \ \
  | | | | | o | | |  automake
  | | |_|_|/| | | |
  | |/| | | | | | |
  | | | | | |/ / /
  | | | | | o | |  autoconf
  | | |_|_|/| | |
  | |/| | |/ / /
  | | | |/| | |
  | o | | | | |  perl
  | o | | | | |  gdbm
  | o | | | | |  readline
  | |/ / / / /
  | o | | | |  ncurses
  | | |_|/ /
  | |/| | |
  | o | | |  pkgconf
  |  / / /
  o | | |  openblas
   / / /
   | o |  libtool
   |/ /
   o |  m4
   o |  libsigsegv
    /
    o  bzip2
    o  diffutils

You can control how the output is displayed with a number of options.

The ASCII output from ``spack graph`` can be difficult to parse for
complicated packages. The output can be changed to the ``graphviz``
``.dot`` format using the ``--dot`` flag.

.. code-block:: console

  $ spack graph --dot trilinos | dot -Tpdf trilinos_graph.pdf

.. _basics-tutorial-uninstall:

---------------------
Uninstalling Packages
---------------------

Earlier we installed many configurations each of zlib and tcl. Now we
will go through and uninstall some of those packages that we didn't
really need.

.. code-block:: console

  $ spack find -d tcl
  ==> 3 installed packages
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
      tcl@8.6.8
          ^zlib@1.2.8


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      tcl@8.6.8
          ^zlib@1.2.8

      tcl@8.6.8
          ^zlib@1.2.11


  $ spack find zlib
  ==> 6 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  zlib@1.2.8  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  zlib@1.2.8  zlib@1.2.8  zlib@1.2.11

We can uninstall packages by spec using the same syntax as install.

.. code-block:: console

  $ spack uninstall zlib %gcc@4.7
  ==> The following packages will be uninstalled:

  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx zlib@1.2.11%gcc+optimize+pic+shared

  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled zlib@1.2.11%gcc@4.7+optimize+pic+shared arch=linux-ubuntu16.04-x86_64 /bq2wtdx

  $ spack find -lf zlib
  ==> 5 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  i426yu3 zlib@1.2.8%clang
  4pt75q7 zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  bkyl5bh zlib@1.2.8%gcc
  64mns5m zlib@1.2.8%gcc cppflags="-O3"
  5nus6kn zlib@1.2.11%gcc

We can also uninstall packages by referring only to their hash.

We can use either ``-f`` (force) or ``-R`` (remove dependents as well) to
remove packages that are required by another installed package.

.. code-block:: console

  $ spack uninstall zlib/i426
  ==> Error: Will not uninstall zlib@1.2.8%clang@3.8.0-2ubuntu4/i426yu3

  The following packages depend on it:
      -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
      6wc66et tcl@8.6.8%clang

  ==> Error: Use \`spack uninstall --dependents\` to uninstall these dependencies as well.

  $ spack uninstall -R zlib/i426
  ==> The following packages will be uninstalled:

      -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
      6wc66et tcl@8.6.8%clang
      i426yu3 zlib@1.2.8%clang+optimize+pic+shared
  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled tcl@8.6.8%clang@3.8.0-2ubuntu4 arch=linux-ubuntu16.04-x86_64 /6wc66et
  ==> Successfully uninstalled zlib@1.2.8%clang@3.8.0-2ubuntu4+optimize+pic+shared arch=linux-ubuntu16.04-x86_64 /i426yu3

Spack will not uninstall packages that are not sufficiently
specified. The ``-a`` (all) flag can be used to uninstall multiple
packages at once.

.. code-block:: console

  $ spack uninstall trilinos
  ==> Error: trilinos matches multiple packages:

      -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      rlsruav trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2
      kqc52mo trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2

  ==> Error: You can either:
      a) use a more specific spec, or
      b) use `spack uninstall --all` to uninstall ALL matching specs.


  $ spack uninstall /rlsr
  ==> The following packages will be uninstalled:

      -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      rlsruav trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2
  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled trilinos@12.12.1%gcc@5.4.0~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2 arch=linux-ubuntu16.04-x86_64 /rlsruav

-----------------------------
Advanced ``spack find`` Usage
-----------------------------

We will go over some additional uses for the ``spack find`` command not
already covered in the :ref:`basics-tutorial-install` and
:ref:`basics-tutorial-uninstall` sections.

The ``spack find`` command can accept what we call "anonymous specs."
These are expressions in spec syntax that do not contain a package
name. For example, ``spack find ^mpich`` will return every installed
package that depends on mpich, and ``spack find cppflags="-O3"`` will
return every package which was built with ``cppflags="-O3"``.

.. code-block:: console

  $ spack find ^mpich
  ==> 8 installed packages
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  hdf5@1.10.4   matio@1.5.9  netcdf@4.6.1            parmetis@4.0.3
  hypre@2.15.1  mumps@5.1.1  netlib-scalapack@2.0.2  trilinos@12.12.1

  $ spack find cppflags=-O3
  ==> 1 installed packages.
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  zlib@1.2.8

The ``find`` command can also show which packages were installed
explicitly (rather than pulled in as a dependency) using the ``-x``
flag. The ``-X`` flag shows implicit installs only. The ``find`` command can
also show the path to which a spack package was installed using the ``-p``
command.

.. code-block:: console

  $ spack find -px
  ==> 10 installed packages
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
      zlib@1.2.11  /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.11-4pt75q7qq6lygf3hgnona4lyc2uwedul

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      hdf5@1.10.4       /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-5vcv5r67vpjzenq4apyebshclelnzuja
      hdf5@1.10.4       /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-ozyvmhzdew66byarohm4p36ep7wtcuiw
      hdf5@1.10.4       /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-xxd7syhgej6onpyfyewxqcqe7ltkt7ob
      tcl@8.6.8         /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8-am4pbatrtga3etyusg2akmsvrswwxno2
      tcl@8.6.8         /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8-qhwyccywhx2i6s7ob2gvjrjtj3rnfuqt
      trilinos@12.12.1  /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-kqc52moweigxqxzwzfqajc6ocxwdwn4w
      zlib@1.2.8        /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-bkyl5bhuep6fmhuxzkmhqy25qefjcvzc
      zlib@1.2.8        /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu
      zlib@1.2.11       /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb

---------------------
Customizing Compilers
---------------------


Spack manages a list of available compilers on the system, detected
automatically from from the user's ``PATH`` variable. The ``spack
compilers`` command is an alias for the command ``spack compiler list``.

.. code-block:: console

  $ spack compilers
  ==> Available compilers
  -- clang ubuntu16.04-x86_64 -------------------------------------
  clang@3.8.0-2ubuntu4  clang@3.7.1-2ubuntu2

  -- gcc ubuntu16.04-x86_64 ---------------------------------------
  gcc@5.4.0  gcc@4.7

The compilers are maintained in a YAML file. Later in the tutorial you
will learn how to configure compilers by hand for special cases. Spack
also has tools to add compilers, and compilers built with Spack can be
added to the configuration.

.. code-block:: console

  $ spack install gcc @7.2.0
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-suf5jtcfehivwfesrc5hjy72r4nukyel
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkgconf-1.4.2-fovrh7alpft646n6mhis5mml6k6e5f4v
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.1-3o765ourmesfrji6yeclb4wb5w54aqbh
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0-nxhwrg7xwc6nbsm2v4ezwe63l6nfidbi
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.14.1-q4fpyuo7ouhkeq6d3oabtrppctpvxmes
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.26.2-ic2kyoadgp3dxfejcbllyplj2wf524fo
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69-3sx2gxeibc4oasqd4o5h6lnwpcpsgd2q
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.16.1-rymw7imfehycqxzj4nuy2oiw3abegooy
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> Installing gmp
  ==> Searching for binary cache of gmp
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing gmp from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/gmp-6.1.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-gmp-6.1.2-qc4qcfz4monpllc3nqupdo7vwinf73sw.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:18:16 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed gmp from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gmp-6.1.2-qc4qcfz4monpllc3nqupdo7vwinf73sw
  ==> Installing isl
  ==> Searching for binary cache of isl
  ==> Installing isl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/isl-0.18/linux-ubuntu16.04-x86_64-gcc-5.4.0-isl-0.18-vttqoutnsmjpm3ogb52rninksc7hq5ax.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:05:19 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed isl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/isl-0.18-vttqoutnsmjpm3ogb52rninksc7hq5ax
  ==> Installing mpfr
  ==> Searching for binary cache of mpfr
  ==> Installing mpfr from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpfr-3.1.6/linux-ubuntu16.04-x86_64-gcc-5.4.0-mpfr-3.1.6-jnt2nnp5pmvikbw7opueajlbwbhmjxyv.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:32:07 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mpfr from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpfr-3.1.6-jnt2nnp5pmvikbw7opueajlbwbhmjxyv
  ==> Installing mpc
  ==> Searching for binary cache of mpc
  ==> Installing mpc from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpc-1.1.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-mpc-1.1.0-iuf3gc3zpgr4n4mditnxhff6x3joxi27.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:30:35 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mpc from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpc-1.1.0-iuf3gc3zpgr4n4mditnxhff6x3joxi27
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  Installing gcc
  ==> Searching for binary cache of gcc
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing gcc from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/gcc-7.2.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-gcc-7.2.0-b7smjjcsmwe5u5fcsvjmonlhlzzctnfs.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat Nov 10 05:22:47 2018 UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed gcc from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gcc-7.2.0-b7smjjcsmwe5u5fcsvjmonlhlzzctnfs

  $ spack find -p gcc
  spack find -p gcc
  ==> 1 installed package
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      gcc@7.2.0  /home/spack1/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gcc-7.2.0-b7smjjcsmwe5u5fcsvjmonlhlzzctnfs

We can add gcc to Spack as an available compiler using the ``spack
compiler add`` command. This will allow future packages to build with
gcc@7.2.0.

.. code-block:: console

  $ spack compiler add `spack location -i gcc@7.2.0`
  ==> Added 1 new compiler to /home/ubuntu/.spack/linux/compilers.yaml
      gcc@7.2.0
  ==> Compilers are defined in the following files:
      /home/ubuntu/.spack/linux/compilers.yaml

We can also remove compilers from our configuration using ``spack compiler remove <compiler_spec>``

.. code-block:: console

  $ spack compiler remove gcc@7.2.0
  ==> Removed compiler gcc@7.2.0
