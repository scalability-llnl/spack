# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Faodel(CMakePackage):
    """Flexible, Asynchronous, Object Data-Exchange Libraries"""

    homepage = "https://github.com/sandialabs/faodel"
    url = "https://github.com/sandialabs/faodel/archive/v1.2108.1.tar.gz"
    git = "https://github.com/sandialabs/faodel.git"

    maintainers("tkordenbrock", "craigulmer")

    tags = ["e4s"]

    license("MIT")

    version("master", branch="master")
    version("1.2108.1", sha256="66c53daa510b28f906faac7c67d944a034900da2e296159a2879c3c0b0080ffd")
    version("1.1906.2", sha256="fd61c0a9c4303cd6b8c33bf04414acfc80ceaf08272be99bf3ebc854b37656a0")
    version("1.1906.1", sha256="4b3caf469ae7db50e9bb8d652e4cb532d33d474279def0f8a483f69385648058")
    version("1.1811.2", sha256="22feb502dad0f56fb8af492f6e2cdc53a97fd6c31f6fa3c655be0a6266c46996")
    version("1.1811.1", sha256="8e95ee99b8c136ff687eb07a2481ee04560cb1526408eb22ab56cd9c60206916")
    version("1.1803.1", sha256="70ce7125c02601e14abe5985243d67adf677ed9e7a4dd6d3eaef8a97cf281a16")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build Faodel as shared libs")
    variant("mpi", default=True, description="Enable MPI")

    variant("hdf5", default=False, description="Build the HDF5-based IOM in Kelpie")
    variant(
        "tcmalloc",
        default=True,
        description="Use tcmalloc from gperftools in Lunasa, potentially other places",
    )

    variant(
        "logging",
        default="stdout",
        values=("stdout", "sbl", "disabled"),
        description="Select where logging interface output is routed",
    )
    variant(
        "network",
        default="nnti",
        values=("nnti", "libfabric"),
        description="RDMA Network library to use for low-level communication",
    )
    variant(
        "serializer",
        default="xdr",
        values=("xdr", "cereal"),
        description="Use Cereal to serialize NNTI data structures else XDR",
    )

    depends_on("mpi", when="+mpi")
    depends_on(
        "boost@1.60.0:"
        "+program_options+exception+locale+system+chrono+log+serialization"
        "+atomic+container+regex+thread+date_time"
    )
    depends_on("cmake@3.8.0:", type="build")
    depends_on("hdf5+mpi", when="+hdf5+mpi")
    depends_on("hdf5~mpi", when="+hdf5~mpi")
    depends_on("libfabric@1.5.3:", when="network=libfabric")
    depends_on("googletest@1.7.0:", type="test")

    # FAODEL requires C++11 support which starts with gcc 4.8.1
    conflicts("%gcc@:4.8.0")

    # Github issue #11267
    # Requires master branch of `leveldb` which is not available in spack
    # (only versions 1.20 and 1.18 are available).
    # depends_on('leveldb', when='+leveldb')
    # variant('leveldb', default=False,
    #        description='Build the LevelDB-based IOM in Kelpie')

    # Only clang requires this patch, but it should be applied for all
    patch("array.patch", when="@1.1803.1")

    # FAODEL Github issue #4
    patch("faodel_mpi.patch", when="@1.1811.1 ~mpi")
    # FAODEL Github issue #5
    patch("faodel_sbl.patch", when="@1.1811.1 logging=sbl")
    patch("lambda-capture-f0267fc.patch", when="@1.1906.1")
    patch("ugni-target-redef-b67e856.patch", when="@1.1906.1")

    def cmake_args(self):
        spec = self.spec

        build_tests = self.run_tests and "+mpi" in spec

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BOOST_ROOT", spec["boost"].prefix),
            self.define("BUILD_DOCS", False),
            self.define("BUILD_TESTS", build_tests),
            self.define_from_variant("Faodel_ENABLE_IOM_HDF5", "hdf5"),
            # self.define_from_variant('Faodel_ENABLE_IOM_LEVELDB', 'leveldb'),
            self.define_from_variant("Faodel_ENABLE_MPI_SUPPORT", "mpi"),
            self.define_from_variant("Faodel_ENABLE_TCMALLOC", "tcmalloc"),
            self.define_from_variant("Faodel_LOGGING_METHOD", "logging"),
            self.define_from_variant("Faodel_NETWORK_LIBRARY", "network"),
            self.define_from_variant("Faodel_NNTI_SERIALIZATION_METHOD", "serializer"),
        ]
        if build_tests:
            args.extend([self.define("GTEST_ROOT", spec["googletest"].prefix)])

        return args
