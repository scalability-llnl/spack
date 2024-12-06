# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPspamm(PythonPackage):
    """Code Generator for Small Sparse Matrix Multiplication"""

    homepage = "https://github.com/SeisSol/PSpaMM/blob/master/README.md"
    git = "https://github.com/SeisSol/PSpaMM.git"

    maintainers("ravil-mobile")

    license("BSD-3-Clause")

    version("develop", branch="master")

    variant("numpy", default=False, description="installs numpy")
    variant("scipy", default=False, description="installs scipy")

    depends_on("py-numpy", when="+numpy")
    depends_on("py-scipy", when="+scipy")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec.prefix)
        env.prepend_path("PYTHONPATH", self.spec.prefix)
