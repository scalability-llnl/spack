# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Sqlcipher(AutotoolsPackage):
    """SQLCipher is an SQLite extension that provides 256 bit AES encryption
    of database files.
    """

    homepage = "https://www.zetetic.net/sqlcipher/"
    url = "https://github.com/sqlcipher/sqlcipher/archive/v4.4.1.tar.gz"
    git = "https://github.com/sqlcipher/sqlcipher.git"

    maintainers("rmsds")

    license("BSD-3-Clause")

    version("4.6.1", sha256="d8f9afcbc2f4b55e316ca4ada4425daf3d0b4aab25f45e11a802ae422b9f53a3")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2021-3119
        version("4.4.1", sha256="a36ed7c879a5e9af1054942201c75fc56f1db22e46bf6c2bbae3975dfeb6782d")
        version("4.4.0", sha256="0924b2ae1079717954498bda78a30de20ce2a6083076b16214a711567821d148")
        version("4.3.0", sha256="fccb37e440ada898902b294d02cde7af9e8706b185d77ed9f6f4d5b18b4c305f")
        version("4.2.0", sha256="105c1b813f848da038c03647a8bfc9d42fb46865e6aaf4edfd46ff3b18cdccfc")
        version("4.1.0", sha256="65144ca3ba4c0f9cd4bae8c20bb42f2b84424bf29d1ebcf04c44a728903b1faa")
        version("4.0.1", sha256="2f803017378c7479cb791be59b7bad8392a15acddbcc094e4433581fe421f4ca")
        version("4.0.0", sha256="c8f5fc6d800aae6107bf23900144804db5510c2676c93fbb269e4a0700837d68")
        # strictly, 3.4.2 is not affected by any CVEs
        version("3.4.2", sha256="69897a5167f34e8a84c7069f1b283aba88cdfa8ec183165c4a5da2c816cfaadb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("openssl")
    depends_on("tcl", type=["build"])
    depends_on("zlib-api")

    def configure_args(self):
        args = []
        args.append("--enable-tempstore=yes")
        args.append("CFLAGS=-DSQLITE_HAS_CODEC")
        return args
