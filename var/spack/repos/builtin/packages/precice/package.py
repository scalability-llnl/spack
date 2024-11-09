# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Precice(CMakePackage):
    """preCICE (Precise Code Interaction Coupling Environment) is a
    coupling library for partitioned multi-physics simulations.
    Partitioned means that preCICE couples existing programs (solvers)
    capable of simulating a subpart of the complete physics involved in
    a simulation."""

    homepage = "https://precice.org/"
    git = "https://github.com/precice/precice.git"
    url = "https://github.com/precice/precice/archive/v1.2.0.tar.gz"
    maintainers("fsimonis", "MakisH")

    tags = ["e4s"]

    license("LGPL-3.0-or-later")

    version("develop", branch="develop")
    version("3.1.2", sha256="e06d5e183f584c51812dcddf958210d1195bea38fa2df13be72303dcb06c869b")
    version("3.1.1", sha256="fe759293942ebc9cb2e6127f356a8c795ab7383c1b074595994ebc92466e478d")
    version("3.1.0", sha256="11e7d3d4055ee30852c0e83692ca7563acaa095bd223ebdbd5c8c851b3646d37")
    version("3.0.0", sha256="efe6cf505d9305af89c6da1fdba246199a75a1c63a6a22103773ed95341879ba")
    version("2.5.1", sha256="a5a37d3430eac395e885eb9cbbed9d0980a15e96c3e44763a3769fa7301e3b3a")
    version("2.5.0", sha256="76ec6ee0d1a66f6f3d3d2d11f03cfc5aa7ef4d9e5deb9b7a4b4455ec7f796c00")
    version("2.4.0", sha256="762e603fbcaa96c4fb0b378b7cb6789d09da0cf6193325603e5eeb13e4c7601c")
    version("2.3.0", sha256="57bab08e8b986f5faa364689d470940dbd9c138e5cfa7b861793e7db56b89da3")
    version("2.2.1", sha256="bca8cedfb5c86656e4fdfaca5cb982b861f9aba926538fa4411bc0d015e09c1f")
    version("2.2.0", sha256="f8c4e0810dcaeb6a40a0fcab64b95c899f0121c968e0730416d4d2a97d39d0c4")
    version("2.1.1", sha256="729b7c24a7a61b3953bb70d96a954ad3a85729a29a35a288b59ba25661117064")
    version("2.1.0", sha256="1e6432724f70d0c6c05fdd645e0026754edbc547719a35bf1d3c12a779b1d00e")
    version("2.0.2", sha256="72864480f32696e7b6da94fd404ef5cd6586e2e1640613e46b75f1afac8569ed")
    version("2.0.1", sha256="e4fe2d2063042761ab325f8c802f88ae088c90862af288ad1a642967d074bd50")
    version("2.0.0", sha256="c8979d366f06e35626a8da08a1c589df77ec13972eb524a1ba99a011e245701f")
    version("1.6.1", sha256="7d0c54faa2c69e52304f36608d93c408629868f16f3201f663a0f9b2008f0763")
    version("1.6.0", sha256="c3b16376fda9eb3449adb6cc3c1e267c3dc792a5d118e37d93a32a59b5a4bc6f")
    version("1.5.2", sha256="051e0d7655a91f8681901e5c92812e48f33a5779309e2f104c99f5a687e1a418")
    version("1.5.1", sha256="fbe151f1a9accf9154362c70d15254935d4f594d189982c3a99fdb3dd9d9e665")
    version("1.5.0", sha256="a2a794becd08717e3049252134ae35692fed71966ed32e22cca796a169c16c3e")
    version("1.4.1", sha256="dde4882edde17882340f9f601941d110d5976340bd71af54c6e6ea22ae56f1a5")
    version("1.4.0", sha256="3499bfc0941fb9f004d5e32eb63d64f93e17b4057fab3ada1cde40c8311bd466")
    version("1.3.0", sha256="610322ba1b03df8e8f7d060d57a6a5afeabd5db4e8c4a638d04ba4060a3aec96")
    version("1.2.0", sha256="0784ecd002092949835151b90393beb6e9e7a3e9bd78ffd40d18302d6da4b05b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    # Skip version 1.1.1 entirely, the cmake was lacking install.

    variant("mpi", default=True, description="Enable MPI support")
    variant("petsc", default=True, description="Enable PETSc support")
    variant("python", default=False, description="Enable Python support", when="@2:")
    variant("shared", default=True, description="Build shared libraries")

    for build_type in ("Release", "RelWithDebInfo", "MinSizeRel"):
        variant(
            "debug_log",
            default=False,
            description="Enable debug log in non-debug builds",
            when=f"@2.4: build_type={build_type}",
        )
        variant(
            "checked",
            default=False,
            description="Enable assertions in non-debug builds",
            when=f"@2.4: build_type={build_type}",
        )

    depends_on("cmake@3.5:", type="build")
    depends_on("cmake@3.10.2:", type="build", when="@1.4:")
    depends_on("cmake@3.16.3:", type="build", when="@2.4:")
    depends_on("cmake@3.22.1:", type="build", when="@3.2:")
    depends_on("pkgconfig", type="build", when="@2.2:")

    # Boost components
    depends_on("boost+log+program_options+system+test+thread")
    depends_on("boost+filesystem", when="@:3.0.0")
    depends_on("boost+signals", when="@:2.3")

    # Baseline versions
    depends_on("boost@1.60.0:")
    depends_on("boost@1.65.1:", when="@1.4:")
    depends_on("boost@1.71.0:", when="@2.4:")
    depends_on("boost@1.74.0:", when="@3.2:")

    # Forward compatibility
    depends_on("boost@:1.72", when="@:2.0.2")
    depends_on("boost@:1.74", when="@:2.1.1")
    depends_on("boost@:1.78", when="@:2.3.0")

    depends_on("eigen@3.2:")
    depends_on("eigen@3.4:", when="@3.2:")
    depends_on("eigen@:3.3.7", type="build", when="@:1.5")  # bug in prettyprint

    depends_on("libxml2")
    depends_on("libxml2@:2.11.99", type="build", when="@:2.5.0")

    depends_on("mpi", when="+mpi")

    depends_on("petsc@3.6:", when="+petsc")
    depends_on("petsc@3.12:", when="+petsc@2.1.0:")
    depends_on("petsc@3.15:", when="+petsc@3.2:")

    depends_on("python@3:", when="+python", type=("build", "run"))
    depends_on("py-numpy@1.17:", when="+python", type=("build", "run"))
    depends_on("py-numpy@1.21.5:", when="+python@3.2:", type=("build", "run"))

    # We require C++14 compiler support
    conflicts("%gcc@:4")
    conflicts("%apple-clang@:5")
    conflicts("%clang@:3.7")
    conflicts("%intel@:16")
    conflicts("%pgi@:17.3")

    def xsdk_tpl_args(self):
        return [
            "-DTPL_ENABLE_BOOST:BOOL=ON",
            "-DTPL_ENABLE_EIGEN3:BOOL=ON",
            "-DTPL_ENABLE_LIBXML2:BOOL=ON",
            self.define_from_variant("TPL_ENABLE_PETSC", "petsc"),
            self.define_from_variant("TPL_ENABLE_PYTHON", "python"),
        ]

    def cmake_args(self):
        """Populate cmake arguments for precice."""
        spec = self.spec

        # Select the correct CMake variables by version
        mpi_option = "MPI"
        petsc_option = "PETSC"
        python_option = "PYTHON"
        if spec.satisfies("@2:"):
            mpi_option = "PRECICE_MPICommunication"
            petsc_option = "PRECICE_PETScMapping"
            python_option = "PRECICE_PythonActions"
        if spec.satisfies("@3:"):
            mpi_option = "PRECICE_FEATURE_MPI_COMMUNICATION"
            petsc_option = "PRECICE_FEATURE_PETSC_MAPPING"
            python_option = "PRECICE_FEATURE_PYTHON_ACTIONS"

        cmake_args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant(mpi_option, "mpi"),
            self.define_from_variant(petsc_option, "petsc"),
            self.define_from_variant(python_option, "python"),
        ]

        # The xSDK installation policies were implemented after 1.5.2.
        # The TPL arguments were removed in 3.0.0.
        if spec.satisfies("@1.6:3"):
            cmake_args.extend(self.xsdk_tpl_args())

        # Release options
        if spec.satisfies("@2.4:"):
            cmake_args.extend(
                [
                    self.define_from_variant("PRECICE_RELEASE_WITH_DEBUG_LOG", "debug_log"),
                    self.define_from_variant("PRECICE_RELEASE_WITH_ASSERTIONS", "checked"),
                ]
            )

        # Disable CPack
        if spec.satisfies("@3:"):
            cmake_args.append("-DPRECICE_CONFIGURE_PACKAGE_GENERATION:BOOL=OFF")

        # Dependencies

        # Boost
        cmake_args.append("-DBOOST_ROOT=%s" % spec["boost"].prefix)

        # Eigen3
        cmake_args.append("-DEIGEN3_INCLUDE_DIR=%s" % spec["eigen"].headers.directories[0])

        # LibXML2
        libxml2_includes = spec["libxml2"].headers.directories[0]
        cmake_args.extend(
            [
                "-DLIBXML2_INCLUDE_DIRS=%s" % libxml2_includes,
                "-DLIBXML2_LIBRARIES=%s" % spec["libxml2"].libs[0],
            ]
        )

        # PETSc
        if "+petsc" in spec:
            cmake_args.extend(["-DPETSC_DIR=%s" % spec["petsc"].prefix, "-DPETSC_ARCH=."])

        # Python
        if "@:2.3 +python" in spec:
            # 2.4.0 and higher use find_package(Python3).
            python_library = spec["python"].libs[0]
            python_include = spec["python"].headers.directories[0]
            numpy_include = join_path(
                spec["py-numpy"].package.module.python_platlib, "numpy", "core", "include"
            )
            cmake_args.extend(
                [
                    "-DPYTHON_INCLUDE_DIR=%s" % python_include,
                    "-DNumPy_INCLUDE_DIR=%s" % numpy_include,
                    "-DPYTHON_LIBRARY=%s" % python_library,
                ]
            )

        return cmake_args
