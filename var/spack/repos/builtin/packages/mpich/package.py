# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys
import re


class Mpich(AutotoolsPackage):
    """MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "http://www.mpich.org"
    url      = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    git      = "https://github.com/pmodels/mpich.git"
    list_url = "http://www.mpich.org/static/downloads/"
    list_depth = 1

    maintainers = ['raffenet', 'yfguo']

    executables = ['^mpichversion$']

    version('develop', submodules=True)
    version('3.4.1', sha256='8836939804ef6d492bcee7d54abafd6477d2beca247157d92688654d13779727')
    version('3.4',   sha256='ce5e238f0c3c13ab94a64936060cff9964225e3af99df1ea11b130f20036c24b')
    version('3.3.2', sha256='4bfaf8837a54771d3e4922c84071ef80ffebddbb6971a006038d91ee7ef959b9')
    version('3.3.1', sha256='fe551ef29c8eea8978f679484441ed8bb1d943f6ad25b63c235d4b9243d551e5')
    version('3.3',   sha256='329ee02fe6c3d101b6b30a7b6fb97ddf6e82b28844306771fa9dd8845108fa0b')
    version('3.2.1', sha256='5db53bf2edfaa2238eb6a0a5bc3d2c2ccbfbb1badd79b664a1a919d2ce2330f1')
    version('3.2',   sha256='0778679a6b693d7b7caff37ff9d2856dc2bfc51318bf8373859bfa74253da3dc')
    version('3.1.4', sha256='f68b5330e94306c00ca5a1c0e8e275c7f53517d01d6c524d51ce9359d240466b')
    version('3.1.3', sha256='afb690aa828467721e9d9ab233fe00c68cae2b7b930d744cb5f7f3eb08c8602c')
    version('3.1.2', sha256='37c3ba2d3cd3f4ea239497d9d34bd57a663a34e2ea25099c2cbef118c9156587')
    version('3.1.1', sha256='455ccfaf4ec724d2cf5d8bff1f3d26a958ad196121e7ea26504fd3018757652d')
    version('3.1',   sha256='fcf96dbddb504a64d33833dc455be3dda1e71c7b3df411dfcf9df066d7c32c39')
    version('3.0.4', sha256='cf638c85660300af48b6f776e5ecd35b5378d5905ec5d34c3da7a27da0acf0b3')

    variant('hwloc', default=True,  description='Use external hwloc package')
    variant('hydra', default=True,  description='Build the hydra process manager')
    variant('romio', default=True,  description='Enable ROMIO MPI I/O implementation')
    variant('verbs', default=False, description='Build support for OpenFabrics verbs.')
    variant('slurm', default=False, description='Enable SLURM support')
    variant('wrapperrpath', default=True, description='Enable wrapper rpath')
    variant(
        'pmi',
        default='pmi',
        description='''PMI interface.''',
        values=('off', 'pmi', 'pmi2', 'pmix'),
        multi=False
    )
    variant(
        'device',
        default='ch4',
        description='''Abstract Device Interface (ADI)
implementation. The ch4 device is in experimental state for versions
before 3.4.''',
        values=('ch3', 'ch4'),
        multi=False
    )
    variant(
        'netmod',
        default='ofi',
        description='''Network module. Only single netmod builds are
supported. For ch3 device configurations, this presumes the
ch3:nemesis communication channel. ch3:sock is not supported by this
spack package at this time.''',
        values=('tcp', 'mxm', 'ofi', 'ucx'),
        multi=False
    )
    variant('pci', default=(sys.platform != 'darwin'),
            description="Support analyzing devices on PCI bus")
    variant('libxml2', default=True,
            description='Use libxml2 for XML support instead of the custom '
                        'minimalistic implementation')
    variant('argobots', default=False,
            description='Enable Argobots support')
    variant('fortran', default=True, description='Enable Fortran support')

    provides('mpi')
    provides('mpi@:3.0', when='@3:')
    provides('mpi@:1.3', when='@1:')

    filter_compiler_wrappers(
        'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpifort', relative_root='bin'
    )

    # Fix using an external hwloc
    # See https://github.com/pmodels/mpich/issues/4038
    # and https://github.com/pmodels/mpich/pull/3540
    # landed in v3.4b1 v3.4a3
    patch('https://github.com/pmodels/mpich/commit/8a851b317ee57366cd15f4f28842063d8eff4483.patch',
          sha256='eb982de3366d48cbc55eb5e0df43373a45d9f51df208abf0835a72dc6c0b4774',
          when='@3.3:3.3.99 +hwloc')

    # fix MPI_Barrier segmentation fault
    # see https://lists.mpich.org/pipermail/discuss/2016-May/004764.html
    # and https://lists.mpich.org/pipermail/discuss/2016-June/004768.html
    patch('mpich32_clang.patch', when='@3.2:3.2.0%clang')
    patch('mpich32_clang.patch', when='@3.2:3.2.0%apple-clang')

    # Fix SLURM node list parsing
    # See https://github.com/pmodels/mpich/issues/3572
    # and https://github.com/pmodels/mpich/pull/3578
    # Even though there is no version 3.3.0, we need to specify 3.3:3.3.0 in
    # the when clause, otherwise the patch will be applied to 3.3.1, too.
    patch('https://github.com/pmodels/mpich/commit/b324d2de860a7a2848dc38aefb8c7627a72d2003.patch',
          sha256='c7d4ecf865dccff5b764d9c66b6a470d11b0b1a5b4f7ad1ffa61079ad6b5dede',
          when='@3.3:3.3.0')

    # This patch for Libtool 2.4.2 enables shared libraries for NAG and is
    # applied by MPICH starting version 3.1.
    patch('nag_libtool_2.4.2_0.patch', when='@:3.0%nag')

    # This patch for Libtool 2.4.2 fixes the problem with '-pthread' flag and
    # enables convenience libraries for NAG. Starting version 3.1, the order of
    # checks for FC and F77 is changed, therefore we need to apply the patch in
    # two steps (the patch files can be merged once the support for versions
    # 3.1 and older is dropped).
    patch('nag_libtool_2.4.2_1.patch', when='@:3.1.3%nag')
    patch('nag_libtool_2.4.2_2.patch', when='@:3.1.3%nag')

    # This patch for Libtool 2.4.6 does the same as the previous two. The
    # problem is not fixed upstream yet and the upper version constraint is
    # given just to avoid application of the patch to the develop version.
    patch('nag_libtool_2.4.6.patch', when='@3.1.4:3.3%nag')

    depends_on('findutils', type='build')
    depends_on('pkgconfig', type='build')

    depends_on('hwloc@2.0.0:', when='@3.3: +hwloc')

    depends_on('libfabric', when='netmod=ofi')
    # The ch3 ofi netmod results in crashes with libfabric 1.7
    # See https://github.com/pmodels/mpich/issues/3665
    depends_on('libfabric@:1.6', when='device=ch3 netmod=ofi')

    depends_on('ucx', when='netmod=ucx')

    # The dependencies on libpciaccess and libxml2 come from the embedded
    # hwloc, which, before version 3.3, was used only for Hydra.
    depends_on('libpciaccess', when="@:3.2+hydra+pci")
    depends_on('libxml2', when='@:3.2+hydra+libxml2')

    # Starting with version 3.3, MPICH uses hwloc directly.
    depends_on('libpciaccess', when="@3.3:+pci")
    depends_on('libxml2', when='@3.3:+libxml2')

    # Starting with version 3.3, Hydra can use libslurm for nodelist parsing
    depends_on('slurm', when='+slurm')

    depends_on('pmix', when='pmi=pmix')

    # +argobots variant requires Argobots
    depends_on('argobots', when='+argobots')

    # building from git requires regenerating autotools files
    depends_on('automake@1.15:', when='@develop', type=("build"))
    depends_on('libtool@2.4.4:', when='@develop', type=("build"))
    depends_on("m4", when="@develop", type=("build")),
    depends_on("autoconf@2.67:", when='@develop', type=("build"))

    # building with "+hwloc' also requires regenerating autotools files
    depends_on('automake@1.15:', when='@3.3:3.3.99 +hwloc', type="build")
    depends_on('libtool@2.4.4:', when='@3.3:3.3.99 +hwloc', type="build")
    depends_on("m4", when="@3.3:3.3.99 +hwloc", type="build"),
    depends_on("autoconf@2.67:", when='@3.3:3.3.99 +hwloc', type="build")

    # MPICH's Yaksa submodule requires python to configure
    depends_on("python@3.0:", when="@develop", type="build")

    conflicts('device=ch4', when='@:3.2')
    conflicts('netmod=ofi', when='@:3.1.4')
    conflicts('netmod=ucx', when='device=ch3')
    conflicts('netmod=mxm', when='device=ch4')
    conflicts('netmod=mxm', when='@:3.1.3')
    conflicts('netmod=tcp', when='device=ch4')
    conflicts('pmi=pmi2', when='device=ch3 netmod=ofi')
    conflicts('pmi=pmix', when='device=ch3')
    conflicts('pmi=pmix', when='+hydra')

    # MPICH does not require libxml2 and libpciaccess for versions before 3.3
    # when ~hydra is set: prevent users from setting +libxml2 and +pci in this
    # case to avoid generating an identical MPICH installation.
    conflicts('+pci', when='@:3.2~hydra')
    conflicts('+libxml2', when='@:3.2~hydra')

    # see https://github.com/pmodels/mpich/pull/5031
    conflicts('%clang@:7', when='@3.4:')

    @run_after('configure')
    def patch_cce(self):
        # Configure misinterprets output from the cce compiler
        # Patching configure instead should be possible, but a first
        # implementation failed in obscure ways that were not worth
        # tracking down when this worked
        if self.spec.satisfies('%cce'):
            filter_file('-L -L', '', 'config.lt', string=True)
            filter_file('-L -L', '', 'libtool', string=True)
            filter_file('-L -L', '', 'config.status', string=True)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r'MPICH Version:\s+(\S+)', output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        def get_spack_compiler_spec(path):
            spack_compilers = spack.compilers.find_compilers([path])
            actual_compiler = None
            # check if the compiler actually matches the one we want
            for spack_compiler in spack_compilers:
                if os.path.dirname(spack_compiler.cc) == path:
                    actual_compiler = spack_compiler
                    break
            return actual_compiler.spec if actual_compiler else None

        def is_enabled(text):
            if text in set(['t', 'true', 'enabled', 'enable', 'with',
                            'yes', '1']):
                return True
            return False

        def is_disabled(text):
            if text in set(['f', 'false', 'disabled', 'disable',
                            'without', 'no', '0']):
                return True
            return False

        results = []
        for exe in exes:
            variants = ''
            output = Executable(exe)(output=str, error=str)
            if re.search(r'--with-hwloc-prefix=embedded', output):
                variants += '~hwloc'

            if re.search(r'--with-pm=hydra', output):
                variants += '+hydra'
            else:
                variants += '~hydra'

            match = re.search(r'--(\S+)-romio', output)
            if match and is_enabled(match.group(1)):
                variants += '+romio'
            elif match and is_disabled(match.group(1)):
                variants += '~romio'

            if re.search(r'--with-ibverbs', output):
                variants += '+verbs'
            elif re.search(r'--without-ibverbs', output):
                variants += '~verbs'

            match = re.search(r'--enable-wrapper-rpath=(\S+)', output)
            if match and is_enabled(match.group(1)):
                variants += '+wrapperrpath'
            match = re.search(r'--enable-wrapper-rpath=(\S+)', output)
            if match and is_disabled(match.group(1)):
                variants += '~wrapperrpath'

            if re.search(r'--disable-fortran', output):
                variants += '~fortran'

            match = re.search(r'--with-slurm=(\S+)', output)
            if match and is_enabled(match.group(1)):
                variants += '+slurm'

            if re.search(r'--enable-libxml2', output):
                variants += '+libxml2'
            elif re.search(r'--disable-libxml2', output):
                variants += '~libxml2'

            if re.search(r'--with-thread-package=argobots', output):
                variants += '+argobots'

            if re.search(r'--with-pmi=no', output):
                variants += ' pmi=off'
            elif re.search(r'--with-pmi=simple', output):
                variants += ' pmi=pmi'
            elif re.search(r'--with-pmi=pmi2/simple', output):
                variants += ' pmi=pmi2'
            elif re.search(r'--with-pmix', output):
                variants += ' pmi=pmix'

            match = re.search(r'MPICH Device:\s+(ch3|ch4)', output)
            if match:
                variants += ' device=' + match.group(1)

            match = re.search(r'--with-device=ch.\S+(ucx|ofi|mxm|tcp)', output)
            if match:
                variants += ' netmod=' + match.group(1)

            match = re.search(r'MPICH CC:\s+(\S+)', output)
            compiler_spec = get_spack_compiler_spec(
                os.path.dirname(match.group(1)))
            if compiler_spec:
                variants += '%' + str(compiler_spec)
            results.append(variants)
        return results

    def setup_build_environment(self, env):
        env.unset('F90')
        env.unset('F90FLAGS')

        # https://bugzilla.redhat.com/show_bug.cgi?id=1795817
        if self.spec.satisfies('%gcc@10:'):
            env.set('FFLAGS', '-fallow-argument-mismatch')
        # Same fix but for macOS - avoids issue #17934
        if self.spec.satisfies('%apple-clang@11:'):
            env.set('FFLAGS', '-fallow-argument-mismatch')

    def setup_run_environment(self, env):
        # Because MPI implementations provide compilers, they have to add to
        # their run environments the code to make the compilers available.
        # For Cray MPIs, the regular compiler wrappers *are* the MPI wrappers.
        # Cray MPIs always have cray in the module name, e.g. "cray-mpich"
        external_modules = self.spec.external_modules
        if external_modules and 'cray' in external_modules[0]:
            # This is intended to support external MPICH instances registered
            # by Spack on Cray machines prior to a879c87; users defining an
            # external MPICH entry for Cray should generally refer to the
            # "cray-mpich" package
            env.set('MPICC', spack_cc)
            env.set('MPICXX', spack_cxx)
            env.set('MPIF77', spack_fc)
            env.set('MPIF90', spack_fc)
        else:
            env.set('MPICC', join_path(self.prefix.bin, 'mpicc'))
            env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
            env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
            env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

        env.set('MPICH_CC', spack_cc)
        env.set('MPICH_CXX', spack_cxx)
        env.set('MPICH_F77', spack_f77)
        env.set('MPICH_F90', spack_fc)
        env.set('MPICH_FC', spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec

        # For Cray MPIs, the regular compiler wrappers *are* the MPI wrappers.
        # Cray MPIs always have cray in the module name, e.g. "cray-mpich"
        external_modules = spec.external_modules
        if external_modules and 'cray' in external_modules[0]:
            spec.mpicc = spack_cc
            spec.mpicxx = spack_cxx
            spec.mpifc = spack_fc
            spec.mpif77 = spack_f77
        else:
            spec.mpicc = join_path(self.prefix.bin, 'mpicc')
            spec.mpicxx = join_path(self.prefix.bin, 'mpic++')

            if '+fortran' in spec:
                spec.mpifc = join_path(self.prefix.bin, 'mpif90')
                spec.mpif77 = join_path(self.prefix.bin, 'mpif77')

        spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpicxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        # If configure exists nothing needs to be done
        if (os.path.exists(self.configure_abs_path) and
            not spec.satisfies('@3.3:3.3.99 +hwloc')):
            return
        # Else bootstrap with autotools
        bash = which('bash')
        bash('./autogen.sh')

    @run_before('autoreconf')
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        # The user can work around this by disabling Fortran explicitly
        # with ~fortran

        f77 = self.compiler.f77
        fc = self.compiler.fc

        fortran_missing = f77 is None or fc is None

        if '+fortran' in self.spec and fortran_missing:
            raise InstallError(
                'mpich +fortran requires Fortran compilers. Configure '
                'Fortran compiler or disable Fortran support with ~fortran'
            )

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--disable-silent-rules',
            '--enable-shared',
            '--with-hwloc-prefix={0}'.format(
                spec['hwloc'].prefix if '^hwloc' in spec else 'embedded'),
            '--with-pm={0}'.format('hydra' if '+hydra' in spec else 'no'),
            '--{0}-romio'.format('enable' if '+romio' in spec else 'disable'),
            '--{0}-ibverbs'.format('with' if '+verbs' in spec else 'without'),
            '--enable-wrapper-rpath={0}'.format('no' if '~wrapperrpath' in
                                                spec else 'yes')
        ]

        if '~fortran' in spec:
            config_args.append('--disable-fortran')

        if '+slurm' in spec:
            config_args.append('--with-slurm=yes')
            config_args.append('--with-slurm-include={0}'.format(
                spec['slurm'].prefix.include))
            config_args.append('--with-slurm-lib={0}'.format(
                spec['slurm'].prefix.lib))
        else:
            config_args.append('--with-slurm=no')

        if 'pmi=off' in spec:
            config_args.append('--with-pmi=no')
        elif 'pmi=pmi' in spec:
            config_args.append('--with-pmi=simple')
        elif 'pmi=pmi2' in spec:
            config_args.append('--with-pmi=pmi2/simple')
        elif 'pmi=pmix' in spec:
            config_args.append('--with-pmix={0}'.format(spec['pmix'].prefix))

        # setup device configuration
        device_config = ''
        if 'device=ch4' in spec:
            device_config = '--with-device=ch4:'
        elif 'device=ch3' in spec:
            device_config = '--with-device=ch3:nemesis:'

        if 'netmod=ucx' in spec:
            device_config += 'ucx'
        elif 'netmod=ofi' in spec:
            device_config += 'ofi'
        elif 'netmod=mxm' in spec:
            device_config += 'mxm'
        elif 'netmod=tcp' in spec:
            device_config += 'tcp'

        config_args.append(device_config)

        # Specify libfabric or ucx path explicitly, otherwise
        # configure might fall back to an embedded version.
        if 'netmod=ofi' in spec:
            config_args.append('--with-libfabric={0}'.format(
                spec['libfabric'].prefix))
        if 'netmod=ucx' in spec:
            config_args.append('--with-ucx={0}'.format(
                spec['ucx'].prefix))

        # In other cases the argument is redundant.
        if '@:3.2+hydra' in spec or '@3.3:' in spec:
            # The root configure script passes the argument to the configure
            # scripts of all instances of hwloc (there are three copies of it:
            # for hydra, for hydra2, and for MPICH itself).
            config_args += self.enable_or_disable('libxml2')

        # If +argobots specified, add argobots option
        if '+argobots' in spec:
            config_args.append('--with-thread-package=argobots')
            config_args.append('--with-argobots=' + spec['argobots'].prefix)

        return config_args
