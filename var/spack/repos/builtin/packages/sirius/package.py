# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sirius(CMakePackage, CudaPackage, ROCmPackage):
    """Domain specific library for electronic structure calculations"""

    homepage = "https://github.com/electronic-structure/SIRIUS"
    url = "https://github.com/electronic-structure/SIRIUS/archive/v6.1.5.tar.gz"
    list_url = "https://github.com/electronic-structure/SIRIUS/releases"
    git = "https://github.com/electronic-structure/SIRIUS.git"

    maintainers("simonpintarelli", "haampie", "dev-zero", "AdhocMan", "toxa81")

    license("BSD-2-Clause")

    version("develop", branch="develop")
    version("master", branch="master")

    version("7.6.1", sha256="16a114dc17e28697750585820e69718a96e6929f88406d266c75cf9a7cdbdaaa")
    version("7.6.0", sha256="e424206fecb35bb2082b5c87f0865a9536040e984b88b041e6f7d531f8a65b20")
    version("7.5.2", sha256="9ae01935578532c84f1d0d673dbbcdd490e26be22efa6c4acf7129f9dc1a0c60")
    version("7.5.1", sha256="aadfa7976e90a109aeb1677042454388a8d1a50d75834d59c86c8aef06bc12e4")
    version("7.5.0", sha256="c583f88ffc02e9acac24e786bc35c7c32066882d2f70a1e0c14b5780b510365d")
    version("7.4.3", sha256="015679a60a39fa750c5d1bd8fb1ce73945524bef561270d8a171ea2fd4687fec")
    version("7.4.0", sha256="f9360a695a1e786d8cb9d6702c82dd95144a530c4fa7e8115791c7d1e92b020b")
    version("7.3.2", sha256="a256508de6b344345c295ad8642dbb260c4753cd87cc3dd192605c33542955d7")
    version("7.3.1", sha256="8bf9848b8ebf0b43797fd359adf8c84f00822de4eb677e3049f22baa72735e98")
    version("7.3.0", sha256="69b5cf356adbe181be6c919032859c4e0160901ff42a885d7e7ea0f38cc772e2")
    version(
        "7.2.7",
        sha256="929bf7f131a4847624858b9c4295532c24b0c06f6dcef5453c0dfc33fb78eb03",
        deprecated=True,
    )
    version(
        "7.2.6",
        sha256="e751fd46cdc7c481ab23b0839d3f27fb00b75dc61dc22a650c92fe8e35336e3a",
        deprecated=True,
    )
    version(
        "7.2.5",
        sha256="794e03d4da91025f77542d3d593d87a8c74e980394f658a0210a4fd91c011f22",
        deprecated=True,
    )
    version(
        "7.2.4",
        sha256="aeed0e83b80c3a79a9469e7f3fe10d80ad331795e38dbc3c49cb0308e2bd084d",
        deprecated=True,
    )
    version(
        "7.2.3",
        sha256="6c10f0e87e50fcc7cdb4d1b2d35e91dba6144de8f111e36c7d08912e5942a906",
        deprecated=True,
    )
    version(
        "7.2.1",
        sha256="01bf6c9893ff471473e13351ca7fdc2ed6c1f4b1bb7afa151909ea7cd6fa0de7",
        deprecated=True,
    )
    version(
        "7.2.0",
        sha256="537800459db8a7553d7aa251c19f3a31f911930194b068bc5bca2dfb2c9b71db",
        deprecated=True,
    )
    version(
        "7.0.2",
        sha256="ee613607ce3be0b2c3f69b560b2415ce1b0e015179002aa90739430dbfaa0389",
        deprecated=True,
    )
    version(
        "7.0.1",
        sha256="cca11433f86e7f4921f7956d6589f27bf0fd5539f3e8f96e66a3a6f274888595",
        deprecated=True,
    )
    version(
        "7.0.0",
        sha256="da783df11e7b65668e29ba8d55c8a6827e2216ad6d88040f84f42ac20fd1bb99",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("openmp", default=True, description="Build with OpenMP support")
    variant("fortran", default=False, description="Build Fortran bindings")
    variant("python", default=False, description="Build Python bindings")
    variant("memory_pool", default=True, description="Build with memory pool")
    variant("elpa", default=False, description="Use ELPA")
    variant("dlaf", default=False, when="@7.5.0:", description="Use DLA-Future")
    variant("vdwxc", default=False, description="Enable libvdwxc support")
    variant("scalapack", default=False, description="Enable scalapack support")
    variant("magma", default=False, description="Enable MAGMA support")
    variant("nlcglib", default=False, description="Enable robust wave function optimization")
    variant("wannier90", default=False, description="Enable Wannier90 library")
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )
    variant("apps", default=True, description="Build applications")
    variant("tests", default=False, description="Build tests")
    variant("single_precision", default=False, description="Use single precision arithmetics")
    variant(
        "profiler", default=True, description="Use internal profiler to measure execution time"
    )
    variant("nvtx", default=False, description="Use NVTX profiler")

    with when("@7.6:"):
        variant(
            "pugixml",
            default=False,
            description="Enable direct reading of UPF v2 pseudopotentials",
        )
        conflicts("+tests~pugixml")
    depends_on("pugixml", when="+pugixml")

    depends_on("cmake@3.23:", type="build")
    depends_on("mpi")
    depends_on("gsl")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api@3")
    depends_on("libxc@3.0.0:")
    depends_on("libxc@4.0.0:", when="@7.2.0:")
    depends_on("spglib")
    depends_on("hdf5+hl")
    depends_on("pkgconfig", type="build")

    # Python module
    depends_on("python", when="+python", type=("build", "run"))
    depends_on("python", when="@:6", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-scipy", when="+python", type=("build", "run"))
    depends_on("py-h5py", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    depends_on("py-pyyaml", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    depends_on("py-voluptuous", when="+python", type=("build", "run"))
    depends_on("py-pybind11", when="+python", type=("build", "run"))
    extends("python", when="+python")

    depends_on("magma", when="+magma")

    with when("@7.0.1:"):
        depends_on("spfft@0.9.13:")
        depends_on("spfft+single_precision", when="+single_precision")
        depends_on("spfft+cuda", when="+cuda")
        depends_on("spfft+rocm", when="+rocm")
        depends_on("spfft+openmp", when="+openmp")

    with when("@7.0.2:"):
        depends_on("spla@1.1.0:")
        depends_on("spla+cuda", when="+cuda")
        depends_on("spla+rocm", when="+rocm")
        # spla removed the openmp option in 1.6.0
        conflicts("^spla@:1.5~openmp", when="+openmp")

    depends_on("nlcglib", when="+nlcglib")
    depends_on("nlcglib+rocm", when="+nlcglib+rocm")
    depends_on("nlcglib+cuda", when="+nlcglib+cuda")

    depends_on("libvdwxc@0.3.0:+mpi", when="+vdwxc")

    depends_on("scalapack", when="+scalapack")

    with when("+dlaf"):
        depends_on("dla-future@0.3.0:")
        depends_on("dla-future +scalapack", when="+scalapack")
        depends_on("dla-future +cuda", when="+cuda")
        depends_on("dla-future +rocm", when="+rocm")

        conflicts("^pika@:0.22.1", when="+cuda")
        conflicts("^pika@:0.22.1", when="+rocm")

    depends_on("rocblas", when="+rocm")
    depends_on("rocsolver", when="@7.5.0: +rocm")

    # FindHIP cmake script only works for < 4.1, but HIP 4.1 is not provided by spack anymore
    conflicts("+rocm", when="@:7.2.0")

    conflicts("^libxc@5.0.0")  # known to produce incorrect results
    conflicts("+single_precision", when="@:7.2.4")
    conflicts("+scalapack", when="^cray-libsci")

    # Propagate openmp to blas
    depends_on("openblas threads=openmp", when="+openmp ^[virtuals=blas,lapack] openblas")
    depends_on("amdblis threads=openmp", when="+openmp ^[virtuals=blas] amdblis")
    depends_on("blis threads=openmp", when="+openmp ^[virtuals=blas] blis")
    depends_on(
        "intel-mkl threads=openmp", when="+openmp ^[virtuals=blas,lapack,fftw-api] intel-mkl"
    )
    depends_on(
        "intel-oneapi-mkl threads=openmp",
        when="+openmp ^[virtuals=blas,lapack,fftw-api] intel-oneapi-mkl",
    )
    depends_on(
        "intel-oneapi-mkl+cluster",
        when="+scalapack ^[virtuals=blas,lapack,fftw-api] intel-oneapi-mkl",
    )

    conflicts("intel-mkl", when="@develop")  # TODO: Change to @7.5.3
    # MKLConfig.cmake introduced in 2021.3
    conflicts("intel-oneapi-mkl@:2021.2", when="^intel-oneapi-mkl")

    depends_on("wannier90", when="@7.5.0: +wannier90")
    depends_on("wannier90+shared", when="@7.5.0: +wannier90+shared")

    depends_on("elpa+openmp", when="+elpa+openmp")
    depends_on("elpa~openmp", when="+elpa~openmp")

    depends_on("eigen@3.4.0:", when="@7.3.2: +tests")

    depends_on("costa+shared", when="@7.3.2:")

    with when("@7.5: +memory_pool"):
        depends_on("umpire~cuda~rocm", when="~cuda~rocm")
        depends_on("umpire+cuda~device_alloc", when="+cuda")
        depends_on("umpire+rocm~device_alloc", when="+rocm")

    patch("mpi_datatypes.patch", when="@:7.2.6")
    patch("fj.patch", when="@7.3.2: %fj")

    def cmake_args(self):
        spec = self.spec

        cm_label = ""
        if "@7.5:" in spec:
            cm_label = "SIRIUS_"

        args = [
            self.define_from_variant(cm_label + "USE_OPENMP", "openmp"),
            self.define_from_variant(cm_label + "USE_ELPA", "elpa"),
            self.define_from_variant(cm_label + "USE_MAGMA", "magma"),
            self.define_from_variant(cm_label + "USE_NLCGLIB", "nlcglib"),
            self.define_from_variant(cm_label + "USE_VDWXC", "vdwxc"),
            self.define_from_variant(cm_label + "USE_MEMORY_POOL", "memory_pool"),
            self.define_from_variant(cm_label + "USE_SCALAPACK", "scalapack"),
            self.define_from_variant(cm_label + "USE_DLAF", "dlaf"),
            self.define_from_variant(cm_label + "CREATE_FORTRAN_BINDINGS", "fortran"),
            self.define_from_variant(cm_label + "CREATE_PYTHON_MODULE", "python"),
            self.define_from_variant(cm_label + "USE_CUDA", "cuda"),
            self.define_from_variant(cm_label + "USE_ROCM", "rocm"),
            self.define_from_variant(cm_label + "BUILD_APPS", "apps"),
            self.define_from_variant(cm_label + "USE_FP32", "single_precision"),
            self.define_from_variant(cm_label + "USE_PROFILER", "profiler"),
            self.define_from_variant(cm_label + "USE_NVTX", "nvtx"),
            self.define_from_variant(cm_label + "USE_WANNIER90", "wannier90"),
            self.define_from_variant(cm_label + "USE_PUGIXML", "pugixml"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]

        lapack = spec["lapack"]
        blas = spec["blas"]

        args.extend(
            [
                self.define("LAPACK_FOUND", "true"),
                self.define("LAPACK_LIBRARIES", lapack.libs.joined(";")),
                self.define("BLAS_FOUND", "true"),
                self.define("BLAS_LIBRARIES", blas.libs.joined(";")),
            ]
        )

        if "+scalapack" in spec and "^cray-libsci" not in spec:
            args.extend(
                [
                    self.define(cm_label + "SCALAPACK_FOUND", "true"),
                    self.define(
                        cm_label + "SCALAPACK_INCLUDE_DIRS", spec["scalapack"].prefix.include
                    ),
                    self.define(
                        cm_label + "SCALAPACK_LIBRARIES", spec["scalapack"].libs.joined(";")
                    ),
                ]
            )

        if "^cray-libsci" in spec:
            args.append(self.define(cm_label + "USE_CRAY_LIBSCI", "ON"))

        if spec["blas"].name in INTEL_MATH_LIBRARIES:
            args.append(self.define(cm_label + "USE_MKL", "ON"))

            if spec.satisfies("@develop"):  # TODO: Change to @7.5.3:
                mkl_mapper = {
                    "threading": {
                        "none": "sequential",
                        "openmp": "gnu_thread",
                        "tbb": "tbb_thread",
                    },
                    "mpi": {"intel-mpi": "intelmpi", "mpich": "mpich", "openmpi": "openmpi"},
                }

                mkl_threads = mkl_mapper["threading"][
                    spec["intel-oneapi-mkl"].variants["threads"].value
                ]

                mpi_provider = spec["mpi"].name
                if mpi_provider in ["mpich", "cray-mpich", "mvapich", "mvapich2"]:
                    mkl_mpi = mkl_mapper["mpi"]["mpich"]
                else:
                    mkl_mpi = mkl_mapper["mpi"][mpi_provider]

                args.extend(
                    [
                        self.define("MKL_INTERFACE", "lp64"),
                        self.define("MKL_THREADING", mkl_threads),
                        self.define("MKL_MPI", mkl_mpi),
                    ]
                )

                if "+scalapack" in self.spec:
                    # options provided by `MKLConfig.cmake`
                    args.extend(
                        [self.define("ENABLE_BLACS", "On"), self.define("ENABLE_SCALAPACK", "On")]
                    )

        if "+elpa" in spec:
            elpa_incdir = os.path.join(spec["elpa"].headers.directories[0], "elpa")
            args.append(self.define(cm_label + "ELPA_INCLUDE_DIR", elpa_incdir))

        if "+cuda" in spec:
            cuda_arch = spec.variants["cuda_arch"].value
            if cuda_arch[0] != "none":
                # Make SIRIUS handle it
                if "@:7.4.3" in spec:
                    args.append(self.define("CMAKE_CUDA_ARCH", ";".join(cuda_arch)))
                else:
                    args.append(self.define("CMAKE_CUDA_ARCHITECTURES", ";".join(cuda_arch)))

        if "+rocm" in spec:
            archs = ",".join(self.spec.variants["amdgpu_target"].value)
            args.extend([self.define("CMAKE_HIP_ARCHITECTURES", archs)])

        return args
