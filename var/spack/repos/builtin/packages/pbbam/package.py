# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pbbam(CMakePackage):
    """The pbbam software package provides components to create, query,
    & edit PacBio BAM files and associated indices.
    These components include a core C++ library,
    bindings for additional languages, and command-line utilities."""

    homepage = "https://github.com/PacificBiosciences/pbbam"
    url      = "https://github.com/PacificBiosciences/pbbam/archive/0.18.0.tar.gz"

    version('0.18.0', sha256='45286e5f7deb7ff629e0643c8a416155915aec7b85d54c60b5cdc07f4d7b234a')

    depends_on('zlib')
    depends_on('boost@1.55.0:')
    depends_on('htslib@1.3.1:')
    depends_on('doxygen+graphviz')

    conflicts('%gcc@:5.2.0')

    def cmake_args(self):
        options = []
        if self.run_tests:
            options.append('-DPacBioBAM_build_tests:BOOL=ON')
        else:
            options.append('-DPacBioBAM_build_tests:BOOL=OFF')

        return options

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree('bin', prefix.bin)
            install_tree('lib', prefix.lib)
            install_tree('pbbam', prefix.include.pbbam)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('PacBioBAM_LIBRARIES', self.prefix.lib)
        env.set('PacBioBAM_INCLUDE_DIRS', self.prefix.include)
