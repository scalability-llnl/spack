# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Manta(CMakePackage):
    """Structural variant and indel caller for mapped sequencing data"""

    homepage = "https://github.com/Illumina/manta"
    url      = "https://github.com/Illumina/manta/releases/download/v1.3.2/manta-1.3.2.release_src.tar.bz2"

    version('1.6.0', sha256='c846d61b02483265c09d58bd85dacf5326a94f38179b5ae4f70694be96e1368f')
    version('1.5.0', sha256='9aa1a59c9cb8d2dd33724a42959c9398aff7840c5bf3c895d2483a8093b3d2dc')
    version('1.4.0', sha256='4f8f827485e3ad9a12318bfcbf62fa622263378767514eb938bc02ad5ad74f10')
    version('1.3.2', sha256='eb346d1a44aff1180732dcd03864b89efc1245652e1993107fb60da4ad739f79')
    version('1.3.1', sha256='9ba943623088e552a4b45bccea48125a0553905f4cc7ea86a9de567e155a5888')
    version('1.3.0', sha256='3db4b5475c33e3aeeb5435969c74364af9d2d77dd3bcf8dc70bf44a851e450dd')

    depends_on('cmake@2.8.12:', type='build')
    depends_on('python@2.7.0:2.7.999', type=('build', 'run'))
    depends_on('zlib')

    patch('for_aarch64.patch', when='target=aarch64:')
