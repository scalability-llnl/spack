# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ActsCore(CMakePackage):
    """
    A Common Tracking Software (ACTS)
    
    This project contains an experiment-independent set of track reconstruction tools. The main philosophy is to provide high-level track reconstruction modules that can be used for any tracking detector. The description of the tracking detector's geometry is optimized for efficient navigation and quick extrapolation of tracks. Converters for several common geometry description languages exist. Having a highly performant, yet largely customizable implementation of track reconstruction algorithms was a primary objective for the design of this toolset. Additionally, the applicability to real-life HEP experiments plays major role in the development process. Apart from algorithmic code, this project also provides an event data model for the description of track parameters and measurements.

    Key features of this project include: tracking geometry description which can be constructed from TGeo, DD4Hep, or GDML input, simple and efficient event data model, performant and highly flexible algorithms for track propagation and fitting, basic seed finding algorithms.
    """

    homepage = "http://acts.web.cern.ch/ACTS/"
    git      = "https://gitlab.cern.ch/acts/acts-core.git"

    version('develop', branch='master')
    version('0.8.0', commit='99eedb38f305e3a1cd99d9b4473241b7cd641fa9') # Used by acts-framework

    variant('legacy', default=True, description='Build the Legacy package')
    variant('examples', default=False, description='Build the examples')
    variant('tests', default=False, description='Build the unit tests')
    variant('integration_tests', default=False, description='Build the integration tests')
    variant('digitization', default=False, description='Build the geometric digitization plugin')
    variant('dd4hep', default=False, description='Build the DD4hep plugin')
    variant('tgeo', default=False, description='Build the TGeo plugin')
    variant('json', default=False, description='Build the Json plugin for Json geometry input/output')
    variant('material', default=False, description='Build the material plugin')

    depends_on('cmake @3.7:', type='build')
    depends_on('boost @1.62: +program_options +test')
    depends_on('eigen @3.2.9:', type='build')
    depends_on('root @6.10: cxxstd=14', when='+tgeo')
    depends_on('dd4hep @1.2:', when='+dd4hep')

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DACTS_BUILD_LEGACY={0}".format(spec.satisfies('+legacy')),
            "-DACTS_BUILD_EXAMPLES={0}".format(spec.satisfies('+examples')),
            "-DACTS_BUILD_TESTS={0}".format(spec.satisfies('+tests')),
            "-DACTS_BUILD_INTEGRATION_TESTS={0}".format(spec.satisfies('+integration_tests')),
            "-DACTS_BUILD_DIGITIZATION_PLUGIN={0}".format(spec.satisfies('+digitization')),
            "-DACTS_BUILD_DD4HEP_PLUGIN={0}".format(spec.satisfies('+dd4hep')),
            "-DACTS_BUILD_TGEO_PLUGIN={0}".format(spec.satisfies('+tgeo')),
            "-DACTS_BUILD_JSON_PLUGIN={0}".format(spec.satisfies('+json')),
            "-DACTS_BUILD_MATERIAL_PLUGIN={0}".format(spec.satisfies('+material'))
        ]
        return args

