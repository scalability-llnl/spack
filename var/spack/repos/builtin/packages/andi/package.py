# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Andi(AutotoolsPackage):
    """andi is used for for estimating the
    evolutionary distance between closely related genomes."""

    homepage = "https://github.com/EvolBioInf/andi"
    url      = "https://github.com/EvolBioInf/andi/archive/v0.10.tar.gz"

    version('0.10',    sha256='1ff371de0b6db4080e402ded2687947dc2d6913e28626edec21dcf5149489ee8')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('gsl')
    depends_on('libdivsufsort')
