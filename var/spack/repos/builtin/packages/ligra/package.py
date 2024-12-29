# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ligra(MakefilePackage):
    """A Lightweight Graph Processing Framework for Shared Memory"""

    homepage = "https://jshun.github.io/ligra/"
    url = "https://github.com/jshun/ligra/archive/v.1.5.tar.gz"

    license("MIT")

    version("1.5", sha256="74113a5a3c19a0e319a5b9ebefc8a67c5d18d4d2a9670363092a966f4163f6b7")
    version("1.4", sha256="bb70a1428c71cf2f7e1512cdedcd8330c754f5a2c8309ab9d9666591cff6a4e1")
    version("1.3", sha256="df848038734bb9724d6c9bd95595c91eb6b07027642be93bff161f020ff257e4")
    version("1.2", sha256="ec8778b0762772fc78437243ccaee72066d67a310bc352d6665dd2de520c04cc")
    version("1.1", sha256="a7311b96fabc286a8f1250d8a6e2d1b1e4545c720fa6bb4acf7ed31211fcc99a")
    version("1.0", sha256="fb39ae0a3eddb26f37b8cc0a543648575a50bcc488cecd4a5f1beaaf2458736c")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Build with OpenMP")
    variant("mkl", default=False, description="Build with Intel MKL")
    # TODO: Add cilk variant when spack has a cilk plus package created.

    depends_on("mkl", when="+mkl")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+openmp"):
            env.set("OPENMP", "1")
        # when +mkl, MKLROOT will be defined by intel-mkl package,
        # triggering a build with mkl support

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.apps)
        env.prepend_path("PATH", self.prefix.utils)

    def build(self, spec, prefix):
        make("-C", "apps")
        make("-C", "utils")

    def install(self, spec, prefix):
        install_tree(".", prefix)
        install_tree("ligra", prefix.include)
