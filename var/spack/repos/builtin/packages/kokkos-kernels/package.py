# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class KokkosKernels(CMakePackage, CudaPackage):
    """Kokkos Kernels provides math kernels, often BLAS or LAPACK
    for small matrices, that can be used in larger Kokkos parallel routines"""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    git = "https://github.com/kokkos/kokkos-kernels.git"
    url = "https://github.com/kokkos/kokkos-kernels/archive/4.0.00.tar.gz"

    tags = ["e4s"]

    test_requires_compiler = True

    maintainers("lucbv", "srajama1", "brian-kelley")

    license("Apache-2.0 WITH LLVM-exception")

    # generate checksum for each release tarball with the following command
    # openssl sha256 kokkos-kernels-x.y.z.tar.gz
    version("develop", branch="develop")
    version("master", branch="master")
    version("4.4.01", sha256="9f741449f5ace5a7d8a5a81194ff2108e5525d16f08fcd9bb6c9bb4853d7720d")
    version("4.4.00", sha256="6559871c091eb5bcff53bae5a0f04f2298971d1aa1b2c135bd5a2dae3f9376a2")
    version("4.3.01", sha256="749553a6ea715ba1e56fa0b13b42866bb9880dba7a94e343eadf40d08c68fab8")
    version("4.3.00", sha256="03c3226ee97dbca4fa56fe69bc4eefa0673e23c37f2741943d9362424a63950e")
    version("4.2.01", sha256="058052b3a40f5d4e447b7ded5c480f1b0d4aa78373b0bc7e43804d0447c34ca8")
    version("4.2.00", sha256="c65df9a101dbbef2d8fd43c60c9ea85f2046bb3535fa1ad16e7c661ddd60401e")
    version("4.1.00", sha256="d6a4108444ea226e43bf6a9c0dfc557f223a72b1142bf81aa78dd60e16ac2d56")
    version("4.0.01", sha256="3f493fcb0244b26858ceb911be64092fbf7785616ad62c81abde0ea1ce86688a")
    version("4.0.00", sha256="750079d0be1282d18ecd280e130ca303044ac399f1e5864488284b92f5ce0a86")
    version("3.7.01", sha256="b2060f5894bdaf7f7d4793b90444fac260460cfa80595afcbcb955518864b446")
    version("3.7.00", sha256="51bc6db3995392065656848e2b152cfd1c3a95a951ab18a3934278113d59f32b")
    version("3.6.01", sha256="f000b156c8c0b80e85d38587907c11d9479aaf362408b812effeda5e22b24d0d")
    version("3.6.00", sha256="2753643fd643b9eed9f7d370e0ff5fa957211d08a91aa75398e31cbc9e5eb0a5")
    version("3.5.00", sha256="a03a41a047d95f9f07cd1e1d30692afdb75b5c705ef524e19c1d02fe60ccf8d1")
    version("3.4.01", sha256="f504aa4afbffb58fa7c4430d0fdb8fd5690a268823fa15eb0b7d58dab9d351e6")
    version("3.4.00", sha256="07ba11869e686cb0d47272d1ef494ccfbcdef3f93ff1c8b64ab9e136a53a227a")
    version("3.3.01", sha256="0f21fe6b5a8b6ae7738290e293aa990719aefe88b32f84617436bfd6074a8f77")
    version("3.3.00", sha256="8d7f78815301afb90ddba7914dce5b718cea792ac0c7350d2f8d00bd2ef1cece")
    version("3.2.01", sha256="c486e5cac19e354a517498c362838619435734d64b44f44ce909b0531c21d95c")
    version("3.2.00", sha256="8ac20ee28ae7813ce1bda461918800ad57fdbac2af86ef5d1ba74e83e10956de")
    version("3.1.00", sha256="27fea241ae92f41bd5b070b1a590ba3a56a06aca750207a98bea2f64a4a40c89")
    version("3.0.00", sha256="e4b832aed3f8e785de24298f312af71217a26067aea2de51531e8c1e597ef0e6")

    depends_on("cxx", type="build")  # generated

    depends_on("kokkos")
    depends_on("kokkos@master", when="@master")
    depends_on("kokkos@develop", when="@develop")
    depends_on("kokkos@4.4.01", when="@4.4.01")
    depends_on("kokkos@4.4.00", when="@4.4.00")
    depends_on("kokkos@4.3.01", when="@4.3.01")
    depends_on("kokkos@4.3.00", when="@4.3.00")
    depends_on("kokkos@4.2.01", when="@4.2.01")
    depends_on("kokkos@4.2.00", when="@4.2.00")
    depends_on("kokkos@4.1.00", when="@4.1.00")
    depends_on("kokkos@4.0.01", when="@4.0.01")
    depends_on("kokkos@4.0.00", when="@4.0.00")
    depends_on("kokkos@3.7.01", when="@3.7.01")
    depends_on("kokkos@3.7.00", when="@3.7.00")
    depends_on("kokkos@3.6.01", when="@3.6.01")
    depends_on("kokkos@3.6.00", when="@3.6.00")
    depends_on("kokkos@3.5.00", when="@3.5.00")
    depends_on("kokkos@3.4.01", when="@3.4.01")
    depends_on("kokkos@3.4.00", when="@3.4.00")
    depends_on("kokkos@3.3.01", when="@3.3.01")
    depends_on("kokkos@3.3.00", when="@3.3.00")
    depends_on("kokkos@3.2.01", when="@3.2.01")
    depends_on("kokkos@3.2.00", when="@3.2.00")
    depends_on("kokkos@3.1.00", when="@3.1.00")
    depends_on("kokkos@3.0.00", when="@3.0.00")
    depends_on("cmake@3.16:", type="build")

    backends = {
        "serial": (False, "enable Serial backend (default)"),
        "cuda": (False, "enable Cuda backend"),
        "openmp": (False, "enable OpenMP backend"),
        "threads": (False, "enable C++ threads backend"),
    }

    for backend in backends:
        deflt_bool, descr = backends[backend]
        variant(backend.lower(), default=deflt_bool, description=descr)
        depends_on("kokkos+%s" % backend.lower(), when="+%s" % backend.lower())

    space_etis = {
        "execspace_cuda": (
            "auto",
            "Whether to pre instantiate kernels for the execution space Kokkos::Cuda",
            "cuda",
        ),
        "execspace_openmp": (
            "auto",
            "Whether to pre instantiate kernels for the execution space "
            "Kokkos::Experimental::OpenMPTarget",
            "openmp",
        ),
        "execspace_threads": (
            "auto",
            "Whether to build kernels for the execution space Kokkos::Threads",
            "threads",
        ),
        "execspace_serial": (
            "auto",
            "Whether to build kernels for the execution space Kokkos::Serial",
            "serial",
        ),
        "memspace_cudauvmspace": (
            "auto",
            "Whether to pre instantiate kernels for the memory space Kokkos::CudaUVMSpace",
            "cuda",
        ),
        "memspace_cudaspace": (
            "auto",
            "Whether to pre instantiate kernels for the memory space Kokkos::CudaSpace",
            "cuda",
        ),
    }
    for eti in space_etis:
        deflt, descr, backend_required = space_etis[eti]
        variant(eti, default=deflt, description=descr)
        depends_on("kokkos+%s" % backend_required, when="+%s" % eti)

    # kokkos-kernels requires KOKKOS_LAMBDA to be available since 4.0.00
    depends_on("kokkos+cuda_lambda", when="@4.0.00:+cuda")

    numeric_etis = {
        "ordinals": (
            "int",
            "ORDINAL_",  # default, cmake name
            ["int", "int64_t"],
        ),  # allowed values
        "offsets": ("int,size_t", "OFFSET_", ["int", "size_t"]),
        "layouts": ("left", "LAYOUT", ["left", "right"]),
        "scalars": ("double", "", ["float", "double", "complex_float", "complex_double"]),
    }
    for eti in numeric_etis:
        deflt, cmake_name, vals = numeric_etis[eti]
        variant(eti, default=deflt, description=eti, values=vals, multi=True)

    tpls = {
        # variant name   #deflt   #spack name  #root var name  #supporting versions  #docstring
        "blas": (False, "blas", "BLAS", "@3.0.00:", "Link to system BLAS"),
        "lapack": (False, "lapack", "LAPACK", "@3.0.00:", "Link to system LAPACK"),
        "mkl": (False, "mkl", "MKL", "@3.0.00:", "Link to system MKL"),
        "cublas": (False, "cuda", None, "@3.0.00:", "Link to CUDA BLAS library"),
        "cusparse": (False, "cuda", None, "@3.0.00:", "Link to CUDA sparse library"),
        "superlu": (False, "superlu", "SUPERLU", "@3.1.00:", "Link to SuperLU library"),
        "cblas": (False, "cblas", "CBLAS", "@3.1.00:", "Link to CBLAS library"),
        "lapacke": (False, "clapack", "LAPACKE", "@3.1.00:", "Link to LAPACKE library"),
        "rocblas": (False, "rocblas", "ROCBLAS", "@3.6.00:", "Link to AMD BLAS library"),
        "rocsparse": (False, "rocsparse", "ROCSPARSE", "@3.6.00:", "Link to AMD sparse library"),
        "cusolver": (False, "cuda", None, "@4.3.00:", "Link to CUDA solver library"),
        "rocsolver": (False, "rocsolver", "ROCSOLVER", "@4.3.00:", "Link to AMD solver library"),
    }

    for tpl in tpls:
        deflt_bool, spackname, rootname, condition, descr = tpls[tpl]
        variant(tpl, default=deflt_bool, when=f"{condition}", description=descr)
        depends_on(spackname, when="+%s" % tpl)

    variant("shared", default=True, description="Build shared libraries")

    # sanity check
    sanity_check_is_file = [join_path("include", "KokkosKernels_config.h")]
    sanity_check_is_dir = ["include"]

    def cmake_args(self):
        spec = self.spec
        options = []

        isdiy = spec.satisfies("+diy")
        if isdiy:
            options.append("-DSpack_WORKAROUND=On")

        options.append("-DKokkos_ROOT=%s" % spec["kokkos"].prefix)
        if spec.satisfies("^kokkos+rocm"):
            options.append("-DCMAKE_CXX_COMPILER=%s" % spec["hip"].hipcc)
        else:
            # Compiler weirdness due to nvcc_wrapper
            options.append("-DCMAKE_CXX_COMPILER=%s" % spec["kokkos"].kokkos_cxx)

        if self.run_tests:
            options.append("-DKokkosKernels_ENABLE_TESTS=ON")

        for tpl in self.tpls:
            on_flag = "+%s" % tpl
            off_flag = "~%s" % tpl
            dflt, spackname, rootname, condition, descr = self.tpls[tpl]
            if on_flag in self.spec:
                options.append("-DKokkosKernels_ENABLE_TPL_%s=ON" % tpl.upper())
                if rootname:
                    options.append("-D%s_ROOT=%s" % (rootname, spec[spackname].prefix))
                else:
                    pass  # this should get picked up automatically, we hope
            elif off_flag in self.spec:
                options.append("-DKokkosKernels_ENABLE_TPL_%s=OFF" % tpl.upper())

        for eti in self.numeric_etis:
            deflt, cmake_name, vals = self.numeric_etis[eti]
            for val in vals:
                keyval = "%s=%s" % (eti, val)
                cmake_option = "KokkosKernels_INST_%s%s" % (cmake_name.upper(), val.upper())
                if keyval in spec:
                    options.append("-D%s=ON" % cmake_option)
                else:
                    options.append("-D%s=OFF" % cmake_option)

        for eti in self.space_etis:
            deflt, descr, _ = self.space_etis[eti]
            if deflt == "auto":
                value = spec.variants[eti].value
                # spack does these as strings, not reg booleans
                if str(value) == "True":
                    options.append("-DKokkosKernels_INST_%s=ON" % eti.upper())
                elif str(value) == "False":
                    options.append("-DKokkosKernels_INST_%s=OFF" % eti.upper())
                else:
                    pass  # don't pass anything, let CMake decide
            else:  # simple option
                on_flag = "+%s" % eti
                off_flag = "~%s" % eti
                if on_flag in self.spec:
                    options.append("-DKokkosKernels_INST_%s=ON" % eti.upper())
                elif off_flag in self.spec:
                    options.append("-DKokkosKernels_INST_%s=OFF" % eti.upper())

        options.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        return options
