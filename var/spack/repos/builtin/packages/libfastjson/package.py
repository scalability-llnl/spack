# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfastjson(AutotoolsPackage):
    """a fast json library for C."""

    homepage = "https://github.com/rsyslog/libfastjson"
    url = "https://github.com/rsyslog/libfastjson/archive/v0.99.8.tar.gz"

    license("MIT")

    version("0.99.8", sha256="7e49057b26a5a9e3c6623e024f95f9fd9a14b571b9150aeb89d6d475fc3633e3")
    version("0.99.7", sha256="a142a6e5fa5c9c4ac32615c42fc663a1a14bff305c922e55192b6abf7d1ce1d8")
    version("0.99.6", sha256="617373e5205c84b5f674354df6ee9cba53ef8a227f0d1aa928666ed8a16d5547")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
