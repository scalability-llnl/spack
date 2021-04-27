.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _inteloneapipackage:


====================
 IntelOneapiPackage
====================


.. contents::


oneAPI packages in Spack
========================

Spack can install and use the Intel oneAPI products. You may either
use spack to install the oneAPI tools or use the `Intel
installers`_. After installation, you may use the tools directly, or
use Spack to build packages with the tools.

The Spack Python class ``IntelOneapiPackage`` is a base class that is
used by ``IntelOneapiCompilers``, ``IntelOneapiMkl``,
``IntelOneapiTbb`` and other classes to implement the oneAPI
packages. See the :ref:<package-list> for the full list of available
oneAPI packages or use::

  spack list -d oneAPI

For more information on a specific package, do::

  spack info <package-name>

Intel no longer releases new versions of Parallel Studio, which can be
used in Spack via the :ref:<intelpackage>. All of its components can
now be found in oneAPI. 

Examples
========

Building a Package With icx
---------------------------

In this example, we build patchelf with ``icc`` and ``icx``. The
compilers are installed with spack.

Install the oneAPI compilers::

  spack install intel-oneapi-compilers

Add the compilers to your ``compilers.yaml`` so spack can use them::

  spack compiler add `spack location -i intel-oneapi-compilers`/compiler/latest/linux/bin/intel64
  spack compiler add `spack location -i intel-oneapi-compilers`/compiler/latest/linux/bin

Verify that the compilers are available::

  spack compiler list

The ``intel-oneapi-compilers`` package includes 2 families of
compilers:

* ``intel``: ``icc``, ``icpc``, ``ifort``. Intel's *classic*
  compilers.
* ``oneapi``: ``icx``, ``icpx``, ``ifx``. Intel's new generation of
  compilers based on LLVM.

To build the ``patchelf`` Spack package with ``icc``, do::

  spack install patchelf%intel

To build with with ``icx``, do ::

  spack install patchelf%oneapi

Using oneAPI MPI to Satisfy a Virtual Dependence
------------------------------------------------------

The ``hdf5`` package works with any compatible MPI implementation. To
build ``hdf5`` with Intel oneAPI MPI do::

  spack install hdf5 +mpi ^intel-oneapi-mpi

Using an Externally Installed oneAPI
====================================

Spack can also use oneAPI tools that are manually installed with
`Intel Installers`_.  The procedures for configuring Spack to use
external compilers and libraries are different.

Compilers
---------

To use the compilers, add some information about the installation to
``compilers.yaml``. For most users, it is sufficient to do::

  spack compiler add /opt/intel/oneapi/compiler/latest/linux/bin/intel64
  spack compiler add /opt/intel/oneapi/compiler/latest/linux/bin

Adapt the paths above if you did not install the tools in the default
location. After adding the compilers, using them is the same
as if you had installed the ``intel-oneapi-compilers`` package.
Another option is to manually add the configuration to
``compilers.yaml`` as described in :ref:`Compiler configuration
<compiler-config>`.

Libraries
---------

If you want Spack to use MKL that you have installed without Spack in
the default location, then add the following to
``~/.spack/packages.yaml``, adjusting the version as appropriate::

  intel-oneapi-mkl:
    externals:
    - spec: intel-oneapi-mkl@2021.1.1
      prefix: /opt/intel/oneapi/


Using oneAPI Tools Installed by Spack
=====================================

Spack can be a convenient way to install and configure compilers and
libaries, even if you do not intend to build a Spack package. If you
want to build a Makefile project using Spack-installed oneAPI compilers,
then use spack to configure your environment::

  spack load intel-oneapi-compilers

And then you can build with::

  CXX=icpx make

You can also use Spack-installed libraries. For example::

  spack load intel-oneapi-mkl

Will update your environment CPATH, LIBRARY_PATH, and other
environment variables for building an application with MKL.

More information
================

This section describes basic use of oneAPI, especially if it has
changed compared to Parallel Studio. See :ref:<intelpackage> for more
information on :ref:<intel-virtual-packages>,
:ref:<intel-unrelated-packages>,
:ref:<intel-integrating-external-libraries>, and
:ref:<using-mkl-tips>.


.. _`Intel installers`: https://software.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top.html
