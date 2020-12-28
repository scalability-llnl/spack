# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

import spack.store
from spack.package import *


class OpenspeedshopUtils(CMakePackage):
    """OpenSpeedShop is a community effort by The Krell Institute with
       current direct funding from DOEs NNSA.  It builds on top of a
       broad list of community infrastructures, most notably Dyninst
       and MRNet from UW, libmonitor from Rice, and PAPI from UTK.
       OpenSpeedShop is an open source multi platform Linux performance
       tool which is targeted to support performance analysis of
       applications running on both single node and large scale IA64,
       IA32, EM64T, AMD64, PPC, ARM, Power8, Intel Phi, Blue Gene and
       Cray platforms.  OpenSpeedShop development is hosted by the Krell
       Institute. The infrastructure and base components of OpenSpeedShop
       are released as open source code primarily under LGPL.
       openspeedshop-utils is a package that does not have the
       qt3 gui.  It was created to avoid a conflict between
       openspeedshop and cbtf-argonavis-gui based on the fact
       that spack will not allow a qt3 and qt4/qt5 dependency in a packages
       dependency tree.
    """

    homepage = "http://www.openspeedshop.org"
    git      = "https://github.com/OpenSpeedShop/openspeedshop.git"

    version('develop', branch='master')
    version('2.4.1', branch='2.4.1')
    version('2.4.0', branch='2.4.0')
    version('2.3.1.5', branch='2.3.1.5')
    version('2.3.1.4', branch='2.3.1.4')
    version('2.3.1.3', branch='2.3.1.3')

    variant('runtime', default=False,
            description="build only the runtime libraries and collectors.")
    variant('cti', default=False,
            description="Build MRNet with the CTI startup option")
    variant('crayfe', default=False,
            description="build only the FE tool using the runtime_dir \
                         to point to target build.")
    variant('cuda', default=False,
            description="build with cuda packages included.")

    variant('build_type', default='None', values=('None',),
            description='CMake build type')

    # MPI variants
    variant('openmpi', default=False,
            description="Build mpi collector for openmpi \
                         MPI when variant is enabled.")
    variant('mpt', default=False,
            description="Build mpi collector for SGI \
                         MPT MPI when variant is enabled.")
    variant('mvapich2', default=False,
            description="Build mpi collector for mvapich2\
                         MPI when variant is enabled.")
    variant('mvapich', default=False,
            description="Build mpi collector for mvapich\
                         MPI when variant is enabled.")
    variant('mpich2', default=False,
            description="Build mpi collector for mpich2\
                         MPI when variant is enabled.")
    variant('mpich', default=False,
            description="Build mpi collector for mpich\
                         MPI when variant is enabled.")

    depends_on("cmake@3.0.2:", type='build')

    # Dependencies for openspeedshop that are common to all
    # the variants of the OpenSpeedShop build
    depends_on("libtool", type='build')
    depends_on("bison", type='build')
    depends_on("flex@2.6.1", type='build')

    # For binutils
    depends_on("binutils", type='build')

    depends_on("elf", type="link")
    depends_on("libdwarf")

    depends_on("sqlite")

    # For boost
    depends_on("boost@1.66.0:1.69.0")

    depends_on("dyninst@develop", when='@develop')
    depends_on("dyninst@10:", when='@2.3.1.3:9999')

    depends_on("python@2.7.14:2.7.99", type=('build', 'run'))

    depends_on("libxml2")

    # Dependencies for the openspeedshop cbtf packages.
    depends_on("cbtf@develop", when='@develop', type=('build', 'link', 'run'))
    depends_on("cbtf@1.9.1.0:9999", when='@2.3.1.3:9999', type=('build', 'link', 'run'))

    depends_on("cbtf-krell@develop", when='@develop', type=('build', 'link', 'run'))
    depends_on("cbtf-krell@1.9.1.0:9999", when='@2.3.1.3:9999', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+crayfe', when='@develop+crayfe', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+crayfe', when='@2.3.1.3:9999+crayfe', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+cti', when='@develop+cti', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+cti', when='@2.3.1.3:9999+cti', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+mpich', when='@develop+mpich', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+mpich', when='@2.3.1.3:9999+mpich', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+mpich2', when='@develop+mpich2', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+mpich2', when='@2.3.1.3:9999+mpich2', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+mpt', when='@develop+mpt', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+mpt', when='@2.3.1.3:9999+mpt', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+mvapich', when='@develop+mvapich', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+mvapich', when='@2.3.1.3:9999+mvapich', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+mvapich2', when='@develop+mvapich2', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+mvapich2', when='@2.3.1.3:9999+mvapich2', type=('build', 'link', 'run'))

    depends_on('cbtf-krell@develop+openmpi', when='@develop+openmpi', type=('build', 'link', 'run'))
    depends_on('cbtf-krell@1.9.1.0:9999+openmpi', when='@2.3.1.3:9999+openmpi', type=('build', 'link', 'run'))

    depends_on("cbtf-argonavis@develop", when='@develop+cuda', type=('build', 'link', 'run'))
    depends_on("cbtf-argonavis@1.9.1.0:9999", when='@2.3.1.3:9999+cuda', type=('build', 'link', 'run'))

    # For MRNet
    depends_on("mrnet@5.0.1-3:+cti", when='@develop+cti', type=('build', 'link', 'run'))
    depends_on("mrnet@5.0.1-3:+lwthreads", when='@develop', type=('build', 'link', 'run'))

    depends_on("mrnet@5.0.1-3:+cti", when='@2.3.1.3:9999+cti', type=('build', 'link', 'run'))
    depends_on("mrnet@5.0.1-3:+lwthreads", when='@2.3.1.3:9999', type=('build', 'link', 'run'))

    patch('arm.patch', when='target=aarch64:')
    parallel = False

    build_directory = 'build_openspeedshop'

    def set_cray_login_node_cmake_options(self, spec, cmake_options):
        # Appends to cmake_options the options that will enable the appropriate
        # Cray login node libraries

        cray_login_node_options = []
        rt_platform = "cray"

        # How do we get the compute node (CNL) cbtf package install
        # directory path?
        # spec['cbtf'].prefix is the login node value for this build, as
        # we only get here when building the login node components and
        # that is all that is known to spack.
        be_ck = spack.store.db.query_one('cbtf-krell arch=cray-CNL-haswell')

        # Equivalent to install-tool cmake arg:
        # '-DCBTF_KRELL_CN_RUNTIME_DIR=%s'
        #               % <base dir>/cbtf_v2.3.1.release/compute)
        cray_login_node_options.append('-DCBTF_KRELL_CN_RUNTIME_DIR=%s'
                                       % be_ck.prefix)
        cray_login_node_options.append('-DRUNTIME_PLATFORM=%s'
                                       % rt_platform)

        cmake_options.extend(cray_login_node_options)

    def cmake_args(self):
        # Appends base options to cmake_args
        spec = self.spec

        compile_flags = "-O2 -g"

        cmake_args = []

        # Indicate building cbtf vers (transfer rawdata files)
        instrumentor_setting = "cbtf"

        if spec.satisfies('+runtime'):
            self.set_defaultbase_cmake_options(spec, cmake_args)

            cmake_args.extend(
                ['-DCMAKE_CXX_FLAGS=%s'  % compile_flags,
                 '-DCMAKE_C_FLAGS=%s'    % compile_flags,
                 '-DINSTRUMENTOR=%s' % instrumentor_setting,
                 '-DCBTF_DIR=%s' % spec['cbtf'].prefix,
                 '-DCBTF_KRELL_DIR=%s' % spec['cbtf-krell'].prefix,
                 '-DMRNET_DIR=%s' % spec['mrnet'].prefix])

        else:

            # Appends base options to cmake_args
            self.set_defaultbase_cmake_options(spec, cmake_args)
            cmake_args.extend(
                ['-DCMAKE_CXX_FLAGS=%s' % compile_flags,
                 '-DCMAKE_C_FLAGS=%s' % compile_flags,
                 '-DINSTRUMENTOR=%s' % instrumentor_setting,
                 '-DSQLITE3_DIR=%s' % spec['sqlite'].prefix,
                 '-DCBTF_DIR=%s' % spec['cbtf'].prefix,
                 '-DCBTF_KRELL_DIR=%s' % spec['cbtf-krell'].prefix,
                 '-DMRNET_DIR=%s' % spec['mrnet'].prefix])

            if spec.satisfies('+crayfe'):
                # We need to build target/compute node
                # components/libraries first then pass
                # those libraries to the openspeedshop
                # login node build
                self.set_cray_login_node_cmake_options(spec, cmake_args)

        cmake_args.extend(['-DBUILD_QT3_GUI=FALSE'])

        return cmake_args

    def set_defaultbase_cmake_options(self, spec, cmake_options):
        # Appends to cmake_options the options that will enable
        # the appropriate base level options to the openspeedshop
        # cmake build.
        python_exe = spec['python'].command.path
        python_library = spec['python'].libs[0]
        python_include = spec['python'].headers.directories[0]

        base_options = []

        base_options.append('-DBINUTILS_DIR=%s' % spec['binutils'].prefix)
        base_options.append('-DLIBELF_DIR=%s' % spec['elf'].prefix)
        base_options.append('-DLIBDWARF_DIR=%s' % spec['libdwarf'].prefix)
        base_options.append('-DPYTHON_EXECUTABLE=%s' % python_exe)
        base_options.append('-DPYTHON_INCLUDE_DIR=%s' % python_include)
        base_options.append('-DPYTHON_LIBRARY=%s' % python_library)
        base_options.append('-DBoost_NO_SYSTEM_PATHS=TRUE')
        base_options.append('-DBoost_NO_BOOST_CMAKE=TRUE')
        base_options.append('-DBOOST_ROOT=%s' % spec['boost'].prefix)
        base_options.append('-DBoost_DIR=%s' % spec['boost'].prefix)
        base_options.append('-DBOOST_LIBRARYDIR=%s' % spec['boost'].prefix.lib)
        base_options.append('-DDYNINST_DIR=%s' % spec['dyninst'].prefix)

        cmake_options.extend(base_options)

    def set_mpi_cmake_options(self, spec, cmake_options):
        # Appends to cmake_options the options that will enable
        # the appropriate MPI implementations

        mpi_options = []

        # openmpi
        if spec.satisfies('+openmpi'):
            mpi_options.append('-DOPENMPI_DIR=%s' % spec['openmpi'].prefix)
        # mpich
        if spec.satisfies('+mpich'):
            mpi_options.append('-DMPICH_DIR=%s' % spec['mpich'].prefix)
        # mpich2
        if spec.satisfies('+mpich2'):
            mpi_options.append('-DMPICH2_DIR=%s' % spec['mpich2'].prefix)
        # mvapich
        if spec.satisfies('+mvapich'):
            mpi_options.append('-DMVAPICH_DIR=%s' % spec['mvapich'].prefix)
        # mvapich2
        if spec.satisfies('+mvapich2'):
            mpi_options.append('-DMVAPICH2_DIR=%s' % spec['mvapich2'].prefix)
        # mpt
        if spec.satisfies('+mpt'):
            mpi_options.append('-DMPT_DIR=%s' % spec['mpt'].prefix)

        cmake_options.extend(mpi_options)

    def setup_run_environment(self, env):
        """Set up the compile and runtime environments for a package."""

        # Find Dyninst library path, this is needed to
        # set the DYNINSTAPI_RT_LIB library which is
        # required for OpenSpeedShop to find loop level
        # performance information
        dyninst_libdir = find_libraries('libdyninstAPI_RT',
                                        root=self.spec['dyninst'].prefix,
                                        shared=True, recursive=True)

        # Set Dyninst RT library path to support OSS loop resolution code
        env.set('DYNINSTAPI_RT_LIB', dyninst_libdir[0])

        # Find openspeedshop library path
        oss_libdir = find_libraries(
            'libopenss-framework',
            root=self.spec['openspeedshop-utils'].prefix,
            shared=True, recursive=True)
        env.prepend_path('LD_LIBRARY_PATH',
                         os.path.dirname(oss_libdir.joined()))

        env.set('OPENSS_RAWDATA_DIR', '.')

        cbtf_mc = '/sbin/cbtf_mrnet_commnode'
        cbtf_lmb = '/sbin/cbtf_libcbtf_mrnet_backend'
        env.set('XPLAT_RSH', 'ssh')
        env.set('MRNET_COMM_PATH',
                join_path(self.spec['cbtf-krell'].prefix + cbtf_mc))
        env.set('CBTF_MRNET_BACKEND_PATH',
                join_path(self.spec['cbtf-krell'].prefix + cbtf_lmb))
        env.prepend_path('PATH', self.spec['mrnet'].prefix.bin)
        env.prepend_path('PATH', self.spec['cbtf-krell'].prefix.bin)
        env.prepend_path('PATH', self.spec['cbtf-krell'].prefix.sbin)
        env.prepend_path('PATH', self.spec['python'].prefix.bin)
