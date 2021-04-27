# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import fnmatch
import glob
import platform
import sys
from llnl.util.filesystem import join_path


class Tau(Package):
    """A portable profiling and tracing toolkit for performance
    analysis of parallel programs written in Fortran, C, C++, UPC,
    Java, Python.
    """

    maintainers = ['wspear', 'eugeneswalker', 'khuck', 'sameershende']
    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "https://www.cs.uoregon.edu/research/tau/tau_releases/tau-2.30.tar.gz"
    git      = "https://github.com/UO-OACISS/tau2"

    version('master', branch='master')
    version('2.30.1', sha256='9c20ca1b4f4e80d885f24491cee598068871f0e9dd67906a5e47e4b4147d08fc')
    version('2.30', sha256='e581c33e21488d69839a00d97fd4451ea579f47249b2750d5c36bea773041eaf')
    version('2.29.1', sha256='4195a0a236bba510ab50a93e13c7f00d9472e8bc46c91de3f0696112a34e34e2')
    version('2.29', sha256='146be769a23c869a7935e8fa5ba79f40ba36b9057a96dda3be6730fc9ca86086')
    version('2.28.2', sha256='64e129a482056755012b91dae2fb4f728dbf3adbab53d49187eca952891c5457')
    version('2.28.1', sha256='b262e5c9977471e9f5a8d729b3db743012df9b0ab8244da2842039f8a3b98b34')
    version('2.28', sha256='68c6f13ae748d12c921456e494006796ca2b0efebdeef76ee7c898c81592883e')
    version('2.27.2p1', sha256='3256771fb71c2b05932b44d0650e6eadc712f1bdedf4c0fb2781db3b266225dd')
    version('2.27.2', sha256='d319a4588ad303b71082254f4f40aa76f6183a01b5bc4bd987f76e1a6026efa1')
    version('2.27.1', sha256='315babab4da25dd08633ad8dbf33d93db77f57d240bcbd3527ed5b8710cb9d8f')
    version('2.27', sha256='d48fdca49cda2d9f25a0cf5dbd961201c8a2b1f025bcbb121d96ad43f211f1a7')
    version('2.26.3', sha256='bd785ed47f20e6b8b2a1d99ce383d292f70b1fb9e2eaab21f5eaf8e64b28e990')
    version('2.26.2', sha256='92ca68db51fd5bd026187e70b397bcd1db9bfb07008d7e8bc935411a97978834')
    version('2.26.1', sha256='d084ff87e5f9fe640a3fc48aa5c8c52f586e7b739787f2bb9a4249005e459896')
    version('2.26', sha256='458228646a13a228841d4133f24af14cc182f4978eb15ef6244d71735abe8d16')
    version('2.25', sha256='ab8a8c15a075af69aa23b4790b4e2d9dffc3b880fc1ff806c21535ab69b6a088')
    version('2.24.1', sha256='bc27052c36377e4b8fc0bbb4afaa57eaa8bcb3f5e5066e576b0f40d341c28a0e')
    version('2.24', sha256='5d28e8b26561c7cd7d0029b56ec0f95fc26803ac0b100c98e00af0b02e7f55e2')
    version('2.23.1', sha256='31a4d0019cec6ef57459a9cd18a220f0130838a5f1a0b5ea7879853f5a38cf88')

    # Disable some default dependencies on Darwin/OSX
    darwin_default = False
    if sys.platform != 'darwin':
        darwin_default = True

    variant('scorep', default=False, description='Activates SCOREP support')
    variant('openmp', default=False, description='Use OpenMP threads')
    variant('pthreads', default=True, description='Use POSIX threads')
    variant('mpi', default=False, description='Specify use of TAU MPI wrapper library')
    variant('phase', default=False, description='Generate phase based profiles')
    variant('papi', default=darwin_default, description='Activates Performance API')
    variant('binutils', default=True, description='Activates support of BFD GNU Binutils')
    variant('libdwarf', default=darwin_default, description='Activates support of libdwarf')
    variant('libelf', default=darwin_default, description='Activates support of libelf')
    variant('libunwind', default=darwin_default, description='Activates support of libunwind')
    variant('otf2', default=True, description='Activates support of Open Trace Format (OTF)')
    variant('pdt', default=True, description='Use PDT for source code instrumentation')
    variant('comm', default=False, description=' Generate profiles with MPI communicator info')
    variant('python', default=False, description='Activates Python support')
    variant('likwid', default=False, description='Activates LIKWID support')
    variant('ompt', default=False, description='Activates OMPT instrumentation')
    variant('opari', default=False, description='Activates Opari2 instrumentation')
    variant('shmem', default=False, description='Activates SHMEM support')
    variant('gasnet', default=False, description='Activates GASNET support')
    variant('cuda', default=False, description='Activates CUDA support')
    variant('rocm', default=False, description='Activates ROCm support')
    variant('level_zero', default=False, description='Activates Intel OneAPI Level Zero support')
    variant('rocprofiler', default=False, description='Activates ROCm rocprofiler support')
    variant('opencl', default=False, description='Activates OpenCL support')
    variant('fortran', default=darwin_default, description='Activates Fortran support')
    variant('io', default=True, description='Activates POSIX I/O support')
    variant('adios2', default=False, description='Activates ADIOS2 output support')
    variant('sqlite', default=False, description='Activates SQLite3 output support')
    variant('profileparam', default=False, description='Generate profiles with parameter mapped event data')

    # Support cross compiling.
    # This is a _reasonable_ subset of the full set of TAU
    # architectures supported:
    variant('craycnl', default=False, description='Build for Cray compute nodes')
    variant('ppc64le', default=False, description='Build for IBM Power LE nodes')
    variant('x86_64', default=False, description='Force build for x86 Linux instead of auto-detect')

    depends_on('zlib', type='link')
    depends_on('pdt', when='+pdt')  # Required for TAU instrumentation
    depends_on('scorep', when='+scorep')
    depends_on('otf2@2.1:', when='+otf2')
    depends_on('likwid', when='+likwid')
    depends_on('papi', when='+papi')
    depends_on('libdwarf', when='+libdwarf')
    depends_on('libelf', when='+libdwarf')
    # TAU requires the ELF header support, libiberty and demangle.
    depends_on('binutils@:2.33.1+libiberty+headers+plugins', when='+binutils')
    depends_on('python@2.7:', when='+python')
    depends_on('libunwind', when='+libunwind')
    depends_on('mpi', when='+mpi', type=('build', 'run', 'link'))
    depends_on('cuda', when='+cuda')
    depends_on('gasnet', when='+gasnet')
    depends_on('adios2', when='+adios2')
    depends_on('sqlite', when='+sqlite')
    depends_on('hwloc')

    # Elf only required from 2.28.1 on
    conflicts('+libelf', when='@:2.28.0')
    conflicts('+libdwarf', when='@:2.28.0')

    # ADIOS2, SQLite only available from 2.29.1 on
    conflicts('+adios2', when='@:2.29.1')
    conflicts('+sqlite', when='@:2.29.1')

    patch('unwind.patch', when="@2.29.0")

    def set_compiler_options(self, spec):

        useropt = ["-O2 -g", self.rpath_args]

        ##########
        # Selecting a compiler with TAU configure is quite tricky:
        # 1 - compilers are mapped to a given set of strings
        #     (and spack cc, cxx, etc. wrappers are not among them)
        # 2 - absolute paths are not allowed
        # 3 - the usual environment variables seems not to be checked
        #     ('CC', 'CXX' and 'FC')
        # 4 - if no -cc=<compiler> -cxx=<compiler> is passed tau is built with
        #     system compiler silently
        # (regardless of what %<compiler> is used in the spec)
        #
        # In the following we give TAU what he expects and put compilers into
        # PATH
        compiler_path = os.path.dirname(self.compiler.cc)
        os.environ['PATH'] = ':'.join([compiler_path, os.environ['PATH']])

        compiler_options = ['-c++=%s' % os.path.basename(self.compiler.cxx),
                            '-cc=%s' % os.path.basename(self.compiler.cc)]

        if '+fortran' in spec and self.compiler.fc:
            compiler_options.append('-fortran=%s' % self.compiler.fc_names[0])

        ##########

        # Construct the string of custom compiler flags and append it to
        # compiler related options
        useropt = ' '.join(useropt)
        useropt = "-useropt=%s" % useropt
        compiler_options.append(useropt)
        return compiler_options

    def setup_build_environment(self, env):
        env.prepend_path('LIBRARY_PATH', self.spec['zlib'].prefix.lib)
        env.prepend_path('LIBRARY_PATH', self.spec['hwloc'].prefix.lib)

    def install(self, spec, prefix):
        # TAU isn't happy with directories that have '@' in the path.  Sigh.
        change_sed_delimiter('@', ';', 'configure')
        change_sed_delimiter('@', ';', 'utils/FixMakefile')
        change_sed_delimiter('@', ';', 'utils/FixMakefile.sed.default')

        # TAU configure, despite the name , seems to be a manually
        # written script (nothing related to autotools).  As such it has
        # a few #peculiarities# that make this build quite hackish.
        options = ["-prefix=%s" % prefix]

        if '+craycnl' in spec:
            options.append('-arch=craycnl')

        if '+ppc64le' in spec:
            options.append('-arch=ibm64linux')

        if '+x86_64' in spec:
            options.append('-arch=x86_64')

        if ('platform=cray' in self.spec) and ('+x86_64' not in spec):
            options.append('-arch=craycnl')

        if '+pdt' in spec:
            options.append("-pdt=%s" % spec['pdt'].prefix)

        if '+scorep' in spec:
            options.append("-scorep=%s" % spec['scorep'].prefix)

        if '+pthreads' in spec:
            options.append('-pthread')

        if '+likwid' in spec:
            options.append("-likwid=%s" % spec['likwid'].prefix)

        if '+papi' in spec:
            options.append("-papi=%s" % spec['papi'].prefix)

        if '+openmp' in spec:
            options.append('-openmp')

        if '+opari' in spec:
            options.append('-opari')

        if '+ompt' in spec:
            options.append('-ompt')

        if '+io' in spec:
            options.append('-iowrapper')

        if '+binutils' in spec:
            options.append("-bfd=%s" % spec['binutils'].prefix)

        if '+libdwarf' in spec:
            options.append("-dwarf=%s" % spec['libdwarf'].prefix)

        if '+libelf' in spec:
            options.append("-elf=%s" % spec['libelf'].prefix)

        if '+libunwind' in spec:
            options.append("-unwind=%s" % spec['libunwind'].prefix)

        if '+otf2' in spec:
            options.append("-otf=%s" % spec['otf2'].prefix)

        if '+mpi' in spec:
            env['CC'] = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx
            env['F77'] = spec['mpi'].mpif77
            env['FC'] = spec['mpi'].mpifc

            options.append('-mpi')
            if '+comm' in spec:
                options.append('-PROFILECOMMUNICATORS')

        if '+profileparam' in spec:
            options.append('-PROFILEPARAM')

        if '+shmem' in spec:
            options.append('-shmem')

        if '+gasnet' in spec:
            options.append('-gasnet=%s' % spec['gasnet'].prefix)

        if '+cuda' in spec:
            options.append("-cuda=%s" % spec['cuda'].prefix)

        if '+level_zero' in spec:
            options.append("-level_zero")

        if '+opencl' in spec:
            options.append("-opencl")

        if '+rocm' in spec:
            options.append("-rocm")

        if '+rocprofiler' in spec:
            options.append("-rocprofiler=%s" % spec['rocprofiler'].prefix)

        if '+adios2' in spec:
            options.append("-adios=%s" % spec['adios2'].prefix)

        if '+sqlite' in spec:
            options.append("-sqlite3=%s" % spec['sqlite'].prefix)

        if '+phase' in spec:
            options.append('-PROFILEPHASE')

        if '+python' in spec:
            options.append('-python')
            # find Python.h (i.e. include/python2.7/Python.h)
            include_path = spec['python'].prefix.include
            found = False
            for root, dirs, files in os.walk(spec['python'].prefix.include):
                for filename in fnmatch.filter(files, 'Python.h'):
                    include_path = root
                    break
                    found = True
                if found:
                    break
            options.append("-pythoninc=%s" % include_path)
            # find libpython*.* (i.e. lib/python2.7/libpython2.7.so)
            lib_path = spec['python'].prefix.lib
            found = False
            file_to_find = 'libpython*.so'
            if (platform.system() == "Darwin"):
                file_to_find = 'libpython*.dylib'
            for root, dirs, files in os.walk(spec['python'].prefix.lib):
                for filename in fnmatch.filter(files, file_to_find):
                    lib_path = root
                    break
                    found = True
                if found:
                    break
            options.append("-pythonlib=%s" % lib_path)

        compiler_specific_options = self.set_compiler_options(spec)
        options.extend(compiler_specific_options)
        configure(*options)

        make("install")

        # Link arch-specific directories into prefix since there is
        # only one arch per prefix the way spack installs.
        self.link_tau_arch_dirs()
        # TAU may capture Spack's internal compiler wrapper. Replace
        # it with the correct compiler.
        self.fix_tau_compilers()

    def link_tau_arch_dirs(self):
        for subdir in os.listdir(self.prefix):
            for d in ('bin', 'lib'):
                src = join_path(self.prefix, subdir, d)
                dest = join_path(self.prefix, d)
                if os.path.isdir(src) and not os.path.exists(dest):
                    os.symlink(join_path(subdir, d), dest)

    def fix_tau_compilers(self):
        filter_file('FULL_CC=' + spack_cc, 'FULL_CC=' + self.compiler.cc,
                    self.prefix + '/include/Makefile', backup=False,
                    string=True)
        filter_file('FULL_CXX=' + spack_cxx, 'FULL_CXX=' +
                    self.compiler.cxx, self.prefix + '/include/Makefile',
                    backup=False, string=True)
        for makefile in os.listdir(self.prefix.lib):
            if makefile.startswith('Makefile.tau'):
                filter_file('FULL_CC=' + spack_cc, 'FULL_CC=' +
                            self.compiler.cc, self.prefix.lib + "/" +
                            makefile, backup=False, string=True)
                filter_file('FULL_CXX=' + spack_cxx, 'FULL_CXX=' +
                            self.compiler.cxx, self.prefix.lib +
                            "/" + makefile, backup=False, string=True)

    def setup_run_environment(self, env):
        pattern = join_path(self.prefix.lib, 'Makefile.*')
        files = glob.glob(pattern)

        # This function is called both at install time to set up
        # the build environment and after install to generate the associated
        # module file. In the former case there is no `self.prefix.lib`
        # directory to inspect. The conditional below will set `TAU_MAKEFILE`
        # in the latter case.
        if files:
            env.set('TAU_MAKEFILE', files[0])
