# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMatrix(RPackage):
    """Classes and methods for dense and sparse matrices and operations on them
    using 'LAPACK' and 'SuiteSparse'."""

    homepage = "http://matrix.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/Matrix_1.2-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Matrix"

    version('1.2-17', sha256='db43e6f0196fd5dfd05a7e88cac193877352c60d771d4ec8772763e645723fcc')
    version('1.2-14', sha256='49a6403547b66675cb44c1afb04bb87130c054510cb2b94971435a826ab41396')
    version('1.2-11', sha256='ba8cd6565612552fe397e909721817b6cc0604a91299d56d118208006888dc0b')
    version('1.2-8',  sha256='3cd2a187c45fc18a0766dc148b7f83dbf6f2163c256e887c41cbaa7c9a20dbb7')
    version('1.2-6',  sha256='4b49b639b7bf612fa3d1c1b1c68125ec7859c8cdadae0c13f499f24099fd5f20')

    depends_on('r@3.0.1:', when='@:1.2-12', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@1.2.13:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
