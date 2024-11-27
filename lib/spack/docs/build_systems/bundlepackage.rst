.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _bundlepackage:

------
Bundle
------

``BundlePackage`` represents a set of packages that are expected to work
well together, such as a collection of commonly used software libraries.
The associated software is specified as dependencies.

If it makes sense, variants, conflicts, and requirements can be added to
the package. :ref:`Variants <variants>` ensure that common build options
are consistent across the packages supporting them.  :ref:`Conflicts
and requirements <packaging_conflicts>` prevent attempts to build with known
bugs or limitations.

For example, if ``MyBundlePackage`` is known to only build on ``linux``,
it could use the ``require`` directive as follows:

.. code-block:: python

    require("platform=linux", msg="MyBundlePackage only builds on linux")

Spack has a number of built-in bundle packages, such as:

* `AmdAocl <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/amd-aocl/package.py>`_
* `EcpProxyApps <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/ecp-proxy-apps/package.py>`_
* `Libc <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/libc/package.py>`_
* `Xsdk <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/xsdk/package.py>`_

where ``Xsdk`` also inherits from ``CudaPackage`` and ``RocmPackage`` and
``Libc`` is a virtual bundle package for the C standard library.


^^^^^^^^
Creation
^^^^^^^^

Be sure to specify the ``bundle`` template if you are using ``spack create``
to generate a package from the template.  For example, use the following
command to create a bundle package whose class name will be ``Mybundle``:

.. code-block:: console

    $ spack create --template bundle --name mybundle



^^^^^^
Phases
^^^^^^

The ``BundlePackage`` base class does not provide any phases by default
since the bundle does not represent a build system.


^^^
URL
^^^

The ``url`` property does not have meaning since there is no package-specific
code to fetch.


^^^^^^^
Version
^^^^^^^

At least one ``version`` must be specified in order for the package to
build.
