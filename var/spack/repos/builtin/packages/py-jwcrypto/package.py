# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJwcrypto(PythonPackage):
    """
    JWCrypto is an implementation of the Javascript Object Signing and Encryption (JOSE)
    Web Standards as they are being developed in the JOSE IETF Working Group and related
    technology.

    JWCrypto uses the Cryptography package for all the crypto functions.
    """

    homepage = "https://jwcrypto.readthedocs.io/en/latest/"
    pypi = "jwcrypto/jwcrypto-1.5.4.tar.gz"
    git = "https://github.com/latchset/jwcrypto"

    maintainers("jeremyfix")

    license("LGPL-3.0")

    version("1.5.4", sha256="0815fbab613db99bad85691da5f136f8860423396667728a264bcfa6e1db36b0")

    depends_on("py-setuptools", type="build")

    depends_on("py-cryptography@3.4:", type=("build", "run"))
    depends_on("py-typing-extensions@4.5:", type=("build", "run"))
