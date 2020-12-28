# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Photos(AutotoolsPackage):
    """ Photos is a Monte Carlo program for bremsstrahlung in the decay
         of particles and resonances."""

    homepage = "http://photospp.web.cern.ch/photospp/"
    url      = "http://photospp.web.cern.ch/photospp/resources/PHOTOS.3.61/PHOTOS.3.61-LHC.tar.gz"

    tags = ['hep']

    version('3.61', sha256='acd3bcb769ba2a3e263de399e9b89fd6296405c9cbc5045b83baba3e60db4b26')

    maintainers = ['vvolkl']

    depends_on('hepmc@:2.99.99')

    def configure_args(self):
        args = []

        args.append('--with-hepmc=%s' % self.spec["hepmc"].prefix)
        args.append('--without-hepmc3')
        return args
