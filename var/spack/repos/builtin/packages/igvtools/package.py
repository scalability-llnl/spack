# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Igvtools(Package):
    """IGVTools suite of command-line utilities for preprocessing data
    files"""

    homepage = "https://software.broadinstitute.org/software/igv/home"
    url = "https://data.broadinstitute.org/igv/projects/downloads/2.3/igvtools_2.3.98.zip"

    version("2.3.98", sha256="07027c179f25960bab9919f255c0f8e08f0861861ac6dc02d92be8313e0316a4")

    depends_on("java@8:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "igvtools.jar"
        install(jar_file, prefix.bin)
        install_tree("genomes", prefix.genomes)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "igvtools.sh")
        script = prefix.bin.igvtools
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file(jar_file, join_path(prefix.bin, jar_file), script, **kwargs)
