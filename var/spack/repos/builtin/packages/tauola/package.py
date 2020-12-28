# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tauola(AutotoolsPackage):
    """ Tauola is a event generator for tau decays."""

    homepage = "https://tauolapp.web.cern.ch/tauolapp/"
    url      = "https://tauolapp.web.cern.ch/tauolapp/resources/TAUOLA.1.1.8/TAUOLA.1.1.8-LHC.tar.gz"

    tags = ['hep']

    version('1.1.8', sha256='3f734e8a967682869cca2c1ffebd3e055562613c40853cc81820d8b666805ed5')

    maintainers = ['vvolkl']

    depends_on('hepmc@:2.99.99')

    def configure_args(self):
        args = []

        args.append('--with-hepmc=%s' % self.spec["hepmc"].prefix)
        args.append('--without-hepmc3')
        return args
