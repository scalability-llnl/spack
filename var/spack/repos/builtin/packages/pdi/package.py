# Copyright (C) 2020-2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *

try:
    from spack.package import *
except:
    pass


class Pdi(CMakePackage):
    """PDI is a library that aims to decouple high-performance simulation codes
    from Input/Output concerns. It offers a declarative application programming
    interface that enables codes to expose the buffers in which they store data
    and to notify PDI of significant steps of the simulation. It supports a
    plugin system to make existing libraries such as HDF5, SIONlib or FTI
    available to codes, potentially mixed in a single execution."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"

    maintainers = ["jbigot"]

    version("develop", branch="main", no_cache=True)
    version("1.8.0", sha256="5d353bfa64f45ee4715b88bd30330030f79f2020cd6bede0ad9b8f9beddadea9")
    version("1.7.1", sha256="d67e3a498bfe4491c4e9aeb40015b32481a7902b122f087dcebf05451a3d9ce1")
    version("1.6.0", sha256="ae45d388c98c5e33d552d5e3216c1f92bf97d5dd01c669107084c1f3202fcd5a")
    version("1.5.5", sha256="11bf5db61f23107dfd2135e637e9233524855c78104c57288c6af21d02d1ea53")
    version("1.5.4", sha256="0af1fe9fb85066772a921efdf1f3bb554559066a62eaebce4c9c6afd3b2a5c38")
    version("1.5.3", sha256="aa2fc692f1352d53cf9444f842144648180183313f5c8e7b799e1cb542f6f1ba")
    version("1.5.2", sha256="8dc14fe7ab1c7efed31e4c7522bc43e191be5dbb4227ffedcb04902d95a6fad0")
    version("1.5.1", sha256="3b93d238823fc06e9ec5bb0f9f9d9e1a42fdc0061004df0e898d728aaa93ce23")
    version("1.5.0", sha256="13cbddbdc728a4e19213395034a147bf4e4eb5518c7c734f621a08311343dd4d")
    version("1.4.3", sha256="b7f049cae9e6fb0ddba3a458e15d6f1578876663c04b18f62b052f9698750974")
    version("1.4.2", sha256="b252d5098f3b13b5d883265597f567aa0aa423c95fe4a10554772d485ce37e86")
    version("1.4.1", sha256="55e17629ca373232a8a2530c4ad83403729c74fbe4fcbcfc32e8128800cb40a4")
    version("1.4.0", sha256="1c273d39df14f44ccb3e6d0fc36f88c19fff7a3f819e7d6d6c80b5ac9eed033b")
    version("1.3.1", sha256="a4a1f9d4d6ca6790487edf65e3d7c9f5a5d17fb0bcdf81dfab94efc854fcc387")
    version("1.3.0", sha256="86947c40f025a09ab228360fa002f7241801f5fb70c75f815210d607cf30b200")
    version("1.2.2", sha256="b93a9165d4b9f1e09790c9be3c950530537cf9a9dc01210afc77e411939bdf41")
    version("1.2.1", sha256="0c90294fb2bb9ca5f6b957d9d8f68f3a3039fc256ba92f7e5bbe316768b43037")
    version("1.2.0", sha256="8d5821d473140ea48036e8f03668bf6295d06f8b7561d464cc1b5748bf8d2aa3")
    version("1.1.0", sha256="8f8a33e1538afde81bb2bbbc3ba8fe3942f0824672a364d0eb2055a0255e8b0c")
    version("1.0.1", sha256="c35f6d19cecfc3963c08c8d516386c1cd782fcdbe4e39aa91dd01376d2346cb6")
    version("1.0.0", sha256="57f5bfd2caa35de144651b0f4db82b2a403997799c258ca3a4e632f8ff2cfc1b")
    version("0.6.5", sha256="a1100effb62d43556bd5e50d82f51e51710dbafc8d85c5a2e03ba7c168460be9")

    variant("benchs", default=False, description="Build benchmarks")
    variant("docs", default=False, description="Build documentation")
    variant("tests", default=False, description="Build tests")
    variant("fortran", default=True, description="Enable Fortran support")
    variant("python", default=True, description="Enable Python support")

    depends_on("benchmark@1.5:", type=("link"), when="@1.5:1.7 +benchs")
    depends_on("cmake@3.5:", type=("build"))
    depends_on("cmake@3.10:", type=("build"), when="+docs")
    depends_on("cmake@3.10:", type=("build"), when="+tests")
    depends_on("cmake@3.10:", type=("build"), when="@1.5:")
    depends_on("cmake@3.16.3:", type=("build"), when="@1.8:")
    depends_on("doxygen@1.8.12:", type=("build"), when="+docs")
    depends_on("doxygen@1.8.13:", type=("build"), when="@1.4.3: +docs")
    depends_on("doxygen@1.8.17:", type=("build"), when="@1.8: +docs")
    depends_on("fmt@6.1.2:", type=("link"), when="@1.5")
    depends_on("googletest@1.8: +gmock", type=("link"), when="@:1.7 +tests")
    depends_on("paraconf@1:", type=("link", "run"), when="@1.6:")
    depends_on("paraconf@0.4.16:", type=("link", "run"), when="@1.5:")
    depends_on("paraconf +fortran", type=("link", "run"), when="+fortran")
    depends_on("paraconf@0.4.14: +shared", type=("link", "run"))
    depends_on("pkgconfig", type=("build"))
    depends_on("python@3.6.5:", type=("build", "link", "run"), when="+python")
    depends_on("python@3.8.2:", type=("build", "link", "run"), when="@1.8: +python")
    depends_on("py-pybind11@2.3:2", type=("link"), when="+python")
    depends_on("py-pybind11@:2.11", type=("link"), when="@:1.6 +python")
    depends_on("py-pybind11@2.4.3:", type=("link"), when="@1.8: +python")
    depends_on("spdlog@1.3.1:1", type=("link", "run"))
    depends_on("spdlog@1.5:", type=("link"), when="@1.5:")
    depends_on("zpp@1.0.8:", type=("build"), when="@:1.7 +fortran")
    depends_on("zpp@1.0.15:", type=("build"), when="@1.5:1.7 +fortran")

    root_cmakelists_dir = "pdi"

    def url_for_version(self, version):
        fixed = ""
        if version <= Version("1.7.1"):
            return (
                f"https://gitlab.maisondelasimulation.fr/pdidev/pdi/-/archive/"
                + f"{version}/pdi-{version}.tar.bz2"
            )
        return f"https://github.com/pdidev/pdi/archive/refs/tags/{version}.tar.gz"

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_BENCHMARKING", "benchs"),
            self.define_from_variant("BUILD_DOCUMENTATION", "docs"),
            self.define_from_variant("BUILD_FORTRAN", "fortran"),
            self.define_from_variant("BUILD_PYTHON", "python"),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]
        return args
