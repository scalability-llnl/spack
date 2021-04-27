# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.environment import SetEnv


class Hpctoolkit(AutotoolsPackage):
    """HPCToolkit is an integrated suite of tools for measurement and analysis
    of program performance on computers ranging from multicore desktop systems
    to the nation's largest supercomputers. By using statistical sampling of
    timers and hardware performance counters, HPCToolkit collects accurate
    measurements of a program's work, resource consumption, and inefficiency
    and attributes them to the full calling context in which they occur."""

    homepage = "http://hpctoolkit.org"
    git      = "https://github.com/HPCToolkit/hpctoolkit.git"
    maintainers = ['mwkrentel']

    version('develop', branch='develop')
    version('master',  branch='master')
    version('2021.03.01', commit='68a051044c952f0f4dac459d9941875c700039e7')
    version('2020.08.03', commit='d9d13c705d81e5de38e624254cf0875cce6add9a')
    version('2020.07.21', commit='4e56c780cffc53875aca67d6472a2fb3678970eb')
    version('2020.06.12', commit='ac6ae1156e77d35596fea743ed8ae768f7222f19')
    version('2020.03.01', commit='94ede4e6fa1e05e6f080be8dc388240ea027f769')
    version('2019.12.28', commit='b4e1877ff96069fd8ed0fdf0e36283a5b4b62240')
    version('2019.08.14', commit='6ea44ed3f93ede2d0a48937f288a2d41188a277c')
    version('2018.12.28', commit='8dbf0d543171ffa9885344f32f23cc6f7f6e39bc')
    version('2018.11.05', commit='d0c43e39020e67095b1f1d8bb89b75f22b12aee9')

    # Options for MPI and hpcprof-mpi.  We always support profiling
    # MPI applications.  These options add hpcprof-mpi, the MPI
    # version of hpcprof.  Cray and Blue Gene need separate options
    # because an MPI module in packages.yaml doesn't work on these
    # systems.
    variant('cray', default=False,
            description='Build for Cray compute nodes, including '
            'hpcprof-mpi.')

    variant('mpi', default=False,
            description='Build hpcprof-mpi, the MPI version of hpcprof.')

    # We can't build with both PAPI and perfmon for risk of segfault
    # from mismatched header files (unless PAPI installs the perfmon
    # headers).
    variant('papi', default=True,
            description='Use PAPI instead of perfmon for access to '
            'the hardware performance counters.')

    variant('all-static', default=False,
            description='Needed when MPICXX builds static binaries '
            'for the compute nodes.')

    variant('cuda', default=False,
            description='Support CUDA on NVIDIA GPUs (2020.03.01 or later).')

    variant('rocm', default=False,
            description='Support ROCM on AMD GPUs, requires ROCM as '
            'external packages (2021.03.01 or later).')

    boost_libs = (
        '+atomic +chrono +date_time +filesystem +system +thread +timer'
        ' +graph +regex +shared +multithreaded visibility=global'
    )

    depends_on('binutils +libiberty', type='link', when='@2021.00:')
    depends_on('binutils +libiberty~nls', type='link', when='@2020.04:2020.99')
    depends_on('binutils@:2.33.1 +libiberty~nls', type='link', when='@:2020.03.99')
    depends_on('boost' + boost_libs)
    depends_on('bzip2+shared', type='link')
    depends_on('dyninst@10.2.0:', when='@2021.00:')
    depends_on('dyninst@9.3.2:', when='@:2020.99')
    depends_on('elfutils+bzip2+xz~nls', type='link')
    depends_on('gotcha@1.0.3:')
    depends_on('intel-tbb+shared')
    depends_on('libdwarf')
    depends_on('libmonitor+hpctoolkit~dlopen', when='@2021.00:')
    depends_on('libmonitor+hpctoolkit+dlopen', when='@:2020.99')
    depends_on('libunwind@1.4: +xz+pic')
    depends_on('mbedtls+pic')
    depends_on('xerces-c transcoder=iconv')
    depends_on('xz+pic', type='link')
    depends_on('zlib+shared')

    depends_on('cuda', when='+cuda')
    depends_on('intel-xed', when='target=x86_64:')
    depends_on('papi', when='+papi')
    depends_on('libpfm4', when='~papi')
    depends_on('mpi', when='+mpi')

    depends_on('hip', when='+rocm')
    depends_on('rocm-dbgapi', when='+rocm')
    depends_on('roctracer-dev', when='+rocm')

    conflicts('%gcc@:4.7.99', when='^dyninst@10.0.0:',
              msg='hpctoolkit requires gnu gcc 4.8.x or later')

    conflicts('%gcc@:4.99.99', when='@2020.03:2020.99',
              msg='hpctoolkit requires gnu gcc 5.x or later')

    conflicts('%gcc@:6.99.99', when='@2021.00:',
              msg='hpctoolkit requires gnu gcc 7.x or later')

    conflicts('+cuda', when='@:2019.99.99',
              msg='cuda requires 2020.03.01 or later')

    conflicts('+rocm', when='@:2020.99.99',
              msg='rocm requires 2021.03.01 or later')

    conflicts('^binutils@2.35:2.35.1',
              msg='avoid binutils 2.35 and 2.35.1 (spews errors)')

    # Fix the build for old revs with gcc 10.x.
    patch('gcc10-enum.patch', when='@2020.01.01:2020.08.99 %gcc@10.0:')

    flag_handler = AutotoolsPackage.build_system_flags

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-binutils=%s'     % spec['binutils'].prefix,
            '--with-boost=%s'        % spec['boost'].prefix,
            '--with-bzip=%s'         % spec['bzip2'].prefix,
            '--with-dyninst=%s'      % spec['dyninst'].prefix,
            '--with-elfutils=%s'     % spec['elfutils'].prefix,
            '--with-gotcha=%s'       % spec['gotcha'].prefix,
            '--with-tbb=%s'          % spec['intel-tbb'].prefix,
            '--with-libdwarf=%s'     % spec['libdwarf'].prefix,
            '--with-libmonitor=%s'   % spec['libmonitor'].prefix,
            '--with-libunwind=%s'    % spec['libunwind'].prefix,
            '--with-mbedtls=%s'      % spec['mbedtls'].prefix,
            '--with-xerces=%s'       % spec['xerces-c'].prefix,
            '--with-lzma=%s'         % spec['xz'].prefix,
            '--with-zlib=%s'         % spec['zlib'].prefix,
        ]

        if '+cuda' in spec:
            args.append('--with-cuda=%s' % spec['cuda'].prefix)

        if spec.target.family == 'x86_64':
            args.append('--with-xed=%s' % spec['intel-xed'].prefix)

        if '+papi' in spec:
            args.append('--with-papi=%s' % spec['papi'].prefix)
        else:
            args.append('--with-perfmon=%s' % spec['libpfm4'].prefix)

        if spec.satisfies('+rocm'):
            args.extend([
                '--with-rocm-hip=%s'    % spec['hip'].prefix,
                '--with-rocm-dbgapi=%s' % spec['rocm-dbgapi'].prefix,
                '--with-rocm-tracer=%s' % spec['roctracer-dev'].prefix,
            ])

        # MPI options for hpcprof-mpi.
        if '+cray' in spec:
            args.extend([
                '--enable-mpi-search=cray',
                '--enable-all-static',
            ])
        elif '+mpi' in spec:
            args.append('MPICXX=%s' % spec['mpi'].mpicxx)

        if '+all-static' in spec:
            args.append('--enable-all-static')

        return args

    # Remove setenv of ROCM, HIP, etc from the module file.  Loading
    # the hpctoolkit module is not relevant to building a GPU app and
    # some variables (HIP_PATH) intefere with building the app.
    def setup_run_environment(self, env):
        keeplist = []
        for elt in env.env_modifications:
            if not (isinstance(elt, SetEnv)
                    and (elt.name.find('ROCM') >= 0
                         or elt.name.find('HIP') >= 0
                         or elt.name.find('CUDA') >= 0)):
                keeplist.append(elt)

        env.clear()
        env.env_modifications = keeplist
