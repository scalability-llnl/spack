# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Haploview(Package):
    """Haploview is designed to simplify and expedite the process of haplotype
    analysis."""

    homepage = "https://www.broadinstitute.org/haploview/haploview"
    url = "https://downloads.sourceforge.net/project/haploview/release/Haploview4.1.jar"

    version(
        "4.1",
        sha256="b3ffe4c3d8bbab6af5eebf89a2dccdb185280088f70ae84c84be60f85f10201d",
        expand=False,
    )

    depends_on("java", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "Haploview{v}.jar".format(v=self.version)
        install(jar_file, prefix.bin)

        script_sh = join_path(os.path.dirname(__file__), "haploview.sh")
        script = prefix.bin.haploview
        install(script_sh, script)
        set_executable(script)

        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("haploview.jar", join_path(prefix.bin, jar_file), script, **kwargs)
