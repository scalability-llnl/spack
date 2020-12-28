# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcpp(RPackage):
    """The 'Rcpp' package provides R functions as well as C++ classes which
    offer a seamless integration of R and C++. Many R data types and objects
    can be mapped back and forth to C++ equivalents which facilitates both
    writing of new code as well as easier integration of third-party libraries.
    Documentation about 'Rcpp' is provided by several vignettes included in
    this package, via the 'Rcpp Gallery' site at <http://gallery.rcpp.org>, the
    paper by Eddelbuettel and Francois (2011, JSS), and the book by
    Eddelbuettel (2013, Springer); see 'citation("Rcpp")' for details on these
    last two."""

    homepage = "http://dirk.eddelbuettel.com/code/rcpp.html"
    url      = "https://cloud.r-project.org/src/contrib/Rcpp_0.12.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rcpp"

    version('1.0.4.6', sha256='45af675ddbbe155e671453b2e84fe32250bb98d4ccb4342b61c1e25cff10b302')
    version('1.0.2', sha256='ad9338d6fc89dd116a3e2c5ecef1956e4be63b6c6aa1b21b2e5f249d65a5129c')
    version('1.0.0',   sha256='b7378bf0dda17ef72aa3f2a318a9cb5667bef50b601dc1096431e17426e18bc2')
    version('0.12.19', sha256='63aeb6d4b58cd2899ded26f38a77d461397d5b0dc5936f187d3ca6cd958ab582')
    version('0.12.18', sha256='fcecd01e53cfcbcf58dec19842b7235a917b8d98988e4003cc090478c5bbd300')
    version('0.12.17', sha256='4227c45c92416b5378ed5761495f9b3932d481bae9a190fb584d17c10744af23')
    version('0.12.16', sha256='d4e1636e53e2b656e173b49085b7abbb627981787cd63d63df325c713c83a8e6')
    version('0.12.15', sha256='bb6fddf67c888ec4e28cdf72539663cdbda8df5861e5579f4fc6b64da836dbde')
    version('0.12.14', sha256='da28fcfc3fe7c48d02f9f3e309b56f4be52b14a01216a23e3de8f9d6deeb7e63')
    version('0.12.13', sha256='a570ad88282fb961ba32c867c49dbd3dce6f4dfc7b59ab1fbde510449827a8ae')
    version('0.12.12', sha256='9f3eb1e6154f4d56b52ab550a22e522e9999c7998388fdc235e48af5e8c6deaf')
    version('0.12.11', sha256='bd8cae275bb45cf98f3e3c6e1b5189bdd9c02e74b25241419ed3e4851d859c7f')
    version('0.12.9', sha256='f0bd0df28ded09cb3cb5c2a348e2f81d1a2bf0b2248e9aecd67aeeeaeabbcd5e')
    version('0.12.6', sha256='1bb54e03b817a3d6ab5917f1bbf5250c6b33f61e466628a378022ed65a010141')
    version('0.12.5', sha256='13449481c91b5271b34d81f462864864c1905bb05021781eee11c36fdafa80ef')

    depends_on('r@3.0.0:', type=('build', 'run'))
