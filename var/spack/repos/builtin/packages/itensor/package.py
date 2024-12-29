# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Itensor(MakefilePackage):
    """ITensor -Intelligent Tensor- is a library for
    implementing tensor network calculations."""

    homepage = "https://itensor.org/index.html"
    url = "https://github.com/ITensor/ITensor/archive/v3.1.6.tar.gz"

    license("Apache-2.0")

    version("3.2.0", sha256="cb2b041514857639cf9e7c326bfeef152d45228b26243dbb9d1a0f82189f1014")
    version("3.1.11", sha256="bc6c48d34c4d4281d15116d7d95d7e6e2b6878b9a60ce33372b8967a96826e95")
    version("3.1.10", sha256="68c149e23a1ab936ef8175ea11fedc0ec64031c3686ede93c3a5ab0c893774f6")
    version("3.1.9", sha256="4dd71b251b63fb7775ef854212df6f1d5d3ac4d6d1905dc03b1e6d2a0a620a17")
    version("3.1.8", sha256="9dae666baa6f9317fa1ca96c6229c6e62bbbb690e5ee7345f3781948903839f4")
    version("3.1.7", sha256="ff3fb3121408fc4be4aa91b16f0b0e6d2fd0129b1c9cd9b075b5197ab9b3d37f")
    version("3.1.6", sha256="1c42cd39c45124063d9812b851b4d99735caff7ac2da971b4287c2018d4cf32a")
    version("3.1.5", sha256="a0661efdda3bfc4fab1796243d4b438b0f17adce08b6bb21a2aaae9766b6a1ec")
    version("3.1.4", sha256="bdcfa786f5165b6f5d1a40a80e7ecca2e59e2ee7050fd60f42ef4a4a55a793c5")
    version("3.1.3", sha256="ff6b04f9c642c6795acd3485f44619282a2dde7a49a4e0dee89b47b69dc3853e")
    version("3.1.2", sha256="3e0f032c211e11be1b5a4adf4a581698a949d03b35c0e9b2e3d9f4bab6dd7967")
    version("3.1.1", sha256="3c12d288e50522b5bd152f956a48ec187486cfeb4ccb1ea9a05d3f0bf3bf8059")
    version("3.1.0", sha256="b887cb9c7fc06f60d9d6834380b643adea8d165d574ab1859883f399725b9db9")
    version("3.0.1", sha256="5e2ac3a5b62fb3e34f1e520e6da911b56659507fb4143118d4a602a5866bc912")
    version("3.0.0", sha256="1d249a3a6442188a9f7829b32238c1025457c2930566d134a785994b1f7c54a9")
    version("2.1.1", sha256="b91a67af66ed0fa7678494f3895b5d5ae7f1dc1026540689f9625f515cb7791c")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=False, description="Enable OpenMP support.")
    variant("hdf5", default=False, description="Build rockstar with HDF5 support.")
    variant("shared", default=False, description="Also build dynamic libraries.")

    depends_on("lapack")
    depends_on("hdf5@:1.10+hl", when="+hdf5")

    conflicts("^openblas threads=none", when="+openmp")
    conflicts("^openblas threads=pthreads", when="+openmp")

    def getcopts(self, spec):
        copts = []
        copts.append(self.compiler.cxx17_flag)
        copts.append(self.compiler.cc_pic_flag)

        if spec.satisfies("%gcc"):
            if not spec.satisfies("arch=aarch64:"):
                copts.append("-m64")
            copts.append("-fconcepts")
        if spec.satisfies("%clang") or spec.satisfies("%fj"):
            copts.append("-Wno-gcc-compat")
        return " " + " ".join(copts)

    def edit(self, spec, prefix):
        # 0.copy options.mk
        mf = "options.mk"
        copy("options.mk.sample", mf)

        # 1.CCCOM
        ccopts = f"CCCOM={spack_cxx}{self.getcopts(spec)}"
        filter_file(r"^CCCOM.+", ccopts, mf)

        # 2.BLAS/LAPACK
        # Set default values
        vpla = "PLATFORM=lapack"
        vlib = "BLAS_LAPACK_LIBFLAGS="
        vlib += spec["lapack"].libs.ld_flags
        vinc = "BLAS_LAPACK_INCLUDEFLAGS=-I"
        vinc += spec["lapack"].prefix.include
        ltype = spec["lapack"].name
        # lapack specific
        if ltype == "openblas":
            vpla = "PLATFORM=openblas"
            if spec.satisfies("%gcc"):
                vinc += " -fpermissive"
            vinc += " -DHAVE_LAPACK_CONFIG_H"
            vinc += " -DLAPACK_COMPLEX_STRUCTURE"
            filter_file("#PLATFORM=lapack", vinc, mf, string=True)
        elif ltype == "intel-mkl":
            vpla = "PLATFORM=mkl"
            filter_file("#PLATFORM=lapack", vinc, mf, string=True)

        filter_file(r"^PLATFORM.+", vpla, mf)
        filter_file(r"^BLAS_LAPACK_LIBFLAGS.+", vlib, mf)

        # 3.HDF5
        if spec.satisfies("+hdf5"):
            hdf5p = f"HDF5_PREFIX={spec['hdf5'].prefix.lib}"
            filter_file("^#HDF5.+", hdf5p, mf)

        # 4.openmp
        if spec.satisfies("+openmp"):
            filter_file("#ITENSOR_USE_OMP", "ITENSOR_USE_OMP", mf)
            filter_file("-fopenmp", self.compiler.openmp_flag, mf)

        # 5.prefix
        filter_file(r"^PREFIX.+", f"PREFIX={os.getcwd()}", mf)

        # 5.shared
        if spec.satisfies("+shared"):
            filter_file("ITENSOR_MAKE_DYLIB=0", "ITENSOR_MAKE_DYLIB=1", mf)

    def install(self, spec, prefix):
        # 0.backup options.mk
        mf = "options.mk"
        copy(mf, "options.mk.build")

        # 1.CCCOM
        ccopts = f"CCCOM={self.compiler.cxx}"
        ccopts += " " + " ".join(spec.compiler_flags["cxxflags"])
        if spec.satisfies("%fj"):
            ccopts += " " + env["FCC_ENV"]
        ccopts += self.getcopts(spec)
        filter_file(r"^CCCOM.+", ccopts, mf)

        # 2.LDFLAGS
        vlib = "BLAS_LAPACK_LIBFLAGS={0} ".format(
            " ".join(spec.compiler_flags["ldflags"] + spec.compiler_flags["ldlibs"])
        )
        filter_file(r"^BLAS_LAPACK_LIBFLAGS=", vlib, mf)

        # 3.prefix
        filter_file(r"^PREFIX.+", f"PREFIX={prefix}", mf)

        # tutorial/project_template/Makefile
        mf2 = join_path("tutorial", "project_template", "Makefile")
        filter_file(r"^LIBRARY_DIR.+", f"LIBRARY_DIR={prefix}", mf2)

        install_tree(".", prefix)
