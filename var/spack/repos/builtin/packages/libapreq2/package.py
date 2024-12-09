# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libapreq2(AutotoolsPackage):
    """httpd-apreq is subproject of the Apache HTTP Server Project
    whose committers develop and maintain the libapreq C library
    and its language bindings for Perl (contributions for additional
    language bindings are most welcome)."""

    homepage = "https://github.com/gitpan/libapreq2"
    url = "https://github.com/gitpan/libapreq2/archive/gitpan_version/2.13.tar.gz"

    license("Apache-2.0")

    version("2.13", sha256="477ce8207e89869e1e4520286697a56d4bd6af348899849ecef43c88bf0872d1")
    version("2.12", sha256="75cc1daa60e781270178c8f9fbe9c68231a7bc96bcc5c7a970cfce75d784b568")
    version("2.08", sha256="9f491588957415ebe0decdf6758fcb5c0d3eaf05a573bdd51de499ae111ffc53")

    depends_on("c", type="build")  # generated

    depends_on("apr")
    depends_on("apr-util")
    depends_on("httpd")
    depends_on("perl", type="build")
