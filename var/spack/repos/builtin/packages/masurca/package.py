# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Masurca(Package):
    """MaSuRCA is whole genome assembly software. It combines the efficiency
    of the de Bruijn graph and Overlap-Layout-Consensus (OLC)
    approaches."""

    homepage = "https://www.genome.umd.edu/masurca.html"
    url = "https://github.com/alekseyzimin/masurca/releases/download/v3.3.1/MaSuRCA-3.3.1.tar.gz"

    license("GPL-3.0-only")

    version("4.1.1", sha256="8758f6196bf7f57e24e08bda84abddfff08feb4cea204c0eb5e1cb9fe8198573")
    version("4.1.0", sha256="15078e24c79fe5aabe42748d64f95d15f3fbd7708e84d88fc07c4b7f2e4b0902")
    version("4.0.9", sha256="a31c2f786452f207c0b0b20e646b6c85b7357dcfd522b697c1009d902d3ed4cf")
    version("4.0.5", sha256="db525c26f2b09d6b359a2830fcbd4a3fdc65068e9a116c91076240fd1f5924ed")
    version("4.0.1", sha256="68628acaf3681d09288b48a35fec7909b347b84494fb26c84051942256299870")
    version("3.3.1", sha256="587d0ee2c6b9fbd3436ca2a9001e19f251b677757fe5e88e7f94a0664231e020")
    version("3.2.9", sha256="795ad4bd42e15cf3ef2e5329aa7e4f2cdeb7e186ce2e350a45127e319db2904b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("perl", type=("build", "run"))
    depends_on(Boost.with_default_variants)
    depends_on("zlib-api")
    patch("arm.patch", when="target=aarch64:")

    def patch(self):
        filter_file("#include <sys/sysctl.h>", "", "global-1/CA8/src/AS_BAT/memoryMappedFile.H")
        if self.spec.target.family == "aarch64":
            for makefile in "Makefile.am", "Makefile.in":
                m = join_path("global-1", "prepare", makefile)
                filter_file("-minline-all-stringops", "", m)
                m = join_path("global-1", makefile)
                filter_file("-minline-all-stringops", "", m)

    def setup_build_environment(self, env):
        if self.spec.satisfies("@4:"):
            env.set("DEST", self.prefix)

    def install(self, spec, prefix):
        installer = Executable("./install.sh")
        installer()
        if self.spec.satisfies("@:4"):
            install_tree(".", prefix)
