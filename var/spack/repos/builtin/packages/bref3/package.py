# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Bref3(Package):
    """Bref3: Converts from VCF format to bref3 format."""

    homepage = "https://faculty.washington.edu/browning/beagle/beagle.html"

    version(
        "2019-11-25",
        sha256="969c0881050c4a48d19be9ea64bf49fa68c1403b69f9f739bbfd865dda639b2d",
        expand=False,
        url="https://faculty.washington.edu/browning/beagle/bref3.25Nov19.28d.jar",
    )
    version(
        "2019-07-12",
        sha256="8a9c3b6c38e36ef4c05a61108f083005fd985026c67d75a8173088f88816a202",
        expand=False,
        url="https://faculty.washington.edu/browning/beagle/bref3.12Jul19.0df.jar",
    )
    version(
        "2018-01-27",
        sha256="4d32f0b6d536c88d5332d961309466c8c3dd9572907a3755450d26d7ba841083",
        expand=False,
        url="https://faculty.washington.edu/browning/beagle/bref.27Jan18.7e1.jar",
    )
    depends_on("java@8", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = os.path.basename(self.stage.archive_file)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.

        if self.version >= Version("2019"):
            script = prefix.bin.bref3
        else:
            script = prefix.bin.bref

        script_sh = join_path(os.path.dirname(__file__), "bref.sh")
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("bref.jar", join_path(prefix.bin, jar_file), script, **kwargs)
