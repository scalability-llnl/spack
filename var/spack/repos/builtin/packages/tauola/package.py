# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tauola(AutotoolsPackage):
    """ Tauola is a event generator for tau decays."""

    homepage = "https://tauolapp.web.cern.ch/tauolapp/"
    url      = "https://tauolapp.web.cern.ch/tauolapp/resources/TAUOLA.1.1.8/TAUOLA.1.1.8-LHC.tar.gz"

    tags = ['hep']

    version('1.1.8', sha256='3f734e8a967682869cca2c1ffebd3e055562613c40853cc81820d8b666805ed5')

    variant('hepmc', default=True, description="Enable hepmc 2.x support")
    variant('hepmc3', default=False, description="Enable hepmc3 support")
    variant('lhapdf', default=False, description="Enable lhapdf support")
    variant('cxxstd',
            default='11',
            values=('11', '14', '17', '20'),
            multi=False,
            description='Use the specified C++ standard when building.')

    maintainers = ['vvolkl']

    depends_on('hepmc', when='+hepmc')
    depends_on('hepmc3', when='+hepmc3')
    depends_on('lhapdf', when='+lhapdf')

    def flag_handler(self, name, flags):
        if name == 'cflags':
            flags.append('-O2')
        elif name == 'cxxflags':
            flags.append('-O2')
            flags.append('-std=c++{0}'.format(self.spec.variants['cxxstd'].value))
        elif name == 'fflags':
            flags.append('-O2')
        return (None, None, flags)

    def configure_args(self):
        args = ['--with-pic']

        args.extend(self.with_or_without('hepmc', 'prefix'))
        args.extend(self.with_or_without('hepmc3', 'prefix'))
        args.extend(self.with_or_without('lhapdf', 'prefix'))
        return args
