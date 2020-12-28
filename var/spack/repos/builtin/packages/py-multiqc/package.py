# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiqc(PythonPackage):
    """MultiQC is a tool to aggregate bioinformatics results across many
    samples into a single report. It is written in Python and contains modules
    for a large number of common bioinformatics tools."""

    homepage = "https://multiqc.info"
    url      = "https://pypi.io/packages/source/m/multiqc/multiqc-1.0.tar.gz"

    version('1.7', sha256='02e6a7fac7cd9ed036dcc6c92b8f8bcacbd28983ba6be53afb35e08868bd2d68')
    version('1.5', sha256='fe0ffd2b0d1067365ba4e54ae8991f2f779c7c684b037549b617020ea883310a')
    version('1.3', sha256='cde17845680131e16521ace04235bb9496c78c44cdc7b5a0fb6fd93f4ad7a13b')
    version('1.0', sha256='1a49331a3d3f2e591a6e9902bc99b16e9205731f0cd2d6eaeee0da3d0f0664c9')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-jinja2@2.9:', type=('build', 'run'))
    depends_on('py-lzstring', type=('build', 'run'))
    depends_on('py-future@0.14.1:', type=('build', 'run'))
    depends_on('py-spectra@0.0.10:', type=('build', 'run'))
    depends_on('py-matplotlib@2.0.0:2.9.9', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-simplejson', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'), when='@1.5:')
    depends_on('py-enum34', type=('build', 'run'), when='@1.4:1.5 ^python@:3.3')
    depends_on('py-enum34', type=('build', 'run'), when='@1.3')
    depends_on('py-markdown', type=('build', 'run'), when='@1.5:')
