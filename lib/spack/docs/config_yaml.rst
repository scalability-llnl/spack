.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _config-yaml:

============================
Spack Settings (config.yaml)
============================

Spack's basic configuration options are set in ``config.yaml``.  You can
see the default settings by looking at
``etc/spack/defaults/config.yaml``:

.. literalinclude:: _spack_root/etc/spack/defaults/config.yaml
   :language: yaml

These settings can be overridden in ``etc/spack/config.yaml`` or
``~/.spack/config.yaml``.  See :ref:`configuration-scopes` for details.

---------------------
``install_tree:root``
---------------------

The location where Spack will install packages and their dependencies.
Default is ``$spack/opt/spack``.

---------------------------------------------------
``install_hash_length`` and ``install_path_scheme``
---------------------------------------------------

The default Spack installation path can be very long and can create problems
for scripts with hardcoded shebangs. Additionally, when using the Intel
compiler, and if there is also a long list of dependencies, the compiler may
segfault. If you see the following:

     .. code-block:: console

       : internal error: ** The compiler has encountered an unexpected problem.
       ** Segmentation violation signal raised. **
       Access violation or stack overflow. Please contact Intel Support for assistance.

it may be because variables containing dependency specs may be too long. There
are two parameters to help with long path names. Firstly, the
``install_hash_length`` parameter can set the length of the hash in the
installation path from 1 to 32. The default path uses the full 32 characters.

Secondly, it is also possible to modify the entire installation
scheme. By default Spack uses
``{architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}``
where the tokens that are available for use in this directive are the
same as those understood by the :meth:`~spack.spec.Spec.format`
method. Using this parameter it is possible to use a different package
layout or reduce the depth of the installation paths. For example

     .. code-block:: yaml

       config:
         install_path_scheme: '{name}/{version}/{hash:7}'

would install packages into sub-directories using only the package
name, version and a hash length of 7 characters.

When using either parameter to set the hash length it only affects the
representation of the hash in the installation directory. You
should be aware that the smaller the hash length the more likely
naming conflicts will occur. These parameters are independent of those
used to configure module names.

.. warning:: Modifying the installation hash length or path scheme after
   packages have been installed will prevent Spack from being
   able to find the old installation directories.

--------------------
``build_stage``
--------------------

Spack is designed to run out of a user home directory, and on many
systems the home directory is a (slow) network file system.  On most systems,
building in a temporary file system is faster.  Usually, there is also more
space available in the temporary location than in the home directory.  If the
username is not already in the path, Spack will append the value of ``$user`` to
the selected ``build_stage`` path.

.. warning:: We highly recommend specifying ``build_stage`` paths that
   distinguish between staging and other activities to ensure
   ``spack clean`` does not inadvertently remove unrelated files.
   Spack prepends ``spack-stage-`` to temporary staging directory names to
   reduce this risk.  Using a combination of ``spack`` and or ``stage`` in
   each specified path, as shown in the default settings and documented
   examples, will add another layer of protection.

By default, Spack's ``build_stage`` is configured like this:

.. code-block:: yaml

   build_stage:
    - $tempdir/$user/spack-stage
    - ~/.spack/stage

This can be an ordered list of paths that Spack should search when trying to
find a temporary directory for the build stage.  The list is searched in
order, and Spack will use the first directory to which it has write access.

Specifying `~/.spack/stage` first will ensure each user builds in their home
directory.  The historic Spack stage path `$spack/var/spack/stage` will build
directly inside the Spack instance.  See :ref:`config-file-variables` for more
on ``$tempdir`` and ``$spack``.

When Spack builds a package, it creates a temporary directory within the
``build_stage``.  After the package is successfully installed, Spack deletes
the temporary directory it used to build.  Unsuccessful builds are not
deleted, but you can manually purge them with :ref:`spack clean --stage
<cmd-spack-clean>`.

.. note::

   The build will fail if there is no writable directory in the ``build_stage``
   list, where any user- and site-specific setting will be searched first.

--------------------
``source_cache``
--------------------

Location to cache downloaded tarballs and repositories.  By default these
are stored in ``$spack/var/spack/cache``.  These are stored indefinitely
by default. Can be purged with :ref:`spack clean --downloads
<cmd-spack-clean>`.

--------------------
``misc_cache``
--------------------

Temporary directory to store long-lived cache files, such as indices of
packages available in repositories.  Defaults to ``~/.spack/cache``.  Can
be purged with :ref:`spack clean --misc-cache <cmd-spack-clean>`.

--------------------
``verify_ssl``
--------------------

When set to ``true`` (default) Spack will verify certificates of remote
hosts when making ``ssl`` connections.  Set to ``false`` to disable, and
tools like ``curl`` will use their ``--insecure`` options.  Disabling
this can expose you to attacks.  Use at your own risk.

--------------------
``ssl_certs``
--------------------

Path to custom certificats for SSL verification. The value can be a 
filesytem path, or an environment variable that expands to an absolute file path.
The default value is set to the environment variable ``SSL_CERT_FILE``
to use the same syntax used by many other applications that automatically
detect custom certificates.
When ``url_fetch_method:curl`` the ``config:ssl_certs`` should resolve to
a single file.  Spack will then set the environment variable ``CURL_CA_BUNDLE``
in the subprocess calling ``curl``.
If ``url_fetch_method:urllib`` then files and directories are supported i.e. 
``config:ssl_certs:$SSL_CERT_FILE`` or ``config:ssl_certs:$SSL_CERT_DIR``
will work.
In all cases the expanded path must be absolute for Spack to use the certificates.
Certificates relative to an environment can be created by prepending the path variable
with the Spack configuration variable``$env``.

--------------------
``checksum``
--------------------

When set to ``true``, Spack verifies downloaded source code using a
checksum, and will refuse to build packages that it cannot verify.  Set
to ``false`` to disable these checks.  Disabling this can expose you to
attacks.  Use at your own risk.

--------------------
``locks``
--------------------

When set to ``true``, concurrent instances of Spack will use locks to
avoid modifying the install tree, database file, etc. If false, Spack
will disable all locking, but you must **not** run concurrent instances
of Spack.  For file systems that don't support locking, you should set
this to ``false`` and run one Spack at a time, but otherwise we recommend
enabling locks.

--------------------
``dirty``
--------------------

By default, Spack unsets variables in your environment that can change
the way packages build. This includes ``LD_LIBRARY_PATH``, ``CPATH``,
``LIBRARY_PATH``, ``DYLD_LIBRARY_PATH``, and others.

By default, builds are ``clean``, but on some machines, compilers and
other tools may need custom ``LD_LIBRARY_PATH`` settings to run.  You can
set ``dirty`` to ``true`` to skip the cleaning step and make all builds
"dirty" by default.  Be aware that this will reduce the reproducibility
of builds.

.. _build-jobs:

--------------
``build_jobs``
--------------

Unless overridden in a package or on the command line, Spack builds all
packages in parallel. The default parallelism is equal to the number of
cores available to the process, up to 16 (the default of ``build_jobs``).
For a build system that uses Makefiles, this ``spack install`` runs:

- ``make -j<build_jobs>``, when ``build_jobs`` is less than the number of
  cores available
- ``make -j<ncores>``, when ``build_jobs`` is greater or equal to the
  number of cores available

If you work on a shared login node or have a strict ulimit, it may be
necessary to set the default to a lower value. By setting ``build_jobs``
to 4, for example, commands like ``spack install`` will run ``make -j4``
instead of hogging every core. To build all software in serial,
set ``build_jobs`` to 1.

Note that specifying the number of jobs on the command line always takes
priority, so that ``spack install -j<n>`` always runs `make -j<n>`, even
when that exceeds the number of cores available.

--------------------
``ccache``
--------------------

When set to ``true`` Spack will use ccache to cache compiles. This is
useful specifically in two cases: (1) when using ``spack dev-build``, and (2)
when building the same package with many different variants. The default is
``false``.

When enabled, Spack will look inside your ``PATH`` for a ``ccache``
executable and stop if it is not found. Some systems come with
``ccache``, but it can also be installed using ``spack install
ccache``. ``ccache`` comes with reasonable defaults for cache size
and location. (See the *Configuration settings* section of ``man
ccache`` to learn more about the default settings and how to change
them). Please note that we currently disable ccache's ``hash_dir``
feature to avoid an issue with the stage directory (see
https://github.com/spack/spack/pull/3761#issuecomment-294352232).

-----------------------
``shared_linking:type``
-----------------------

Control whether Spack embeds ``RPATH`` or ``RUNPATH`` attributes in ELF binaries
so that they can find their dependencies. Has no effect on macOS.
Two options are allowed:

 1. ``rpath`` uses ``RPATH`` and forces the ``--disable-new-tags`` flag to be passed to the linker
 2. ``runpath`` uses ``RUNPATH`` and forces the ``--enable-new-tags`` flag to be passed to the linker

``RPATH`` search paths have higher precedence than ``LD_LIBRARY_PATH``
and ld.so will search for libraries in transitive ``RPATHs`` of
parent objects.

``RUNPATH`` search paths have lower precedence than ``LD_LIBRARY_PATH``,
and ld.so will ONLY search for dependencies in the ``RUNPATH`` of
the loading object.

DO NOT MIX the two options within the same install tree.

-----------------------
``shared_linking:bind``
-----------------------

This is an *experimental option* that controls whether Spack embeds absolute paths
to needed shared libraries in ELF executables and shared libraries on Linux. Setting
this option to ``true`` has two advantages:

1. **Improved startup time**: when running an executable, the dynamic loader does not
   have to perform a search for needed libraries, they are loaded directly.
2. **Reliability**: libraries loaded at runtime are those that were linked to. This
   minimizes the risk of accidentally picking up system libraries.

In the current implementation, Spack sets the soname (shared object name) of
libraries to their install path upon installation. This has two implications:

1. binding does not apply to libraries installed *before* the option was enabled;
2. toggling the option off does *not* prevent binding of libraries installed when
   the option was still enabled.

It is also worth noting that:

1. Applications relying on ``dlopen(3)`` will continue to work, even when they open
   a library by name. This is because ``RPATH``\s are retained in binaries also
   when ``bind`` is enabled.
2. ``LD_PRELOAD`` continues to work for the typical use case of overriding
   symbols, such as preloading a library with a more efficient ``malloc``.
   However, the preloaded library will be loaded *additionally to*, instead of
   *in place of* another library with the same name --- this can be problematic
   in very rare cases where libraries rely on a particular ``init`` or ``fini``
   order.

.. note::

   In some cases packages provide *stub libraries* that only contain an interface
   for linking, but lack an implementation for runtime. An example of this is
   ``libcuda.so``, provided by the CUDA toolkit; it can be used to link against,
   but the library needed at runtime is the one installed with the CUDA driver.
   To avoid binding those libraries, they can be marked as non-bindable using
   a property in the package:

   .. code-block:: python

      class Example(Package):
         non_bindable_shared_objects = ["libinterface.so"]

----------------------
``install_status``
----------------------

When set to ``true``, Spack will show information about its current progress
as well as the current and total package numbers. Progress is shown both
in the terminal title and inline. Setting it to ``false`` will not show any
progress information.

To work properly, this requires your terminal to reset its title after
Spack has finished its work, otherwise Spack's status information will
remain in the terminal's title indefinitely. Most terminals should already
be set up this way and clear Spack's status information.

-----------
``aliases``
-----------

Aliases can be used to define new Spack commands. They can be either shortcuts
for longer commands or include specific arguments for convenience. For instance,
if users want to use ``spack install``'s ``-v`` argument all the time, they can
create a new alias called ``inst`` that will always call ``install -v``:

.. code-block:: yaml

   aliases:
     inst: install -v
