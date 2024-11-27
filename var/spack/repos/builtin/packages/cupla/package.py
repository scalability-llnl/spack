# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cupla(Package):
    """C++ User interface for the Platform independent Library Alpaka"""

    homepage = "https://github.com/alpaka-group/cupla"
    git = "https://github.com/alpaka-group/cupla.git"
    url = "https://github.com/alpaka-group/cupla/archive/refs/tags/0.3.0.tar.gz"

    maintainers("vvolkl")

    version("develop", branch="dev")
    version("master", branch="master")
    version("0.3.0", sha256="035512517167967697e73544c788453de5e3f0bc4e8d4864b41b2e287365cbaf")

    depends_on("cxx", type="build")  # generated

    depends_on("alpaka@0.6.0:0.7")

    def install(self, spec, prefix):
        install_tree("include", self.prefix.include)
        install_tree("src", self.prefix.src)
        install_tree("doc", self.prefix.share.cupla.doc)
        install_tree("example", self.prefix.example)
        install_tree("cmake", self.prefix.cmake)
        install("Findcupla.cmake", self.prefix)
        install("cuplaConfig.cmake", self.prefix)

    def setup_run_environment(self, env):
        env.set("CUPLA_ROOT", self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)
        env.set("CUPLA", self.prefix.share.cupla)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("CUPLA_ROOT", self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)
        env.set("CUPLA", self.prefix.share.cupla)
