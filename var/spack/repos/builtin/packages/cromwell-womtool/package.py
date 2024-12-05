# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class CromwellWomtool(Package):
    """Command line utilities for interacting with the
    Workflow Object Model (WOM).
    """

    homepage = "https://cromwell.readthedocs.io/en/stable/WOMtool/"
    url = "https://github.com/broadinstitute/cromwell/releases/download/44/womtool-44.jar"

    version(
        "44",
        sha256="b17c0f4933d7b136c7d9760f7858f6439e3c6371f12492e2aeaab3209c28f80a",
        expand=False,
    )

    depends_on("java@8", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "womtool-{0}.jar".format(self.version)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "womtool.sh")
        script = prefix.bin.womtool
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("womtool.jar", join_path(prefix.bin, jar_file), script, **kwargs)
