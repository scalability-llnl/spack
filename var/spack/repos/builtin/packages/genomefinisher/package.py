# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Genomefinisher(Package):
    """GFinisher is an application tools for refinement and finalization of
    prokaryotic genomes assemblies using the bias of GC Skew to identify
    assembly errors and organizes the contigs/scaffolds with genomes
    references."""

    homepage = "https://gfinisher.sourceforge.net"
    url = "https://sourceforge.net/projects/gfinisher/files/GenomeFinisher_1.4.zip"

    version("1.4", sha256="8efbebaab4b577c72193f14c2c362b96fb949981fd66d2cca1364839af8bf1e3")

    depends_on("java@8:", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "GenomeFinisher.jar"
        install(jar_file, prefix.bin)
        install_tree("lib", prefix.lib)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "genomefinisher.sh")
        script = prefix.bin.genomefinisher
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the jar file
        # jar file.
        java = spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file(jar_file, join_path(prefix.bin, jar_file), script, **kwargs)
