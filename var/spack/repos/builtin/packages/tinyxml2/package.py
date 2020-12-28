# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tinyxml2(CMakePackage):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml2/"
    url = "https://github.com/leethomason/tinyxml2/archive/3.0.0.tar.gz"

    version('4.0.1', sha256='14b38ef25cc136d71339ceeafb4856bb638d486614103453eccd323849267f20')
    version('4.0.0', sha256='90add44f06de081047d431c08d7269c25b4030e5fe19c3bc8381c001ce8f258c')
    version('3.0.0', sha256='128aa1553e88403833e0cccf1b651f45ce87bc207871f53fdcc8e7f9ec795747')
    version('2.2.0', sha256='f891224f32e7a06bf279290619cec80cc8ddc335c13696872195ffb87f5bce67')
    version('2.1.0', sha256='4bdd6569fdce00460bf9cda0ff5dcff46d342b4595900d849cc46a277a74cce6')
    version('2.0.2', sha256='3cc3aa09cd1ce77736f23488c7cb24e65e11daed4e870ddc8d352aa4070c7c74')
