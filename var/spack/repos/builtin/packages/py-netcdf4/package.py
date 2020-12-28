# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetcdf4(PythonPackage):
    """Python interface to the netCDF Library."""

    homepage = "https://github.com/Unidata/netcdf4-python"
    url      = "https://pypi.io/packages/source/n/netCDF4/netCDF4-1.2.7.tar.gz"

    maintainers = ['skosukhin']

    version('1.5.3',   sha256='2a3ca855848f4bbf07fac366da77a681fcead18c0a8813d91d46302f562dc3be')
    version('1.4.2',   sha256='b934af350459cf9041bcdf5472e2aa56ed7321c018d918e9f325ec9a1f9d1a30')
    version('1.2.7',   sha256='0c449b60183ee06238a8f9a75de7b0eed3acaa7a374952ff9f1ff06beb8f94ba')
    version('1.2.3.1', sha256='55edd74ef9aabb1f7d1ea3ffbab9c555da2a95632a97f91c0242281dc5eb919f')

    depends_on('py-setuptools',   type='build')
    depends_on('py-cython@0.19:', type='build')

    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-cftime', type=('build', 'run'))

    depends_on('netcdf-c')
    depends_on('hdf5@1.8.0:+hl')

    # The installation script tries to find hdf5 using pkg-config. However, the
    # version of hdf5 installed with Spack does not have pkg-config files.
    # Therefore, if pkg-config finds hdf5.pc at all (e.g. provided by
    # Ubuntu/Debian package manager), it is definitely not what we need. The
    # following patch disables the usage of pkg-config at all.
    patch('disable_pkgconf.patch')

    # Older versions of the package get a false negative result when checking
    # the version of HDF5.
    patch('check_hdf5version.patch', when='@:1.2.9 ^hdf5@1.10:')

    # We can skip the 'build' phase to avoid recompilation of the library.
    phases = ['install']

    def setup_build_environment(self, env):
        """Ensure installed netcdf and hdf5 libraries are used"""
        # Explicitly set these variables so setup.py won't erroneously pick up
        # system versions
        # See: http://unidata.github.io/netcdf4-python
        env.set('USE_SETUPCFG', '0')
        env.set('USE_NCCONFIG', '1')
        env.set('HDF5_DIR', self.spec['hdf5'].prefix)
        env.set('HDF5_INCDIR', self.spec['hdf5'].prefix.include)
        env.set('HDF5_LIBDIR', self.spec['hdf5'].prefix.lib)
        env.set('NETCDF4_DIR', self.spec['netcdf-c'].prefix)
        env.set('NETCDF4_INCDIR', self.spec['netcdf-c'].prefix.include)
        env.set('NETCDF4_LIBDIR', self.spec['netcdf-c'].prefix.lib)
