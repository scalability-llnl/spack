# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Astral(Package):
    """ASTRAL is a tool for estimating an unrooted species tree given a set of
    unrooted gene trees."""

    homepage = "https://github.com/smirarab/ASTRAL"
    url = "https://github.com/smirarab/ASTRAL/archive/v4.10.7.tar.gz"

    license("Apache-2.0")

    version("5.7.1", sha256="8aa6fd4324efca325d3dde432517090fac314bea95f407b1dd59977181fec77e")
    version(
        "5.6.1",
        sha256="b49a67c9fe19c0c92a89dc2f1a3928840e698a53054a595c61546ca98448a076",
        url="https://github.com/smirarab/ASTRAL/archive/untagged-697f19dbce69929ece09.tar.gz",
    )
    version("4.10.7", sha256="314b49e0129ec06a7c78a1b60d590259ede6a5e75253407031e108d8048fcc79")

    depends_on("java@11", type=("build", "run"))
    depends_on("zip", type="build")

    def install(self, spec, prefix):
        make = Executable("./make.sh")
        make()
        mkdirp(prefix.bin)
        install_tree("lib", prefix.tools.lib)
        jar_file = f"astral.{self.version}.jar"
        install(jar_file, prefix.tools)

        script_sh = join_path(os.path.dirname(__file__), "astral.sh")
        script = prefix.bin.astral
        install(script_sh, script)
        set_executable(script)

        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("astral.jar", join_path(prefix.tools, jar_file), script, **kwargs)

    def setup_run_environment(self, env):
        env.set("ASTRAL_HOME", self.prefix.tools)
