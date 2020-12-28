# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRversions(RPackage):
    """Query the main 'R' 'SVN' repository to find the versions
       'r-release' and 'r-oldrel' refer to, and also all previous 'R'
       versions and their release dates.
    """

    homepage = "https://cloud.r-project.org/package=rversions"
    url      = "https://cloud.r-project.org/src/contrib/rversions_2.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rversions"

    version('2.0.1', sha256='51ec1f64e7d628e88d716a020d5d521eba71d472e3c9ae7b694428ef6dd786c5')
    version('2.0.0', sha256='b50c321d9e973284ae6b1d0c89bd46a40f5174de51fb28e3c77cd12ef34f6f56')
    version('1.1.0', sha256='14a5a2f06b74e332fd9cbd4d715baa6165f5269c9ba2c0b9f1d0c6540dde9c3c')
    version('1.0.3', sha256='21d0809f46505de89a2be7be9449e39c39cff5bc77e584dec976ee6c0b884f44')
    version('1.0.2', sha256='c8ec8e24524cc42893e445e01e1a65d15889d28959877cd6b3c5e5f08221b176')
    version('1.0.1', sha256='9099d37d2f6cc1cab0cd0fdddfb9657c7bd3651226810b496e2808f458c80ae3')
    version('1.0.0', sha256='ce1e5368ff1d15665ca2db700521a96cf44f0e78daaab68aabbdaf7ed7393b4d')

    depends_on('r-curl', type=('build', 'run'))
    depends_on('r-xml2@1.0.0:', type=('build', 'run'))
