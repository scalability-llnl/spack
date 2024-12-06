# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bamutil(MakefilePackage):
    """bamUtil is a repository that contains several programs
    that perform operations on SAM/BAM files. All of these programs
    are built into a single executable, bam.
    """

    homepage = "https://genome.sph.umich.edu/wiki/BamUtil"
    url = "https://github.com/statgen/bamUtil/archive/refs/tags/v1.0.15.tar.gz"
    git = "https://github.com/statgen/bamUtil.git"
    maintainers("snehring")

    version("1.0.15", sha256="24ac4bdb81eded6e33f60dba85ec3d32ebdb06d42f75df775c2632bbfbd8cce9")
    version(
        "1.0.13",
        sha256="16c1d01c37d1f98b98c144f3dd0fda6068c1902f06bd0989f36ce425eb0c592b",
        url="https://genome.sph.umich.edu/w/images/7/70/BamUtilLibStatGen.1.0.13.tgz",
    )

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("git", type="build", when="@1.0.15:")

    patch("libstatgen-issue-9.patch", when="@1.0.13")
    patch("libstatgen-issue-19.patch", when="@1.0.13")
    patch("libstatgen-issue-17.patch", when="@1.0.13")
    patch("libstatgen-issue-7.patch", when="@1.0.13")
    patch("verifybamid-issue-8.patch", when="@1.0.13")

    parallel = False

    @when("@1.0.15")
    def edit(self, spec, prefix):
        filter_file("git://", "https://", "Makefile.inc", string=True)

    @when("@1.0.15:")
    def build(self, spec, prefix):
        make("cloneLib")
        make()

    @property
    def install_targets(self):
        return ["install", "INSTALLDIR={0}".format(self.prefix.bin)]
