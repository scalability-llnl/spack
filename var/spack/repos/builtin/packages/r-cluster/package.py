# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCluster(RPackage):
    """Methods for Cluster analysis. Much extended the original from Peter
    Rousseeuw, Anja Struyf and Mia Hubert, based on Kaufman and Rousseeuw
    (1990) "Finding Groups in Data"."""

    homepage = "https://cloud.r-project.org/package=cluster"
    url      = "https://cloud.r-project.org/src/contrib/cluster_2.0.7-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cluster"

    version('2.1.0', sha256='eaf955bef8f616ea563351ec7f597c445aec43e65991ca975e382ef1fd70aa14')
    version('2.0.7-1', sha256='b10141090cf3c2b62260611a0ea822eb2f7bab9f4fd656c48bdc12b65c5c3dbf')
    version('2.0.5', sha256='4b309133bc2ad7b8fe4fa538dd69635bc8a4cd724a3c95f01084098876c57bae')
    version('2.0.4', sha256='d4d925c4fc1fc4f2e2e3c9208e518507aad6c28bb143b4358a05a8a8944ac6e4')

    depends_on('r@3.0.1:', when='@:2.0.6', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@2.0.7:2.0.7-1', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@2.0.8:', type=('build', 'run'))
