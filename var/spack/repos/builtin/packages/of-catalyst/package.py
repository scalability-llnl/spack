# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OfCatalyst(CMakePackage):
    """Of-catalyst is a library for OpenFOAM that provides a runtime-selectable
    function object for embedding ParaView Catalyst in-situ visualization
    into arbitrary OpenFOAM simulations.
    Supports in-situ conversion of the following types:
      1) finite volume meshes and fields, single or multi-region;
      2) finite area meshes and fields, single region;
      3) lagrangian (clouds), single or multiple clouds.
    This offering is part of the community repository supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """

    # Currently only via git
    homepage = "https://develop.openfoam.com/Community/catalyst"
    gitrepo  = "https://develop.openfoam.com/Community/catalyst.git"

    version('1806', git=gitrepo, tag='v1806')
    version('develop', branch='develop', git=gitrepo)

    variant('full', default=False, description='Build against paraview (full) or catalyst (light)')

    depends_on('openfoam-com@1806', when='@1806', type=('build', 'link', 'run'))
    depends_on('openfoam-com@develop', when='@develop', type=('build', 'link', 'run'))
    depends_on('catalyst@5.5:', when='~full')
    depends_on('paraview@5.5:+osmesa~qt', when='+full')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(self.prefix,
                             'lib'))

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return join_path(self.stage.source_path, join_path('src', 'catalyst'))

    def cmake_args(self):
        """Populate cmake arguments for ParaView."""
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY:PATH=%s' % join_path(
                self.stage.source_path,
                'spack-build'),
            '-DCMAKE_INSTALL_PREFIX:PATH=%s' % self.prefix
        ]

        return cmake_args
