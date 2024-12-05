.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
installed packages can be put into build cache tarballs, pushed to
your Spack mirror and then downloaded and installed by others.

Whenever a mirror provides prebuilt packages, Spack will take these packages
into account during concretization and installation, making ``spack install``
significantly faster.


.. note::

    We use the terms "build cache" and "mirror" often interchangeably. Mirrors
    are used during installation both for sources and prebuilt packages. Build
    caches refer to mirrors that provide prebuilt packages.


----------------------
Creating a build cache
----------------------

Build caches are created via:

.. code-block:: console

    $ spack buildcache push <path/url/mirror name> <spec>

This command takes the locally installed spec and its dependencies, and
creates tarballs of their install prefixes. It also generates metadata files,
signed with GPG. These tarballs and metadata files are then pushed to the
provided binary cache, which can be a local directory or a remote URL.

Here is an example where a build cache is created in a local directory named
"spack-cache", to which we push the "ninja" spec:

.. code-block:: console

    $ spack buildcache push ./spack-cache ninja
    ==> Pushing binary packages to file:///home/spackuser/spack/spack-cache/build_cache

Note that ``ninja`` must be installed locally for this to work.

Once you have a build cache, you can add it as a mirror, discussed next.

---------------------------------------
Finding or installing build cache files
---------------------------------------

To find build caches or install build caches, a Spack mirror must be configured
with:

.. code-block:: console

    $ spack mirror add <name> <url or path>


Both web URLs and local paths on the filesystem can be specified. In the previous
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

    $ spack buildcache update-index ./spack-cache

Now you can use list:

.. code-block:: console

    $  spack buildcache list
    ==> 1 cached build.
    -- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
    ninja@1.10.2

With ``mymirror`` configured and an index available, Spack will automatically
use it during concretization and installation. That means that you can expect
``spack install ninja`` to fetch prebuilt packages from the mirror. Let's
verify by re-installing ninja:

.. code-block:: console

    $ spack uninstall ninja
    $ spack install ninja
    ==> Installing ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz
    ==> Fetching file:///home/spackuser/spack/spack-cache/build_cache/linux-ubuntu20.04-skylake-gcc-9.3.0-ninja-1.10.2-yxferyhmrjkosgta5ei6b4lqf6bxbscz.spec.json.sig
    gpg: Signature made Do 12 Jan 2023 16:01:04 CET
    gpg:                using RSA key 61B82B2B2350E171BD17A1744E3A689061D57BF6
    gpg: Good signature from "example (GPG created for Spack) <example@example.com>" [ultimate]
    ==> Fetching file:///home/spackuser/spack/spack-cache/build_cache/linux-ubuntu20.04-skylake/gcc-9.3.0/ninja-1.10.2/linux-ubuntu20.04-skylake-gcc-9.3.0-ninja-1.10.2-yxferyhmrjkosgta5ei6b4lqf6bxbscz.spack
    ==> Extracting ninja-1.10.2-yxferyhmrjkosgta5ei6b4lqf6bxbscz from binary cache
    ==> ninja: Successfully installed ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz
    Search: 0.00s.  Fetch: 0.17s.  Install: 0.12s.  Total: 0.29s
    [+] /home/harmen/spack/opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz


It worked! You've just completed a full example of creating a build cache with
a spec of interest, adding it as a mirror, updating its index, listing the contents,
and finally, installing from it.

By default Spack falls back to building from sources when the mirror is not available
or when the package is simply not already available. To force Spack to only install
prebuilt packages, you can use

.. code-block:: console

   $ spack install --use-buildcache only <package>

For example, to combine all of the commands above to add the E4S build cache
and then install from it exclusively, you would do:

.. code-block:: console

    $ spack mirror add E4S https://cache.e4s.io
    $ spack buildcache keys --install --trust
    $ spack install --use-buildcache only <package>

We use ``--install`` and ``--trust`` to say that we are installing keys to our
keyring, and trusting all downloaded keys.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
List of popular build caches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Extreme-scale Scientific Software Stack (E4S) <https://e4s-project.github.io/>`_: `build cache <https://oaciss.uoregon.edu/e4s/inventory.html>`_'

-------------------
Build cache signing
-------------------

By default, Spack will add a cryptographic signature to each package pushed to
a build cache, and verifies the signature when installing from a build cache.

Keys for signing can be managed with the :ref:`spack gpg <cmd-spack-gpg>` command,
as well as ``spack buildcache keys`` as mentioned above.

You can disable signing when pushing with ``spack buildcache push --unsigned``,
and disable verification when installing from any build cache with
``spack install --no-check-signature``.

Alternatively, signing and verification can be enabled or disabled on a per build cache
basis:

.. code-block:: console

    $ spack mirror add --signed <name> <url>  # enable signing and verification
    $ spack mirror add --unsigned <name> <url>  # disable signing and verification

    $ spack mirror set --signed <name>  # enable signing and verification for an existing mirror
    $ spack mirror set --unsigned <name>  # disable signing and verification for an existing mirror

Or you can directly edit the ``mirrors.yaml`` configuration file:

.. code-block:: yaml

    mirrors:
      <name>:
        url: <url>
        signed: false # disable signing and verification

See also :ref:`mirrors`.

----------
Relocation
----------

When using buildcaches across different machines, it is likely that the install
root will be different from the one used to build the binaries.

To address this issue, Spack automatically relocates all paths encoded in binaries
and scripts to their new location upon install.

Note that there are some cases where this is not possible: if binaries are built in
a relatively short path, and then installed to a longer path, there may not be enough
space in the binary to encode the new path. In this case, Spack will fail to install
the package from the build cache, and a source build is required.

To reduce the likelihood of this happening, it is highly recommended to add padding to
the install root during the build, as specified in the :ref:`config <config-yaml>`
section of the configuration:

.. code-block:: yaml

   config:
     install_tree:
       root: /opt/spack
       padded_length: 128


.. _binary_caches_oci:

---------------------------------
Automatic push to a build cache
---------------------------------

Sometimes it is convenient to push packages to a build cache as soon as they are installed. Spack can do this by setting autopush flag when adding a mirror:

.. code-block:: console

    $ spack mirror add --autopush <name> <url or path>

Or the autopush flag can be set for an existing mirror:

.. code-block:: console

    $ spack mirror set --autopush <name>  # enable automatic push for an existing mirror
    $ spack mirror set --no-autopush <name>  # disable automatic push for an existing mirror

Then after installing a package it is automatically pushed to all mirrors with ``autopush: true``. The command

.. code-block:: console

    $ spack install <package>

will have the same effect as

.. code-block:: console

    $ spack install <package>
    $ spack buildcache push <cache> <package>  # for all caches with autopush: true

.. note::

    Packages are automatically pushed to a build cache only if they are built from source.

-----------------------------------------
OCI / Docker V2 registries as build cache
-----------------------------------------

Spack can also use OCI or Docker V2 registries such as Dockerhub, Quay.io,
Github Packages, GitLab Container Registry, JFrog Artifactory, and others
as build caches. This is a convenient way to share binaries using public
infrastructure, or to cache Spack built binaries in Github Actions and
GitLab CI.

To get started, configure an OCI mirror using ``oci://`` as the scheme,
and optionally specify a username and password (or personal access token):

.. code-block:: console

    $ spack mirror add --oci-username username --oci-password password my_registry oci://example.com/my_image

Spack follows the naming conventions of Docker, with Dockerhub as the default
registry. To use Dockerhub, you can omit the registry domain:

.. code-block:: console

    $ spack mirror add --oci-username username --oci-password password my_registry oci://username/my_image

From here, you can use the mirror as any other build cache:

.. code-block:: console

    $ spack buildcache push my_registry <specs...>  # push to the registry
    $ spack install <specs...> # install from the registry

A unique feature of buildcaches on top of OCI registries is that it's incredibly
easy to generate get a runnable container image with the binaries installed. This
is a great way to make applications available to users without requiring them to
install Spack -- all you need is Docker, Podman or any other OCI-compatible container
runtime.

To produce container images, all you need to do is add the ``--base-image`` flag
when pushing to the build cache:

.. code-block:: console

    $ spack buildcache push --base-image ubuntu:20.04 my_registry ninja
    Pushed to example.com/my_image:ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz.spack

    $ docker run -it example.com/my_image:ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz.spack
    root@e4c2b6f6b3f4:/# ninja --version
    1.11.1

If ``--base-image`` is not specified, distroless images are produced. In practice,
you won't be able to run these as containers, since they don't come with libc and
other system dependencies. However, they are still compatible with tools like
``skopeo``, ``podman``, and ``docker`` for pulling and pushing.

.. note::
    The docker ``overlayfs2`` storage driver is limited to 128 layers, above which a
    ``max depth exceeded`` error may be produced when pulling the image. There
    are `alternative drivers <https://docs.docker.com/storage/storagedriver/>`_.

------------------------------------
Spack build cache for GitHub Actions
------------------------------------

To significantly speed up Spack in GitHub Actions, binaries can be cached in
GitHub Packages. This service is an OCI registry that can be linked to a GitHub
repository.

Spack offers a public build cache for GitHub Actions with a set of common packages,
which lets you get started quickly. See the following resources for more information:

* `spack/setup-spack <https://github.com/spack/setup-spack>`_ for setting up Spack in GitHub
  Actions
* `spack/github-actions-buildcache <https://github.com/spack/github-actions-buildcache>`_ for
  more details on the public build cache

.. _cmd-spack-buildcache:

--------------------
``spack buildcache``
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache push``
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
