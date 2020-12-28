# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybedtools(PythonPackage):
    """Python wrapper -- and more -- for Aaron Quinlan's BEDTools"""

    homepage = "http://daler.github.io/pybedtools"
    url      = "https://github.com/daler/pybedtools/archive/v0.6.9.tar.gz"

    version('0.8.0', sha256='f0d9f24135d13d6d02d5c0d1bded771848d3642b00a2d3c3d86b2a1fcd5ce532')
    version('0.7.10', sha256='bc81c1655e998d8090d852f109925fc7fd3dad3ff90371cf80807dd4438a826a')
    version('0.7.9',  sha256='49cdb62b81bb6bf28fecf6fc9519aa31e333d150347ca4ce2d2cd2aa5ec2ca57')
    version('0.7.8',  sha256='0d49d92ba6d6cec85956cc4f947c9f431dc30aeea05125643a1b8786a59dc402')
    version('0.7.7',  sha256='e4f87da5009928046ac233d2c8a7c2121820aa6d74de45922ec1405464c62862')
    version('0.7.6',  sha256='639880a45ef60bd10d4ed31e6e7f7e901a6dbd909373df8f63f5aeccde446754')
    version('0.7.5',  sha256='ef221c38281cb9be1e8014d6513f6fd9b2722306a70e4ac2484d0d7034bc5b03')
    version('0.7.4',  sha256='39172a31c59ccf355fcff885f652cdc825341cabbab4ba78ac03862c42caa9da')
    version('0.7.3',  sha256='ba6875297116b776cb1eb79ddb9fe24db9cbee8f6922940f84984d533ef9000b')
    version('0.7.2',  sha256='0d0a80a42667742d53b1ef1947f4645dc16b060c7aacb4721c48f8028cc33c5e')
    version('0.6.9',  sha256='2639e80917999e76572017fd93757e8d7ceb384f0b92647ccfdd23a0d60def7c')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')

    depends_on('bedtools2', type='run')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
