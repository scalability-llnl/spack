# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUv(PythonPackage):
    """An extremely fast Python package and project manager, written in Rust."""

    homepage = "https://github.com/astral-sh/uv"
    pypi = "uv/0.4.15.tar.gz"

    license("APACHE 2.0 or MIT")

    version("0.4.27", sha256="c13eea45257362ecfa2a2b31de9b62fbd0542e211a573562d98ab7c8fc50d8fc")
    version("0.4.17", sha256="01564bd760eff885ad61f44173647a569732934d1a4a558839c8088fbf75e53f")
    version("0.4.16", sha256="2144995a87b161d063bd4ef8294b1e948677bd90d01f8394d0e3fca037bb847f")
    version("0.4.15", sha256="8e36b8e07595fc6216d01e729c81a0b4ff029a93cc2ef987a73d3b650d6d559c")

    depends_on("rust", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-maturin@1:1", type="build")
    depends_on("cmake", type="build")

    def setup_build_environment(self, env):
        env.set("CMAKE", self.spec["cmake"].prefix.bin.cmake)

    executables = ["^uv$"]
