# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

from spack.package import *


class Herwig3(AutotoolsPackage):
    """Herwig is a multi-purpose particle physics event generator."""

    homepage = "https://herwig.hepforge.org"
    url      = "https://herwig.hepforge.org/downloads/Herwig-7.2.1.tar.bz2"

    tags = ['hep']

    version('7.2.1', sha256='d4fff32f21c5c08a4b2e563c476b079859c2c8e3b78d853a8a60da96d5eea686')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('lhapdf',   type='link')
    depends_on('thepeg@2.2.1', when='@7.2.1', type='link')
    depends_on('boost', type='link')
    depends_on('python', type=('build', 'run'))
    depends_on('gsl', type='link')
    depends_on('fastjet', type='link')
    depends_on('vbfnlo@3:', type='link')
    depends_on('madgraph5amc', type='link')
    depends_on('njet', type='link')
    depends_on('py-gosam', type='link', when='^python@2.7:2.7.99')
    depends_on('gosam-contrib', type='link')
    depends_on('openloops', type='link')

    force_autoreconf = True

    def autoreconf(self, spec, prefix):
        autoreconf('--install', '--verbose', '--force')

    @run_before('build')
    def install_lhapdfsets(self):
        mkdirp(self.prefix.tmppdfsets)
        lhapdf = which('lhapdf')
        if self.spec.satisfies('@7.2.0:'):
            lhapdf("--pdfdir=" + self.prefix.tmppdfsets,
                   # "--source=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current",
                   # "--listdir=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current",
                   "install", "MHT2014lo68cl", "MMHT2014nlo68cl",
                   "CT14lo", "CT14nlo")

    def configure_args(self):
        args = ['--with-gsl=' + self.spec['gsl'].prefix,
                '--with-thepeg=' + self.spec['thepeg'].prefix,
                '--with-thepeg-headers=' + self.spec['thepeg'].prefix.include,
                '--with-fastjet=' + self.spec['fastjet'].prefix,
                '--with-boost=' + self.spec['boost'].prefix,
                '--with-madgraph=' + self.spec['madgraph5amc'].prefix,
                '--with-openloops=' + self.spec['openloops'].prefix,
                '--with-gosam-contrib=' + self.spec['gosam-contrib'].prefix,
                '--with-njet=' + self.spec['njet'].prefix,
                '--with-vbfnlo=' + self.spec['vbfnlo'].prefix]

        if self.spec.satisfies('^python@2.7:2.7.99'):
            args.append('--with-gosam=' + self.spec['gosam'].prefix)

        return args

    def flag_handler(self, name, flags):
        if name == 'fcflags':
            flags.append('-std=legacy')
            return (None, flags, None)
        elif name in ['cflags', 'cxxflags', 'cppflags']:
            return (None, flags, None)

        return (flags, None, None)

    def setup_build_environment(self, env):
        thepeg_home = self.spec['thepeg'].prefix
        env.prepend_path('LD_LIBRARY_PATH', thepeg_home.lib.ThePEG)
        env.set('LHAPDF_DATA_PATH', self.prefix.tmppdfsets)
        env.set('HERWIGINCLUDE', '-I' + self.prefix.include)
        env.set('BOOSTINCLUDE', '-I' + self.spec['boost'].prefix.include)
        env.set('HERWIGINSTALL', self.prefix)

    def build(self, spec, prefix):
        make()
        with working_dir('MatrixElement/FxFx'):
            make()

    def install(self, spec, prefix):
        make('install')
        with working_dir('MatrixElement/FxFx'):
            make('install')

    @run_after('install')
    def remove_lhapdfsets(self):
        shutil.rmtree(self.prefix.tmppdfsets)
