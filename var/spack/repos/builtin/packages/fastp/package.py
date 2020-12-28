# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastp(MakefilePackage):
    """A tool designed to provide fast
    all-in-one preprocessing for FastQ files."""

    homepage = "https://github.com/OpenGene/fastp"
    url      = "https://github.com/OpenGene/fastp/archive/v0.20.0.tar.gz"

    version('0.20.0', sha256='8d751d2746db11ff233032fc49e3bcc8b53758dd4596fdcf4b4099a4d702ac22')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make('install', 'PREFIX={0}'.format(prefix))
