# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAmap(RPackage):
    """Tools for Clustering and Principal Component Analysis
       (With robust methods, and parallelized functions)."""

    homepage = "http://mulcyber.toulouse.inra.fr/projects/amap/"
    url      = "https://cloud.r-project.org/src/contrib/amap_0.8-16.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/amap/"

    version('0.8-17', sha256='6b8473d1d35a9cbc611661882c8f681162e8f913f911ccd51629200ae72289c6')
    version('0.8-16', sha256='d3775ad7f660581f7d2f070e426be95ae0d6743622943e6f5491988e5217d4e2')

    depends_on('r@2.10.0:', when='@:0.8-16', type=('build', 'run'))
    depends_on('r@3.6.0:', when='@0.8-17:', type=('build', 'run'))
