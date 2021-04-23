.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _binary_caches:

============
Build Caches
============

Some sites may encourage users to set up their own test environments
before carrying out central installations, or some users may prefer to set
up these environments on their own motivation. To reduce the load of
recompiling otherwise identical package specs in different installations,
installed packages can be put into build cache tarballs, uploaded to
your Spack mirror and then downloaded and installed by others.


--------------------------
Creating build cache files
--------------------------

A compressed tarball of an installed package is created. Tarballs are created
for all of its link and run dependency packages as well. Compressed tarballs are
signed with gpg and signature and tarball and put in a ``.spack`` file. Optionally,
the rpaths (and ids and deps on macOS) can be changed to paths relative to
the Spack install tree before the tarball is created.

Build caches are created via:

.. code-block:: console

    $ spack buildcache create <spec>


If you wanted to create a build cache in a local directory, you would provide
the ``-d`` argument to target that directory, again also specifying the spec.
Here is an example creating a local directory, "spack-cache" and creating
build cache files for the "ninja" spec:

.. code-block:: console

    $ mkdir -p ./spack-cache
    $ spack buildcache create -d ./spack-cache ninja
    ==> Buildcache files will be output to file:///home/spackuser/spack/spack-cache/build_cache
    gpgconf: socketdir is '/run/user/1000/gnupg'
    gpg: using "E6DF6A8BD43208E4D6F392F23777740B7DBD643D" as default secret key for signing

Note that the targeted spec must already be installed. Once you have a build cache,
you can add it as a mirror, discussed next.

---------------------------------------
Finding or installing build cache files
---------------------------------------

To find build caches or install build caches, a Spack mirror must be configured
with:

.. code-block:: console

    $ spack mirror add <name> <url>


Note that the url can be a web url _or_ a local filesystem location. In the previous
example, you might add the directory "spack-cache" and call it ``mymirror``:


.. code-block:: console

    $ spack mirror add mymirror ./spack-cache


You can see that the mirror is added with ``spack mirror list`` as follows:

.. code-block:: console


    $ spack mirror list
    mymirror           file:///home/spackuser/spack/spack-cache
    spack-public       https://spack-llnl-mirror.s3-us-west-2.amazonaws.com/


At this point, you've create a buildcache, but spack hasn't indexed it, so if
you run ``spack buildcache list`` you won't see any results. You need to index
this new build cache as follows:

.. code-block:: console

    $ spack buildcache update-index -d spack-cache/

Now you can use list:

.. code-block:: console

    $  spack buildcache list
    ==> 1 cached build.
    -- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
    ninja@1.10.2


Great! So now let's say you have a different spack installation, or perhaps just
a different environment for the same one, and you want to install a package from
that build cache. Let's first uninstall the actual library "ninja" to see if we can
re-install it from the cache.

.. code-block:: console

    $ spack uninstall ninja


And now reinstall from the buildcache

.. code-block:: console

    $ spack buildcache install ninja
    ==> buildcache spec(s) matching ninja 
    ==> Fetching file:///home/spackuser/spack/spack-cache/build_cache/linux-ubuntu20.04-skylake/gcc-9.3.0/ninja-1.10.2/linux-ubuntu20.04-skylake-gcc-9.3.0-ninja-1.10.2-i4e5luour7jxdpc3bkiykd4imke3mkym.spack
    ####################################################################################################################################### 100.0%
    ==> Installing buildcache for spec ninja@1.10.2%gcc@9.3.0 arch=linux-ubuntu20.04-skylake
    gpgconf: socketdir is '/run/user/1000/gnupg'
    gpg: Signature made Tue 23 Mar 2021 10:16:29 PM MDT
    gpg:                using RSA key E6DF6A8BD43208E4D6F392F23777740B7DBD643D
    gpg: Good signature from "spackuser (GPG created for Spack) <spackuser@noreply.users.github.com>" [ultimate]


It worked! You've just completed a full example of creating a build cache with
a spec of interest, adding it as a mirror, updating it's index, listing the contents,
and finally, installing from it.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
List of popular build caches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Extreme-scale Scientific Software Stack (E4S) <https://e4s-project.github.io/>`_: `build cache <https://oaciss.uoregon.edu/e4s/inventory.html>`_


----------
Relocation
----------

Initial build and later installation do not necessarily happen at the same
location. Spack provides a relocation capability and corrects for RPATHs and
non-relocatable scripts. However, many packages compile paths into binary
artifacts directly. In such cases, the build instructions of this package would
need to be adjusted for better re-locatability.

.. _cmd-spack-buildcache:

--------------------
``spack buildcache``
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create tarball of installed Spack package and all dependencies.
Tarballs are checksummed and signed if gpg2 is available.
Places them in a directory ``build_cache`` that can be copied to a mirror.
Commands like ``spack buildcache install`` will search Spack mirrors for build_cache to get the list of build caches.

==============  ========================================================================================================================
Arguments       Description
==============  ========================================================================================================================
``<specs>``     list of partial specs or hashes with a leading ``/`` to match from installed packages and used for creating build caches
``-d <path>``   directory in which ``build_cache`` directory is created, defaults to ``.``
``-f``          overwrite ``.spack`` file in ``build_cache`` directory if it exists
``-k <key>``    the key to sign package with. In the case where multiple keys exist, the package will be unsigned unless ``-k`` is used.
``-r``          make paths in binaries relative before creating tarball
``-y``          answer yes to all create unsigned ``build_cache`` questions
==============  ========================================================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache list``
^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieves all specs for build caches available on a Spack mirror.

==============  =====================================================================================
Arguments       Description
==============  =====================================================================================
``<specs>``     list of partial package specs to be matched against specs downloaded for build caches
==============  =====================================================================================

E.g. ``spack buildcache list gcc`` with print only commands to install ``gcc`` package(s)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache install``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieves all specs for build caches available on a Spack mirror and installs build caches
with specs matching the specs input.

==============  ==============================================================================================
Arguments       Description
==============  ==============================================================================================
``<specs>``     list of partial package specs or hashes with a leading ``/`` to be installed from build caches
``-f``          remove install directory if it exists before unpacking tarball
``-y``          answer yes to all to don't verify package with gpg questions
==============  ==============================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache keys``
^^^^^^^^^^^^^^^^^^^^^^^^^

List public keys available on Spack mirror.

=========  ==============================================
Arguments  Description
=========  ==============================================
``-i``     trust the keys downloaded with prompt for each
``-y``     answer yes to all trust all keys downloaded
=========  ==============================================
