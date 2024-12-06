# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Msmc2(MakefilePackage):
    """
    This program implements MSMC2, a method to infer population size history
    and population separation history from whole genome sequencing data.
    """

    homepage = "https://github.com/stschiff/msmc2"
    url = "https://github.com/stschiff/msmc2/archive/v2.1.1.tar.gz"

    maintainers("robqiao")

    license("GPL-3.0-or-later")

    version("2.1.4", sha256="e513723b9e956f01de8de89ff6d32c071f509512425185d12faa5bb76cf440d0")
    version("2.1.2", sha256="c8c2b6ed6ef1b5d6e6e15ec0d968288e5bdae2bea1f3b4ec790f599e96bb26cd")
    version("2.1.1", sha256="151dd75a8b0371ff94eed9504a7a73a2924e10466de30c230c1bb3c35a1a0913")
    version("2.0.2", sha256="91152b2494342148ff84a1e5c6d2f5f0d53acba12722cd68ff5807ba4e82af55")
    version("2.0.1", sha256="97e859e6f08689baf29d3c61b6904cfa5a292f8ce7b3532e055ce3047d8472f4")
    version("2.0.0", sha256="9de38239f6e729a0f6f492ca671e2e70541eb5db558d816e64184c06611a1c7e")

    depends_on("gsl", type=("build", "run"))
    depends_on("dmd@:2.081.0", type="build")

    def edit(self, spec, prefix):
        # Set DMD compiler
        filter_file(
            "dmd", join_path(self.spec["dmd"].prefix.linux.bin64, "dmd"), "Makefile", string=True
        )

        gsllibdir = spec["gsl"].libs.directories[0]

        # Set GSLDIR
        filter_file(
            "GSLDIR=/usr/local/lib", "GSLDIR={0}".format(gsllibdir), "Makefile", string=True
        )

    def install(self, spec, prefix):
        install_tree("build/release", prefix.bin)
