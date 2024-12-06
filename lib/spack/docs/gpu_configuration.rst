.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

==========================
Using External GPU Support
==========================

Many packages come with a ``+cuda`` or ``+rocm`` variant. With no added
configuration Spack will download and install the needed components.
It may be preferable to use existing system support: the following sections
help with using a system installation of GPU libraries.

-----------------------------------
Using an External ROCm Installation
-----------------------------------

Spack breaks down ROCm into many separate component packages. The following
is an example ``packages.yaml`` that organizes a consistent set of ROCm
components for use by dependent packages:

.. code-block:: yaml

   packages:
     all:
       compiler: [rocmcc@=5.3.0]
       variants: amdgpu_target=gfx90a
     hip:
       buildable: false
       externals:
       - spec: hip@5.3.0
         prefix: /opt/rocm-5.3.0/hip
     hsa-rocr-dev:
       buildable: false
       externals:
       - spec: hsa-rocr-dev@5.3.0
         prefix: /opt/rocm-5.3.0/
     llvm-amdgpu:
       buildable: false
       externals:
       - spec: llvm-amdgpu@5.3.0
         prefix: /opt/rocm-5.3.0/llvm/
     comgr:
       buildable: false
       externals:
       - spec: comgr@5.3.0
         prefix: /opt/rocm-5.3.0/
     hipsparse:
       buildable: false
       externals:
       - spec: hipsparse@5.3.0
         prefix: /opt/rocm-5.3.0/
     hipblas:
       buildable: false
       externals:
       - spec: hipblas@5.3.0
         prefix: /opt/rocm-5.3.0/
     rocblas:
       buildable: false
       externals:
       - spec: rocblas@5.3.0
         prefix: /opt/rocm-5.3.0/
     rocprim:
       buildable: false
       externals:
       - spec: rocprim@5.3.0
         prefix: /opt/rocm-5.3.0/rocprim/

This is in combination with the following compiler definition:

.. code-block:: yaml

   compilers:
   - compiler:
       spec: rocmcc@=5.3.0
       paths:
         cc: /opt/rocm-5.3.0/bin/amdclang
         cxx: /opt/rocm-5.3.0/bin/amdclang++
         f77: null
         fc: /opt/rocm-5.3.0/bin/amdflang
       operating_system: rhel8
       target: x86_64

This includes the following considerations:

- Each of the listed externals specifies ``buildable: false`` to force Spack
  to use only the externals we defined.
- ``spack external find`` can automatically locate some of the ``hip``/``rocm``
  packages, but not all of them, and furthermore not in a manner that
  guarantees a complementary set if multiple ROCm installations are available.
- The ``prefix`` is the same for several components, but note that others
  require listing one of the subdirectories as a prefix.

-----------------------------------
Using an External CUDA Installation
-----------------------------------

CUDA is split into fewer components and is simpler to specify:

.. code-block:: yaml

   packages:
     all:
       variants:
       - cuda_arch=70
     cuda:
       buildable: false
       externals:
       - spec: cuda@11.0.2
         prefix: /opt/cuda/cuda-11.0.2/

where ``/opt/cuda/cuda-11.0.2/lib/`` contains ``libcudart.so``.



-----------------------------------
Using an External OpenGL API
-----------------------------------
Depending on whether we have a graphics card or not, we may choose to use OSMesa or GLX to implement the OpenGL API.

If a graphics card is unavailable, OSMesa is recommended and can typically be built with Spack.
However, if we prefer to utilize the system GLX tailored to our graphics card, we need to declare it as an external. Here's how to do it:


.. code-block:: yaml

  packages:
    libglx:
      require: [opengl]
    opengl:
      buildable: false
      externals:
      - prefix: /usr/
        spec: opengl@4.6

Note that prefix has to be the root of both the libraries and the headers, using is /usr not the path the the lib.
To know which spec for opengl is available use ``cd /usr/include/GL && grep -Ri gl_version``.
