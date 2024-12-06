.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _cudapackage:

----
Cuda
----

Different from other packages, ``CudaPackage`` does not represent a build system.
Instead its goal is to simplify and unify usage of ``CUDA`` in other packages by providing a `mixin-class <https://en.wikipedia.org/wiki/Mixin>`_.

You can find source for the package at
`<https://github.com/spack/spack/blob/develop/lib/spack/spack/build_systems/cuda.py>`__.

^^^^^^^^
Variants
^^^^^^^^

This package provides the following variants:

* **cuda**

  This variant is used to enable/disable building with ``CUDA``. The default
  is disabled (or ``False``).

* **cuda_arch**

  This variant supports the optional specification of one or multiple architectures.
  Valid values are maintained in the ``cuda_arch_values`` property and
  are the numeric character equivalent of the compute capability version
  (e.g., '10' for version 1.0). Each provided value affects associated
  ``CUDA`` dependencies and compiler conflicts.
  
  The variant builds both PTX code for the _virtual_ architecture
  (e.g. ``compute_10``) and binary code for the _real_ architecture (e.g. ``sm_10``).

  GPUs and their compute capability versions are listed at
  https://developer.nvidia.com/cuda-gpus .

^^^^^^^^^
Conflicts
^^^^^^^^^

Conflicts are used to prevent builds with known bugs or issues. While
base ``CUDA`` conflicts have been included with this package, you may
want to add more for your software.

For example, if your package requires ``cuda_arch`` to be specified when
``cuda`` is enabled, you can add the following conflict to your package
to terminate such build attempts with a suitable message:

.. code-block:: python

    conflicts("cuda_arch=none", when="+cuda",
              msg="CUDA architecture is required")

Similarly, if your software does not support all versions of the property,
you could add ``conflicts`` to your package for those versions.  For example,
suppose your software does not work with CUDA compute capability versions
prior to SM 5.0 (``50``).  You can add the following code to display a
custom message should a user attempt such a build:

.. code-block:: python

    unsupported_cuda_archs = [
        "10", "11", "12", "13",
        "20", "21",
        "30", "32", "35", "37"
    ]
    for value in unsupported_cuda_archs:
        conflicts(f"cuda_arch={value}", when="+cuda",
                  msg=f"CUDA architecture {value} is not supported")

^^^^^^^
Methods
^^^^^^^

This package provides one custom helper method, which is used to build
standard CUDA compiler flags.

**cuda_flags**

    This built-in static method returns a list of command line flags
    for the chosen ``cuda_arch`` value(s).  The flags are intended to
    be passed to the CUDA compiler driver (i.e., ``nvcc``).

    This method must be explicitly called when you are creating the
    arguments for your build in order to use the values.

^^^^^
Usage
^^^^^

This helper package can be added to your package by adding it as a base
class of your package.  For example, you can add it to your
:ref:`CMakePackage <cmakepackage>`-based package as follows:

.. code-block:: python
   :emphasize-lines: 1,7-16

    class MyCudaPackage(CMakePackage, CudaPackage):
        ...
        def cmake_args(self):
            spec = self.spec
            args = []
            ...
            if spec.satisfies("+cuda"):
                # Set up the cuda macros needed by the build
                args.append("-DWITH_CUDA=ON")
                cuda_arch_list = spec.variants["cuda_arch"].value
                cuda_arch = cuda_arch_list[0]
                if cuda_arch != "none":
                    args.append(f"-DCUDA_FLAGS=-arch=sm_{cuda_arch}")
            else:
                # Ensure build with cuda is disabled
                args.append("-DWITH_CUDA=OFF")
            ...
            return args

assuming only the ``WITH_CUDA`` and ``CUDA_FLAGS`` flags are required.
You will need to customize options as needed for your build.

This example also illustrates how to check for the ``cuda`` variant using
``self.spec`` and how to retrieve the ``cuda_arch`` variant's value, which
is a list, using ``self.spec.variants["cuda_arch"].value``.

With over 70 packages using ``CudaPackage`` as of January 2021 there are
lots of examples to choose from to get more ideas for using this package.
