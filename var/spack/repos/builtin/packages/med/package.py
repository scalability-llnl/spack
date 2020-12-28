# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Med(CMakePackage):
    """The MED file format is a specialization of the HDF5 standard."""

    homepage = "http://docs.salome-platform.org/latest/dev/MEDCoupling/med-file.html"
    url = "http://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz"

    maintainers = ['likask']

    version('4.0.0', sha256='a474e90b5882ce69c5e9f66f6359c53b8b73eb448c5f631fa96e8cd2c14df004')
    version('3.2.0', sha256='d52e9a1bdd10f31aa154c34a5799b48d4266dc6b4a5ee05a9ceda525f2c6c138')

    variant('api23', default=True, description='Enable API2.3')

    depends_on('mpi')
    depends_on('hdf5@:1.8.19+mpi', when='@3.2.0')
    depends_on('hdf5@:1.10.2+mpi', when='@4.0.0')

    # C++11 requires a space between literal and identifier
    patch('add_space.patch', when='@3.2.0')

    # FIXME This is minimal installation.

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+api23' in spec:
            options.extend([
                '-DCMAKE_CXX_FLAGS:STRING=-DMED_API_23=1',
                '-DCMAKE_C_FLAGS:STRING=-DMED_API_23=1',
                '-DMED_API_23=1'])

        options.extend([
            '-DMEDFILE_USE_MPI=YES'
            '-DMEDFILE_BUILD_TESTS={0}'.format(
                'ON' if self.run_tests else 'OFF'),
            '-DMEDFILE_BUILD_PYTHON=OFF',
            '-DMEDFILE_INSTALL_DOC=OFF',
            '-DMEDFILE_BUILD_SHARED_LIBS=OFF',
            '-DMEDFILE_BUILD_STATIC_LIBS=ON',
            '-DCMAKE_Fortran_COMPILER='])

        options.extend([
            '-DHDF5_ROOT_DIR=%s' % spec['hdf5'].prefix,
            '-DMPI_ROOT_DIR=%s' % spec['mpi'].prefix])

        return options
