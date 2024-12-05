# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmicrohttpd(AutotoolsPackage):
    """GNU libmicrohttpd is a small C library that is supposed to make
    it easy to run an HTTP server as part of another application.
    """

    homepage = "https://www.gnu.org/software/libmicrohttpd/"
    url = "https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.71.tar.gz"

    maintainers("hainest")

    license("LGPL-2.1-or-later")

    version("0.9.76", sha256="f0b1547b5a42a6c0f724e8e1c1cb5ce9c4c35fb495e7d780b9930d35011ceb4c")
    version("0.9.75", sha256="9278907a6f571b391aab9644fd646a5108ed97311ec66f6359cebbedb0a4e3bb")
    version("0.9.74", sha256="42035d0261373324bfb434018f4ab892514b10253d1af232e41b4cc2c11e650b")
    version("0.9.73", sha256="a37b2f1b88fd1bfe74109586be463a434d34e773530fc2a74364cfcf734c032e")
    version("0.9.72", sha256="0ae825f8e0d7f41201fd44a0df1cf454c1cb0bc50fe9d59c26552260264c2ff8")
    version("0.9.71", sha256="e8f445e85faf727b89e9f9590daea4473ae00ead38b237cf1eda55172b89b182")
    version("0.9.70", sha256="90d0a3d396f96f9bc41eb0f7e8187796049285fabef82604acd4879590977307")
    version("0.9.50", sha256="d1b6385068abded29b6470e383287aa7705de05ae3c08ad0bf5747ac4dc6ebd7")

    depends_on("c", type="build")  # generated

    variant("https", default=False, description="HTTPS support with GnuTLS")

    depends_on("gettext")
    depends_on("gnutls", when="+https")
    depends_on("libgcrypt", when="+https")

    def configure_args(self):
        options = [
            "--enable-static=no",  # don't build static libs
            "--enable-shared=yes",  # always build shared libs
            "--with-pic",  # always build PIC libs
            "--disable-rpath",  # let spack handle the RPATH
            "--disable-doc",  # don't build the docs
            "--disable-examples",  # don't build the examples
            "--disable-curl",  # disable cURL-based testcases
        ]

        if self.spec.satisfies("+https"):
            options.append("--enable-https")
            prefix = self.spec["gnutls"].prefix
            options.append("--with-gnutls={0}".format(prefix))
            prefix = self.spec["libgcrypt"].prefix
            options.append("--with-libgcrypt-prefix={0}".format(prefix))

        return options
