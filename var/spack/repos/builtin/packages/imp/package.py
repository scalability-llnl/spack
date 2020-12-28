# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imp(CMakePackage):
    """IMP, the Integrative Modeling Platform."""

    homepage = "https://integrativemodeling.org"
    url      = "https://github.com/salilab/imp/archive/2.8.0.tar.gz"

    version('2.8.0', sha256='0b46b8988febd7cdfc5838849007f9a547493ed4b6c752fe54571467eeb1acd2')

    depends_on('python@2.7:')
    depends_on('swig')
    depends_on('boost@1.40:')
    depends_on('hdf5')
    depends_on('eigen')
