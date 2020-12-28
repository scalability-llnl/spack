# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Relax(CMakePackage):
    """A set of Reflex libraries for the most common used general data types in
       the LHC Computing Grid"""

    homepage = "https://twiki.cern.ch/twiki/bin/view/LCG/RELAX"
    url      = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/RELAX-1.tar.gz"

    tags = ['hep']

    # The RELAX project stopped using a fixed release model since it moved to
    # ROOT 6, so any package checksum is a lie...
    version('root6')

    depends_on('clhep')
    depends_on('gsl')
    depends_on('hepmc@:2.99.99')
    depends_on('root@6.0.0:')

    def cmake_args(self):
        spec = self.spec
        cxxstd = self.spec['root'].variants['cxxstd'].value
        hepmc_lib = spec['hepmc'].prefix.lib.join('libHepMC.so')

        args = [
            '-DCMAKE_CXX_STANDARD={0}'.format(cxxstd),
            '-DROOT_BINARY_PATH={0}'.format(spec['root'].prefix.bin),
            '-DHEPMC_INCLUDE_DIR={0}'.format(spec['hepmc'].prefix.include),
            '-DHEPMC_LIBRARIES={0}'.format(hepmc_lib)
        ]

        return args
