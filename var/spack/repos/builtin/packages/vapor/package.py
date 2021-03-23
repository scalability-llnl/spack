# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vapor(CMakePackage):
    """VAPOR is the Visualization and Analysis Platform for Ocean, Atmosphere,
       and Solar Researchers.

       VAPOR provides an interactive 3D visualization environment that can also
       produce animations and still frame images."""

    homepage = "https://www.vapor.ucar.edu/"
    url      = "https://github.com/NCAR/VAPOR/archive/3.3.0.tar.gz"

    maintainers = ['RemiLacroix-IDRIS']

    version('3.3.0', sha256='508f93db9f6d9307be260820b878d054553aeb1719087a14770889f9e50a18ac')

    depends_on('gl')  # GUI
    depends_on('qt@5:+opengl+dbus')  # GUI
    depends_on('netcdf-c')
    depends_on('udunits')
    depends_on('freetype')
    depends_on('libgeotiff')
    depends_on('jpeg')
    depends_on('glew')  # GUI
    depends_on('assimp')
    depends_on('libtiff')
    depends_on('proj')
    depends_on('glm@0.9.9.1:')
    depends_on('python@3.6.0:3.6.99')
    depends_on('py-numpy')

    def cmake_args(self):
        with open('site.local', 'w') as f:
            python = self.spec['python']
            f.write('set (PYTHONVERSION {0})\n'.format(python.version.up_to(2)))
            f.write('set (PYTHONDIR {0})\n'.format(python.home))
            f.write('set (PYTHONPATH {0})\n'.format(python.package.site_packages_dir))

        args = ['-DBUILD_OSP=OFF']
        return args

    def setup_run_environment(self, env):
        # set VAPOR_HOME in the module file
        env.set('VAPOR_HOME', self.prefix)
