# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Varscan(Package):
    """Variant calling and somatic mutation/CNV detection for next-generation
    sequencing data"""

    homepage = "https://dkoboldt.github.io/varscan/"
    url = "https://github.com/dkoboldt/varscan/releases/download/2.4.2/VarScan.v2.4.2.jar"

    version(
        "2.4.2",
        sha256="34ff6462f91fb6ed3f11e867ab4a179efae5dd8214b97fa261fc616f23d4d031",
        expand=False,
    )

    depends_on("java", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.jar)
        jar_file = "VarScan.v{v}.jar".format(v=self.version.dotted)
        install(jar_file, prefix.jar)

        script_sh = join_path(os.path.dirname(__file__), "varscan.sh")
        script = prefix.bin.varscan
        install(script_sh, script)
        set_executable(script)

        java = join_path(self.spec["java"].prefix, "bin", "java")
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("varscan.jar", join_path(prefix.jar, jar_file), script, **kwargs)

    def setup_run_environment(self, env):
        env.set("VARSCAN_HOME", self.prefix.jar)
        env.set("CLASSPATH", self.prefix.jar)
