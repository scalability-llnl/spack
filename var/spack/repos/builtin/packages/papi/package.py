# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import sys

import llnl.util.filesystem as fs
from spack.package import *


class Papi(AutotoolsPackage):
    """PAPI provides the tool designer and application engineer with a
       consistent interface and methodology for use of the performance
       counter hardware found in most major microprocessors. PAPI
       enables software engineers to see, in near real time, the
       relation between software performance and processor events.  In
       addition Component PAPI provides access to a collection of
       components that expose performance measurement opportunities
       across the hardware and software stack."""
    homepage = "http://icl.cs.utk.edu/papi/index.html"
    maintainers = ['G-Ragghianti']

    url = "http://icl.cs.utk.edu/projects/papi/downloads/papi-5.4.1.tar.gz"
    version('6.0.0.1', sha256='3cd7ed50c65b0d21d66e46d0ba34cd171178af4bbf9d94e693915c1aca1e287f')
    version('6.0.0', sha256='3442709dae3405c2845b304c06a8b15395ecf4f3899a89ceb4d715103cb4055f')
    version('5.7.0', sha256='d1a3bb848e292c805bc9f29e09c27870e2ff4cda6c2fba3b7da8b4bba6547589')
    version('5.6.0', sha256='49b7293f9ca2d74d6d80bd06b5c4be303663123267b4ac0884cbcae4c914dc47')
    version('5.5.1', sha256='49dc2c2323f6164c4a7e81b799ed690ee73158671205e71501f849391dd2c2d4')
    version('5.5.0', sha256='3ea15e6cc2354017335b659c1635409ddab1414e70573aa4df91fd892e99f98d')
    version('5.4.3', sha256='3aefd581e274f0a103f001f1ffd1009019b297c637e97f4b8c5fc13fa5a1e675')
    version('5.4.1', sha256='e131c1449786fe870322a949e44f974a5963824f683232e653fb570cc65d4e87')
    version('5.3.0', sha256='99f2f36398b370e75d100b4a189d5bc0ac4f5dd66df44d441f88fd32e1421524')

    variant('example', default=True, description='Install the example files')
    variant('infiniband', default=False, description='Enable Infiniband support')
    variant('powercap', default=False, description='Enable powercap interface support')
    variant('rapl', default=False, description='Enable RAPL support')
    variant('lmsensors', default=False, description='Enable lm_sensors support')
    variant('sde', default=False, description='Enable software defined events')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('nvml', default=False, description='Enable NVML support')

    variant('shared', default=True, description='Build shared libraries')
    # PAPI requires building static libraries, so there is no "static" variant
    variant('static_tools', default=False, description='Statically link the PAPI tools')
    # The PAPI configure option "--with-shlib-tools" is deprecated
    # and therefore not implemented here

    depends_on('lm-sensors', when='+lmsensors')
    depends_on('cuda', when='+cuda')
    depends_on('cuda', when='+nvml')

    conflicts('%gcc@8:', when='@5.3.0', msg='Requires GCC version less than 8.0')
    conflicts('+sde', when='@:5', msg='Software defined events (SDE) added in 6.0.0')
    conflicts('^cuda', when='@:5', msg='CUDA support for versions < 6.0.0 not implemented')

    # This is the only way to match exactly version 6.0.0 without also
    # including version 6.0.0.1 due to spack version matching logic
    conflicts('@5.9.99999:6.0.0.a', when='+static_tools', msg='Static tools cannot build on version 6.0.0')

    # Does not build with newer versions of gcc, see
    # https://bitbucket.org/icl/papi/issues/46/cannot-compile-on-arch-linux
    patch('https://bitbucket.org/icl/papi/commits/53de184a162b8a7edff48fed01a15980664e15b1/raw', sha256='64c57b3ad4026255238cc495df6abfacc41de391a0af497c27d0ac819444a1f8', when='@5.4.0:5.6.99%gcc@8:')
    patch('crayftn-fixes.patch', when='@6.0.0:%cce@9:')

    configure_directory = 'src'

    def setup_build_environment(self, env):
        if '+lmsensors' in self.spec and self.version >= Version('6'):
            env.set('PAPI_LMSENSORS_ROOT', self.spec['lm-sensors'].prefix)
        if '^cuda' in self.spec:
            env.set('PAPI_CUDA_ROOT', self.spec['cuda'].prefix)

    setup_run_environment = setup_build_environment

    def configure_args(self):
        spec = self.spec
        # PAPI uses MPI if MPI is present; since we don't require
        # an MPI package, we ensure that all attempts to use MPI
        # fail, so that PAPI does not get confused
        options = ['MPICC=:']
        # Build a list of PAPI components
        components = filter(
            lambda x: spec.variants[x].value,
            ['example', 'infiniband', 'powercap', 'rapl', 'lmsensors', 'sde',
             'cuda', 'nvml'])
        if components:
            options.append('--with-components=' + ' '.join(components))

        build_shared = 'yes' if '+shared' in spec else 'no'
        options.append('--with-shared-lib=' + build_shared)

        if '+static_tools' in spec:
            options.append('--with-static-tools')

        return options

    @run_before('configure')
    def fortran_check(self):
        if not self.compiler.fc:
            msg = 'PAPI requires a Fortran compiler to build'
            raise RuntimeError(msg)

    @run_before('configure')
    def component_configure(self):
        configure_script = Executable('./configure')
        if '+lmsensors' in self.spec and self.version < Version('6'):
            with working_dir("src/components/lmsensors"):
                configure_script(
                    "--with-sensors_incdir=%s/sensors" %
                    self.spec['lm-sensors'].headers.directories[0],
                    "--with-sensors_libdir=%s" %
                    self.spec['lm-sensors'].libs.directories[0])

    @run_before('build')
    def fix_build(self):
        # Don't use <malloc.h>
        for level in [".", "*", "*/*"]:
            files = glob.iglob(join_path(level, "*.[ch]"))
            filter_file(r"\<malloc\.h\>", "<stdlib.h>", *files)

    @run_after('install')
    def fix_darwin_install(self):
        # The shared library is not installed correctly on Darwin
        if sys.platform == 'darwin':
            os.rename(join_path(self.prefix.lib, 'libpapi.so'),
                      join_path(self.prefix.lib, 'libpapi.dylib'))
            fs.fix_darwin_install_name(self.prefix.lib)
