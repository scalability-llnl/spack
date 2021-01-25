# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pism(CMakePackage):
    """Parallel Ice Sheet Model"""

    homepage = "http://pism-docs.org/wiki/doku.php:="
    url      = "https://github.com/pism/pism/archive/v1.1.4.tar.gz"
    git      = "https://github.com/pism/pism.git"

    maintainers = ['citibeth']

    version('develop', branch='dev')
    version('1.2.1', sha256='f1b1373d8c76b265e12404d5372c1a14cf490d3c53317d2a493f10e337a47202')
    version('1.2.2', sha256='ecb880af26643e80b890f74efcf0e4d7e5d60adbc921ef281d3f00904020c624')
    version('1.1.4', sha256='8ccb867af3b37e8d103351dadc1d7e77512e64379519fe8a2592668deb27bc44')
    version('0.7.x', branch='stable0.7')
    version('icebin', branch='efischer/dev')

    variant('extra', default=False,
            description='Build extra executables (testing/verification)')
    variant('shared', default=True,
            description='Build shared Pism libraries')
    variant('python', default=False,
            description='Build python bindings')
    variant('icebin', default=False,
            description='Build classes needed by IceBin')
    variant('proj', default=True,
            description='Use PROJ library to compute cell areas, '
            'longitudes, and latitudes.')
    variant('parallel-netcdf4', default=False,
            description='Enables parallel NetCDF-4 I/O.')
    variant('parallel-netcdf3', default=False,
            description='Enables parallel NetCDF-3 I/O using PnetCDF.')
    variant('parallel-hdf5', default=False,
            description='Enables parallel HDF5 I/O.')
    # variant('tao', default=False,
    #         description='Use TAO in inverse solvers.')

    description = 'Build PISM documentation (requires LaTeX and Doxygen)'
    variant('doc', default=False, description=description)

    variant('examples', default=False,
            description='Install examples directory')

    description = 'Report errors through Everytrace (requires Everytrace)'
    variant('everytrace', default=False, description=description)

    # CMake build options not transferred to Spack variants
    # (except from CMakeLists.txt)
    #
    # option (Pism_TEST_USING_VALGRIND "Add extra regression tests
    #         using valgrind" OFF)
    # mark_as_advanced (Pism_TEST_USING_VALGRIND)
    #
    # option (Pism_ADD_FPIC "Add -fPIC to C++ compiler flags
    #         (CMAKE_CXX_FLAGS). Try turning it off if it does not work." ON)
    # option (Pism_LINK_STATICALLY
    #         "Set CMake flags to try to ensure that everything is
    #         linked statically")
    # option (Pism_LOOK_FOR_LIBRARIES
    #         "Specifies whether PISM should look for libraries. (Disable
    #         this on Crays.)" ON)
    # option (Pism_USE_TR1
    #        "Use the std::tr1 namespace to access shared pointer
    #        definitions. Disable to get shared pointers from the std
    #        namespace (might be needed with some compilers)." ON)
    # option (Pism_USE_TAO "Use TAO in inverse solvers." OFF)

    depends_on('fftw')
    depends_on('gsl')
    depends_on('mpi')
    depends_on('netcdf-c')    # Only the C interface is used, no netcdf-cxx4
    depends_on('petsc')
    depends_on('udunits')
    depends_on('proj@:4', when='@:1.1')
    depends_on('proj@5:', when='@1.2:')   # Can use PROJ.4 or PROJ.5+ API
    depends_on('everytrace', when='+everytrace')

    extends('python', type=('build', 'run'), when='+python')
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'), when='@1.1: +python')
    depends_on('python@2.7:2.8', type=('build', 'run'), when='@:1.0 +python')
    depends_on('swig', type='build', when='+python')
    depends_on('py-petsc4py', type=('build', 'run'), when='+python')

    # The following Python packages are needed to do all the examples
    # in the User’s Manual (which run Python scripts):
    # https://pism-docs.org/sphinx/installation/prerequisites.html
    depends_on('py-matplotlib', type=('run'), when='+python')
    depends_on('py-numpy', type=('run'), when='+python')
    depends_on('py-netcdf4', type=('run'), when='+python')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            # Fortran not needed for PISM...
            # '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DPism_BUILD_EXTRA_EXECS=%s' %
            ('YES' if '+extra' in spec else 'NO'),
            '-DBUILD_SHARED_LIBS=%s' %
            ('YES' if '+shared' in spec else 'NO'),
            '-DPism_BUILD_PYTHON_BINDINGS=%s' %
            ('YES' if '+python' in spec else 'NO'),
            '-DPism_BUILD_ICEBIN=%s' %
            ('YES' if '+icebin' in spec else 'NO'),
            '-DPism_USE_PROJ4=%s' %
            ('YES' if '+proj' in spec else 'NO'),
            '-DPism_USE_PARALLEL_NETCDF4=%s' %
            ('YES' if '+parallel-netcdf4' in spec else 'NO'),
            '-DPism_USE_PNETCDF=%s' %
            ('YES' if '+parallel-netcdf3' in spec else 'NO'),
            '-DPism_USE_PARALLEL_HDF5=%s' %
            ('YES' if '+parallel-hdf5' in spec else 'NO'),
            '-DPism_BUILD_PDFS=%s' %
            ('YES' if '+doc' in spec else 'NO'),
            '-DPism_INSTALL_EXAMPLES=%s' %
            ('YES' if '+examples' in spec else 'NO'),
            '-DPism_USE_EVERYTRACE=%s' %
            ('YES' if '+everytrace' in spec else 'NO')]

        # See suggestion at https://github.com/spack/spack/issues/16246
        if spec.satisfies('+python'):
            args.append('-DPYTHON_EXECUTABLE:FILEPATH={0}'.format(
            self.spec['python'].command.path))

        return args

    def setup_run_environment(self, env):
        env.set('PISM_PREFIX', self.prefix)
        env.set('PISM_BIN', self.prefix.bin)


# From email correspondence with Constantine Khroulev:
#
# > Do you have handy a table of which versions of PETSc are required
# > for which versions of PISM?
#
# We don't. The installation manual [1] specifies the minimum PETSc
# version for the latest "stable" release (currently PETSc 3.3). The
# stable PISM version should support all PETSc versions starting from the
# one specified in the manual and up to the latest PETSc release.
#
# The current development PISM version should be built with the latest
# PETSc release at the time (the "maint" branch of PETSc).
#
# Thanks to Git it is relatively easy to find this info, though:
#
# | PISM version | PETSc version |
# |--------------+---------------|
# |          0.7 | 3.3 and later |
# |          0.6 | 3.3           |
# |       new_bc | 3.4.4         |
# |          0.5 | 3.2           |
# |          0.4 | 3.1           |
# |          0.3 | 2.3.3 to 3.1  |
# |          0.2 | 2.3.3 to 3.0  |
# |          0.1 | 2.3.3-p2      |



# Correspondence with @ckhroulev March 2019
#
#  > What are the implications to PISM of building PETSc with / without 
# scalapack?
# 
# The only effect is on PISM's performance (i.e. faster / slower), 
# although we haven't used ScaLAPACK and don't know if it makes any 
# difference.
# 
# There are two reasons we recommend building PETSc with "--with-fc=0":
# 
# 1) PISM does not use PETSc's Fortran API.
# 2) Because of 1) most PISM users don't need to install a Fortran compiler.
# 
# You cannot build PISM using PETSc configured with 
# "--with-scalar-type=complex". Other than that you are free to configure 
# PETSc any way you want, e.g. with or without ScaLAPACK and with or 
# without Fortran support. So feel free to remove --with-fc=0 if you need to.
