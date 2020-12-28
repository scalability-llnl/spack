# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class BlasrLibcpp(Package):
    """Blasr_libcpp is a library used by blasr
    and other executables such as samtoh5,
    loadPulses for analyzing PacBio sequences."""

    homepage = "https://github.com/PacificBiosciences/blasr_libcpp"
    url      = "https://github.com/PacificBiosciences/blasr_libcpp/archive/5.3.1.tar.gz"

    maintainers = ['robqiao']

    version('5.3.1', sha256='45a673255bfe7e29ed1f5bdb6410aa45cb6b907400d038c3da9daf1058b09156')

    depends_on('pbbam')
    depends_on('hdf5+cxx@1.8.12:1.8.99')
    # maximum version is 1.8.20 currently. There doesn't appear to be a
    # major version 1.9 and the 1.10.1 version doesn't build correctly.
    # https://github.com/PacificBiosciences/blasr/issues/355

    depends_on('python@2.7:2.8', type='build')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        configure_args = [
            'PBBAM_INC={0}'.format(self.spec['pbbam'].prefix.include),
            'PBBAM_LIB={0}'.format(self.spec['pbbam'].prefix.lib),
            'HDF5_INC={0}'.format(self.spec['hdf5'].prefix.include),
            'HDF5_LIB={0}'.format(self.spec['hdf5'].prefix.lib)
        ]
        python('configure.py', *configure_args)

    def build(self, spec, prefix):
        os.environ['CPLUS_INCLUDE_PATH'] = self.stage.source_path
        make()

    def install(self, spec, prefix):
        install_tree('alignment', prefix.alignment)
        install_tree('hdf', prefix.hdf)
        install_tree('pbdata', prefix.pbdata)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('LD_LIBRARY_PATH', self.spec.prefix.hdf)
        env.prepend_path('LD_LIBRARY_PATH', self.spec.prefix.alignment)
        env.prepend_path('LD_LIBRARY_PATH', self.spec.prefix.pbdata)

    def setup_run_environment(self, env):
        env.prepend_path('LD_LIBRARY_PATH',
                         self.spec['blasr-libcpp'].prefix.pbdata)
        env.prepend_path('LD_LIBRARY_PATH',
                         self.spec['blasr-libcpp'].prefix.alignment)
        env.prepend_path('LD_LIBRARY_PATH',
                         self.spec['blasr-libcpp'].prefix.hdf)
