# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.build_systems.cmake
import spack.build_systems.python
from spack.package import *


class PyPybind11(CMakePackage, PythonExtension):
    """pybind11 -- Seamless operability between C++11 and Python.

    pybind11 is a lightweight header-only library that exposes C++ types in
    Python and vice versa, mainly to create Python bindings of existing C++
    code. Its goals and syntax are similar to the excellent Boost.Python
    library by David Abrahams: to minimize boilerplate code in traditional
    extension modules by inferring type information using compile-time
    introspection.
    """

    homepage = "https://pybind11.readthedocs.io"
    url = "https://github.com/pybind/pybind11/archive/refs/tags/v2.10.1.tar.gz"
    git = "https://github.com/pybind/pybind11.git"

    maintainers("ax3l")

    version("master", branch="master")
    version("2.13.5", sha256="b1e209c42b3a9ed74da3e0b25a4f4cd478d89d5efbb48f04b277df427faf6252")
    version("2.13.4", sha256="efc901aa0aab439a3fea6efeaf930b5a349fb06394bf845c64ce15a9cf8f0240")
    version("2.13.3", sha256="6e7a84ec241544f2f5e30c7a82c09c81f0541dd14e9d9ef61051e07105f9c445")
    version("2.13.2", sha256="50eebef369d28f07ce1fe1797f38149e5928817be8e539239f2aadfd95b227f3")
    version("2.13.1", sha256="51631e88960a8856f9c497027f55c9f2f9115cafb08c0005439838a05ba17bfc")
    version("2.13.0", sha256="8ac2bd138ea3c12683d3496361af6bee0f7754f86bf050e6c61e3966de688215")
    version("2.12.0", sha256="bf8f242abd1abcd375d516a7067490fb71abd79519a282d22b6e4d19282185a7")
    version("2.11.1", sha256="d475978da0cdc2d43b73f30910786759d593a9d8ee05b1b6846d1eb16c6d2e0c")
    version("2.11.0", sha256="7af30a84c6810e721829c4646e31927af9d8861e085aa5dd37c3c8b8169fcda1")
    version("2.10.4", sha256="832e2f309c57da9c1e6d4542dedd34b24e4192ecb4d62f6f4866a737454c9970")
    version("2.10.1", sha256="111014b516b625083bef701df7880f78c2243835abdb263065b6b59b960b6bad")
    version("2.10.0", sha256="eacf582fa8f696227988d08cfc46121770823839fe9e301a20fbce67e7cd70ec")
    version("2.9.2", sha256="6bd528c4dbe2276635dc787b6b1f2e5316cf6b49ee3e150264e455a0d68d19c1")
    version("2.9.1", sha256="c6160321dc98e6e1184cc791fbeadd2907bb4a0ce0e447f2ea4ff8ab56550913")
    version("2.9.0", sha256="057fb68dafd972bc13afb855f3b0d8cf0fa1a78ef053e815d9af79be7ff567cb")
    version("2.8.1", sha256="f1bcc07caa568eb312411dde5308b1e250bd0e1bc020fae855bf9f43209940cc")
    version("2.8.0", sha256="9ca7770fc5453b10b00a4a2f99754d7a29af8952330be5f5602e7c2635fa3e79")
    version("2.7.1", sha256="616d1c42e4cf14fa27b2a4ff759d7d7b33006fdc5ad8fd603bb2c22622f27020")
    version("2.7.0", sha256="6cd73b3d0bf3daf415b5f9b87ca8817cc2e2b64c275d65f9500250f9fee1677e")
    version("2.6.2", sha256="8ff2fff22df038f5cd02cea8af56622bc67f5b64534f1b83b9f133b8366acff2")
    version("2.6.1", sha256="cdbe326d357f18b83d10322ba202d69f11b2f49e2d87ade0dc2be0c5c34f8e2a")
    version("2.5.0", sha256="97504db65640570f32d3fdf701c25a340c8643037c3b69aec469c10c93dc8504")
    version("2.4.3", sha256="1eed57bc6863190e35637290f97a20c81cfe4d9090ac0a24f3bbf08f265eb71d")
    version("2.3.0", sha256="0f34838f2c8024a6765168227ba587b3687729ebf03dc912f88ff75c7aa9cfe8")
    version("2.2.4", sha256="b69e83658513215b8d1443544d0549b7d231b9f201f6fc787a2b2218b408181e")
    version("2.2.3", sha256="3a3b7b651afab1c5ba557f4c37d785a522b8030dfc765da26adc2ecd1de940ea")
    version("2.2.2", sha256="b639a2b2cbf1c467849660801c4665ffc1a4d0a9e153ae1996ed6f21c492064e")
    version("2.2.1", sha256="f8bd1509578b2a1e7407d52e6ee8afe64268909a1bbda620ca407318598927e7")
    version("2.2.0", sha256="1b0fda17c650c493f5862902e90f426df6751da8c0b58c05983ab009951ed769")
    version("2.1.1", sha256="f2c6874f1ea5b4ad4ffffe352413f7d2cd1a49f9050940805c2a082348621540")
    version("2.1.0", sha256="2860f2b8d0c9f65f0698289a161385f59d099b7ead1bf64e8993c486f2b93ee0")

    depends_on("cxx", type="build")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-pytest", type="test")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    extends("python")

    # Spack defaults to False but pybind11 defaults to True (and IPO is highly
    # encouraged to be used)
    variant("ipo", default=True, description="CMake interprocedural optimization")

    with when("build_system=cmake"):
        generator("ninja")
        depends_on("cmake@3.13:", type="build")
        depends_on("cmake@3.18:", type="build", when="@2.6.0:")

    # https://github.com/pybind/pybind11/#supported-compilers
    conflicts("%clang@:3.2")
    conflicts("%apple-clang@:4")
    conflicts("%gcc@:4.7")
    conflicts("%msvc@:16")
    conflicts("%intel@:17")

    # https://github.com/pybind/pybind11/pull/5208
    conflicts("%gcc@14:", when="@:2.13.1")

    # https://github.com/pybind/pybind11/pull/1995
    @when("@:2.4")
    def patch(self):
        """see https://github.com/spack/spack/issues/13559"""
        filter_file(
            "import sys",
            'import sys; return "{0}"'.format(self.prefix.include),
            "pybind11/__init__.py",
            string=True,
        )


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define("PYBIND11_TEST", self.pkg.run_tests),
            self.define("prefix_for_pc_file", self.prefix),
        ]

    def install(self, pkg, spec, prefix):
        super().install(pkg, spec, prefix)
        python_builder = spack.build_systems.python.PythonPipBuilder(pkg)
        python_builder.install(pkg, spec, prefix)

    def setup_build_environment(self, env):
        env.set("PYBIND11_USE_CMAKE", 1)

    @run_after("install")
    def install_test(self):
        if not self.pkg.run_tests:
            return

        with working_dir("spack-test", create=True):
            # test include helper points to right location
            py_inc = python(
                "-c", "import pybind11 as py; print(py.get_include())", output=str
            ).strip()
            for inc in [py_inc, self.prefix.include]:
                inc_file = join_path(inc, "pybind11", "pybind11.h")
                assert os.path.isfile(inc_file)
