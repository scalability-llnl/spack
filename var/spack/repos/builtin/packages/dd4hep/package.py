# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dd4hep(CMakePackage):
    """DD4hep is a software framework for providing a complete solution for
       full detector description (geometry, materials, visualization, readout,
       alignment, calibration, etc.) for the full experiment life cycle
       (detector concept development, detector optimization, construction,
       operation). It offers a consistent description through a single source
       of detector information for simulation, reconstruction, analysis, etc.
       It distributed under the LGPLv3 License."""

    homepage = "https://dd4hep.web.cern.ch/dd4hep/"
    url      = "https://github.com/AIDASoft/DD4hep/archive/v01-12-01.tar.gz"
    git      = "https://github.com/AIDASoft/DD4hep.git"

    maintainers = ['vvolkl', 'drbenmorgan']

    tags = ['hep']

    version('master', branch='master')
    version('1.16', sha256='ea9755cd255cf1b058e0e3cd743101ca9ca5ff79f4c60be89f9ba72b1ae5ec69')
    version('1.15', sha256='992a24bd4b3dfaffecec9d1c09e8cde2c7f89d38756879a47b23208242f4e352')
    version('1.14.1', sha256='5b5742f1e23c2b36d3174cca95f810ce909c0eb66f3d6d7acb0ba657819e6717')
    version('1.14', sha256='b603aa3c0db8dda392253aa71fa4a0f0c3c9715d47df0b895d45c1e8849f4895')
    version('1.13.1', sha256='83fa70cd74ce93b2f52f098388dff58d179f05ace5b50aea3f408bb8abf7cb73')
    version('1.13', sha256='0b1f9d902ebe21a9178c1e41204c066b29f68c8836fd1d03a9ce979811ddb295')
    version('1.12.1', sha256='85e8c775ec03c499ce10911e228342e757c81ce9ef2a9195cb253b85175a2e93')
    version('1.12', sha256='133a1fb8ce0466d2482f3ebb03e60b3bebb9b2d3e33d14ba15c8fbb91706b398')
    version('1.11.2', sha256='96a53dd26cb8df11c6dae54669fbc9cc3c90dd47c67e07b24be9a1341c95abc4')
    version('1.11.1', sha256='d7902dd7f6744bbda92f6e303ad5a3410eec4a0d2195cdc86f6c1167e72893f0')
    version('1.11', sha256='25643296f15f9d11ad4ad550b7c3b92e8974fc56f1ee8e4455501010789ae7b6')
    version('1.10', sha256='1d6b5d1c368dc8bcedd9c61b7c7e1a44bad427f8bd34932516aff47c88a31d95')

    generator = 'Ninja'

    # Workarounds for various TBB issues in DD4hep v1.11
    # See https://github.com/AIDASoft/DD4hep/pull/613 .
    patch('tbb-workarounds.patch', when='@1.11')
    patch('tbb2.patch', when='@1.12.1')

    variant('xercesc', default=False, description="Enable 'Detector Builders' based on XercesC")
    variant('geant4', default=False, description="Enable the simulation part based on Geant4")
    variant('assimp', default=False, description="Enable CAD interface based on Assimp")
    variant('hepmc3', default=False, description="Enable build with hepmc3")
    variant('lcio', default=False, description="Enable build with lcio")
    variant('edm4hep', default=True, description="Enable build with edm4hep")
    variant('geant4units', default=False, description="Use geant4 units throughout")
    variant('debug', default=False,
            description="Enable debug build flag - adds extra info in"
            " some places in addtion to the debug build type")

    depends_on('cmake @3.12:', type='build')
    depends_on('ninja', type='build')
    depends_on('boost @1.49:')
    depends_on('root @6.08: +gdml +math +opengl +python +x')
    extends('python')
    depends_on('xerces-c', when='+xercesc')
    depends_on('geant4@10.2.2:', when='+geant4')
    depends_on('assimp@5.0.2:', when='+assimp')
    depends_on('hepmc3', when="+hepmc3")
    depends_on('lcio', when="+lcio")
    depends_on('edm4hep', when="+edm4hep")

    def cmake_args(self):
        spec = self.spec
        cxxstd = spec['root'].variants['cxxstd'].value
        # root can be built with cxxstd=11, but dd4hep requires 14
        if cxxstd == "11":
            cxxstd = "14"
        args = [
            self.define_from_variant('DD4HEP_USE_EDM4HEP', 'edm4hep'),
            self.define_from_variant('DD4HEP_USE_XERCESC', 'xercesc'),
            self.define_from_variant('DD4HEP_USE_GEANT4', 'geant4'),
            self.define_from_variant('DD4HEP_USE_LCIO', 'lcio'),
            self.define_from_variant('DD4HEP_USE_HEPMC3', 'hepmc3'),
            self.define_from_variant('DD4HEP_USE_GEANT4_UNITS', 'geant4units'),
            self.define_from_variant('DD4HEP_BUILD_DEBUG', 'debug'),
            # Downloads assimp from github and builds it on the fly.
            # However, with spack it is preferrable to have a proper external
            # dependency, so we disable it.
            self.define('DD4HEP_LOAD_ASSIMP', False),
            "-DCMAKE_CXX_STANDARD={0}".format(cxxstd),
            "-DBUILD_TESTING={0}".format(self.run_tests),
            "-DBOOST_ROOT={0}".format(spec['boost'].prefix),
            "-DBoost_NO_BOOST_CMAKE=ON",
            "-DPYTHON_EXECUTABLE={0}".format(spec['python'].command.path),
        ]
        return args

    def setup_run_environment(self, env):
        # used p.ex. in ddsim to find DDDetectors dir
        env.set("DD4hepINSTALL", self.prefix)
        env.set("DD4HEP", self.prefix.examples)
        env.set("DD4hep_DIR", self.prefix)
        env.set("DD4hep_ROOT", self.prefix)

    def url_for_version(self, version):
        # dd4hep releases are dashes and padded with a leading zero
        # the patch version is omitted when 0
        # so for example v01-12-01, v01-12 ...
        base_url = self.url.rsplit('/', 1)[0]
        if len(version) == 1:
            major = version[0]
            minor, patch = 0, 0
        elif len(version) == 2:
            major, minor = version
            patch = 0
        else:
            major, minor, patch = version
        # By now the data is normalized enough to handle it easily depending
        # on the value of the patch version
        if patch == 0:
            version_str = 'v%02d-%02d.tar.gz' % (major, minor)
        else:
            version_str = 'v%02d-%02d-%02d.tar.gz' % (major, minor, patch)

        return base_url + '/' + version_str
