# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pythia8(AutotoolsPackage):
    """The Pythia program is a standard tool for the generation of events in
    high-energy collisions, comprising a coherent set of physics models for
    the evolution from a few-body hard process to a complex multiparticle
    final state."""

    homepage = "http://home.thep.lu.se/Pythia/"
    url      = "http://home.thep.lu.se/~torbjorn/pythia8/pythia8244.tgz"

    tags = ['hep']

    maintainers = ['ChristianTackeGSI']

    version('8304', sha256='d3897018fb6d545eaf93bf43f32580c984a9bff49259d9dd29dff6edfbe9d9a1')
    version('8303', sha256='cd7c2b102670dae74aa37053657b4f068396988ef7da58fd3c318c84dc37913e')
    version('8302', sha256='7372e4cc6f48a074e6b7bc426b040f218ec4a64b0a55e89da6af56933b5f5085')
    version('8301', sha256='51382768eb9aafb97870dca1909516422297b64ef6a6b94659259b3e4afa7f06')
    version('8244', sha256='e34880f999daf19cdd893a187123927ba77d1bf851e30f6ea9ec89591f4c92ca')
    version('8240', sha256='d27495d8ca7707d846f8c026ab695123c7c78c7860f04e2c002e483080418d8d')
    version('8235', sha256='e82f0d6165a8250a92e6aa62fb53201044d8d853add2fdad6d3719b28f7e8e9d')
    version('8230', sha256='332fad0ed4f12e6e0cb5755df0ae175329bc16bfaa2ae472d00994ecc99cd78d')
    version('8212', sha256='f8fb4341c7e8a8be3347eb26b00329a388ccf925313cfbdba655a08d7fd5a70e')

    variant('shared', default=True, description='Build shared library')
    variant('hepmc', default=True, description='Build HepMC2 extensions')
    variant('evtgen', default=False, description='Build EvtGen extensions')
    variant('root', default=False, description='Build ROOT extensions')
    variant('fastjet', default=False, description='Build fastjet extensions')

    depends_on('rsync', type='build')
    depends_on('hepmc@:2.99.99', when="+hepmc")
    depends_on('root', when="+root")
    depends_on('evtgen', when="+evtgen")
    depends_on("fastjet@3.0.0:", when="+fastjet")

    conflicts("^evtgen+pythia8", when="+evtgen",
              msg="Building pythia with evtgen bindings and "
              "evtgen with pythia bindings results in a circular dependency "
              "that cannot be resolved at the moment! "
              "Use pythia8+evtgen^evtgen~pythia8")

    def configure_args(self):
        args = []

        if '+shared' in self.spec:
            args.append('--enable-shared')
        if '+hepmc' in self.spec:
            args.append('--with-hepmc=%s' % self.spec["hepmc"].prefix)
        else:
            args.append('--without-hepmc')
        if '+fastjet' in self.spec:
            args.append('--with-fastjet3=%s' % self.spec["fastjet"].prefix)
        else:
            args.append('--without-fastjet3')
        if '+evtgen' in self.spec:
            args.append('--with-evtgen=%s' % self.spec["evtgen"].prefix)
        else:
            args.append('--without-evtgen')
        if '+root' in self.spec:
            args.append('--with-root=%s' % self.spec["root"].prefix)
        else:
            args.append('--without-root')

        return args

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('PYTHIA8', self.prefix)
        env.set('PYTHIA8DATA', self.prefix.share.Pythia8.xmldoc)
