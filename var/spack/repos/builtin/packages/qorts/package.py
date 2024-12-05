# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Qorts(RPackage):
    """The QoRTs software package is a fast, efficient, and portable
    multifunction toolkit designed to assist in the analysis, quality
    control, and data management of RNA-Seq and DNA-Seq datasets. Its
    primary function is to aid in the detection and identification of
    errors, biases, and artifacts produced by high-throughput sequencing
    technology."""

    homepage = "https://github.com/hartleys/QoRTs"
    url = "https://github.com/hartleys/QoRTs/releases/download/v1.2.42/QoRTs_1.2.42.tar.gz"

    version("1.2.42", sha256="c9f73ce8d5aac1036d13c50475458a61a24cbe5c0baf7ac65b87a7118c51ec08")

    depends_on("java", type="run")

    resource(
        name="QoRTs.jar",
        url="https://github.com/hartleys/QoRTs/releases/download/v1.2.42/QoRTs.jar",
        sha256="e808d2e05c67ee41eee605b7821aafa7ae894288ebb01d8b1bfb136970c801ce",
        placement="jarfile",
        expand=False,
    )

    @run_after("install")
    def install_jar(self):
        install_tree(join_path(self.stage.source_path, "jarfile"), self.prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "QoRTs.sh")
        script = self.prefix.bin.QoRTs
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"backup": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("QoRTs.jar", join_path(self.prefix.bin, "QoRTs.jar"), script, **kwargs)
