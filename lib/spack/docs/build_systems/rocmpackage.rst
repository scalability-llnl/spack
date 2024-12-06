.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _rocmpackage:

----
ROCm
----

The ``ROCmPackage`` is not a build system but a helper package. Like ``CudaPackage``,
it provides standard variants, dependencies, and conflicts to facilitate building
packages using GPUs though for AMD in this case.

You can find the source for this package (and suggestions for setting up your
``compilers.yaml`` and ``packages.yaml`` files) at
`<https://github.com/spack/spack/blob/develop/lib/spack/spack/build_systems/rocm.py>`__.

^^^^^^^^
Variants
^^^^^^^^

This package provides the following variants:

* **rocm**

  This variant is used to enable/disable building with ``rocm``.
  The default is disabled (or ``False``).

* **amdgpu_target**

  This variant supports the optional specification of the AMD GPU architecture.
  Valid values are the names of the GPUs (e.g., ``gfx701``), which are maintained
  in the ``amdgpu_targets`` property.

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^

This package defines basic ``rocm`` dependencies, including ``llvm`` and ``hip``.

^^^^^^^^^
Conflicts
^^^^^^^^^

Conflicts are used to prevent builds with known bugs or issues. This package
already requires that the ``amdgpu_target`` always be specified for ``rocm``
builds. It also defines a conflict that prevents builds with an ``amdgpu_target``
when ``rocm`` is disabled.

Refer to `Conflicts <https://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=conflicts#conflicts>`__
for more information on package conflicts.

^^^^^^^
Methods
^^^^^^^

This package provides one custom helper method, which is used to build
standard AMD hip compiler flags.

**hip_flags**

    This built-in static method returns the appropriately formatted
    ``--amdgpu-target`` build option for ``hipcc``.

    This method must be explicitly called when you are creating the
    arguments for your build in order to use the values.

^^^^^
Usage
^^^^^

This helper package can be added to your package by adding it as a base
class of your package.  For example, you can add it to your
:ref:`CMakePackage <cmakepackage>`-based package as follows:

.. code-block:: python
   :emphasize-lines: 1,3-7,14-25

    class MyRocmPackage(CMakePackage, ROCmPackage):
        ...
        # Ensure +rocm and amdgpu_targets are passed to dependencies
        depends_on("mydeppackage", when="+rocm")
        for val in ROCmPackage.amdgpu_targets:
            depends_on(f"mydeppackage amdgpu_target={val}",
                       when=f"amdgpu_target={val}")
        ...

        def cmake_args(self):
            spec = self.spec
            args = []
            ...
            if spec.satisfies("+rocm"):
                # Set up the hip macros needed by the build
                args.extend([
                    "-DENABLE_HIP=ON",
                    f"-DHIP_ROOT_DIR={spec['hip'].prefix}"])
                rocm_archs = spec.variants["amdgpu_target"].value
                if "none" not in rocm_archs:
                    args.append(f"-DHIP_HIPCC_FLAGS=--amdgpu-target={','.join(rocm_archs}")
            else:
                # Ensure build with hip is disabled
                args.append("-DENABLE_HIP=OFF")
            ...
            return args
        ...

assuming only on the ``ENABLE_HIP``, ``HIP_ROOT_DIR``, and ``HIP_HIPCC_FLAGS``
macros are required to be set and the only dependency needing rocm options
is ``mydeppackage``. You will need to customize the flags as needed for your
build.

This example also illustrates how to check for the ``rocm`` variant using
``self.spec`` and how to retrieve the ``amdgpu_target`` variant's value
using ``self.spec.variants["amdgpu_target"].value``.

All five packages using ``ROCmPackage`` as of January 2021 also use the
:ref:`CudaPackage <cudapackage>`. So it is worth looking at those packages
to get ideas for creating a package that can support both ``cuda`` and
``rocm``.
