# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


def cross_detect():
    if spack.architecture.platform().name == 'cray':
        if which('srun'):
            return 'cray-aries-slurm'
        if which('aprun'):
            return 'cray-aries-alps'
    return 'none'


class Upcxx(Package):
    """UPC++ is a C++ library that supports Partitioned Global Address Space
    (PGAS) programming, and is designed to interoperate smoothly and
    efficiently with MPI, OpenMP, CUDA and AMTs. It leverages GASNet-EX to
    deliver low-overhead, fine-grained communication, including Remote Memory
    Access (RMA) and Remote Procedure Call (RPC)."""

    homepage = "https://upcxx.lbl.gov"
    maintainers = ['bonachea']

    git = 'https://bonachea@bitbucket.org/berkeleylab/upcxx.git'
    version('develop', branch='develop')
    version('master',  branch='master')

    version('2021.3.0', sha256='3433714cd4162ffd8aad9a727c12dbf1c207b7d6664879fc41259a4b351595b7')
    version('2020.11.0', sha256='f6f212760a485a9f346ca11bb4751e7095bbe748b8e5b2389ff9238e9e321317',
            url='https://bitbucket.org/berkeleylab/upcxx/downloads/upcxx-2020.11.0-memory_kinds_prototype.tar.gz')
    version('2020.10.0', sha256='623e074b512bf8cad770a04040272e1cc660d2749760398b311f9bcc9d381a37')
    version('2020.3.0', sha256='01be35bef4c0cfd24e9b3d50c88866521b9cac3ad4cbb5b1fc97aea55078810f')
    version('2019.9.0', sha256='7d67ccbeeefb59de9f403acc719f52127a30801a2c2b9774a1df03f850f8f1d4')
    version('2019.3.2', sha256='dcb0b337c05a0feb2ed5386f5da6c60342412b49cab10f282f461e74411018ad')

    variant('mpi', default=False,
            description='Enables MPI-based spawners and mpi-conduit')

    variant('cuda', default=False,
            description='Builds a CUDA-enabled version of UPC++')

    variant('cross', default=cross_detect(),
            description="UPC++ cross-compile target (autodetect by default)")

    conflicts('cross=none', when='platform=cray',
              msg='cross=none is unacceptable on Cray.' +
                  'Please specify an appropriate "cross" value')

    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')
    # Require Python2 2.7.5+ up to v2019.9.0
    depends_on('python@2.7.5:2.999',
               type=("build", "run"), when='@:2019.9.0')
    # v2020.3.0 and later also permit Python3
    depends_on('python@2.7.5:', type=("build", "run"), when='@2020.3.0:')

    # All flags should be passed to the build-env in autoconf-like vars
    flag_handler = env_flags

    def url_for_version(self, version):
        if version > Version('2019.3.2'):
            url = "https://bitbucket.org/berkeleylab/upcxx/downloads/upcxx-{0}.tar.gz"
        else:
            url = "https://bitbucket.org/berkeleylab/upcxx/downloads/upcxx-{0}-offline.tar.gz"
        return url.format(version)

    def setup_build_environment(self, env):
        # ensure we use the correct python
        env.set('UPCXX_PYTHON', self.spec['python'].command.path)

        if '+mpi' in self.spec:
            env.set('GASNET_CONFIGURE_ARGS',
                    '--enable-mpi --enable-mpi-compat')
        else:
            env.set('GASNET_CONFIGURE_ARGS', '--without-mpicc')

        if 'cross=none' not in self.spec:
            env.set('CROSS', self.spec.variants['cross'].value)

        if '+cuda' in self.spec:
            env.set('UPCXX_CUDA', '1')
            env.set('UPCXX_CUDA_NVCC', self.spec['cuda'].prefix.bin.nvcc)

    def setup_run_environment(self, env):
        # ensure we use the correct python
        env.set('UPCXX_PYTHON', self.spec['python'].command.path)

        env.set('UPCXX_INSTALL', self.prefix)
        env.set('UPCXX', self.prefix.bin.upcxx)
        if 'platform=cray' in self.spec:
            env.set('UPCXX_GASNET_CONDUIT', 'aries')
            env.set('UPCXX_NETWORK', 'aries')

    def setup_dependent_package(self, module, dep_spec):
        dep_spec.upcxx = self.prefix.bin.upcxx

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('UPCXX_INSTALL', self.prefix)
        env.set('UPCXX', self.prefix.bin.upcxx)
        if 'platform=cray' in self.spec:
            env.set('UPCXX_GASNET_CONDUIT', 'aries')
            env.set('UPCXX_NETWORK', 'aries')

    def install(self, spec, prefix):
        # UPC++ follows autoconf naming convention for LDLIBS, which is 'LIBS'
        if (env.get('LDLIBS')):
            env['LIBS'] = env['LDLIBS']

        if spec.version <= Version('2019.9.0'):
            env['CC'] = self.compiler.cc
            if '+mpi' in self.spec:
                if 'platform=cray' in self.spec:
                    env['GASNET_CONFIGURE_ARGS'] += \
                        " --with-mpicc=" + self.compiler.cc
                else:
                    env['CXX'] = spec['mpi'].mpicxx
            else:
                env['CXX'] = self.compiler.cxx
            installsh = Executable("./install")
            installsh(prefix)
        else:
            if 'platform=cray' in self.spec:
                # Spack loads the cray-libsci module incorrectly on ALCF theta,
                # breaking the Cray compiler wrappers
                # cray-libsci is irrelevant to our build, so disable it
                for var in ['PE_PKGCONFIG_PRODUCTS', 'PE_PKGCONFIG_LIBS']:
                    env[var] = ":".join(
                        filter(lambda x: "libsci" not in x.lower(),
                               env[var].split(":")))
                # Undo spack compiler wrappers:
                # the C/C++ compilers must work post-install
                # hack above no longer works after the fix to UPC++ issue #287
                real_cc = join_path(env['CRAYPE_DIR'], 'bin', 'cc')
                real_cxx = join_path(env['CRAYPE_DIR'], 'bin', 'CC')
                # workaround a bug in the UPC++ installer: (issue #346)
                env['GASNET_CONFIGURE_ARGS'] += \
                    " --with-cc=" + real_cc + " --with-cxx=" + real_cxx
                if '+mpi' in self.spec:
                    env['GASNET_CONFIGURE_ARGS'] += " --with-mpicc=" + real_cc
            else:
                real_cc = self.compiler.cc
                real_cxx = self.compiler.cxx
                if '+mpi' in self.spec:
                    real_cxx = spec['mpi'].mpicxx

            env['CC'] = real_cc
            env['CXX'] = real_cxx

            installsh = Executable("./configure")
            installsh('--prefix=' + prefix)

            make()

            make('install')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        if self.spec.version <= Version('2019.9.0'):
            spack.main.send_warning_to_tty(
                "run_tests not supported in UPC++ version " +
                self.spec.version.string + " -- SKIPPED")
        else:
            # enable testing of unofficial conduits (mpi)
            test_networks = 'NETWORKS=$(CONDUITS)'
            # build hello world against installed tree in all configurations
            make('test_install', test_networks)
            make('tests-clean')  # cleanup
            # build all tests for all networks in debug mode
            make('tests', test_networks)
            if 'cross=none' in self.spec:
                make('run-tests', 'NETWORKS=smp')  # runs tests for smp backend
            make('tests-clean')  # cleanup
