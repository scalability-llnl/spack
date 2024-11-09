# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mstk(CMakePackage):
    """MSTK is a mesh framework that allows users to represent,
    manipulate and query unstructured 3D arbitrary topology meshes
    in a general manner without the need to code their own data
    structures. MSTK is a flexible framework in that it allows a
    variety of underlying representations for the mesh while
    maintaining a common interface. It allows users to choose from
    different mesh representations either at initialization (implemented)
    or during the program execution (not yet implemented) so that the
    optimal data structures are used for the particular algorithm.
    The interaction of users and applications with MSTK is through a
    functional interface that acts as though the mesh always contains
    vertices, edges, faces and regions and maintains connectivity between
    all these entities."""

    homepage = "https://github.com/MeshToolkit/MSTK"
    git = "https://github.com/MeshToolkit/MSTK"
    url = "https://github.com/MeshToolkit/MSTK/archive/3.3.6.tar.gz"

    maintainers("raovgarimella", "julienloiseau")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("3.3.6", sha256="30041ee6f32d754e5d9b46db8f62609bb66d2686f8e6e16ad254f552849cb0f1")
    version("3.3.5", sha256="64c976e12d1393aafd086ef941b176add6cfb963f463c33259596e7ef641cdd8")
    version("3.3.4", sha256="bd34d31fc1fc468147a51e8d837d6bf9902ca8d38c7c0615e7f20968d4659da2")
    version("3.3.3", sha256="54ea7929c9046915472f38367c83f75af634a6989ce0b89aad17fb9f4a25023e")
    version("3.3.2", sha256="fb4ffa97af4d0a0d4771c8585d0b27538b013d8b1cfaff992e5e054fef62af0b")
    version("3.3.1", sha256="9fdb0c33c1b68714d708b355d963547cf41332812658d4560d4db43904fc78de")
    version("3.3.0", sha256="205c48fb5619937b5dd83788da739b7c2060155b7c41793e29ce05422b8f7dfb")
    version("3.2.1", sha256="09bc6684abb576e34c324322db6f71f8987c6ec436a54256b85ef4db40185470")
    version("3.2.0", sha256="57e58c5a7a456dbc608ce9f834a06c212a1aa64ac3ebc880ea0b8a19b000dab0")
    version("3.1.3", sha256="03f6901cd6d563e1705a173c1a2fbbef10ab9a43f533f6ba758e357c03bdfa16")
    version("3.1.2", sha256="1eb44c29554f45695f875fc60ab81554a2c46a041ef58a7224f3767d30e2846e")
    version("3.1.1", sha256="5a03873c69fb38acd7ce27f2a5fa0643dd1cfcc3e214cff4aa26ee717651cc0b")
    version("3.1.0", sha256="70e68d8a90cd2367015e0ab3459ed230a7995ad2297671742d9be6e28bc03dcf")
    version("3.0.4", sha256="99e4c996bf22fd325335ed1391dfe735b0a338e8e4d733204d56dde7ef4eedf3")
    version("3.0.3", sha256="618e371a48077f2b4ccfafd4d174c05f007b2ea7a51e0399df67442639409518")
    version("3.0.2", sha256="b0172cd68e5137b8585d82c37b8a4af4b7e884f04d1b7d006a399d39447fe89e")
    version("3.0.1", sha256="d44e4bf01b118b1d19710aa839b3f5f0c1a8391264a435f641ba4bd23bcf45ec")
    version("3.0.0", sha256="d993ff5fc6c431067eb97e4089835c7790397d9c1ad88a56523c0591d451df19")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("exodusii", default=False, description="Enable ExodusII")
    variant("use_markers", default=True, description="Enable use of markers")
    variant("parallel", default=False, description="Enable Parallel Support")
    variant(
        "partitioner",
        default="none",
        values=("none", "metis", "zoltan", "all"),
        multi=False,
        description="Choose partitioner",
    )
    conflicts("partitioner=none", when="+parallel")
    conflicts("partitioner=all", when="-parallel")
    conflicts("partitioner=zoltan", when="-parallel")

    # MSTK turns on METIS only for parallel builds
    conflicts("partitioner=metis", when="-parallel")

    # dependencies
    depends_on("cmake@3.11:", type="build")

    #
    depends_on("mpi", when="+parallel")

    depends_on("zoltan -fortran", when="partitioner=zoltan")
    depends_on("zoltan -fortran", when="partitioner=all")
    depends_on("metis", when="partitioner=metis")
    depends_on("metis", when="partitioner=all")

    # Exodusii variant
    # The default exodusii build with mpi support
    depends_on("exodusii", when="+exodusii")

    # Unit testing variant
    depends_on("unittest-cpp", type="test")

    def cmake_args(self):
        options = []
        if "+use_markers" in self.spec:
            options.append("-DMSTK_USE_MARKERS=ON")
        else:
            options.append("-DMSTK_USE_MARKERS=OFF")

        # Parallel variant
        if "+parallel" in self.spec:
            options.append("-DENABLE_PARALLEL=ON")
        else:
            options.append("-DENABLE_PARALLEL=OFF")

        if "partitioner=none" in self.spec:
            options.append("-DENABLE_METIS=OFF")
            options.append("-DENABLE_ZOLTAN=OFF")
        else:
            if "zoltan" in self.spec:
                options.append("-DENABLE_ZOLTAN=ON")
            else:
                options.append("-DENABLE_ZOLTAN=OFF")
            if "metis" in self.spec:
                options.append("-DENABLE_METIS=ON")
            else:
                options.append("-DENABLE_METIS=OFF")

        # ExodusII variant
        if "+exodusii" in self.spec:
            options.append("-DENABLE_ExodusII=ON")
        else:
            options.append("-DENABLE_ExodusII=OFF")

        # Unit test variant
        if self.run_tests:
            options.append("-DENABLE_Tests=ON")
        else:
            options.append("-DENABLE_Tests=OFF")

        return options
