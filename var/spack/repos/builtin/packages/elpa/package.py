# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

#
# Please note that you can open issues on the github page of ELPA:
# https://github.com/marekandreas/elpa/issues
#


class Elpa(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Eigenvalue solvers for Petaflop-Applications (ELPA)"""

    homepage = "https://elpa.mpcdf.mpg.de/"
    url = "https://elpa.mpcdf.mpg.de/software/tarball-archive/Releases/2015.11.001/elpa-2015.11.001.tar.gz"
    git = "https://gitlab.mpcdf.mpg.de/elpa/elpa.git"

    license("LGPL-3.0-only")

    version("master", branch="master")

    version(
        "2024.03.001", sha256="41c6cbf56d2dac26443faaba8a77307d261bf511682a64b96e24def77c813622"
    )
    version(
        "2023.11.001-patched",
        sha256="62ee109afc06539507f459c08b958dc4db65b757dbd77f927678c77f7687415e",
        url="https://elpa.mpcdf.mpg.de/software/tarball-archive/Releases/2023.11.001/elpa-2023.11.001-patched.tar.gz",
    )
    version(
        "2023.05.001", sha256="ec64be5d6522810d601a3b8e6a31720e3c3eb4af33a434d8a64570d76e6462b6"
    )
    version(
        "2022.11.001", sha256="75db3ac146f9a6a1598e3418ddcab2be2f40a30ef9ec4c00a3b5d3808c99c430"
    )
    version(
        "2021.11.001", sha256="fb361da6c59946661b73e51538d419028f763d7cb9dacf9d8cd5c9cd3fb7802f"
    )
    version(
        "2021.05.002_bugfix",
        sha256="deabc48de5b9e4b2f073d749d335c8f354a7ce4245b643a23b7951cd6c90224b",
    )
    version(
        "2021.05.001", sha256="a4f1a4e3964f2473a5f8177f2091a9da5c6b5ef9280b8272dfefcbc3aad44d41"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Activates OpenMP support")
    variant("mpi", default=True, description="Activates MPI support")

    with when("@2021.11.001:"):
        variant(
            "autotune", default=False, description="Enables autotuning for matrix restribution"
        )
        variant(
            "gpu_streams", default=True, when="+cuda", description="Activates GPU streams support"
        )

    patch("fujitsu.patch", when="%fj")

    depends_on("autoconf@2.71:", type="build", when="@master")
    depends_on("automake", type="build", when="@master")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+mpi")
    depends_on("rocblas", when="+rocm")
    depends_on("libtool", type="build")
    depends_on("python@3:", type="build")
    depends_on("scalapack", when="+autotune")

    # Force openmp propagation on some providers of blas/lapack, as adviced by docs
    # https://gitlab.mpcdf.mpg.de/elpa/elpa/-/blob/master/documentation/PERFORMANCE_TUNING.md?ref_type=heads#builds-with-openmp-enabled
    with when("+openmp"):
        requires("^openblas threads=openmp", when="^[virtuals=blas,lapack] openblas")
        requires("^intel-mkl threads=openmp", when="^[virtuals=blas,lapack] intel-mkl")
        requires(
            "^intel-oneapi-mkl threads=openmp", when="^[virtuals=blas,lapack] intel-oneapi-mkl"
        )
        requires(
            "^intel-parallel-studio threads=openmp",
            when="^[virtuals=blas,lapack] intel-parallel-studio",
        )

    # fails to build due to broken type-bound procedures in OMP parallel regions
    conflicts(
        "+openmp",
        when="@2021.05.001: %gcc@:7",
        msg="ELPA-2021.05.001+ requires GCC-8+ for OpenMP support",
    )
    conflicts("+mpi", when="+rocm", msg="ROCm support and MPI are not yet compatible")
    conflicts(
        "+gpu_streams",
        when="@:2023.11.001-patched +openmp",
        msg="GPU streams currently not supported in combination with OpenMP",
    )

    def url_for_version(self, version):
        return "https://elpa.mpcdf.mpg.de/software/tarball-archive/Releases/{0}/elpa-{0}.tar.gz".format(
            str(version)
        )

    # override default implementation which returns static lib
    @property
    def libs(self):
        libname = "libelpa_openmp" if "+openmp" in self.spec else "libelpa"
        return find_libraries(libname, root=self.prefix, shared=True, recursive=True)

    @property
    def headers(self):
        suffix = "_openmp" if self.spec.satisfies("+openmp") else ""

        # upstream sometimes adds tarball suffixes not part of the internal version
        elpa_version = str(self.spec.version)
        for vsuffix in ("_bugfix", "-patched"):
            if elpa_version.endswith(vsuffix):  # implementation of py3.9 removesuffix
                elpa_version = elpa_version[: -len(vsuffix)]

        incdir = os.path.join(
            self.spec.prefix.include,
            "elpa{suffix}-{version}".format(suffix=suffix, version=elpa_version),
        )

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    build_directory = "spack-build"
    parallel = False

    def configure_args(self):
        spec = self.spec
        options = []

        options += self.with_or_without("mpi")

        # New options use the "-kernels" suffix
        kernels = "-kernels" if spec.satisfies("@2023.11:") else ""

        # TODO: --disable-sse-assembly, --enable-sparc64, --enable-neon-arch64
        # Don't include vsx; as of 2022.05 it fails (reported upstream).
        # Altivec SSE intrinsics are used anyway.
        simd_features = ["sse", "avx", "avx2", "avx512", "sve128", "sve256", "sve512"]

        for feature in simd_features:
            msg = "--enable-{0}" if feature in spec.target else "--disable-{0}"
            options.append(msg.format(feature + kernels))

        if spec.target.family != "x86_64":
            options.append("--disable-sse-assembly")

        if spec.satisfies("%aocc") or spec.satisfies("%fj"):
            options.append("--disable-shared")
            options.append("--enable-static")

        # If no features are found, enable the generic ones
        if not any(f in spec.target for f in simd_features):
            options.append("--enable-generic" + kernels)

        if self.compiler.name == "gcc":
            options.extend(["CFLAGS=-O3", "FCFLAGS=-O3 -ffree-line-length-none"])

        if spec.satisfies("%aocc"):
            options.extend(["FCFLAGS=-O3", "CFLAGS=-O3"])

        if spec.satisfies("%fj"):
            options.append("--disable-Fortran2008-features")
            options.append("--enable-FUGAKU")
            if spec.satisfies("+openmp"):
                options.extend(["FCFLAGS=-Kparallel"])

        cuda_flag = "nvidia-gpu"
        if spec.satisfies("+cuda"):
            prefix = spec["cuda"].prefix
            # Can't yet be changed to the new option --enable-nvidia-gpu-kernels
            # https://github.com/marekandreas/elpa/issues/55
            options.append(f"--enable-{cuda_flag}")
            options.append("--with-cuda-path={0}".format(prefix))
            options.append("--with-cuda-sdk-path={0}".format(prefix))

            if spec.satisfies("+gpu_streams"):
                options.append("--enable-gpu-streams=nvidia")

            cuda_arch = spec.variants["cuda_arch"].value[0]

            if cuda_arch != "none":
                options.append(
                    "--with-{0}-compute-capability=sm_{1}".format(cuda_flag.upper(), cuda_arch)
                )
        else:
            options.append(f"--disable-{cuda_flag}" + kernels)

        if spec.satisfies("+rocm"):
            # Can't yet be changed to the new option --enable-amd-gpu-kernels
            # https://github.com/marekandreas/elpa/issues/55
            options.append("--enable-amd-gpu")
            options.append("CXX={0}".format(self.spec["hip"].hipcc))

            if spec.satisfies("+gpu_streams"):
                options.append("--enable-gpu-streams=amd")

        elif self.spec.satisfies("@2021.05.001:"):
            options.append("--disable-amd-gpu" + kernels)

        options += self.enable_or_disable("openmp")

        # Additional linker search paths and link libs
        ldflags = [spec["blas"].libs.search_flags, spec["lapack"].libs.search_flags, "-lstdc++"]
        libs = [spec["lapack"].libs.link_flags, spec["blas"].libs.link_flags]

        options += [f'LDFLAGS={" ".join(ldflags)}', f'LIBS={" ".join(libs)}']

        if self.spec.satisfies("+mpi"):
            options += [
                "CC={0}".format(spec["mpi"].mpicc),
                "CXX={0}".format(spec["mpi"].mpicxx),
                "FC={0}".format(spec["mpi"].mpifc),
                "SCALAPACK_LDFLAGS={0}".format(spec["scalapack"].libs.joined()),
            ]

        if self.spec.satisfies("+autotune"):
            options.append("--enable-autotune-redistribute-matrix")
            # --enable-autotune-redistribute-matrix requires --enable-scalapack-tests as well
            options.append("--enable-scalapack-tests")

        options.append("--disable-silent-rules")
        options.append("--without-threading-support-check-during-build")

        return options
