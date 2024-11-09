# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Mercury(CMakePackage):
    """Mercury is a C library for implementing RPC, optimized for HPC"""

    homepage = "https://mercury-hpc.github.io/"
    url = "https://github.com/mercury-hpc/mercury/releases/download/v1.0.1/mercury-1.0.1.tar.bz2"
    git = "https://github.com/mercury-hpc/mercury.git"

    maintainers("soumagne")

    tags = ["e4s"]

    license("GPL-2.0-only")

    version("master", branch="master", submodules=True)
    version("2.3.1", sha256="36182d49f2db7e2b075240cab4aaa1d4ec87a7756450c87643ededd1e6f16104")
    version("2.3.0", sha256="e9e62ce1bb2fd482f0e85ad75fa255d9750c6fed50ba441a03de93b3b8eae742")
    version("2.2.0", sha256="e66490cf63907c3959bbb2932b5aaf51d96a481b17f0935f409f3a862eff97f6")
    version("2.1.0", sha256="9a58437161e9273b1b1c484d2f1a477a89eea9afe84575415025d47656f3761b")
    version("2.0.1", sha256="335946d9620ac669643ffd9861a5fb3ee486834bab674b7779eaac9d6662e3fa")
    version("2.0.0", sha256="9e80923712e25df56014309df70660e828dbeabbe5fcc82ee024bcc86e7eb6b7")
    version("1.0.1", sha256="02febd56c401ef7afa250caf28d012b37dee842bfde7ee16fcd2f741b9cf25b3")
    version("1.0.0", sha256="fb0e44d13f4652f53e21040435f91d452bc2b629b6e98dcf5292cd0bece899d4")
    version("0.9.0", sha256="40868e141cac035213fe79400f8926823fb1f5a0651fd7027cbe162b063843ef")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("bmi", default=False, description="Use BMI plugin")
    variant("mpi", default=False, description="Use MPI plugin")
    variant("ofi", default=True, when="@1.0.0:", description="Use OFI libfabric plugin")
    variant("psm", default=False, when="@2.2.0:", description="Use PSM plugin")
    variant("psm2", default=False, when="@2.2.0:", description="Use PSM2 plugin")
    # NOTE: the sm plugin does not require any package dependency.
    variant("sm", default=True, description="Use shared-memory plugin")
    variant("ucx", default=False, when="@2.1.0:", description="Use UCX plugin")
    # NOTE: if boostsys is False, mercury will install its own copy
    # of the preprocessor headers.
    variant("boostsys", default=True, description="Use preprocessor headers from boost dependency")
    variant("shared", default=True, description="Build with shared libraries")
    # NOTE: the 'udreg' variant requires that the MPICH_GNI_NDREG_ENTRIES=1024
    #   environment variable be set at run time to avoid conflicts with
    #   Cray-MPICH if libfabric and MPI are used at the same time
    variant(
        "udreg",
        default=False,
        when="@1.0.0:+ofi",
        description="Enable udreg on supported Cray Aries platforms",
    )
    variant("debug", default=False, description="Enable Mercury to print debug output")
    variant("checksum", default=True, description="Checksum verify all request/response messages")
    variant(
        "hwloc", default=False, when="@2.2.0:", description="Use hwloc to retrieve NIC information"
    )

    depends_on("cmake@2.8.12.2:", type="build")
    depends_on("bmi", when="+bmi")
    depends_on("mpi", when="+mpi")
    with when("+ofi"):
        depends_on("libfabric@1.5:", when="@:2.0.1")
        depends_on("libfabric@1.7:", when="@2.1.0:")
    # openpa dependency is removed in 2.1.0
    depends_on("openpa@1.0.3:", when="@:2.0.1%gcc@:4.8")
    # We only need Boost preprocessor headers
    depends_on("boost@1.48:", when="+boostsys")
    depends_on("boost", when="@:0.9")  # internal boost headers were added in 1.0.0
    depends_on("ucx+thread_multiple", when="+ucx")

    # Fix CMake check_symbol_exists
    # See https://github.com/mercury-hpc/mercury/issues/299
    patch("fix-cmake-3.15-check_symbol_exists.patch", when="@1.0.0:1.0.1")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%cce"):
            if name == "ldflags":
                flags.append("-Wl,-z,muldefs")
        return (None, None, flags)

    def cmake_args(self):
        """Populate cmake arguments for Mercury."""
        spec = self.spec
        define = self.define
        define_from_variant = self.define_from_variant
        parallel_tests = "+mpi" in spec and self.run_tests

        cmake_args = [
            define_from_variant("BUILD_SHARED_LIBS", "shared"),
            define("MERCURY_USE_BOOST_PP", True),
            define_from_variant("MERCURY_USE_CHECKSUMS", "checksum"),
            define("MERCURY_USE_SYSTEM_MCHECKSUM", False),
            define("MERCURY_USE_XDR", False),
            define_from_variant("NA_USE_BMI", "bmi"),
            define_from_variant("NA_USE_MPI", "mpi"),
            define_from_variant("NA_USE_SM", "sm"),
        ]

        if "@2.3.0:" in spec:
            cmake_args.append(define("BUILD_TESTING_UNIT", self.run_tests))

        if "@2.2.0:" in spec:
            cmake_args.extend(
                [
                    define_from_variant("NA_USE_PSM", "psm"),
                    define_from_variant("NA_USE_PSM2", "psm2"),
                ]
            )
            if "+ofi" in spec:
                cmake_args.append(define_from_variant("NA_OFI_USE_HWLOC", "hwloc"))

        if "@2.1.0:" in spec:
            cmake_args.append(define_from_variant("NA_USE_UCX", "ucx"))

        if "@2.0.0:" in spec:
            cmake_args.extend(
                [
                    define_from_variant("MERCURY_ENABLE_DEBUG", "debug"),
                    define("MERCURY_TESTING_ENABLE_PARALLEL", parallel_tests),
                ]
            )

        # Previous versions of mercury had more extensive CMake options
        if "@:1.0.1" in spec:
            cmake_args.extend(
                [
                    define("MERCURY_ENABLE_PARALLEL_TESTING", parallel_tests),
                    define("MERCURY_ENABLE_POST_LIMIT", False),
                    define_from_variant("MERCURY_ENABLE_VERBOSE_ERROR", "debug"),
                    define("MERCURY_USE_EAGER_BULK", True),
                    define("MERCURY_USE_SELF_FORWARD", True),
                ]
            )

        if "@1.0.0:" in spec:
            cmake_args.extend(
                [
                    define_from_variant("MERCURY_USE_SYSTEM_BOOST", "boostsys"),
                    define_from_variant("NA_USE_OFI", "ofi"),
                ]
            )

        if "+ofi" in spec:
            ofi_fabrics = spec["libfabric"].variants["fabrics"].value
            if "gni" in ofi_fabrics:
                cmake_args.append(define_from_variant("NA_OFI_GNI_USE_UDREG", "udreg"))
            if self.run_tests:
                supported = ["tcp", "verbs", "gni", "cxi"]
                ofi_test_fabrics = list(filter(lambda x: x in supported, ofi_fabrics))
                cmake_args.append(
                    define("NA_OFI_TESTING_PROTOCOL", format(";".join(ofi_test_fabrics)))
                )

        return cmake_args

    def check(self):
        """Unit tests fail when run in parallel."""

        with working_dir(self.builder.build_directory):
            make("test", parallel=False)
