# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

from spack.package import *


class Mfem(Package, CudaPackage, ROCmPackage):
    """Free, lightweight, scalable C++ library for finite element methods."""

    tags = ["fem", "finite-elements", "high-order", "amr", "hpc", "radiuss", "e4s"]

    homepage = "http://www.mfem.org"
    git = "https://github.com/mfem/mfem.git"

    maintainers("v-dobrev", "tzanio", "acfisher", "markcmiller86")

    test_requires_compiler = True

    # Recommended mfem builds to test when updating this file: see the shell
    # script 'test_builds.sh' in the same directory as this file.

    # mfem is downloaded from a URL shortener at request of upstream
    # author Tzanio Kolev <tzanio@llnl.gov>.  See here:
    #     https://github.com/mfem/mfem/issues/53
    #
    # The following procedure should be used to verify security when a
    # new version is added:
    #
    # 1. Verify that no checksums on old versions have changed.
    #
    # 2. Verify that the shortened URL for the new version is listed at:
    #    https://mfem.org/download/
    #
    # 3. Use http://getlinkinfo.com or similar to verify that the
    #    underling download link for the latest version comes has the
    #    prefix: http://mfem.github.io/releases
    #
    # If this quick verification procedure fails, additional discussion
    # will be required to verify the new version.

    license("BSD-3-Clause")

    # 'develop' is a special version that is always larger (or newer) than any
    # other version.
    version("develop", branch="master")

    version(
        "4.7.0",
        sha256="5e889493f5f79848f7b2d16afaae307c59880ac2a7ff2315551c60ca54717751",
        url="https://bit.ly/mfem-4-7",
        extension="tar.gz",
    )

    version(
        "4.6.0",
        sha256="5fa9465b5bec56bfb777a4d2826fba48d85fbace4aed8b64a2fd4059bf075b15",
        url="https://bit.ly/mfem-4-6",
        extension="tar.gz",
    )

    version(
        "4.5.2",
        sha256="7003c908c8265810ff97cb37531521b3aed24959975833a01ea05adfdb36e0f7",
        url="https://bit.ly/mfem-4-5-2",
        extension="tar.gz",
    )

    version(
        "4.5.0",
        sha256="4f201bec02fc5460a902596697b6c1deb7b15ac57c71f615b2ab4a8eb65665f7",
        url="https://bit.ly/mfem-4-5",
        extension="tar.gz",
    )

    version(
        "4.4.0",
        sha256="37250dbef6e97b16dc9ab50973e8d68bc165bb4afcdaf91b3b72c8972c87deef",
        url="https://bit.ly/mfem-4-4",
        extension="tar.gz",
    )

    version(
        "4.3.0",
        sha256="3a495602121b986049286ea0b23512279cdbdfb43c15c42a1511b521051fbe38",
        url="https://bit.ly/mfem-4-3",
        extension="tar.gz",
    )

    version(
        "4.2.0",
        sha256="4352a225b55948d2e73a5ee88cece0e88bdbe7ba6726a23d68b2736d3221a86d",
        url="https://bit.ly/mfem-4-2",
        extension="tar.gz",
    )

    version(
        "4.1.0",
        sha256="4c83fdcf083f8e2f5b37200a755db843cdb858811e25a8486ad36b2cbec0e11d",
        url="https://bit.ly/mfem-4-1",
        extension="tar.gz",
    )

    version(
        "4.0.0",
        sha256="df5bdac798ea84a263979f6fbf79de9013e1c55562f95f98644c3edcacfbc727",
        url="https://bit.ly/mfem-4-0",
        extension="tar.gz",
    )

    # Tagged development version used by the laghos package:
    version(
        "3.4.1-laghos-v2.0", tag="laghos-v2.0", commit="4cb8d2cbc19aac5528df650b4a41c54158d1d2c2"
    )

    version(
        "3.4.0",
        sha256="4e73e4fe0482636de3c5dc983cd395839a83cb16f6f509bd88b053e8b3858e05",
        url="https://bit.ly/mfem-3-4",
        extension="tar.gz",
    )

    version(
        "3.3.2",
        sha256="b70fa3c5080b9ec514fc05f4a04ff74322b99ac4ecd6d99c229f0ed5188fc0ce",
        url="https://goo.gl/Kd7Jk8",
        extension="tar.gz",
    )

    # Tagged development version used by the laghos package:
    version(
        "3.3.1-laghos-v1.0", tag="laghos-v1.0", commit="e1f466e6bf80d5f8449b9e1585c414bad4704195"
    )

    version(
        "3.3",
        sha256="b17bd452593aada93dc0fee748fcfbbf4f04ce3e7d77fdd0341cc9103bcacd0b",
        url="http://goo.gl/Vrpsns",
        extension="tar.gz",
    )

    version(
        "3.2",
        sha256="2938c3deed4ec4f7fd5b5f5cfe656845282e86e2dcd477d292390058b7b94340",
        url="http://goo.gl/Y9T75B",
        extension="tar.gz",
    )

    version(
        "3.1",
        sha256="841ea5cf58de6fae4de0f553b0e01ebaab9cd9c67fa821e8a715666ecf18fc57",
        url="http://goo.gl/xrScXn",
        extension="tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    variant("static", default=True, description="Build static library")
    variant("shared", default=False, description="Build shared library")
    variant("mpi", default=True, sticky=True, description="Enable MPI parallelism")
    # Can we make the default value for "metis" to depend on the "mpi" value?
    variant("metis", default=True, sticky=True, description="Enable METIS support")
    variant("openmp", default=False, description="Enable OpenMP parallelism")
    # Note: "+cuda" and "cuda_arch" variants are added by the CudaPackage
    # Note: "+rocm" and "amdgpu_target" variants are added by the ROCmPackage
    variant("occa", default=False, description="Enable OCCA backend")
    variant("raja", default=False, description="Enable RAJA backend")
    variant("libceed", default=False, description="Enable libCEED backend")
    variant("umpire", default=False, description="Enable Umpire support")
    variant("amgx", default=False, description="Enable NVIDIA AmgX solver support")

    variant(
        "threadsafe",
        default=False,
        description=(
            "Enable thread safe features."
            " Required for OpenMP."
            " May cause minor performance issues."
        ),
    )
    variant(
        "superlu-dist", default=False, description="Enable MPI parallel, sparse direct solvers"
    )
    variant("strumpack", default=False, description="Enable support for STRUMPACK")
    variant("suite-sparse", default=False, description="Enable serial, sparse direct solvers")
    variant("petsc", default=False, description="Enable PETSc solvers, preconditioners, etc.")
    variant("mumps", default=False, description="Enable MUMPS solver.")
    variant("slepc", default=False, description="Enable SLEPc integration")
    variant("sundials", default=False, description="Enable Sundials time integrators")
    variant("pumi", default=False, description="Enable functionality based on PUMI")
    variant("gslib", default=False, description="Enable functionality based on GSLIB")
    variant("mpfr", default=False, description="Enable precise, 1D quadrature rules")
    variant("lapack", default=False, description="Use external blas/lapack routines")
    variant("debug", default=False, description="Build debug instead of optimized version")
    variant("netcdf", default=False, description="Enable Cubit/Genesis reader")
    variant("conduit", default=False, description="Enable binary data I/O using Conduit")
    variant("zlib", default=True, description="Support zip'd streams for I/O")
    variant("gnutls", default=False, description="Enable secure sockets using GnuTLS")
    variant(
        "libunwind", default=False, description="Enable backtrace on error support using Libunwind"
    )
    variant("fms", default=False, when="@4.3.0:", description="Enable FMS I/O support")
    variant("ginkgo", default=False, when="@4.3.0:", description="Enable Ginkgo support")
    variant("hiop", default=False, when="@4.4.0:", description="Enable HiOp support")
    # TODO: SIMD, ADIOS2, MKL CPardiso, Axom/Sidre
    variant(
        "timer",
        default="auto",
        values=("auto", "std", "posix", "mac", "mpi"),
        description="Timing functions to use in mfem::StopWatch",
    )
    variant("examples", default=False, description="Build and install examples")
    variant("miniapps", default=False, description="Build and install miniapps")
    variant("exceptions", default=False, description="Enable the use of exceptions")
    variant(
        "precision",
        default="double",
        values=("single", "double"),
        multi=False,
        description="Floating point precision",
        when="@4.7.0:",
    )
    variant(
        "cxxstd",
        default="auto",
        values=("auto", conditional("98", when="@:3"), "11", "14", "17"),
        multi=False,
        description="C++ language standard",
    )

    conflicts("+shared", when="@:3.3.2")
    conflicts("~static~shared")
    conflicts("~threadsafe", when="@:3+openmp")

    conflicts("+cuda", when="@:3")
    conflicts("+rocm", when="@:4.1")
    conflicts("+cuda+rocm")
    conflicts("+netcdf", when="@:3.1")
    conflicts("+superlu-dist", when="@:3.1")
    # STRUMPACK support was added in mfem v3.3.2, however, here we allow only
    # strumpack v3+ support for which is available starting with mfem v4.0:
    conflicts("+strumpack", when="@:3")
    conflicts("+gnutls", when="@:3.1")
    conflicts("+zlib", when="@:3.2")
    conflicts("+mpfr", when="@:3.2")
    conflicts("+petsc", when="@:3.2")
    conflicts("+slepc", when="@:4.1")
    conflicts("+sundials", when="@:3.2")
    conflicts("+pumi", when="@:3.3.2")
    conflicts("+gslib", when="@:4.0")
    conflicts("timer=mac", when="@:3.3.0")
    conflicts("timer=mpi", when="@:3.3.0")
    conflicts("~metis+mpi", when="@:3.3.0")
    conflicts("+metis~mpi", when="@:3.3.0")
    conflicts("+conduit", when="@:3.3.2")
    conflicts("+occa", when="mfem@:3")
    conflicts("+raja", when="mfem@:3")
    conflicts("+libceed", when="mfem@:4.0")
    conflicts("+umpire", when="mfem@:4.0")
    conflicts("+amgx", when="mfem@:4.1")
    conflicts("+amgx", when="~cuda")
    conflicts("+mpi~cuda ^hypre+cuda")
    conflicts("+mpi ^hypre+cuda", when="@:4.2")
    conflicts("+mpi~rocm ^hypre+rocm")
    conflicts("+mpi ^hypre+rocm", when="@:4.3")

    conflicts("+superlu-dist", when="~mpi")
    conflicts("+strumpack", when="~mpi")
    conflicts("+petsc", when="~mpi")
    conflicts("+slepc", when="~petsc")
    conflicts("+pumi", when="~mpi")
    conflicts("timer=mpi", when="~mpi")
    conflicts("+mumps", when="~mpi")

    # See https://github.com/mfem/mfem/issues/2957
    conflicts("^mpich@4:", when="@:4.3+mpi")

    depends_on("mpi", when="+mpi")
    depends_on("hipsparse", when="@4.4.0:+rocm")

    with when("+mpi"):
        depends_on("hypre")
        depends_on("hypre@2.10.0:2.13", when="@:3.3")
        depends_on("hypre@:2.20.0", when="@3.4:4.2")
        depends_on("hypre@:2.23.0", when="@4.3.0")

    # If hypre is built with +cuda, propagate cuda_arch
    requires("^hypre@2.22.1:", when="+mpi+cuda ^hypre+cuda")
    for sm_ in CudaPackage.cuda_arch_values:
        requires(f"^hypre cuda_arch={sm_}", when=f"+mpi+cuda cuda_arch={sm_} ^hypre+cuda")
    # If hypre is built with +rocm, propagate amdgpu_target
    requires("^hypre@2.23.0: ", when="+mpi+rocm ^hypre+rocm")
    for gfx in ROCmPackage.amdgpu_targets:
        requires(f"^hypre amdgpu_target={gfx}", when=f"+mpi+rocm amdgpu_target={gfx} ^hypre+rocm")

    depends_on("metis", when="+metis")
    depends_on("blas", when="+lapack")
    depends_on("lapack@3.0:", when="+lapack")

    depends_on("sundials@2.7.0", when="@:3.3.0+sundials~mpi")
    depends_on("sundials@2.7.0+mpi+hypre", when="@:3.3.0+sundials+mpi")
    depends_on("sundials@2.7.0:", when="@3.3.2:+sundials~mpi")
    depends_on("sundials@2.7.0:+mpi+hypre", when="@3.3.2:+sundials+mpi")
    depends_on("sundials@5.0.0:5", when="@4.1.0:4.4+sundials~mpi")
    depends_on("sundials@5.0.0:5+mpi+hypre", when="@4.1.0:4.4+sundials+mpi")
    depends_on("sundials@5.0.0:6.7.0", when="@4.5.0:+sundials~mpi")
    depends_on("sundials@5.0.0:6.7.0+mpi+hypre", when="@4.5.0:+sundials+mpi")
    conflicts("cxxstd=11", when="^sundials@6.4.0:")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "sundials@5.4.0:+cuda cuda_arch={0}".format(sm_),
            when="@4.2.0:+sundials+cuda cuda_arch={0}".format(sm_),
        )
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "sundials@5.7.0:+rocm amdgpu_target={0}".format(gfx),
            when="@4.6.0:+sundials+rocm amdgpu_target={0}".format(gfx),
        )
    depends_on("pumi", when="+pumi~shared")
    depends_on("pumi+shared", when="+pumi+shared")
    depends_on("pumi@2.2.3:2.2.5", when="@4.2.0:4.3.0+pumi")
    depends_on("pumi@2.2.6:", when="@4.4.0:+pumi")
    depends_on("gslib+mpi", when="+gslib+mpi")
    depends_on("gslib~mpi~mpiio", when="+gslib~mpi")
    depends_on("gslib@1.0.5:1.0.6", when="@:4.2+gslib")
    depends_on("gslib@1.0.7:", when="@4.3.0:+gslib")
    depends_on("suite-sparse", when="+suite-sparse")
    depends_on("superlu-dist", when="+superlu-dist")
    # If superlu-dist is built with +cuda, propagate cuda_arch
    for sm_ in CudaPackage.cuda_arch_values:
        requires(
            f"^superlu-dist cuda_arch={sm_}",
            when=f"+superlu-dist+cuda cuda_arch={sm_} ^superlu-dist+cuda",
        )
    # If superlu-dist is built with +rocm, propagate amdgpu_target
    for gfx in ROCmPackage.amdgpu_targets:
        requires(
            f"^superlu-dist+rocm amdgpu_target={gfx}",
            when=f"+superlu-dist+rocm amdgpu_target={gfx} ^superlu-dist+rocm",
        )
    depends_on("strumpack@3.0.0:", when="+strumpack~shared")
    depends_on("strumpack@3.0.0:+shared", when="+strumpack+shared")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "strumpack+cuda cuda_arch={0}".format(sm_),
            when="+strumpack+cuda cuda_arch={0}".format(sm_),
        )
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "strumpack+rocm amdgpu_target={0}".format(gfx),
            when="+strumpack+rocm amdgpu_target={0}".format(gfx),
        )
    # The PETSc tests in MFEM will fail if PETSc is not configured with
    # MUMPS (and SuiteSparse in older versions). On the other hand, PETSc built
    # with MUMPS is not strictly required, so we do not require it here.
    depends_on("petsc@3.8:+mpi+hypre", when="+petsc")
    depends_on("slepc@3.8.0:", when="+slepc")
    # If petsc is built with +cuda, propagate cuda_arch to petsc and slepc
    for sm_ in CudaPackage.cuda_arch_values:
        requires(f"^petsc cuda_arch={sm_}", when=f"+cuda+petsc cuda_arch={sm_} ^petsc+cuda")
        depends_on(f"slepc+cuda cuda_arch={sm_}", when=f"+cuda+slepc cuda_arch={sm_} ^petsc+cuda")
    # If petsc is built with +rocm, propagate amdgpu_target to petsc and slepc
    for gfx in ROCmPackage.amdgpu_targets:
        requires(
            f"^petsc amdgpu_target={gfx}", when=f"+rocm+petsc amdgpu_target={gfx} ^petsc+rocm"
        )
        depends_on(
            f"slepc+rocm amdgpu_target={gfx}", when=f"+rocm+slepc amdgpu_target={gfx} ^petsc+rocm"
        )
    depends_on("mumps@5.1.1:", when="+mumps")
    depends_on("mpfr", when="+mpfr")
    depends_on("netcdf-c@4.1.3:", when="+netcdf")
    depends_on("unwind", when="+libunwind")
    depends_on("zlib-api", when="+zlib")
    depends_on("gnutls", when="+gnutls")
    depends_on("conduit@0.3.1:,master:", when="+conduit")
    depends_on("conduit+mpi", when="+conduit+mpi")
    depends_on("libfms@0.2.0:", when="+fms")
    depends_on("ginkgo@1.4.0:", when="+ginkgo")
    conflicts("cxxstd=11", when="^ginkgo")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "ginkgo+cuda cuda_arch={0}".format(sm_), when="+ginkgo+cuda cuda_arch={0}".format(sm_)
        )
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "ginkgo+rocm amdgpu_target={0}".format(gfx),
            when="+ginkgo+rocm amdgpu_target={0}".format(gfx),
        )
    depends_on("hiop@0.4.6:~mpi", when="+hiop~mpi")
    depends_on("hiop@0.4.6:+mpi", when="+hiop+mpi")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "hiop+cuda cuda_arch={0}".format(sm_), when="+hiop+cuda cuda_arch={0}".format(sm_)
        )
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "hiop+rocm amdgpu_target={0}".format(gfx),
            when="+hiop+rocm amdgpu_target={0}".format(gfx),
        )

    # The MFEM 4.0.0 SuperLU interface fails when using hypre@2.16.0 and
    # superlu-dist@6.1.1. See https://github.com/mfem/mfem/issues/983.
    # This issue was resolved in v4.1.
    conflicts("+superlu-dist", when="mfem@:4.0 ^hypre@2.16.0: ^superlu-dist@6:")
    # The STRUMPACK v3 interface in MFEM seems to be broken as of MFEM v4.1
    # when using hypre version >= 2.16.0.
    # This issue is resolved in v4.2.
    conflicts("+strumpack", when="mfem@4.0.0:4.1 ^hypre@2.16.0:")
    conflicts("+strumpack ^strumpack+cuda", when="~cuda")

    depends_on("occa@1.0.8:", when="@:4.1+occa")
    depends_on("occa@1.1.0", when="@4.2.0:+occa")
    depends_on("occa+cuda", when="+occa+cuda")
    # TODO: propagate "+rocm" variant to occa when it is supported

    depends_on("raja@0.7.0:0.9.0", when="@4.0.0+raja")
    depends_on("raja@0.10.0:0.12.1", when="@4.0.1:4.2.0+raja")
    depends_on("raja@0.13.0", when="@4.3.0+raja")
    depends_on("raja@0.14.0:2022.03", when="@4.4.0:4.5.0+raja")
    depends_on("raja@2022.10.3:", when="@4.5.2:+raja")
    conflicts("cxxstd=11", when="^raja@2022.03.0:")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "raja+cuda cuda_arch={0}".format(sm_), when="+raja+cuda cuda_arch={0}".format(sm_)
        )
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "raja+rocm amdgpu_target={0}".format(gfx),
            when="+raja+rocm amdgpu_target={0}".format(gfx),
        )

    depends_on("libceed@0.6", when="@:4.1+libceed")
    depends_on("libceed@0.7:0.8", when="@4.2.0+libceed")
    depends_on("libceed@0.8:0.9", when="@4.3.0+libceed")
    depends_on("libceed@0.10.1:", when="@4.4.0:+libceed")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "libceed+cuda cuda_arch={0}".format(sm_),
            when="+libceed+cuda cuda_arch={0}".format(sm_),
        )
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "libceed+rocm amdgpu_target={0}".format(gfx),
            when="+libceed+rocm amdgpu_target={0}".format(gfx),
        )

    depends_on("umpire@2.0.0:2.1.0", when="@:4.3.0+umpire")
    depends_on("umpire@3.0.0:", when="@4.4.0:+umpire")
    conflicts("cxxstd=11", when="^umpire@2022.03.0:")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "umpire+cuda cuda_arch={0}".format(sm_), when="+umpire+cuda cuda_arch={0}".format(sm_)
        )
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "umpire+rocm amdgpu_target={0}".format(gfx),
            when="+umpire+rocm amdgpu_target={0}".format(gfx),
        )

    # AmgX: propagate the cuda_arch and mpi settings:
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "amgx+mpi cuda_arch={0}".format(sm_), when="+amgx+mpi cuda_arch={0}".format(sm_)
        )
        depends_on(
            "amgx~mpi cuda_arch={0}".format(sm_), when="+amgx~mpi cuda_arch={0}".format(sm_)
        )

    for using_double_cond in ["@:4.6", "precision=double"]:
        with when(using_double_cond):
            # May need to enforce precision consistency on other packages in the
            # future.
            depends_on("hypre precision=double", when="+mpi")
            depends_on("petsc+double", when="+petsc")
            depends_on("mumps+double", when="+mumps")
    with when("precision=single"):
        # May need to enforce precision consistency on other packages in the
        # future.
        depends_on("hypre precision=single", when="+mpi")
        depends_on("petsc~double", when="+petsc")
        depends_on("mumps+float", when="+mumps")

    patch("mfem_ppc_build.patch", when="@3.2:3.3.0 arch=ppc64le")
    patch("mfem-3.4.patch", when="@3.4.0")
    patch("mfem-3.3-3.4-petsc-3.9.patch", when="@3.3.0:3.4.0 +petsc ^petsc@3.9.0:")
    patch("mfem-4.2-umpire.patch", when="@4.2.0+umpire")
    patch("mfem-4.2-slepc.patch", when="@4.2.0+slepc")
    patch("mfem-4.2-petsc-3.15.0.patch", when="@4.2.0+petsc ^petsc@3.15.0:")
    patch("mfem-4.3-hypre-2.23.0.patch", when="@4.3.0")
    patch("mfem-4.3-cusparse-11.4.patch", when="@4.3.0+cuda")
    # Patch to fix MFEM makefile syntax error. See
    # https://github.com/mfem/mfem/issues/1042 for the bug report and
    # https://github.com/mfem/mfem/pull/1043 for the bugfix contributed
    # upstream.
    patch("mfem-4.0.0-makefile-syntax-fix.patch", when="@4.0.0")
    patch("mfem-4.5.patch", when="@4.5.0")
    patch("mfem-4.6.patch", when="@4.6.0")
    patch(
        "https://github.com/mfem/mfem/pull/4005.patch?full_index=1",
        when="@4.6.0 +gslib+shared+miniapps",
        sha256="2a31682d876626529e2778a216d403648b83b90997873659a505d982d0e65beb",
    )
    patch("mfem-4.7.patch", when="@4.7.0")

    phases = ["configure", "build", "install"]

    def setup_build_environment(self, env):
        env.unset("MFEM_DIR")
        env.unset("MFEM_BUILD_DIR")
        # Workaround for changes made by the 'kokkos-nvcc-wrapper' package
        # which can be a dependency e.g. through PETSc that uses Kokkos:
        if "^kokkos-nvcc-wrapper" in self.spec:
            env.set("MPICH_CXX", spack_cxx)
            env.set("OMPI_CXX", spack_cxx)
            env.set("MPICXX_CXX", spack_cxx)

    #
    # Note: Although MFEM does support CMake configuration, MFEM
    # development team indicates that vanilla GNU Make is the
    # preferred mode of configuration of MFEM and the mode most
    # likely to be up to date in supporting *all* of MFEM's
    # configuration options. So, don't use CMake
    #
    def get_make_config_options(self, spec, prefix):
        def yes_no(varstr):
            return "YES" if varstr in self.spec else "NO"

        xcompiler = "" if "~cuda" in spec else "-Xcompiler="

        # We need to add rpaths explicitly to allow proper export of link flags
        # from within MFEM. We use the following two functions to do that.
        ld_flags_from_library_list = self.ld_flags_from_library_list
        ld_flags_from_dirs = self.ld_flags_from_dirs

        def find_optional_library(name, prefix):
            for shared in [True, False]:
                for path in ["lib64", "lib"]:
                    lib = find_libraries(
                        name, join_path(prefix, path), shared=shared, recursive=False
                    )
                    if lib:
                        return lib
            return LibraryList([])

        # Determine how to run MPI tests, e.g. when using '--test=root', when
        # Spack is run inside a batch system job.
        mfem_mpiexec = "mpirun"
        mfem_mpiexec_np = "-np"
        if "SLURM_JOBID" in os.environ:
            mfem_mpiexec = "srun"
            mfem_mpiexec_np = "-n"
        elif "LSB_JOBID" in os.environ:
            if "LLNL_COMPUTE_NODES" in os.environ:
                mfem_mpiexec = "lrun"
                mfem_mpiexec_np = "-n"
            else:
                mfem_mpiexec = "jsrun"
                mfem_mpiexec_np = "-p"
        elif "FLUX_EXEC_PATH" in os.environ:
            mfem_mpiexec = "flux run"
            mfem_mpiexec_np = "-n"
        elif "PBS_JOBID" in os.environ:
            mfem_mpiexec = "mpiexec"
            mfem_mpiexec_np = "-n"

        metis5_str = "NO"
        if ("+metis" in spec) and spec["metis"].satisfies("@5:"):
            metis5_str = "YES"

        zlib_var = "MFEM_USE_ZLIB" if (spec.satisfies("@4.1.0:")) else "MFEM_USE_GZSTREAM"

        options = [
            "PREFIX=%s" % prefix,
            "MFEM_USE_MEMALLOC=YES",
            "MFEM_DEBUG=%s" % yes_no("+debug"),
            # NOTE: env["CXX"] is the spack c++ compiler wrapper. The real
            # compiler is defined by env["SPACK_CXX"].
            "CXX=%s" % env["CXX"],
            "MFEM_USE_LIBUNWIND=%s" % yes_no("+libunwind"),
            "%s=%s" % (zlib_var, yes_no("+zlib")),
            "MFEM_USE_METIS=%s" % yes_no("+metis"),
            "MFEM_USE_METIS_5=%s" % metis5_str,
            "MFEM_THREAD_SAFE=%s" % yes_no("+threadsafe"),
            "MFEM_USE_MPI=%s" % yes_no("+mpi"),
            "MFEM_USE_LAPACK=%s" % yes_no("+lapack"),
            "MFEM_USE_SUPERLU=%s" % yes_no("+superlu-dist"),
            "MFEM_USE_STRUMPACK=%s" % yes_no("+strumpack"),
            "MFEM_USE_SUITESPARSE=%s" % yes_no("+suite-sparse"),
            "MFEM_USE_SUNDIALS=%s" % yes_no("+sundials"),
            "MFEM_USE_PETSC=%s" % yes_no("+petsc"),
            "MFEM_USE_SLEPC=%s" % yes_no("+slepc"),
            "MFEM_USE_PUMI=%s" % yes_no("+pumi"),
            "MFEM_USE_GSLIB=%s" % yes_no("+gslib"),
            "MFEM_USE_NETCDF=%s" % yes_no("+netcdf"),
            "MFEM_USE_MPFR=%s" % yes_no("+mpfr"),
            "MFEM_USE_GNUTLS=%s" % yes_no("+gnutls"),
            "MFEM_USE_OPENMP=%s" % yes_no("+openmp"),
            "MFEM_USE_CONDUIT=%s" % yes_no("+conduit"),
            "MFEM_USE_CUDA=%s" % yes_no("+cuda"),
            "MFEM_USE_HIP=%s" % yes_no("+rocm"),
            "MFEM_USE_OCCA=%s" % yes_no("+occa"),
            "MFEM_USE_RAJA=%s" % yes_no("+raja"),
            "MFEM_USE_AMGX=%s" % yes_no("+amgx"),
            "MFEM_USE_CEED=%s" % yes_no("+libceed"),
            "MFEM_USE_UMPIRE=%s" % yes_no("+umpire"),
            "MFEM_USE_FMS=%s" % yes_no("+fms"),
            "MFEM_USE_GINKGO=%s" % yes_no("+ginkgo"),
            "MFEM_USE_HIOP=%s" % yes_no("+hiop"),
            "MFEM_MPIEXEC=%s" % mfem_mpiexec,
            "MFEM_MPIEXEC_NP=%s" % mfem_mpiexec_np,
            "MFEM_USE_EXCEPTIONS=%s" % yes_no("+exceptions"),
            "MFEM_USE_MUMPS=%s" % yes_no("+mumps"),
        ]
        if spec.satisfies("@4.7.0:"):
            options += ["MFEM_PRECISION=%s" % spec.variants["precision"].value]

        # Determine C++ standard to use:
        cxxstd = None
        if self.spec.satisfies("@4.0.0:"):
            cxxstd = "11"
        if self.spec.satisfies("^raja@2022.03.0:"):
            cxxstd = "14"
        if self.spec.satisfies("^umpire@2022.03.0:"):
            cxxstd = "14"
        if self.spec.satisfies("^sundials@6.4.0:"):
            cxxstd = "14"
        if self.spec.satisfies("^ginkgo"):
            cxxstd = "14"
        cxxstd_req = spec.variants["cxxstd"].value
        if cxxstd_req != "auto":
            # Constraints for valid standard level should be imposed during
            # concretization based on 'conflicts' or other directives.
            cxxstd = cxxstd_req
        cxxstd_flag = None
        if cxxstd:
            if "+cuda" in spec:
                cxxstd_flag = "-std=c++" + cxxstd
            else:
                cxxstd_flag = getattr(self.compiler, "cxx" + cxxstd + "_flag")

        cuda_arch = None if "~cuda" in spec else spec.variants["cuda_arch"].value

        cxxflags = spec.compiler_flags["cxxflags"].copy()

        if cxxflags:
            # Add opt/debug flags if they are not present in global cxx flags
            opt_flag_found = any(f in self.compiler.opt_flags for f in cxxflags)
            debug_flag_found = any(f in self.compiler.debug_flags for f in cxxflags)

            if "+debug" in spec:
                if not debug_flag_found:
                    cxxflags.append("-g")
                if not opt_flag_found:
                    cxxflags.append("-O0")
            else:
                if not opt_flag_found:
                    cxxflags.append("-O2")

            cxxflags = [(xcompiler + flag) for flag in cxxflags]
            if "+cuda" in spec:
                cxxflags += [
                    "-x=cu --expt-extended-lambda -arch=sm_%s" % cuda_arch,
                    "-ccbin %s" % (spec["mpi"].mpicxx if "+mpi" in spec else env["CXX"]),
                ]
            if cxxstd_flag:
                cxxflags.append(cxxstd_flag)
            # The cxxflags are set by the spack c++ compiler wrapper. We also
            # set CXXFLAGS explicitly, for clarity, and to properly export the
            # cxxflags in the variable MFEM_CXXFLAGS in config.mk.
            options += ["CXXFLAGS=%s" % " ".join(cxxflags)]

        elif cxxstd_flag:
            options += ["BASE_FLAGS=%s" % cxxstd_flag]

        # Treat any 'CXXFLAGS' in the environment as extra c++ flags which are
        # handled through the 'CPPFLAGS' makefile variable in MFEM. Also, unset
        # 'CXXFLAGS' from the environment to prevent it from overriding the
        # defaults.
        if "CXXFLAGS" in env:
            options += ["CPPFLAGS=%s" % env["CXXFLAGS"]]
            del env["CXXFLAGS"]

        if "~static" in spec:
            options += ["STATIC=NO"]
        if "+shared" in spec:
            options += ["SHARED=YES", "PICFLAG=%s" % (xcompiler + self.compiler.cxx_pic_flag)]

        if "+mpi" in spec:
            options += ["MPICXX=%s" % spec["mpi"].mpicxx]
            hypre = spec["hypre"]
            # The hypre package always links with 'blas' and 'lapack'.
            all_hypre_libs = hypre.libs + hypre["lapack"].libs + hypre["blas"].libs
            hypre_gpu_libs = ""
            if "+cuda" in hypre:
                hypre_gpu_libs = " -lcusparse -lcurand -lcublas"
            elif "+rocm" in hypre:
                hypre_rocm_libs = LibraryList([])
                if "^rocsparse" in hypre:
                    hypre_rocm_libs += hypre["rocsparse"].libs
                if "^rocrand" in hypre:
                    hypre_rocm_libs += hypre["rocrand"].libs
                hypre_gpu_libs = " " + ld_flags_from_library_list(hypre_rocm_libs)
            options += [
                "HYPRE_OPT=-I%s" % hypre.prefix.include,
                "HYPRE_LIB=%s%s" % (ld_flags_from_library_list(all_hypre_libs), hypre_gpu_libs),
            ]

        if "+metis" in spec:
            options += [
                "METIS_OPT=-I%s" % spec["metis"].prefix.include,
                "METIS_LIB=%s" % ld_flags_from_library_list(spec["metis"].libs),
            ]

        if "+lapack" in spec:
            lapack_blas = spec["lapack"].libs + spec["blas"].libs
            options += [
                # LAPACK_OPT is not used
                "LAPACK_LIB=%s"
                % ld_flags_from_library_list(lapack_blas)
            ]

        if "+superlu-dist" in spec:
            lapack_blas = spec["lapack"].libs + spec["blas"].libs
            options += [
                "SUPERLU_OPT=-I%s -I%s"
                % (spec["superlu-dist"].prefix.include, spec["parmetis"].prefix.include),
                "SUPERLU_LIB=%s %s"
                % (
                    ld_flags_from_dirs(
                        [spec["superlu-dist"].prefix.lib, spec["parmetis"].prefix.lib],
                        ["superlu_dist", "parmetis"],
                    ),
                    ld_flags_from_library_list(lapack_blas),
                ),
            ]

        if "+strumpack" in spec:
            strumpack = spec["strumpack"]
            sp_opt = ["-I%s" % strumpack.prefix.include]
            sp_lib = [ld_flags_from_library_list(strumpack.libs)]
            # Parts of STRUMPACK use fortran, so we need to link with the
            # fortran library and also the MPI fortran library:
            if "~shared" in strumpack:
                if os.path.basename(env["FC"]) == "gfortran":
                    gfortran = Executable(env["FC"])
                    libext = "dylib" if sys.platform == "darwin" else "so"
                    libfile = os.path.abspath(
                        gfortran("-print-file-name=libgfortran.%s" % libext, output=str).strip()
                    )
                    gfortran_lib = LibraryList(libfile)
                    sp_lib += [ld_flags_from_library_list(gfortran_lib)]
                if "+mpi" in strumpack:
                    mpi = strumpack["mpi"]
                    if ("^mpich" in strumpack) or ("^mvapich2" in strumpack):
                        sp_lib += [ld_flags_from_dirs([mpi.prefix.lib], ["mpifort"])]
                    elif "^openmpi" in strumpack:
                        sp_lib += [ld_flags_from_dirs([mpi.prefix.lib], ["mpi_mpifh"])]
                    elif "^spectrum-mpi" in strumpack:
                        sp_lib += [ld_flags_from_dirs([mpi.prefix.lib], ["mpi_ibm_mpifh"])]
            if "+openmp" in strumpack:
                # The "+openmp" in the spec means strumpack will TRY to find
                # OpenMP; if not found, we should not add any flags -- how do
                # we figure out if strumpack found OpenMP?
                if not self.spec.satisfies("%apple-clang"):
                    sp_opt += [xcompiler + self.compiler.openmp_flag]
            if "^parmetis" in strumpack:
                parmetis = strumpack["parmetis"]
                sp_opt += [parmetis.headers.cpp_flags]
                sp_lib += [ld_flags_from_library_list(parmetis.libs)]
            if "^netlib-scalapack" in strumpack:
                scalapack = strumpack["scalapack"]
                sp_opt += ["-I%s" % scalapack.prefix.include]
                sp_lib += [ld_flags_from_dirs([scalapack.prefix.lib], ["scalapack"])]
            elif "^scalapack" in strumpack:
                scalapack = strumpack["scalapack"]
                sp_opt += [scalapack.headers.cpp_flags]
                sp_lib += [ld_flags_from_library_list(scalapack.libs)]
            if "+butterflypack" in strumpack:
                bp = strumpack["butterflypack"]
                sp_opt += ["-I%s" % bp.prefix.include]
                bp_libs = find_libraries(
                    ["libdbutterflypack", "libzbutterflypack"],
                    bp.prefix,
                    shared=("+shared" in bp),
                    recursive=True,
                )
                sp_lib += [ld_flags_from_library_list(bp_libs)]
            if "+zfp" in strumpack:
                zfp = strumpack["zfp"]
                sp_opt += ["-I%s" % zfp.prefix.include]
                zfp_lib = find_libraries(
                    "libzfp", zfp.prefix, shared=("+shared" in zfp), recursive=True
                )
                sp_lib += [ld_flags_from_library_list(zfp_lib)]
            if "+cuda" in strumpack:
                # assuming also ("+cuda" in spec)
                sp_lib += ["-lcusolver", "-lcublas"]
            options += [
                "STRUMPACK_OPT=%s" % " ".join(sp_opt),
                "STRUMPACK_LIB=%s" % " ".join(sp_lib),
            ]

        if "+suite-sparse" in spec:
            ss_spec = "suite-sparse:" + self.suitesparse_components
            options += [
                "SUITESPARSE_OPT=-I%s" % spec[ss_spec].prefix.include,
                "SUITESPARSE_LIB=%s" % ld_flags_from_library_list(spec[ss_spec].libs),
            ]

        if "+sundials" in spec:
            sun_spec = "sundials:" + self.sundials_components
            options += [
                "SUNDIALS_OPT=%s" % spec[sun_spec].headers.cpp_flags,
                "SUNDIALS_LIB=%s" % ld_flags_from_library_list(spec[sun_spec].libs),
            ]

        if "+petsc" in spec:
            petsc = spec["petsc"]
            if "+shared" in petsc:
                options += [
                    "PETSC_OPT=%s" % petsc.headers.cpp_flags,
                    "PETSC_LIB=%s" % ld_flags_from_library_list(petsc.libs),
                ]
            else:
                options += ["PETSC_DIR=%s" % petsc.prefix]

        if "+slepc" in spec:
            slepc = spec["slepc"]
            options += [
                "SLEPC_OPT=%s" % slepc.headers.cpp_flags,
                "SLEPC_LIB=%s" % ld_flags_from_library_list(slepc.libs),
            ]

        if "+pumi" in spec:
            pumi_libs = [
                "pumi",
                "crv",
                "ma",
                "mds",
                "apf",
                "pcu",
                "gmi",
                "parma",
                "lion",
                "mth",
                "apf_zoltan",
                "spr",
            ]
            pumi_dep_zoltan = ""
            pumi_dep_parmetis = ""
            if "+zoltan" in spec["pumi"]:
                pumi_dep_zoltan = ld_flags_from_dirs([spec["zoltan"].prefix.lib], ["zoltan"])
                if "+parmetis" in spec["zoltan"]:
                    pumi_dep_parmetis = ld_flags_from_dirs(
                        [spec["parmetis"].prefix.lib], ["parmetis"]
                    )
            options += [
                "PUMI_OPT=-I%s" % spec["pumi"].prefix.include,
                "PUMI_LIB=%s %s %s"
                % (
                    ld_flags_from_dirs([spec["pumi"].prefix.lib], pumi_libs),
                    pumi_dep_zoltan,
                    pumi_dep_parmetis,
                ),
            ]

        if "+gslib" in spec:
            options += [
                "GSLIB_OPT=-I%s" % spec["gslib"].prefix.include,
                "GSLIB_LIB=%s" % ld_flags_from_dirs([spec["gslib"].prefix.lib], ["gs"]),
            ]

        if "+netcdf" in spec:
            lib_flags = ld_flags_from_dirs([spec["netcdf-c"].prefix.lib], ["netcdf"])
            hdf5 = spec["hdf5:hl"]
            if hdf5.satisfies("~shared"):
                hdf5_libs = hdf5.libs
                hdf5_libs += LibraryList(find_system_libraries("libdl"))
                lib_flags += " " + ld_flags_from_library_list(hdf5_libs)
            options += [
                "NETCDF_OPT=-I%s" % spec["netcdf-c"].prefix.include,
                "NETCDF_LIB=%s" % lib_flags,
            ]

        if "+zlib" in spec:
            if "@:3.3.2" in spec:
                options += ["ZLIB_DIR=%s" % spec["zlib-api"].prefix]
            else:
                options += [
                    "ZLIB_OPT=-I%s" % spec["zlib-api"].prefix.include,
                    "ZLIB_LIB=%s" % ld_flags_from_library_list(spec["zlib-api"].libs),
                ]

        if "+mpfr" in spec:
            options += [
                "MPFR_OPT=-I%s" % spec["mpfr"].prefix.include,
                "MPFR_LIB=%s" % ld_flags_from_dirs([spec["mpfr"].prefix.lib], ["mpfr"]),
            ]

        if "+gnutls" in spec:
            options += [
                "GNUTLS_OPT=-I%s" % spec["gnutls"].prefix.include,
                "GNUTLS_LIB=%s" % ld_flags_from_dirs([spec["gnutls"].prefix.lib], ["gnutls"]),
            ]

        if "+libunwind" in spec:
            libunwind = spec["unwind"]
            headers = find_headers("libunwind", libunwind.prefix.include)
            headers.add_macro("-g")
            libs = find_optional_library("libunwind", libunwind.prefix)
            # When mfem uses libunwind, it also needs "libdl".
            libs += LibraryList(find_system_libraries("libdl"))
            options += [
                "LIBUNWIND_OPT=%s" % headers.cpp_flags,
                "LIBUNWIND_LIB=%s" % ld_flags_from_library_list(libs),
            ]

        if "+openmp" in spec:
            options += ["OPENMP_OPT=%s" % (xcompiler + self.compiler.openmp_flag)]

        if "+cuda" in spec:
            options += [
                "CUDA_CXX=%s" % join_path(spec["cuda"].prefix, "bin", "nvcc"),
                "CUDA_ARCH=sm_%s" % cuda_arch,
            ]
            # Check if we are using a CUDA installation where the math libs are
            # in a separate directory:
            culibs = ["libcusparse"]
            cuda_libs = find_optional_library(culibs, spec["cuda"].prefix)
            if not cuda_libs:
                p0 = os.path.realpath(join_path(spec["cuda"].prefix, "bin", "nvcc"))
                p0 = os.path.dirname(p0)
                p1 = os.path.dirname(p0)
                while p1 != p0:
                    cuda_libs = find_optional_library(culibs, join_path(p1, "math_libs"))
                    if cuda_libs:
                        break
                    p0, p1 = p1, os.path.dirname(p1)
                if not cuda_libs:
                    raise InstallError("Required CUDA libraries not found: %s" % culibs)
                options += ["CUDA_LIB=%s" % ld_flags_from_library_list(cuda_libs)]

        if "+rocm" in spec:
            amdgpu_target = ",".join(spec.variants["amdgpu_target"].value)
            options += ["HIP_CXX=%s" % spec["hip"].hipcc, "HIP_ARCH=%s" % amdgpu_target]
            hip_headers = HeaderList([])
            hip_libs = LibraryList([])
            # To use a C++ compiler that supports -xhip flag one can use
            # something like this:
            #   options += [
            #       "HIP_CXX=%s" % (spec["mpi"].mpicxx if "+mpi" in spec else spack_cxx),
            #       "HIP_FLAGS=-xhip --offload-arch=%s" % amdgpu_target,
            #   ]
            #   hip_libs += find_libraries("libamdhip64", spec["hip"].prefix.lib)
            if "^hipsparse" in spec:  # hipsparse is needed @4.4.0:+rocm
                hipsparse = spec["hipsparse"]
                hip_headers += hipsparse.headers
                hip_libs += hipsparse.libs
                # Note: MFEM's defaults.mk wants to find librocsparse.* in
                # $(HIP_DIR)/lib, so we set HIP_DIR to be $ROCM_PATH when using
                # external HIP, or the prefix of rocsparse (which is a
                # dependency of hipsparse) when using Spack-built HIP.
                if spec["hip"].external:
                    options += ["HIP_DIR=%s" % env["ROCM_PATH"]]
                else:
                    options += ["HIP_DIR=%s" % hipsparse["rocsparse"].prefix]
            if "^rocthrust" in spec and not spec["hip"].external:
                # petsc+rocm needs the rocthrust header path
                hip_headers += spec["rocthrust"].headers
            if "^rocprim" in spec and not spec["hip"].external:
                # rocthrust [via petsc+rocm] has a dependency on rocprim
                hip_headers += spec["rocprim"].headers
            if "^hipblas" in spec and not spec["hip"].external:
                # superlu-dist+rocm needs the hipblas header path
                hip_headers += spec["hipblas"].headers
            if "%cce" in spec:
                # We assume the proper Cray CCE module (cce) is loaded:
                proc = str(spec.target.family)
                craylibs_var = "CRAYLIBS_" + proc.upper()
                craylibs_path = env.get(craylibs_var, None)
                if not craylibs_path:
                    raise InstallError(
                        f"The environment variable {craylibs_var} is not defined.\n"
                        "\tMake sure the 'cce' module is in the compiler spec."
                    )
                craylibs = [
                    "libmodules",
                    "libfi",
                    "libcraymath",
                    "libf",
                    "libu",
                    "libcsup",
                    "libpgas-shmem",
                ]
                hip_libs += find_libraries(craylibs, craylibs_path)
                craylibs_path2 = join_path(craylibs_path, "../../../cce-clang", proc, "lib")
                hip_libs += find_libraries("libunwind", craylibs_path2)

            if hip_headers:
                options += ["HIP_OPT=%s" % hip_headers.cpp_flags]
            if hip_libs:
                options += ["HIP_LIB=%s" % ld_flags_from_library_list(hip_libs)]

        if "+occa" in spec:
            options += [
                "OCCA_OPT=-I%s" % spec["occa"].prefix.include,
                "OCCA_LIB=%s" % ld_flags_from_dirs([spec["occa"].prefix.lib], ["occa"]),
            ]

        if "+raja" in spec:
            raja = spec["raja"]
            raja_opt = "-I%s" % raja.prefix.include
            raja_lib = find_libraries(
                "libRAJA", raja.prefix, shared=("+shared" in raja), recursive=True
            )
            if raja.satisfies("^camp"):
                camp = raja["camp"]
                raja_opt += " -I%s" % camp.prefix.include
                raja_lib += find_optional_library("libcamp", camp.prefix)
            options += [
                "RAJA_OPT=%s" % raja_opt,
                "RAJA_LIB=%s" % ld_flags_from_library_list(raja_lib),
            ]

        if "+amgx" in spec:
            amgx = spec["amgx"]
            if "+shared" in amgx:
                options += [
                    "AMGX_OPT=-I%s" % amgx.prefix.include,
                    "AMGX_LIB=%s" % ld_flags_from_library_list(amgx.libs),
                ]
            else:
                options += ["AMGX_DIR=%s" % amgx.prefix]

        if "+libceed" in spec:
            options += [
                "CEED_OPT=-I%s" % spec["libceed"].prefix.include,
                "CEED_LIB=%s" % ld_flags_from_dirs([spec["libceed"].prefix.lib], ["ceed"]),
            ]

        if "+umpire" in spec:
            umpire = spec["umpire"]
            umpire_opts = umpire.headers
            umpire_libs = umpire.libs
            if "^camp" in umpire:
                umpire_opts += umpire["camp"].headers
            if "^fmt" in umpire:
                umpire_opts += umpire["fmt"].headers
                umpire_libs += umpire["fmt"].libs
            options += [
                "UMPIRE_OPT=%s" % umpire_opts.cpp_flags,
                "UMPIRE_LIB=%s" % ld_flags_from_library_list(umpire_libs),
            ]

        timer_ids = {"std": "0", "posix": "2", "mac": "4", "mpi": "6"}
        timer = spec.variants["timer"].value
        if timer != "auto":
            options += ["MFEM_TIMER_TYPE=%s" % timer_ids[timer]]

        if "+conduit" in spec:
            conduit = spec["conduit"]
            headers = HeaderList(find(conduit.prefix.include, "conduit.hpp", recursive=True))
            conduit_libs = ["libconduit", "libconduit_relay", "libconduit_blueprint"]
            libs = find_libraries(conduit_libs, conduit.prefix.lib, shared=("+shared" in conduit))
            libs += LibraryList(find_system_libraries("libdl"))
            if "+hdf5" in conduit:
                hdf5 = conduit["hdf5"]
                headers += find_headers("hdf5", hdf5.prefix.include)
                libs += hdf5.libs

            ##################
            # cyrush note:
            ##################
            # spack's HeaderList is applying too much magic, undermining us:
            #
            #  It applies a regex to strip back to the last "include" dir
            #  in the path. In our case we need to pass the following
            #  as part of the CONDUIT_OPT flags:
            #
            #    -I<install_path>/include/conduit
            #
            #  I tried several ways to present this path to the HeaderList,
            #  but the regex always kills the trailing conduit dir
            #  breaking build.
            #
            #  To resolve the issue, we simply join our own string with
            #  the headers results (which are important b/c they handle
            #  hdf5 paths when enabled).
            ##################

            # construct proper include path
            conduit_include_path = conduit.prefix.include.conduit
            # add this path to the found flags
            conduit_opt_flags = "-I{0} {1}".format(conduit_include_path, headers.cpp_flags)

            options += [
                "CONDUIT_OPT=%s" % conduit_opt_flags,
                "CONDUIT_LIB=%s" % ld_flags_from_library_list(libs),
            ]

        if "+fms" in spec:
            libfms = spec["libfms"]
            options += [
                "FMS_OPT=%s" % libfms.headers.cpp_flags,
                "FMS_LIB=%s" % ld_flags_from_library_list(libfms.libs),
            ]

        if "+ginkgo" in spec:
            ginkgo = spec["ginkgo"]
            options += [
                "GINKGO_DIR=%s" % ginkgo.prefix,
                "GINKGO_BUILD_TYPE=%s" % ginkgo.variants["build_type"].value,
            ]

        if "+hiop" in spec:
            hiop = spec["hiop"]
            hiop_hdrs = hiop.headers
            hiop_libs = hiop.libs
            hiop_hdrs += spec["lapack"].headers + spec["blas"].headers
            hiop_libs += spec["lapack"].libs + spec["blas"].libs
            hiop_opt_libs = ["magma", "umpire", "hipblas", "hiprand"]
            for opt_lib in hiop_opt_libs:
                if "^" + opt_lib in hiop:
                    hiop_hdrs += hiop[opt_lib].headers
                    hiop_libs += hiop[opt_lib].libs
            # raja's libs property does not work
            if "^raja" in hiop:
                raja = hiop["raja"]
                hiop_hdrs += raja.headers
                hiop_libs += find_libraries(
                    "libRAJA", raja.prefix, shared=("+shared" in raja), recursive=True
                )
                if raja.satisfies("^camp"):
                    camp = raja["camp"]
                    hiop_hdrs += camp.headers
                    hiop_libs += find_optional_library("libcamp", camp.prefix)
            if hiop.satisfies("@0.6:+cuda"):
                hiop_libs += LibraryList(["cublas", "curand"])
            options += [
                "HIOP_OPT=%s" % hiop_hdrs.cpp_flags,
                "HIOP_LIB=%s" % ld_flags_from_library_list(hiop_libs),
            ]

        if "+mumps" in spec:
            mumps = spec["mumps"]
            mumps_opt = ["-I%s" % mumps.prefix.include]
            if "+openmp" in mumps:
                if not self.spec.satisfies("%apple-clang"):
                    mumps_opt += [xcompiler + self.compiler.openmp_flag]
            options += [
                "MUMPS_OPT=%s" % " ".join(mumps_opt),
                "MUMPS_LIB=%s" % ld_flags_from_library_list(mumps.libs),
            ]

        return options

    def configure(self, spec, prefix):
        options = self.get_make_config_options(spec, prefix)
        make("config", *options, parallel=False)
        make("info", parallel=False)

    def build(self, spec, prefix):
        make("lib")

    @run_after("build")
    def check_or_test(self):
        # Running 'make check' or 'make test' may fail if MFEM_MPIEXEC or
        # MFEM_MPIEXEC_NP are not set appropriately.
        if not self.run_tests:
            # check we can build ex1 (~mpi) or ex1p (+mpi).
            make("-C", "examples", "ex1p" if ("+mpi" in self.spec) else "ex1", parallel=False)
            # make('check', parallel=False)
        else:
            make("all")
            make("test", parallel=False)

    def install(self, spec, prefix):
        make("install", parallel=False)

        # TODO: The way the examples and miniapps are being installed is not
        # perfect. For example, the makefiles do not work.

        install_em = ("+examples" in spec) or ("+miniapps" in spec)
        if install_em and ("+shared" in spec):
            make("examples/clean", "miniapps/clean")
            # This is a hack to get the examples and miniapps to link with the
            # installed shared mfem library:
            with working_dir("config"):
                os.rename("config.mk", "config.mk.orig")
                copy(str(self.config_mk), "config.mk")
                # Add '/mfem' to MFEM_INC_DIR for miniapps that include directly
                # headers like "general/forall.hpp":
                filter_file("(MFEM_INC_DIR.*)$", "\\1/mfem", "config.mk")
                shutil.copystat("config.mk.orig", "config.mk")
                # TODO: miniapps linking to libmfem-common.* will not work.

        prefix_share = join_path(prefix, "share", "mfem")

        if "+examples" in spec:
            make("examples")
            install_tree("examples", join_path(prefix_share, "examples"))

        if "+miniapps" in spec:
            make("miniapps")
            install_tree("miniapps", join_path(prefix_share, "miniapps"))

        if install_em:
            install_tree("data", join_path(prefix_share, "data"))

    examples_src_dir = "examples"
    examples_data_dir = "data"

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        # Clean the 'examples' directory -- at least one example is always built
        # and we do not want to cache executables.
        make("examples/clean", parallel=False)
        cache_extra_test_sources(self, [self.examples_src_dir, self.examples_data_dir])

    def test_ex10(self):
        """build and run ex10(p)"""
        # MFEM has many examples to serve as a suitable smoke check. ex10
        # was chosen arbitrarily among the examples that work both with
        # MPI and without it
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)

        mesh = join_path("..", self.examples_data_dir, "beam-quad.mesh")
        test_exe = "ex10p" if ("+mpi" in self.spec) else "ex10"

        with working_dir(test_dir):
            make = which("make")
            make(f"CONFIG_MK={self.config_mk}", test_exe, "parallel=False")

            ex10 = which(test_exe)
            ex10("--mesh", mesh)

    # this patch is only needed for mfem 4.1, where a few
    # released files include byte order marks
    @when("@4.1.0")
    def patch(self):
        # Remove the byte order mark since it messes with some compilers
        files_with_bom = [
            "fem/gslib.hpp",
            "fem/gslib.cpp",
            "linalg/hiop.hpp",
            "miniapps/gslib/field-diff.cpp",
            "miniapps/gslib/findpts.cpp",
            "miniapps/gslib/pfindpts.cpp",
        ]
        bom = "\xef\xbb\xbf" if sys.version_info < (3,) else "\ufeff"
        for f in files_with_bom:
            filter_file(bom, "", f)

    @property
    def suitesparse_components(self):
        """Return the SuiteSparse components needed by MFEM."""
        ss_comps = "umfpack,cholmod,colamd,amd,camd,ccolamd,suitesparseconfig"
        if self.spec.satisfies("@3.2:"):
            ss_comps = "klu,btf," + ss_comps
        return ss_comps

    @property
    def sundials_components(self):
        """Return the SUNDIALS components needed by MFEM."""
        spec = self.spec
        sun_comps = "arkode,cvodes,nvecserial,kinsol"
        if "+mpi" in spec:
            if spec.satisfies("@4.2:"):
                sun_comps += ",nvecparallel,nvecmpiplusx"
            else:
                sun_comps += ",nvecparhyp,nvecparallel"
        if "+cuda" in spec and "+cuda" in spec["sundials"]:
            sun_comps += ",nveccuda"
        if "+rocm" in spec and "+rocm" in spec["sundials"]:
            sun_comps += ",nvechip"
        return sun_comps

    @property
    def headers(self):
        """Export the main mfem header, mfem.hpp."""
        hdrs = HeaderList(find(self.prefix.include, "mfem.hpp", recursive=False))
        return hdrs or None

    @property
    def libs(self):
        """Export the mfem library file."""
        libs = find_libraries(
            "libmfem", root=self.prefix.lib, shared=("+shared" in self.spec), recursive=False
        )
        return libs or None

    @property
    def config_mk(self):
        """Export the location of the config.mk file.
        This property can be accessed using spec["mfem"].package.config_mk
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
            f = join_path(d, "config.mk")
            if os.access(f, os.R_OK):
                return FileList(f)
        return FileList(find(self.prefix, "config.mk", recursive=True))

    @property
    def test_mk(self):
        """Export the location of the test.mk file.
        This property can be accessed using spec["mfem"].package.test_mk.
        In version 3.3.2 and newer, the location of test.mk is also defined
        inside config.mk, variable MFEM_TEST_MK.
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
            f = join_path(d, "test.mk")
            if os.access(f, os.R_OK):
                return FileList(f)
        return FileList(find(self.prefix, "test.mk", recursive=True))

    # See also find_system_libraries in lib/spack/llnl/util/filesystem.py
    # where the similar list of paths is used.
    sys_lib_paths = [
        "/lib64",
        "/lib",
        "/usr/lib64",
        "/usr/lib",
        "/usr/local/lib64",
        "/usr/local/lib",
        "/usr/lib/x86_64-linux-gnu",
    ]

    def is_sys_lib_path(self, dir):
        return dir in self.sys_lib_paths

    @property
    def xlinker(self):
        return "-Wl," if "~cuda" in self.spec else "-Xlinker="

    # Similar to spec[pkg].libs.ld_flags but prepends rpath flags too.
    # Also does not add system library paths as defined by 'sys_lib_paths'
    # above -- this is done to avoid issues like this:
    # https://github.com/mfem/mfem/issues/1088.
    def ld_flags_from_library_list(self, libs_list):
        flags = [
            "%s-rpath,%s" % (self.xlinker, dir)
            for dir in libs_list.directories
            if not self.is_sys_lib_path(dir)
        ]
        flags += ["-L%s" % dir for dir in libs_list.directories if not self.is_sys_lib_path(dir)]
        flags += [libs_list.link_flags]
        return " ".join(flags)

    def ld_flags_from_dirs(self, pkg_dirs_list, pkg_libs_list):
        flags = [
            "%s-rpath,%s" % (self.xlinker, dir)
            for dir in pkg_dirs_list
            if not self.is_sys_lib_path(dir)
        ]
        flags += ["-L%s" % dir for dir in pkg_dirs_list if not self.is_sys_lib_path(dir)]
        flags += ["-l%s" % lib for lib in pkg_libs_list]
        return " ".join(flags)
