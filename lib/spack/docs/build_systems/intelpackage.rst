.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _intelpackage:

-----
Intel
-----

.. contents::

^^^^^^^^^^^^^^^^^^^^^^^^
Intel packages in Spack
^^^^^^^^^^^^^^^^^^^^^^^^

This is an earlier version of Intel software development tools and has
now been replaced by Intel oneAPI Toolkits.

Spack can install and use several software development products offered by Intel.
Some of these are available under no-cost terms, others require a paid license.
All share the same basic steps for configuration, installation, and, where
applicable, license management. The Spack Python class ``IntelPackage`` implements
these steps.

Spack interacts with Intel tools in several routes, like it does for any
other package:

.. _`route 1`:

1. Accept system-provided tools after you declare them to Spack as *external packages*.

.. _`route 2`:

2. Install the products for you as *internal packages* in Spack.

.. _`route 3`:

3. *Use* the packages, regardless of installation route, to install what we'll
   call *client packages* for you, this being Spack's primary purpose.

An auxiliary route follows from route 2, as it would for most Spack
packages, namely:

.. _`route 4`:

4. Make Spack-installed Intel tools available outside of Spack for ad-hoc use,
   typically through Spack-managed modulefiles.

This document covers routes 1 through 3.


""""""""""""""""""""""""""""""""""
Packages under no-cost license
""""""""""""""""""""""""""""""""""

Intel's standalone performance library products, notably MKL and MPI, are
available for use under a `simplified license
<https://software.intel.com/en-us/license/intel-simplified-software-license>`_
since 2017 [fn1]_. They are packaged in Spack as:

* ``intel-mkl`` -- Math Kernel Library (linear algebra and FFT),
* ``intel-mpi`` -- The Intel-MPI implementation (derived from MPICH),
* ``intel-ipp`` -- Primitives for image-, signal-, and data-processing,
* ``intel-daal`` -- Machine learning and data analytics.

Some earlier versions of these libraries were released under a paid license.
For these older versions, the license must be available at installation time of
the products and during compilation of client packages.

The library packages work well with the Intel compilers but do not require them
-- those packages can just as well be used with other compilers.  The Intel
compiler invocation commands offer custom options to simplify linking Intel
libraries (sometimes considerably), but Spack always uses fairly explicit
linkage anyway.


""""""""""""""""""
Licensed packages
""""""""""""""""""

Intel's core software development products that provide compilers, analyzers,
and optimizers do require a paid license.  In Spack, they are packaged as:

* ``intel-parallel-studio`` -- the entire suite of compilers and libraries,
* ``intel`` -- a subset containing just the compilers and the Intel-MPI runtime [fn2]_.

..
    TODO: Confirm and possible change(!) the scope of MPI components (runtime
    vs. devel) in current (and previous?) *cluster/professional/composer*
    editions, i.e., presence in downloads, possibly subject to license
    coverage(!); see `discussion in PR #4300
    <https://github.com/spack/spack/pull/4300#issuecomment-305582898>`_.  [NB:
    An "mpi" subdirectory is not indicative of the full MPI SDK being present
    (i.e., ``mpicc``, ..., and header files).  The directory may just as well
    contain only the MPI runtime (``mpirun`` and shared libraries) .]
    See also issue #8632.

The license is needed at installation time and to compile client packages, but
never to merely run any resulting binaries. The license status for a given
Spack package is normally specified in the *package code* through directives like
`license_required` (see :ref:`Licensed software <license>`).
For the Intel packages, however, the *class code* provides these directives (in
exchange of forfeiting a measure of OOP purity) and takes care of idiosyncasies
like historic version dependence.

The libraries that are provided in the standalone packages are also included in the
all-encompassing ``intel-parallel-studio``. To complicate matters a bit, that
package is sold in 3 "editions", of which only the upper-tier ``cluster``
edition supports *compiling* MPI applications, and hence only that edition can
provide the ``mpi`` virtual package.  (As mentioned [fn2]_, all editions
provide support for *running* MPI applications.)

The edition forms the leading part of the version number for Spack's
``intel*`` packages discussed here. This differs from the primarily numeric
version numbers seen with most other Spack packages. For example, we have:


.. code-block:: console

   $ spack info intel-parallel-studio
   ...
   Preferred version:
       professional.2018.3    http:...

   Safe versions:
       professional.2018.3    http:...
       ...
       composer.2018.3        http:...
       ...
       cluster.2018.3         http:...
       ...
   ...

The full studio suite, capable of compiling MPI applications, currently
requires about 12 GB of disk space when installed (see section `Install steps
for packages with compilers and libraries`_ for detailed instructions).
If you need to save disk space or installation time, you could install the
``intel`` compilers-only subset (0.6 GB) and just the library packages you
need, for example ``intel-mpi`` (0.5 GB) and ``intel-mkl`` (2.5 GB).

.. _intel-unrelated-packages:

""""""""""""""""""""
Unrelated packages
""""""""""""""""""""

The following packages do not use the Intel installer and are not in class ``IntelPackage``
that is discussed here:

* ``intel-gpu-tools`` -- Test suite and low-level tools for the Linux `Direct
  Rendering Manager <https://en.wikipedia.org/wiki/Direct_Rendering_Manager>`_
* ``intel-mkl-dnn`` -- Math Kernel Library for Deep Neural Networks (``CMakePackage``)
* ``intel-xed`` -- X86 machine instructions encoder/decoder
* ``intel-tbb`` -- Standalone version of Intel Threading Building Blocks. Note that
  a TBB runtime version is included with ``intel-mkl``, and development
  versions are provided by the packages ``intel-parallel-studio`` (all
  editions) and its ``intel`` subset.

""""""""""""""""""""""""""""""""""""""""""
Configuring Spack to use Intel licenses
""""""""""""""""""""""""""""""""""""""""""

If you wish to integrate licensed Intel products into Spack as external packages
(`route 1`_ above) we assume that their license configuration is in place and
is working [fn3]_. In this case, skip to section `Integration of Intel tools
installed external to Spack`_.

If you plan to have Spack install licensed products for you (`route 2`_ above),
the Intel product installer that Spack will run underneath must have access to
a license that is either provided by a *license server* or as a *license file*.
The installer may be able to locate a license that is already configured on
your system.  If it cannot, you must configure Spack to provide either the
server location or the license file.

For authoritative information on Intel licensing, see:

* https://software.intel.com/en-us/faq/licensing
* https://software.intel.com/en-us/articles/how-do-i-manage-my-licenses

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pointing to an existing license server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installing and configuring a license server is outside the scope of Spack. We
assume that:

* Your system administrator has a license server running.
* The license server offers valid licenses for the Intel packages of interest.
* You can access these licenses under the user id running Spack.

Be aware of the difference between (a) installing and configuring a license
server, and (b) configuring client software to *use* a server's
so-called floating licenses.  We are concerned here with (b) only. The
process of obtaining a license from a server for temporary use is called
"checking out a license".  For that, a client application such as the Intel
package installer or a compiler needs to know the host name and port number of
one or more license servers that it may query [fn4]_.

Follow one of three methods to `point client software to a floating license server
<https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license>`_.
Ideally, your license administrator will already have implemented one that can
be used unchanged in Spack: Look for the environment variable
``INTEL_LICENSE_FILE`` or for files
``/opt/intel/licenses/*.lic`` that contain::

  SERVER  hostname  hostid_or_ANY  portnum
  USE_SERVER

The relevant tokens, among possibly others, are the ``USE_SERVER`` line,
intended specifically for clients, and one or more ``SERVER`` lines above it
which give the network address.

If you cannot find pre-existing ``/opt/intel/licenses/*.lic`` files and the
``INTEL_LICENSE_FILE`` environment variable is not set (even after you loaded
any relevant modulefiles), ask your license administrator for the server
address(es) and place them in a "global" license file within your Spack
directory tree `as shown below <Spack-managed file_>`_).


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Installing a standalone license file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you purchased a user-specific license, follow `Intel's instructions
<https://software.intel.com/en-us/faq/licensing#license-management>`_
to "activate" it for your serial number, then download the resulting license file.
If needed, `request to have the file re-sent
<https://software.intel.com/en-us/articles/resend-license-file>`_ to you.

Intel's license files are text files that contain tokens in the proprietary
"FLEXlm" format and whose name ends in ``.lic``.
Intel installers and compilers look for license files in several locations when they run.
Place your license by one of the following means, in order of decreasing preference:

* Default directory

  Install your license file in the directory ``/opt/intel/licenses/`` if you
  have write permission to it. This directory is inspected by all Intel tools
  and is therefore preferred, as no further configuration will be needed.
  Create the directory if it does not yet exist.  For the file name, either
  keep the downloaded name or use another suitably plain yet descriptive
  name that ends in ``.lic``. Adjust file permissions for access by licensed
  users.


* Directory given in environment variable

  If you cannot use the default directory, but your system already has set the
  environment variable ``INTEL_LICENSE_FILE`` independent from Spack [fn5]_,
  then, if you have the necessary write permissions, place your license file in
  one of the directories mentioned in this environment variable.  Adjust file
  permissions to match licensed users.

  .. tip::

      If your system has not yet set and used the environment variable
      ``INTEL_LICENSE_FILE``, you could start using it with the ``spack
      install`` stage of licensed tools and subsequent client packages. You
      would, however, be in a bind to always set that variable in the same
      manner, across updates and re-installations, and perhaps accommodate
      additions to it. As this may be difficult in the long run, we recommend
      that you do *not* attempt to start using the variable solely for Spack.

.. _`Spack-managed file`:

* Spack-managed file

  The first time Spack encounters an Intel package that requires a license, it
  will initialize a Spack-global Intel-specific license file for you, as a
  template with instructional comments, and bring up an editor [fn6]_.  Spack
  will do this *even if you have a working license elsewhere* on the system.

  * To proceed with an externally configured license, leave the newly templated
    file as is (containing comments only) and close the editor. You do not need
    to touch the file again.

  * To configure your own standalone license, copy the contents of your
    downloaded license file into the opened file, save it, and close the editor.

  * To use a license server (i.e., a floating network license) that is not
    already configured elsewhere on the system, supply your license server
    address(es) in the form of ``SERVER`` and ``USE_SERVER`` lines at the
    *beginning of the file* [fn7]_, in the format shown in section `Pointing to
    an existing license server`_. Save the file and close the editor.

  To revisit and manually edit this file, such as prior to a subsequent
  installation attempt, find it at
  ``$SPACK_ROOT/etc/spack/licenses/intel/intel.lic`` .

  Spack will place symbolic links to this file in each directory where licensed
  Intel binaries were installed.  If you kept the template unchanged, Intel tools
  will simply ignore it.


.. _integrate-external-intel:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Integration of Intel tools installed *external* to Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section discusses `route 1`_ from the introduction.

A site that already uses Intel tools, especially licensed ones, will likely
have some versions already installed on the system, especially at a time when
Spack is just being introduced. It will be useful to make such previously
installed tools available for use by Spack as they are. How to do this varies
depending on the type of the tools:

""""""""""""""""""""""""""""""""""
Integrating external compilers
""""""""""""""""""""""""""""""""""

For Spack to use external Intel compilers, you must tell it both *where* to
find them and *when* to use them.  The present section documents the "where"
aspect, involving ``compilers.yaml`` and, in most cases, long absolute paths.
The "when" aspect actually relates to `route 3`_ and requires explicitly
stating the compiler as a spec component (in the form ``foo %intel`` or ``foo
%intel@compilerversion``) when installing client packages or altering Spack's
compiler default in ``packages.yaml``.
See section `Selecting Intel compilers <Selecting Intel compilers_>`_ for details.

To integrate a new set of externally installed Intel compilers into Spack
follow section
:ref:`Compiler configuration <compiler-config>`.
Briefly, prepare your shell environment like you would if you were to use these
compilers normally, i.e., typically by a ``module load ...`` or a shell
``source ...`` command, then use ``spack compiler find`` to make Spack aware of
these compilers.  This will create a new entry in a suitably scoped and possibly new
``compilers.yaml`` file. You could certainly create such a compiler entry
manually, but this is error-prone due to the indentation and different data
types involved.

The Intel compilers need and use the system's native GCC compiler (``gcc`` on
most systems, ``clang`` on macOS) to provide certain functionality, notably to
support C++. To provide a different GCC compiler for the Intel tools, or more
generally set persistent flags for all invocations of the Intel compilers, locate
the ``compilers.yaml`` entry that defines your Intel compiler, and, using a
text editor, change one or both of the following:

1. At the ``modules:`` tag, add a ``gcc`` module to the list.
2. At the ``flags:`` tag, add ``cflags:``, ``cxxflags:``, and ``fflags:`` key-value entries.

Consult the examples under
:ref:`Compiler configuration <compiler-config>`
and
:ref:`Vendor-Specific Compiler Configuration <vendor-specific-compiler-configuration>`
in the Spack documentation.
When done, validate your compiler definition by running
``spack compiler info intel@compilerversion`` (replacing ``compilerversion`` by
the version that you defined).

Be aware that both the GCC integration and persistent compiler flags can also be
affected by an advanced third method:

3. A modulefile that provides the Intel compilers for you
   could, for the benefit of users outside of Spack, implicitly
   integrate a specific ``gcc`` version via compiler flag environment variables
   or (hopefully not) via a sneaky extra ``PATH`` addition.

Next, visit section `Selecting Intel Compilers`_ to learn how to tell
Spack to use the newly configured compilers.

.. _intel-integrating-external-libraries:

""""""""""""""""""""""""""""""""""
Integrating external libraries
""""""""""""""""""""""""""""""""""

Configure external library-type packages (as opposed to compilers)
in the files ``$SPACK_ROOT/etc/spack/packages.yaml`` or
``~/.spack/packages.yaml``, following the Spack documentation under
:ref:`External Packages <sec-external-packages>`.

Similar to ``compilers.yaml``, the ``packages.yaml`` files define a package
external to Spack in terms of a Spack spec and resolve each such spec via
either the ``paths`` or ``modules`` tokens to a specific pre-installed package
version on the system.  Since Intel tools generally need environment variables
to interoperate, which cannot be conveyed in a mere ``paths`` specification,
the ``modules`` token will be more sensible to use. It resolves the Spack-side
spec to a modulefile generated and managed outside of Spack's purview,
which Spack will load internally and transiently when the corresponding spec is
called upon to compile client packages.

Unlike for compilers, where ``spack find compilers [spec]`` generates an entry
in an existing or new ``compilers.yaml`` file, Spack does not offer a command
to generate an entirely new ``packages.yaml`` entry.  You must create
new entries yourself in a text editor, though the command ``spack config
[--scope=...] edit packages`` can help with selecting the proper file.
See section
:ref:`Configuration Scopes <configuration-scopes>`
for an explanation about the different files
and section
:ref:`Build customization <packages-config>`
for specifics and examples for ``packages.yaml`` files.

.. If your system administrator did not provide modules for pre-installed Intel
   tools, you could do well to ask for them, because installing multiple copies
   of the Intel tools, as is won't to happen once Spack is in the picture, is
   bound to stretch disk space and patience thin. If you *are* the system
   administrator and are still new to modules, then perhaps it's best to follow
   the `next section <Installing Intel tools within Spack_>`_ and install the tools
   solely within Spack.

The following example integrates packages embodied by hypothetical
external modulefiles ``intel-mkl/18/...`` into
Spack as packages ``intel-mkl@...``:

.. code-block:: console

   $ spack config edit packages

Make sure the file begins with:

.. code-block:: yaml

   packages:

Adapt the following example. Be sure to maintain the indentation:

.. code-block:: yaml

   # other content ...

     intel-mkl:
       externals:
       - spec: "intel-mkl@2018.2.199  arch=linux-centos6-x86_64"
         modules:
         -  intel-mkl/18/18.0.2
       - spec: "intel-mkl@2018.3.222  arch=linux-centos6-x86_64"
         modules:
         -  intel-mkl/18/18.0.3

The version numbers for the ``intel-mkl`` specs defined here correspond to file
and directory names that Intel uses for its products because they were adopted
and declared as such within Spack's package repository. You can inspect the
versions known to your current Spack installation by:

.. code-block:: console

   $ spack info intel-mkl

Using the same version numbers for external packages as for packages known
internally is useful for clarity, but not strictly necessary.  Moreover, with a
``packages.yaml`` entry, you can go beyond internally known versions.

.. _compiler-neutral-package:

Note that the Spack spec in the example does not contain a compiler
specification. This is intentional, as the Intel library packages can be used
unmodified with different compilers.

A slightly more advanced example illustrates how to provide
:ref:`variants <basic-variants>`
and how to use the ``buildable: False`` directive to prevent Spack from installing
other versions or variants of the named package through its normal internal
mechanism.

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       externals:
       - spec: "intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64"
         modules:
         -  intel/18/18.0.2
       - spec: "intel-parallel-studio@cluster.2018.3.222 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64"
         modules:
         -  intel/18/18.0.3
       buildable: False

One additional example illustrates the use of ``prefix:`` instead of
``modules:``, useful when external modulefiles are not available or not
suitable:

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       externals:
       - spec: "intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal"
         prefix: /opt/intel
       - spec: "intel-parallel-studio@cluster.2018.3.222 +mkl+mpi+ipp+tbb+daal"
         prefix: /opt/intel
       buildable: False

Note that for the Intel packages discussed here, the directory values in the
``prefix:`` entries must be the high-level and typically version-less
"installation directory" that has been used by Intel's product installer.
Such a directory will typically accumulate various product versions.  Amongst
them, Spack will select the correct version-specific product directory based on
the ``@version`` spec component that each path is being defined for.

For further background and details, see
:ref:`External Packages <sec-external-packages>`.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installing Intel tools *within* Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section discusses `route 2`_ from the introduction.

When a system does not yet have Intel tools installed already, or the installed
versions are undesirable, Spack can install these tools like any regular Spack
package for you and, with appropriate pre- and post-install configuration, use its
compilers and/or libraries to install client packages.

.. _intel-install-studio:

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Install steps for packages with compilers and libraries
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The packages ``intel-parallel-studio`` and ``intel`` (which is a subset of the
former) are many-in-one products that contain both compilers and a set of
library packages whose scope depends on the edition.
Because they are general products geared towards shell environments,
it can be somewhat involved to integrate these packages at their full extent
into Spack.

Note: To install library-only packages like ``intel-mkl``, ``intel-mpi``, and ``intel-daal``
follow `the next section <intel-install-libs_>`_ instead.

1. Review the section `Configuring spack to use intel licenses`_.

.. _intel-compiler-anticipation:

2. To install a version of ``intel-parallel-studio`` that provides Intel
   compilers at a version that you have *not yet declared in Spack*,
   the following preparatory steps are recommended:

   A. Determine the compiler spec that the new ``intel-parallel-studio`` package
      will provide, as follows: From the package version, combine the last two
      digits of the version year, a literal "0" (zero), and the version component
      that immediately follows the year.

      ==========================================  ======================
      Package version                             Compiler spec provided
      ------------------------------------------  ----------------------
       ``intel-parallel-studio@edition.YYyy.u``   ``intel@yy.0.u``
      ==========================================  ======================

      Example: The package ``intel-parallel-studio@cluster.2018.3`` will provide
      the compiler with spec ``intel@18.0.3``.

   .. _`config-compiler-anticipated`:

   B. Add a new compiler section with the newly anticipated version at the
      end of a ``compilers.yaml`` file in a suitable scope.  For example, run:

      .. code-block:: console

         $ spack config --scope=user/linux edit compilers

      and append a stub entry:

      .. code-block:: yaml

         - compiler:
             target:     x86_64
             operating_system:   centos6
             modules:    []
             spec:       intel@18.0.3
             paths:
               cc:       /usr/bin/true
               cxx:      /usr/bin/true
               f77:      /usr/bin/true
               fc:       /usr/bin/true

      Replace ``18.0.3`` with the version that you determined in the preceding
      step. The exact contents under ``paths:`` do not matter yet, but the paths must exist.

   This temporary stub is required such that the ``intel-parallel-studio`` package
   can be installed for the ``intel`` compiler (which the package itself is going
   to provide after the installation) rather than an arbitrary system compiler.
   The paths given in ``cc``, ``cxx``, ``f77``, ``fc`` must exist, but will
   never be used to build anything during the installation of ``intel-parallel-studio``.

   The reason for this stub is that ``intel-parallel-studio`` also provides the
   ``mpi`` and ``mkl`` packages and when concretizing a spec, Spack ensures
   strong consistency of the used compiler across all dependencies:  [fn8]_.
   Installing a package ``foo +mkl %intel`` will make Spack look for a package
   ``mkl %intel``, which can be provided by ``intel-parallel-studio+mkl %intel``,
   but not by ``intel-parallel-studio+mkl %gcc``.

   Failure to do so may result in additional installations of ``mkl``, ``intel-mpi`` or
   even ``intel-parallel-studio`` as dependencies for other packages.

   .. _`verify-compiler-anticipated`:

3. Verify that the compiler version provided by the new ``studio`` version
   would be used as expected if you were to compile a client package:

   .. code-block:: console

      $ spack spec zlib %intel

   If the version does not match, explicitly state the anticipated compiler version, e.g.:

   .. code-block:: console

      $ spack spec zlib %intel@18.0.3

   if there are problems, review and correct the compiler's ``compilers.yaml``
   entry, be it still in stub form or already complete (as it would be for a
   re-installation).

4. Install the new ``studio`` package using Spack's regular ``install``
   command.
   It may be wise to provide the anticipated compiler (`see above
   <verify-compiler-anticipated_>`_) as an explicit concretization
   element:

   .. code-block:: console

      $ spack install intel-parallel-studio@cluster.2018.3  %intel@18.0.3

5. Follow the same steps as under `Integrating external compilers`_ to tell
   Spack the minutiae for actually using those compilers with client packages.
   If you placed a stub entry in a ``compilers.yaml`` file, now is the time to
   edit it and fill in the particulars.

   * Under ``paths:``, give the full paths to the actual compiler binaries (``icc``,
     ``ifort``, etc.) located within the Spack installation tree, in all their
     unsightly length [fn9]_.

     To determine the full path to the C compiler, adapt and run:

     .. code-block:: console

        $ find `spack location -i intel-parallel-studio@cluster.2018.3` \
               -name icc -type f -ls

     If you get hits for both ``intel64`` and ``ia32``, you almost certainly will
     want to use the ``intel64`` variant.  The ``icpc`` and ``ifort`` compilers
     will be located in the same directory as ``icc``.

   * Make sure to specify ``modules: ['intel-parallel-studio-cluster2018.3-intel-18.0.3-HASH']``
     (with ``HASH`` being the short hash as displayed when running
     ``spack find -l intel-parallel-studio@cluster.2018.3`` and the versions adapted accordingly)
     to ensure that the correct and complete environment for the Intel compilers gets
     loaded when running them. With modern versions of the Intel compiler you may otherwise see
     issues about missing libraries. Please also note that module name must exactly match
     the name as returned by ``module avail`` (and shown in the example above).

   * Use the ``modules:`` and/or ``cflags:`` tokens to further specify a suitable accompanying
     ``gcc`` version to help pacify picky client packages that ask for C++
     standards more recent than supported by your system-provided ``gcc`` and its
     ``libstdc++.so``.

   * If you specified a custom variant (for example ``+vtune``) you may want to add this as your
     preferred variant in the packages configuration for the ``intel-parallel-studio`` package
     as described in :ref:`package-preferences`. Otherwise you will have to specify
     the variant every time ``intel-parallel-studio`` is being used as ``mkl``, ``fftw`` or ``mpi``
     implementation to avoid pulling in a different variant.

   * To set the Intel compilers for default use in Spack, instead of the usual ``%gcc``,
     follow section `Selecting Intel compilers`_.

.. tip::

   Compiler packages like ``intel-parallel-studio`` can easily be above 10 GB
   in size, which can tax the disk space available for temporary files on
   small, busy, or restricted systems (like virtual machines). The Intel
   installer will stop and report insufficient space as::

       ==> './install.sh' '--silent' 'silent.cfg'
       ...
       Missing critical prerequisite
       -- Not enough disk space

   As first remedy, clean Spack's existing staging area:

   .. code-block:: console

      $ spack clean --stage

   then retry installing the large package. Spack normally cleans staging
   directories but certain failures may prevent it from doing so.

   If the error persists, tell Spack to use an alternative location for
   temporary files:

   1. Run ``df -h`` to identify an alternative location on your system.

   2. Tell Spack to use that location for staging. Do **one** of the following:

      * Run Spack with the environment variable ``TMPDIR`` altered for just a
        single command. For example, to use your ``$HOME`` directory:

        .. code-block:: console

           $ TMPDIR="$HOME/spack-stage"  spack install ....

        This example uses Bourne shell syntax. Adapt for other shells as needed.

      * Alternatively, customize
        Spack's ``build_stage`` :ref:`configuration setting <config-overrides>`.

        .. code-block:: console

           $ spack config edit config

        Append:

        .. code-block:: yaml

           config:
             build_stage:
             - /home/$user/spack-stage

        Do not duplicate the ``config:`` line if it already is present.
        Adapt the location, which here is the same as in the preceding example.

   3. Retry installing the large package.


.. _intel-install-libs:

""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Install steps for library-only packages
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To install library-only packages like ``intel-mkl``, ``intel-mpi``, and ``intel-daal``
follow the steps given here.
For packages that contain a compiler, follow `the previous section
<intel-install-studio_>`_ instead.

1. For pre-2017 product releases, review the section `Configuring Spack to use Intel licenses`_.

2. Inspect the package spec. Specify an explicit compiler if necessary, e.g.:

   .. code-block:: console

      $ spack spec intel-mpi@2018.3.199
      $ spack spec intel-mpi@2018.3.199  %intel

   Check that the package will use the compiler flavor and version that you expect.

3. Install the package normally within Spack. Use the same spec as in the
   previous command, i.e., as general or as specific as needed:

   .. code-block:: console

      $ spack install intel-mpi@2018.3.199
      $ spack install intel-mpi@2018.3.199  %intel@18

4. To prepare the new packages for use with client packages,
   follow `Selecting libraries to satisfy virtual packages`_.


""""""""""""""""
Debug notes
""""""""""""""""

* You can trigger a wall of additional diagnostics using Spack options, e.g.:

  .. code-block:: console

     $ spack --debug -v install intel-mpi

  The ``--debug`` option can also be useful while installing client
  packages `(see below) <Using Intel tools in Spack to install client
  packages_>`_ to confirm the integration of the Intel tools in Spack, notably
  MKL and MPI.

* The ``.spack/`` subdirectory of an installed ``IntelPackage`` will contain,
  besides Spack's usual archival items, a copy of the ``silent.cfg`` file that
  was passed to the Intel installer:

  .. code-block:: console

     $ grep COMPONENTS ...intel-mpi...<hash>/.spack/silent.cfg
     COMPONENTS=ALL

* If an installation error occurs, Spack will normally clean up and remove a
  partially installed target directory. You can direct Spack to keep it using
  ``--keep-prefix``, e.g.:

  .. code-block:: console

     $ spack install --keep-prefix  intel-mpi

  You must, however, *remove such partial installations* prior to subsequent
  installation attempts. Otherwise, the Intel installer will behave
  incorrectly.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using Intel tools in Spack to install client packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finally, this section pertains to `route 3`_ from the introduction.

Once Intel tools are installed within Spack as external or internal packages
they can be used as intended for installing client packages.


.. _`select-intel-compilers`:

""""""""""""""""""""""""""
Selecting Intel compilers
""""""""""""""""""""""""""

Select Intel compilers to compile client packages, like any compiler in Spack,
by one of the following means:

* Request the Intel compilers explicitly in the client spec, e.g.:

  .. code-block:: console

     $ spack install libxc@3.0.0%intel


* Alternatively, request Intel compilers implicitly by package preferences.
  Configure the order of compilers in the appropriate ``packages.yaml`` file,
  under either an ``all:`` or client-package-specific entry, in a
  ``compiler:`` list. Consult the Spack documentation for
  `Configuring Package Preferences <https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#configuring-package-preferences>`_
  and
  :ref:`Package Preferences <package-preferences>`.

Example: ``etc/spack/packages.yaml`` might simply contain:

.. code-block:: yaml

  packages:
    all:
      compiler: [ intel, gcc, ]

To be more specific, you can state partial or full compiler version numbers,
for example:

.. code-block:: yaml

  packages:
    all:
      compiler: [ intel@18, intel@17, gcc@4.4.7, gcc@4.9.3, gcc@7.3.0, ]


.. _intel-virtual-packages:

""""""""""""""""""""""""""""""""""""""""""""""""
Selecting libraries to satisfy virtual packages
""""""""""""""""""""""""""""""""""""""""""""""""

Intel packages, whether integrated into Spack as external packages or
installed within Spack, can be called upon to satisfy the requirement of a
client package for a library that is available from different providers.
The relevant virtual packages for Intel are ``blas``, ``lapack``,
``scalapack``, and ``mpi``.

In both integration routes, Intel packages can have optional
:ref:`variants <basic-variants>`
which alter the list of virtual packages they can satisfy.  For Spack-external
packages, the active variants are a combination of the defaults declared in
Spack's package repository and the spec it is declared as in ``packages.yaml``.
Needless to say, those should match the components that are actually present in
the external product installation. Likewise, for Spack-internal packages, the
active variants are determined, persistently at installation time, from the
defaults in the repository and the spec selected to be installed.

To have Intel packages satisfy virtual package requests for all or selected
client packages, edit the ``packages.yaml`` file.  Customize, either in the
``all:`` or a more specific entry, a ``providers:`` dictionary whose keys are
the virtual packages and whose values are the Spack specs that satisfy the
virtual package, in order of decreasing preference.  To learn more about the
``providers:`` settings, see the Spack tutorial for
`Configuring Package Preferences <https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#configuring-package-preferences>`_
and the section
:ref:`Package Preferences <package-preferences>`.

Example: The following fairly minimal example for ``packages.yaml`` shows how
to exclusively use the standalone ``intel-mkl`` package for all the linear
algebra virtual packages in Spack, and ``intel-mpi`` as the preferred MPI
implementation. Other providers can still be chosen on a per-package basis.

.. code-block:: yaml

  packages:
    all:
      providers:
        mpi:       [intel-mpi]
        blas:      [intel-mkl]
        lapack:    [intel-mkl]
        scalapack: [intel-mkl]

If you have access to the ``intel-parallel-studio@cluster`` edition, you can
use instead:

.. code-block:: yaml

    all:
      providers:
        mpi:       [intel-parallel-studio+mpi]
        # Note: +mpi vs. +mkl
        blas:      [intel-parallel-studio+mkl]
        lapack:    [intel-parallel-studio+mkl]
        scalapack: [intel-parallel-studio+mkl]

If you installed ``intel-parallel-studio`` within Spack ("`route 2`_"), make
sure you followed the `special installation step
<intel-compiler-anticipation_>`_ to ensure that its virtual packages match the
compilers it provides.


""""""""""""""""""""""""""""""""""""""""""""
Using Intel tools as explicit dependency
""""""""""""""""""""""""""""""""""""""""""""

With the proper installation as detailed above, no special steps should be
required when a client package specifically (and thus deliberately) requests an
Intel package as dependency, this being one of the target use cases for Spack.

.. _using-mkl-tips:

"""""""""""""""""""""""""""""""""""""""""""""""
Tips for configuring client packages to use MKL
"""""""""""""""""""""""""""""""""""""""""""""""

The Math Kernel Library (MKL) is provided by several Intel packages, currently
``intel-parallel-studio`` when variant ``+mkl`` is active (it is by default)
and the standalone ``intel-mkl``. Because of these different provider packages,
a *virtual* ``mkl`` package is declared in Spack.

* To use MKL-specific APIs in a client package:

  Declare a dependency on ``mkl``, rather than a specific provider like
  ``intel-mkl``.  Declare the dependency either absolutely or conditionally
  based on variants that your package might have declared:

  .. code-block:: python

     # Examples for absolute and conditional dependencies:
     depends_on("mkl")
     depends_on("mkl", when="+mkl")
     depends_on("mkl", when="fftw=mkl")

  The ``MKLROOT`` environment variable (part of the documented API) will be set
  during all stages of client package installation, and is available to both
  the Spack packaging code and the client code.

* To use MKL as provider for BLAS, LAPACK, or ScaLAPACK:

  The packages that provide ``mkl`` also provide the narrower
  virtual ``blas``, ``lapack``, and ``scalapack`` packages.
  See the relevant :ref:`Packaging Guide section <blas_lapack_scalapack>`
  for an introduction.
  To portably use these virtual packages, construct preprocessor and linker
  option strings in your package configuration code using the package functions
  ``.headers`` and ``.libs`` in conjunction with utility functions from the
  following classes:

  * :py:class:`llnl.util.filesystem.FileList`,
  * :py:class:`llnl.util.filesystem.HeaderList`,
  * :py:class:`llnl.util.filesystem.LibraryList`.

  .. tip::
     *Do not* use constructs like ``.prefix.include`` or ``.prefix.lib``, with
     Intel or any other implementation of ``blas``, ``lapack``, and
     ``scalapack``.

  For example, for an
  :ref:`AutotoolsPackage <autotoolspackage>`
  use ``.libs.ld_flags`` to transform the library file list into linker options
  passed to ``./configure``:

  .. code-block:: python

      def configure_args(self):
          args = []
          ...
          args.append("--with-blas=%s" % self.spec["blas"].libs.ld_flags)
          args.append("--with-lapack=%s" % self.spec["lapack"].libs.ld_flags)
          ...

  .. tip::
     Even though ``.ld_flags`` will return a string of multiple words, *do not*
     use quotes for options like ``--with-blas=...`` because Spack passes them
     to ``./configure`` without invoking a shell.

  Likewise, in a
  :ref:`MakefilePackage <makefilepackage>`
  or similar package that does not use AutoTools you may need to provide include
  and link options for use on command lines or in environment variables.
  For example, to generate an option string of the form ``-I<dir>``, use:

  .. code-block:: python

    self.spec["blas"].headers.include_flags

  and to generate linker options (``-L<dir> -llibname ...``), use the same as above,

  .. code-block:: python

    self.spec["blas"].libs.ld_flags

  See
  :ref:`MakefilePackage <makefilepackage>`
  and more generally the
  :ref:`Packaging Guide <blas_lapack_scalapack>`
  for background and further examples.


^^^^^^^^^^
Footnotes
^^^^^^^^^^

.. [fn1] Strictly speaking, versions from ``2017.2`` onward.

.. [fn2] The package ``intel`` intentionally does not have a ``+mpi`` variant since
   it is meant to be small. The native installer will always add MPI *runtime*
   components because it follows defaults defined in the download package, even
   when ``intel-parallel-studio ~mpi`` has been requested.

   For ``intel-parallel-studio +mpi``, the class function
   :py:func:``.IntelPackage.pset_components``
   will include ``"intel-mpi intel-imb"`` in a list of component patterns passed
   to the Intel installer. The installer will extend each pattern word with an
   implied glob-like ``*`` to resolve it to package names that are
   *actually present in the product BOM*.
   As a side effect, this pattern approach accommodates occasional package name
   changes, e.g., capturing both ``intel-mpirt`` and ``intel-mpi-rt`` .

.. [fn3] How could the external installation have succeeded otherwise?

.. [fn4] According to Intel's documentation, there is supposedly a way to install a
   product using a network license even `when a FLEXlm server is not running
   <https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license>`_:
   Specify the license in the form ``port@serverhost`` in the
   ``INTEL_LICENSE_FILE`` environment variable. All other means of specifying a
   network license require that the license server be up.

.. [fn5]  Despite the name, ``INTEL_LICENSE_FILE`` can hold several and diverse entries.
   They  can be either directories (presumed to contain ``*.lic`` files), file
   names, or network locations in the form ``port@host`` (on Linux and Mac),
   with all items separated by ":" (on Linux and Mac).

.. [fn6] Should said editor turn out to be ``vi``, you better be in a position
   to know how to use it.

.. [fn7] Comment lines in FLEXlm files, indicated by ``#`` as the first
   non-whitespace character on the line, are generally allowed anywhere in the file.
   There `have been reports <https://github.com/spack/spack/issues/6534>`_,
   however, that as of 2018, ``SERVER`` and ``USE_SERVER`` lines must precede
   any comment lines.

..
    .. [fnX] The name component ``intel`` of the compiler spec is separate from (in
       a different namespace than) the names of the Spack packages
       ``intel-parallel-studio`` and ``intel``. Both of the latter provide the former.

.. [fn8] Spack's close coupling of installed packages to compilers, which both
   necessitates the detour for installing ``intel-parallel-studio``, and
   largely limits any of its provided virtual packages to a single compiler, heavily
   favors `recommending to install Intel Parallel Studio outside of Spack
   <integrate-external-intel_>`_ and declare it for Spack in ``packages.yaml``
   by a `compiler-less spec <compiler-neutral-package_>`_.

.. [fn9] With some effort, you can convince Spack to use shorter paths.

   .. warning:: Altering the naming scheme means that Spack will lose track of
      all packages it has installed for you so far.
      That said, the time is right for this kind of customization
      when you are defining a new set of compilers.

   The relevant tunables are:

   1. Set the ``install_tree`` location in ``config.yaml``
      (:ref:`see doc <config-yaml>`).
   2. Set the hash length in ``install-path-scheme``, also in ``config.yaml``
      (:ref:`q.v. <config-yaml>`).
   3. You will want to set the *same* hash length for
      :ref:`module files <modules-projections>`
      if you have Spack produce them for you, under ``projections`` in
      ``modules.yaml``.
