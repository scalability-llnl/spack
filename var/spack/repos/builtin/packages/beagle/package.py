# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Beagle(Package):
    """Beagle is a software package for phasing genotypes and for imputing
    ungenotyped markers."""

    homepage = "https://faculty.washington.edu/browning/beagle/beagle.html"
    maintainers("snehring")

    version(
        "5.4",
        sha256="bcdc78b7229b2e7ffd779bc6131a9c45a1bdb509afbb9fac41e6d5cb39aed19c",
        expand=False,
        url="https://faculty.washington.edu/browning/beagle/beagle.19Apr22.7c0.jar",
    )
    version(
        "5.1",
        sha256="994f926a4ec0eac665631f37c4a961d3f75c966c71841079275364013c90996c",
        expand=False,
        url="https://faculty.washington.edu/browning/beagle/beagle.25Nov19.28d.jar",
    )
    version(
        "5.0",
        sha256="8390fe18b53786b676b67dddae6d1c086d6225e518f6a82047f4138196b48621",
        expand=False,
        url="https://faculty.washington.edu/browning/beagle/beagle.12Jul19.0df.jar",
    )
    version(
        "4.1",
        sha256="6c94610b278fc108c3e80b1134226911be1fc92b7d378ba648ac3eb97c5a3207",
        expand=False,
        url="https://faculty.washington.edu/browning/beagle/beagle.27Jan18.7e1.jar",
    )

    depends_on("java@8:", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = os.path.basename(self.stage.archive_file)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "beagle.sh")
        script = prefix.bin.beagle
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("beagle.jar", join_path(prefix.bin, jar_file), script, **kwargs)
