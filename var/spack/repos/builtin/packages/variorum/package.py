# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Variorum(CMakePackage):
    """Variorum is a library providing vendor-neutral interfaces for
    monitoring and controlling underlying hardware features.
    """

    homepage = "https://variorum.readthedocs.io"
    git = "https://github.com/llnl/variorum.git"
    url = "https://github.com/llnl/variorum/archive/v0.1.0.tar.gz"

    maintainers("slabasan", "rountree")

    license("MIT")

    version("dev", branch="dev")
    version("0.8.0", sha256="0e7288d523488b2a585af8ffeb7874721526f46df563b21fc51e8846bf65f7d8")
    version("0.7.0", sha256="36ec0219379ea2b7c8f9770b3271335c776ff5a3de71585714c33356345b2f0c")
    version("0.6.0", sha256="c0928a0e6901808ee50142d1034de15edc2c90d7d1b9fbce43757226e7c04306")
    version("0.5.0", sha256="de331762e7945ee882d08454ff9c66436e2b6f87f761d2b31c6ab3028723bfed")
    version("0.4.1", sha256="be7407b856bc2239ecaa27d3df80aee2f541bb721fbfa183612bd9c0ce061f28")
    version("0.4.0", sha256="70ff1c5a3ae15d0bd07d409ab6f3c128e69528703a829cb18ecb4a50adeaea34")
    version("0.3.0", sha256="f79563f09b8fe796283c879b05f7730c36d79ca0346c12995b7bccc823653f42")
    version("0.2.0", sha256="b8c010b26aad8acc75d146c4461532cf5d9d3d24d6fc30ee68f6330a68e65744")
    version("0.1.0", tag="v0.1.0", commit="7747ee48cc60567bb3f09e732f24c041ecac894d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    ############
    # Variants #
    ############
    variant("shared", default=True, description="Build Variorum as shared lib")
    variant("docs", default=False, description="Build Variorum's documentation")
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release"),
    )

    ########################
    # Package dependencies #
    ########################
    depends_on("cmake@2.8:", type="build")
    depends_on("hwloc")
    depends_on("jansson", type="link")

    #########################
    # Documentation related #
    #########################
    depends_on("py-sphinx", when="+docs", type="build")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        cmake_args.append("-DJANSSON_DIR={0}".format(spec["jansson"].prefix))

        if spec.satisfies("%cce"):
            cmake_args.append("-DCMAKE_C_FLAGS=-fcommon")
            cmake_args.append("-DCMAKE_CCC_FLAGS=-fcommon")
            cmake_args.append("-DCMAKE_Fortran_FLAGS=-ef")

        if "+shared" in spec:
            cmake_args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            cmake_args.append("-DBUILD_SHARED_LIBS=OFF")

        if "+docs" in spec:
            cmake_args.append("-DBUILD_DOCS=ON")
            sphinx_build_exe = join_path(spec["py-sphinx"].prefix.bin, "sphinx-build")
            cmake_args.append("-DSPHINX_EXECUTABLE=" + sphinx_build_exe)
        else:
            cmake_args.append("-DBUILD_DOCS=OFF")

        if "build_type=Debug" in spec:
            cmake_args.append("-DVARIORUM_DEBUG=ON")
        else:
            cmake_args.append("-DVARIORUM_DEBUG=OFF")

        if self.run_tests:
            cmake_args.append("-DBUILD_TESTS=ON")
        else:
            cmake_args.append("-DBUILD_TESTS=OFF")

        return cmake_args
