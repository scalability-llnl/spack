# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Trimmomatic(Package):
    """A flexible read trimming tool for Illumina NGS data."""

    homepage = "http://www.usadellab.org/cms/?page=trimmomatic"
    url = "http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.36.zip"

    license("GPL-3.0-only")

    # Older version aren't explicitly made available, but the URL
    # works as we'd like it to, so...
    version("0.39", sha256="2f97e3a237378d55c221abfc38e4b11ea232c8a41d511b8b4871f00c0476abca")
    version("0.38", sha256="d428af42b6c400a2e7ee5e6b4cab490eddc621f949b086bd7dddb698dcf1647c")
    version("0.36", sha256="4846c42347b663b9d6d3a8cef30da2aec89fc718bf291392c58e5afcea9f70fe")
    version("0.33", sha256="6968583a6c5854a44fff7d427e7ccdcb8dc17f4616082dd390a0633f87a09e3d")

    depends_on("java@8", type="run", when="@:0.38")
    depends_on("java@8:", type="run", when="@0.39:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "trimmomatic-{v}.jar".format(v=self.version.dotted)
        install(jar_file, prefix.bin)

        # Put the adapter files someplace sensible
        install_tree("adapters", prefix.share.adapters)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "trimmomatic.sh")
        script = prefix.bin.trimmomatic
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("trimmomatic.jar", join_path(prefix.bin, jar_file), script, **kwargs)
