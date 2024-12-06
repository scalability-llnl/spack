# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import unlink

from spack.package import *


class Pasta(PythonPackage):
    """PASTA (Practical Alignment using SATe and Transitivity)"""

    homepage = "https://github.com/smirarab/pasta"
    git = "https://github.com/smirarab/pasta"
    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("1.9.0", commit="370ae2d21ef461bcb2cef7c20cb5a4a1db7ff99d")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-dendropy@4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("java", type="run")

    resource(
        name="tools",
        git="https://github.com/smirarab/sate-tools-linux",
        commit="90fb074d61af554e94d1a67583dd3a80b11417ea",
        destination=".",
    )

    def setup_build_environment(self, env):
        tools = join_path(self.prefix, "sate-tools-linux")
        env.set("PASTA_TOOLS_DEVDIR", tools)
        env.set("PASTA_TOOLS_RUNDIR", self.prefix.bin)

    def setup_run_environment(self, env):
        env.set("PASTA_TOOLS_RUNDIR", self.prefix.bin)

    @run_before("install")
    def install_resource(self):
        with working_dir(self.stage.source_path):
            tools = tools = join_path(self.prefix, "sate-tools-linux")
            install_tree("sate-tools-linux", tools)

    @run_after("install")
    def install_stragglers(self):
        # install script negelects to actually copy some things
        scripts = join_path(self.stage.source_path, "resources", "scripts")
        with working_dir(scripts):
            unlink(join_path(self.prefix.bin, "hmmeralign"))
            install("hmmeralign", self.prefix.bin)
        src_bin = join_path(self.stage.source_path, "bin")
        with working_dir(src_bin):
            install("treeshrink", self.prefix.bin)
