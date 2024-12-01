# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mgis(CMakePackage):
    """
    The MFrontGenericInterfaceSupport project (MGIS) provides helper
    functions for various solvers to interact with behaviour written
    using MFront generic interface.

    MGIS is written in C++.
    Bindings are provided for C and fortran (2003).
    A FEniCS binding is also available.
    """

    homepage = "https://thelfer.github.io/mgis/web/index.html"
    url = "https://github.com/thelfer/MFrontGenericInterfaceSupport/archive/MFrontGenericInterfaceSupport-1.2.tar.gz"
    git = "https://github.com/thelfer/MFrontGenericInterfaceSupport.git"
    maintainers("thelfer")

    license("LGPL-3.0-only")

    # development branches
    version("master", branch="master")
    version("rliv-2.2", branch="rliv-2.2")
    version("rliv-2.1", branch="rliv-2.1")
    version("rliv-2.0", branch="rliv-2.0")
    version("rliv-1.2", branch="rliv-1.2")
    version("rliv-1.1", branch="rliv-1.1")
    version("rliv-1.0", branch="rliv-1.0")

    # released version
    version(
        "2.2",
        sha256="b3776d7b3a534ca626525a42b97665f7660ae2b28ea57b3f53fd7e8538da1ceb",
        preferred=True,
    )
    version("2.1", sha256="f5b556aab130da0c423f395fe4c35d6bf509dd8fc958242f2e37ea788464aea9")
    version("2.0", sha256="cb427d77f2c79423e969815b948a8b44da33a4370d1760e8c1e22a569f3585e2")
    version("1.2.2", sha256="dc24e85cc90ec656ed707eef3d511317ad800915014d9e4e9cf8818b406586d5")
    version("1.2.1", sha256="a2d7cae3a24546adcf1d1bf7f13f012170d359370f5b6b2c1730b19eb507601d")
    version("1.2", sha256="ed82ab91cbe17c00ef36578dbfcb4d1817d4c956619b7cccbea3e3f1a3b31940")
    version("1.1", sha256="06593d7a052678deaee87ef60b2213db7545c5be9823f261d3388b3978a0b7a5")
    version("1.0.1", sha256="6102621455bc5d9b1591cd33e93b2e15a9572d2ce59ca6dfa30ba57ae1265c08")
    version("1.0", sha256="279c98da00fa6855edf29c2b8f8bad6e7732298dc62ef67d028d6bbeaac043b3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # variants
    variant("c", default=True, description="Enables c bindings")
    variant("fortran", default=True, description="Enables fortran bindings")
    variant("python", default=True, description="Enables python bindings")
    variant("static", default=False, description="Enables static libraries")

    # dependencies
    depends_on("tfel@4.2.0", when="@2.2")
    depends_on("tfel@4.1.0", when="@2.1")
    depends_on("tfel@4.0.0", when="@2.0")
    depends_on("tfel@3.4.3", when="@1.2.2")
    depends_on("tfel@3.4.1", when="@1.2.1")
    depends_on("tfel@3.4.0", when="@1.2")
    depends_on("tfel@3.3.0", when="@1.1")
    depends_on("tfel@3.2.1", when="@1.0.1")
    depends_on("tfel@3.2.0", when="@1.0")
    depends_on("tfel@rliv-4.2", when="@rliv-2.2")
    depends_on("tfel@rliv-4.1", when="@rliv-2.1")
    depends_on("tfel@rliv-4.0", when="@rliv-2.0")
    depends_on("tfel@rliv-3.4", when="@rliv-1.2")
    depends_on("tfel@rliv-3.3", when="@rliv-1.1")
    depends_on("tfel@rliv-3.2", when="@rliv-1.0")
    depends_on("tfel@master", when="@master")
    depends_on(
        "boost+python+numpy+exception+container", when="+python", type=("build", "link", "run")
    )
    depends_on("py-numpy", when="+python", type=("build", "link", "run"))

    extends("python", when="+python")

    def patch(self):
        """Fix the test suite to use the PYTHONPATH provided by the spack buildenv"""
        filter_file("tests/;", "tests:", "bindings/python/tests/CMakeLists.txt")

    def check(self):
        """skip target 'test' which doesn't build the test programs used by tests"""
        with working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                self._if_make_target_execute("check")
            elif self.generator == "Ninja":
                self._if_ninja_target_execute("check")

    def cmake_args(self):
        args = []

        args.append("-DUSE_EXTERNAL_COMPILER_FLAGS=ON")

        for i in ["c", "fortran", "python"]:
            if "+" + i in self.spec:
                args.append("-Denable-{0}-bindings=ON".format(i))
            else:
                args.append("-Denable-{0}-bindings=OFF".format(i))

        if "+python" in self.spec:
            # adding path to python
            python = self.spec["python"]
            args.append("-DPYTHON_LIBRARY={0}".format(python.libs[0]))
            args.append("-DPYTHON_INCLUDE_DIR={0}".format(python.headers.directories[0]))
            args.append("-DPython_ADDITIONAL_VERSIONS={0}".format(python.version.up_to(2)))
            # adding path to boost
            args.append("-DBOOST_ROOT={0}".format(self.spec["boost"].prefix))

        if "+static" in self.spec:
            args.append("-Denable-static=ON")

        return args
