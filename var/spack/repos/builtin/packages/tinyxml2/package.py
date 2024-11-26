# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tinyxml2(CMakePackage):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml2/"
    url = "https://github.com/leethomason/tinyxml2/archive/3.0.0.tar.gz"

    license("Zlib")

    version("10.0.0", sha256="3bdf15128ba16686e69bce256cc468e76c7b94ff2c7f391cc5ec09e40bff3839")
    version("9.0.0", sha256="cc2f1417c308b1f6acc54f88eb70771a0bf65f76282ce5c40e54cfe52952702c")
    version("8.0.0", sha256="6ce574fbb46751842d23089485ae73d3db12c1b6639cda7721bf3a7ee862012c")
    version("7.0.0", sha256="fa0d1c745d65d4d833e62cb183e23c2034dc7a35ec1a4977e808bdebb9b4fe60")
    version("6.2.0", sha256="cdf0c2179ae7a7931dba52463741cf59024198bbf9673bf08415bcb46344110f")
    version("4.0.1", sha256="14b38ef25cc136d71339ceeafb4856bb638d486614103453eccd323849267f20")
    version("4.0.0", sha256="90add44f06de081047d431c08d7269c25b4030e5fe19c3bc8381c001ce8f258c")
    version("3.0.0", sha256="128aa1553e88403833e0cccf1b651f45ce87bc207871f53fdcc8e7f9ec795747")
    version("2.2.0", sha256="f891224f32e7a06bf279290619cec80cc8ddc335c13696872195ffb87f5bce67")
    version("2.1.0", sha256="4bdd6569fdce00460bf9cda0ff5dcff46d342b4595900d849cc46a277a74cce6")
    version("2.0.2", sha256="3cc3aa09cd1ce77736f23488c7cb24e65e11daed4e870ddc8d352aa4070c7c74")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=False, description="Build shared library")

    def cmake_args(self):
        args = []

        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")

        return args
