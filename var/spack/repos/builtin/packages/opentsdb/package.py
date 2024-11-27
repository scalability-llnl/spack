# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opentsdb(AutotoolsPackage):
    """
    OpenTSDB is a distributed, scalable Time Series Database (TSDB) written on
    top of HBase.  OpenTSDB was written to address a common need: store, index
    and serve metrics collected from computer systems (network gear, operating
    systems, applications) at a large scale, and make this data easily
    accessible and graphable.
    """

    homepage = "https://github.com/OpenTSDB"
    url = "https://github.com/OpenTSDB/opentsdb/archive/v2.4.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.4.0", sha256="eb6bf323d058bd456a3b92132f872ca0e4f4a0b0d5e3ed325ebc03dcd64abfd0")
    version("2.3.2", sha256="5de8a3ff21bfa431d53859e278e23100fddde239aa2f25e8dee7810098cfd131")
    version("2.3.1", sha256="cc3c13aa18a733e1d353558623b5d3620d5322f3894a84d84cb24c024a70a8d7")
    version("2.3.0", sha256="c5641ff63a617a5f1ba787b17a10f102dceb3826ce7a4f3b6fd74d1b6409f722")
    version("2.2.2", sha256="031fb2b8fab083ad035dafecdac259a1316af0f1c6d28f8846e07ad03d36ff02")
    version("2.2.1", sha256="e2f335dcb3dfdc74cc80b2f70dc3c68d239d0832c4bf9af278b7df5a58c06990")
    version("2.2.0", sha256="fa9856e17fcd9c804878ea0be59377b64cca3ce25bc8424ed1ab786dce2432a0")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("java", type="run")
