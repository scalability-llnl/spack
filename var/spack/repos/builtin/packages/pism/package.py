from spack import *
import spack.build_environment
import llnl.util.tty as tty
import os

class Pism(CMakePackage):
    """Parallel Ice Sheet Model"""

    homepage = "http://pism-docs.org/wiki/doku.php:="
    url      = "https://github.com/pism/pism/tarball/123"

    version('88beceba', 'de444fc48fd1e818c23e459bb3d74202')		# On the new_bc branch


    variant('extra', default=False, description='Build extra executables (mostly testing/verification)')
    variant('shared', default=True, description='Build shared Pism libraries')
    variant('python', default=False, description='Build python bindings')
    variant('proj', default=False, description='Use Proj.4 to compute cell areas, longitudes, and latitudes.')
    variant('parallel-netcdf4', default=False, description='Enables parallel NetCDF-4 I/O.')
    variant('parallel-netcdf3', default=False, description='Enables parallel NetCDF-3 I/O using PnetCDF.')
    variant('parallel-hdf5', default=False, description='Enables parallel HDF5 I/O.')
    #variant('tao', default=False, description='Use TAO in inverse solvers.')

    # CMake build options not transferred to Spack variants
    #option (Pism_TEST_USING_VALGRIND "Add extra regression tests using valgrind" OFF)
    #mark_as_advanced (Pism_TEST_USING_VALGRIND)
    #
    #option (Pism_ADD_FPIC "Add -fPIC to C++ compiler flags (CMAKE_CXX_FLAGS). Try turning it off if it does not work." ON)
    #option (Pism_LINK_STATICALLY "Set CMake flags to try to ensure that everything is linked statically")
    #option (Pism_LOOK_FOR_LIBRARIES "Specifies whether PISM should look for libraries. (Disable this on Crays.)" ON)
    #option (Pism_USE_TR1 "Use the std::tr1 namespace to access shared pointer definitions. Disable to get shared pointers from the std namespace (might be needed with some compilers)." ON)
	#option (Pism_USE_TAO "Use TAO in inverse solvers." OFF)

    depends_on('fftw')
    depends_on('gsl')
    depends_on('mpi')
    depends_on('netcdf')    # Only the C interface is used, no netcdf-cxx4
    depends_on('petsc')
    depends_on('udunits2')
    depends_on('proj')

    extends('python@2.7', when='+python')			# Is this OK even if we we're building ~python variant?
    depends_on('py-matplotlib', when='+python')        # Implies py-numpy too

    # Build dependencies
    depends_on('cmake')

    def config_args(self, spec, prefix):
        return [
            '-DPism_BUILD_EXTRA_EXECS=%s' % ('YES' if '+extra' in spec else 'NO'),
            '-DBUILD_SHARED_LIBS     =%s' % ('YES' if '+shared' in spec else 'NO'),
            '-DPism_BUILD_PYTHON_BINDINGS=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DPism_USE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
            '-DPism_USE_PARALLEL_NETCDF4=%s' % ('YES' if '+parallel-netcdf4' in spec else 'NO'),
            '-DPism_USE_PNETCDF=%s' % ('YES' if '+parallel-netcdf3' in spec else 'NO'),
            '-DPism_USE_PARALLEL_HDF5=%s' % ('YES' if '+parallel-hdf5' in spec else 'NO')]

    def install_version(self, spec, prefix):
        #cmake = which('cmake')
        #make = which('make')


        options = self.config_args(spec, prefix) + spack.build_environment.get_std_cmake_args(self)

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        with working_dir(build_directory, create=True):
            print 'CMAKE', source_directory, options
            cmake(source_directory, *options)
            make()
            make("install")   # Installs binaries but no headers
            print 'PATH', self.stage.path
            print 'SOURCE_PATH', self.stage.source_path
            print 'CMAKE2', source_directory
            install_tree(os.path.join(source_directory, 'src'), prefix.include)

# > Do you have handy a table of which versions of PETSc are required for which
# > versions of PISM?
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
