# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openslp(AutotoolsPackage):
    """OpenSLP project is an effort to develop an open-source,
    commercial-grade, implementation of IETF Standards track
    Service Location Protocol (RFC 2608). The interface conforms
    to IETF Standards track, "An API for Service Location"
    (RFC 2614)"""

    homepage = "http://www.openslp.org/"
    url = "https://github.com/openslp-org/openslp/archive/openslp-2.0.0.tar.gz"

    version("2.0.0", sha256="9dda45ff52cf8561ca1414ac8b4947ed2d9b43e66aec03478fa0ed37121a5ea2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("flex", type="build")
    depends_on("byacc", type="build")

    configure_directory = "openslp"
