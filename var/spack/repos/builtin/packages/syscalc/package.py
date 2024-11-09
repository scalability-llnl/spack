# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Syscalc(MakefilePackage):
    """A tool to derive theoretical systematic uncertainties"""

    homepage = "https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/SysCalc"
    url = "https://bazaar.launchpad.net/~mgtools/mg5amcnlo/SysCalc/tarball/17"

    version(
        "1.1.7",
        sha256="ac73df0f9f195eb62601fafc2eede3db17a562750f7971616870d6df4abd1b6c",
        url="https://bazaar.launchpad.net/~mgtools/mg5amcnlo/SysCalc/tarball/17",
        extension=".tgz",
    )

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    tags = ["hep"]

    depends_on("lhapdf@6:")

    def url_for_version(self, version):
        url = self.url.rsplit("/", 1)[0]
        url += "/SysCalc_V{0}.tar.gz"

        url = url.format(version)
        return url

    def build(self, spec, prefix):
        with working_dir("mg5amcnlo/SysCalc"):
            make("all")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir("mg5amcnlo/SysCalc"):
            install("sys_calc", prefix.bin)
            install_tree("include", prefix.include)
