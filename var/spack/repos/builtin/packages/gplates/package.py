# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Gplates(CMakePackage):
    """GPlates is desktop software for the interactive visualisation of
    plate-tectonics. GPlates offers a novel combination of interactive
    plate-tectonic reconstructions, geographic information system (GIS)
    functionality and raster data visualisation. GPlates enables both the
    visualisation and the manipulation of plate-tectonic reconstructions
    and associated data through geological time."""

    homepage = 'https://www.gplates.org'
    url      = 'https://sourceforge.net/projects/gplates/files/gplates/2.0/gplates-2.0.0-unixsrc.tar.bz2/download'

    version('2.1.0', sha256='5a52242520d7e243c541e164c8417b23f4e17fcd79ed81f865b2c13628bb0e07')
    version('2.0.0', sha256='1c27d3932a851153baee7cec48e57c2bbc87e4eea02f8a986882515ba4b44c0b')

    depends_on('cmake@2.8.8:', type='build')
    depends_on('ninja', type='build')
    # Qt 5 does not support (at least) the Q_WS_* constants.
    depends_on('qt+opengl@4.4.0:4.99')
    depends_on('qwt@6.0.1:')
    depends_on('glu')
    depends_on('glew')
    # GDAL's OGRSFDriverRegistrar is not compatible anymore starting with 2.0.
    depends_on('gdal@1.3.2:1.99')
    depends_on('cgal@3.5:')
    # The latest release of gplates came out before PROJ.6 was released,
    # so I'm assuming it's not supported.
    depends_on('proj@4.6.0:5')
    # Boost's Python library has a different name starting with 1.67.
    # There were changes to Boost's optional in 1.61 that make the build fail.
    depends_on('boost+python@1.34:1.60')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('python@2:2.99')

    # When built in parallel, headers are not generated before they are used
    # (specifically, ViewportWindowUi.h) with the Makefiles generator.
    generator = 'Ninja'

    def url_for_version(self, version):
        url = 'https://sourceforge.net/projects/gplates/files/gplates/{0}/gplates-{1}-unixsrc.tar.bz2/download'
        return url.format(version.up_to(2), version)

    def patch(self):
        # GPlates overrides FindPythonLibs and finds the static library, which
        # can not be used easily. Fall back to CMake's version, which finds
        # the shared library instead.
        force_remove('cmake/modules/FindPythonLibs.cmake')

        # GPlates only installs its binary for the Release configuration.
        filter_file('CONFIGURATIONS release',
                    'CONFIGURATIONS Debug Release RelWithDebInfo MinSizeRel',
                    'src/CMakeLists.txt')
