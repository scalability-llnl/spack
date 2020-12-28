# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GosamContrib(AutotoolsPackage):
    """Additional libraries for GoSam MC generator"""

    homepage = "https://gosam.hepforge.org"
    url      = "https://gosam.hepforge.org/downloads/?f=gosam-contrib-2.0.tar.gz"

    tags = ['hep']

    version('2.0', sha256='c05beceea74324eb51c1049773095e2cb0c09c8c909093ee913d8b0da659048d')
    version('1.0', sha256='a29d4232d9190710246abc2ed97fdcd8790ce83580f56a360f3456b0377c40ec')

    def configure_args(self):
        args = ["FFLAGS=-std=legacy"]
        return args
