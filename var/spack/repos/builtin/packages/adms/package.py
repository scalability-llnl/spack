# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Adms(AutotoolsPackage):
    """ADMS is a code generator that converts electrical compact device models
    specified in high-level description language into ready-to-compile c code
    for the API of spice simulators."""

    homepage = "https://sourceforge.net/projects/mot-adms/"
    url = "https://github.com/Qucs/ADMS/releases/download/release-2.3.7/adms-2.3.7.tar.gz"
    git = "https://github.com/Qucs/ADMS.git"

    maintainers("cessenat")

    license("GPL-3.0-only")

    version("master", branch="master")
    version("2.3.7", sha256="3a78e1283ecdc3f356410474b3ff44c4dcc82cb89772087fd3bbde8a1038ce08")

    depends_on("c", type="build")  # generated

    depends_on("bison@2.5:", type="build")
    depends_on("flex", type="build")
    depends_on("perl-xml-libxml", type="build")

    @when("@master")
    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("./bootstrap.sh")
