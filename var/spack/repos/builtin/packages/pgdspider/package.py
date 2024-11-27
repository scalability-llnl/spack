# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Pgdspider(Package):
    """ "PGDSpider is a powerful automated data conversion tool for population
    genetic and genomics programs"""

    homepage = "http://www.cmpg.unibe.ch/software/PGDSpider"
    url = "http://www.cmpg.unibe.ch/software/PGDSpider/PGDSpider_2.1.1.2.zip"

    license("BSD-3-Clause")

    version("2.1.1.5", sha256="8564427caf1f5c6200ba8f22a2bc2ef0fa87ae7c6571e4df3b8438cc00fa121c")
    version("2.1.1.2", sha256="a630ef9f3ef0c36be0d613867c5293378d77b52396ac701bc7b9ec5d3ba7f2e1")

    depends_on("java", type=("build", "run"))
    depends_on("bcftools")
    depends_on("bwa")
    depends_on("samtools")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "PGDSpider{0}-cli.jar".format(self.version.up_to(1))
        install(jar_file, prefix.bin)

        script_sh = join_path(os.path.dirname(__file__), "pgdspider.sh")
        script = prefix.bin.pgdspider
        install(script_sh, script)
        set_executable(script)

        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("pgdspider.jar", join_path(prefix.bin, jar_file), script, **kwargs)
