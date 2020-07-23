# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import glob


class Pfunit(CMakePackage):
    """pFUnit is a unit testing framework enabling JUnit-like testing of
    serial and MPI-parallel software written in Fortran."""

    homepage = "http://pfunit.sourceforge.net/"
    url      = "https://github.com/Goddard-Fortran-Ecosystem/pFUnit/archive/3.2.9.tar.gz"

    maintainers = ['citibeth']

    # Currently investigating build fails for v 4.0.0.
    # See discussion in PR #11642.
    # version('4.0.0',  sha256='b8b6470f2b1e2b19c164c244c10e803bd69c8da9a6a5a65ba7c479fb8b92a1e1') # noqa: E501
    version('3.3.3',  sha256='9f673b58d20ad23148040a100227b4f876458a9d9aee0f0d84a5f0eef209ced5')
    version('3.3.2',  sha256='b1cc2e109ba602ea71bccefaa3c4a06e7ab1330db9ce6c08db89cfde497b8ab8')
    version('3.3.1',  sha256='f8f4bea7de991a518a0371b4c70b19e492aa9a0d3e6715eff9437f420b0cdb45')
    version('3.3.0',  sha256='4036ab448b821b500fbe8be5e3d5ab3e419ebae8be82f7703bcf84ab1a0ff862')
    version('3.2.10', sha256='b9debba6d0e31b682423ffa756531e9728c10acde08c4d8e1609b4554f552b1a')
    version('3.2.9',  sha256='403f9a150865700c8b4240fd033162b8d3e8aeefa265c50c5a6fe14c455fbabc')

    variant('shared', default=True,
            description='Build shared library in addition to static')
    variant('mpi', default=False, description='Enable MPI')
    variant('use_comm_world', default=False,
            description='Enable MPI_COMM_WORLD for testing')
    variant('openmp', default=False, description='Enable OpenMP')
    variant('docs', default=False, description='Build docs')

    variant('max_array_rank', values=int, default=5,
            description='Max number of Fortran dimensions of array asserts')

    depends_on('python@2.7:', type=('build', 'run'))  # python3 too!
    depends_on('mpi', when='+mpi')

    conflicts("use_comm_world", when="~mpi")
    patch("mpi-test.patch", when="+use_comm_world")
    # XLF is not able to handle the deferred
    # procedure overrides--it insists that
    # an abstract extended type is needed,
    # which prevents compilation; for this
    # specific version, a patch has been
    # developed to stub deferred procedures
    # that interfere with inheritance/building
    patch("xl-deferred.patch", when='@3.2.9 %xl_r')

    def patch(self):
        # The package tries to put .mod files in directory ./mod;
        # spack needs to put them in a standard location:
        for file in glob.glob('*/CMakeLists.txt'):
            filter_file(r'.*/mod($|[^\w].*)', '', file)

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DPYTHON_EXECUTABLE=%s' % spec['python'].command,
            '-DBUILD_SHARED=%s' % ('YES' if '+shared' in spec else 'NO'),
            '-DCMAKE_Fortran_MODULE_DIRECTORY=%s' % spec.prefix.include,
            '-DBUILD_DOCS=%s' % ('YES' if '+docs' in spec else 'NO'),
            '-DOPENMP=%s' % ('YES' if '+openmp' in spec else 'NO'),
            '-DMAX_RANK=%s' % spec.variants['max_array_rank'].value]

        if spec.satisfies('@3.2.9 %xl_r'):
            # DCMAKE_Fortran_MODULE_DIRECTORY setting is
            # not sufficient for XLF build, at least on rzansel
            # need to create the path so module files can be placed
            # appropriately
            try:
                mkdir(self.prefix.include)
            except FileExistsError:
                pass

            args.append('-DCMAKE_Fortran_STANDARD_INCLUDE_DIRECTORIES=%s' %
                        spec.prefix.include)

        if spec.satisfies('+mpi'):
            args.extend(['-DMPI=YES', '-DMPI_USE_MPIEXEC=YES',
                         '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc])
        else:
            args.append('-DMPI=NO')
        return args

    def check(self):
        """Searches the CMake-generated Makefile for the target ``test``
        and runs it if found.
        """
        args = ['tests']
        if self.spec.satisfies('+mpi'):
            args.append('MPI=YES')
        if self.spec.satisfies('+openmp'):
            args.append('OPENMP=YES')
        with working_dir(self.build_directory):
            make(*args)

    def compiler_vendor(self):
        vendors = {'%gcc': 'GNU', '%clang': 'GNU', '%intel': 'Intel',
                   '%pgi': 'PGI', '%nag': 'NAG', '%xl_r': 'XL'}
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                return value
        raise InstallError('Unsupported compiler.')

    def setup_build_environment(self, env):
        env.set('PFUNIT', self.spec.prefix)
        env.set('F90_VENDOR', self.compiler_vendor())

    def setup_run_environment(self, env):
        env.set('PFUNIT', self.spec.prefix)
        env.set('F90_VENDOR', self.compiler_vendor())

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('PFUNIT', self.spec.prefix)
        env.set('F90_VENDOR', self.compiler_vendor())
