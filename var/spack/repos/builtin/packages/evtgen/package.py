# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Evtgen(AutotoolsPackage):
    """ EvtGen is a Monte Carlo event generator that simulates
        the decays of heavy flavour particles, primarily B and D mesons. """

    homepage = "https://evtgen.hepforge.org/"
    url      = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/evtgen-R01-07-00.tar.gz"

    tags = ['hep']

    maintainers = ['vvolkl']

    version('02-00-00', sha256='02372308e1261b8369d10538a3aa65fe60728ab343fcb64b224dac7313deb719')
    version('01-07-00', sha256='2648f1e2be5f11568d589d2079f22f589c283a2960390bbdb8d9d7f71bc9c014', preferred=True)

    variant('pythia8', default=True, description='Build with pythia8')
    variant('tauola', default=False, description='Build with tauola')
    variant('photos', default=False, description='Build with photos')

    patch("g2c.patch")

    depends_on('hepmc@:2.99.99')
    depends_on("pythia8", when="+pythia8")
    depends_on("tauola", when="+tauola")
    depends_on("photos", when="+photos")

    conflicts("^pythia8+evtgen", when="+pythia8",
              msg="Building pythia with evtgen bindings and "
              "evtgen with pythia bindings results in a circular dependency "
              "that cannot be resolved at the moment! "
              "Use evtgen+pythia8^pythia8~evtgen.")

    def configure_args(self):
        args = []

        args.append('--hepmcdir=%s' % self.spec["hepmc"].prefix)
        if '+pythia8' in self.spec:
            args.append('--pythiadir=%s' % self.spec['pythia8'].prefix)
        if '+photos' in self.spec:
            args.append('--photosdir=%s' % self.spec['photos'].prefix)
        if '+tauola' in self.spec:
            args.append('--tauoladir=%s' % self.spec['tauola'].prefix)

        return args

    def build(self, spec, prefix):
        # avoid parallel compilation errors
        # due to libext_shared depending on lib_shared
        make('lib_shared')
        make('all')

    def setup_run_environment(self, env):
        env.set("EVTGEN", self.prefix.share)
