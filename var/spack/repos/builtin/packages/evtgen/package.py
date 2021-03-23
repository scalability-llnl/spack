# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Evtgen(CMakePackage):
    """ EvtGen is a Monte Carlo event generator that simulates
        the decays of heavy flavour particles, primarily B and D mesons. """

    homepage = "https://evtgen.hepforge.org/"
    url      = "https://evtgen.hepforge.org/downloads?f=EvtGen-02.00.00.tar.gz"

    tags = ['hep']

    maintainers = ['vvolkl']

    version('02.00.00', sha256='02372308e1261b8369d10538a3aa65fe60728ab343fcb64b224dac7313deb719')
    # switched to cmake in 02.00.00
    version('01.07.00', sha256='2648f1e2be5f11568d589d2079f22f589c283a2960390bbdb8d9d7f71bc9c014', deprecated=True)

    variant('pythia8', default=True, description='Build with pythia8')
    variant('tauola', default=False, description='Build with tauola')
    variant('photos', default=False, description='Build with photos')
    variant('hepmc3', default=False, description='Link with hepmc3 (instead of hepmc)')

    patch("g2c.patch", when='@01.07.00')

    depends_on('hepmc', when='~hepmc3')
    depends_on('hepmc3', when='+hepmc3')
    depends_on("pythia8", when="+pythia8")
    depends_on("tauola~hepmc3", when="+tauola~hepmc3")
    depends_on("photos~hepmc3", when="+photos~hepmc3")
    depends_on("tauola+hepmc3", when="+tauola+hepmc3")
    depends_on("photos+hepmc3", when="+photos+hepmc3")

    conflicts("^pythia8+evtgen", when="+pythia8",
              msg="Building pythia with evtgen bindings and "
              "evtgen with pythia bindings results in a circular dependency "
              "that cannot be resolved at the moment! "
              "Use evtgen+pythia8^pythia8~evtgen.")
    conflicts('+hepmc3', when='@:01.99.99',
              msg='hepmc3 support was added in 02.00.00')

    def cmake_args(self):
        args = []

        args.append(self.define_from_variant('EVTGEN_PYTHIA', 'pythia8'))
        args.append(self.define_from_variant('EVTGEN_TAUOLA', 'tauola'))
        args.append(self.define_from_variant('EVTGEN_PHOTOS', 'photos'))
        args.append(self.define_from_variant('EVTGEN_HEPMC3', 'hepmc3'))

        return args

    # Taken from AutotoolsPackage
    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in
        :py:meth:`~.AutotoolsPackage.configure_args`
        and an appropriately set prefix.
        """
        options = getattr(self, 'configure_flag_args', [])
        options += ['--prefix={0}'.format(prefix)]
        options += self.configure_args()

        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).configure(*options)

    @when('@:01.99.99')
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

    @when('@:01.99.99')
    def cmake(self, spec, prefix):
        pass

    @when('@:01.99.99')
    def build(self, spec, prefix):
        self.configure(spec, prefix)
        # avoid parallel compilation errors
        # due to libext_shared depending on lib_shared
        with working_dir(self.build_directory):
            make('lib_shared')
            make('all')

    @when('@:01.99.99')
    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('install')

    def setup_run_environment(self, env):
        env.set("EVTGEN", self.prefix.share)
