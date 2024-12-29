# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mruby(Package):
    """mruby is the lightweight implementation of the Ruby language complying
    to (part of) the ISO standard. Its syntax is Ruby 2.x compatible."""

    homepage = "https://mruby.org/"
    url = "https://github.com/mruby/mruby/archive/refs/tags/3.0.0.tar.gz"
    git = "https://github.com/mruby/mruby.git"

    maintainers("mdorier")
    license("MIT")

    version("master", branch="master")
    version("3.3.0", sha256="53088367e3d7657eb722ddfacb938f74aed1f8538b3717fe0b6eb8f58402af65")
    version("3.2.0", sha256="3c198e4a31d31fe8524013066fac84a67fe6cd6067d92c25a1c79089744cb608")
    version("3.1.0", sha256="64ce0a967028a1a913d3dfc8d3f33b295332ab73be6f68e96d0f675f18c79ca8")
    version("3.0.0", sha256="95b798cdd931ef29d388e2b0b267cba4dc469e8722c37d4ef8ee5248bc9075b0")
    version("2.1.2", sha256="4dc0017e36d15e81dc85953afb2a643ba2571574748db0d8ede002cefbba053b")
    version("2.1.1", sha256="bb27397ee9cb7e0ddf4ff51caf5b0a193d636b7a3c52399684c8c383b41c362a")
    version("2.1.0", sha256="d6733742a07e553c52ab71df08b0604b3b571768bbc0c2729fbf0389d1bb5d13")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cxx_exception", description="Enable C++ exceptions", default=False, when="@3.1.0:")

    depends_on("ruby@3.0.0:", type=("build"))
    depends_on("bison", type=("build"))

    def patch(self):
        """Create a config.rb file for rake to use"""
        import os

        here = os.path.dirname(os.path.abspath(__file__))
        copy(os.path.join(here, "config.rb"), os.path.join("build_config", "spack.rb"))

    def install(self, spec, prefix):
        import os

        rb = spec["ruby"]
        env["MRUBY_CONFIG"] = os.path.join("build_config", "spack.rb")
        env["GEM_PATH"] = os.path.join(
            rb.prefix, "lib", "ruby", "gems", str(rb.version.up_to(2)) + ".0"
        )
        if "+cxx_exception" in spec:
            env["MRUBY_ENABLE_CXX_EXCEPTION"] = "ON"
        rake()
        build_path = os.path.join("build", "host")
        for d in ["include", "lib", "bin", "mrblib", "mrbgems"]:
            prefix_d = os.path.join(prefix, d)
            build_path_d = os.path.join(build_path, d)
            mkdirp(prefix_d)
            install_tree(build_path_d, prefix_d)
        install_tree("include", prefix.include)
